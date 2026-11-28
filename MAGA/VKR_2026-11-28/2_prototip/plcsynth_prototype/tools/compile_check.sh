#!/usr/bin/env bash
# Проверка сгенерированных программ сторонним компилятором matiec (iec2c) — тем же, что в OpenPLC и Beremiz.
#
# Использование:
#   IEC2C=/путь/к/iec2c MATIEC_LIB=/путь/к/matiec/lib ./tools/compile_check.sh
# Без переменных скрипт ищет iec2c в PATH и в типовых местах OpenPLC_v3.
# Результат: results/compile_matiec.csv (программа; код возврата; число строк с ошибками; первая ошибка)
# и полные журналы в results/compile_matiec/.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/results/compile_matiec"
CSV="$ROOT/results/compile_matiec.csv"

find_iec2c() {
  if [ -n "${IEC2C:-}" ] && [ -x "$IEC2C" ]; then echo "$IEC2C"; return; fi
  if command -v iec2c >/dev/null 2>&1; then command -v iec2c; return; fi
  for p in "$HOME/OpenPLC_v3/webserver/iec2c" "$HOME/OpenPLC_v3/utils/matiec_src/iec2c" \
           "/opt/OpenPLC_v3/webserver/iec2c" "$HOME/matiec/iec2c" "$HOME/Beremiz/matiec/iec2c"; do
    if [ -x "$p" ]; then echo "$p"; return; fi
  done
}

find_lib() {
  if [ -n "${MATIEC_LIB:-}" ] && [ -d "$MATIEC_LIB" ]; then echo "$MATIEC_LIB"; return; fi
  local d; d="$(dirname "$1")"
  for p in "$d/lib" "$d/../utils/matiec_src/lib" "$d/matiec_src/lib" "$HOME/OpenPLC_v3/utils/matiec_src/lib" \
           "$HOME/matiec/lib"; do
    if [ -f "$p/ieclib.txt" ]; then (cd "$p" && pwd); return; fi
  done
}

IEC2C_BIN="$(find_iec2c)"
if [ -z "$IEC2C_BIN" ]; then
  echo "iec2c не найден. Установите OpenPLC_v3 или matiec и задайте IEC2C=/путь/к/iec2c." >&2
  exit 2
fi
LIB="$(find_lib "$IEC2C_BIN")"
if [ -z "$LIB" ]; then
  echo "Не найдена библиотека matiec (папка lib с ieclib.txt). Задайте MATIEC_LIB=/путь/к/lib." >&2
  exit 2
fi
echo "iec2c: $IEC2C_BIN"
echo "lib:   $LIB"
mkdir -p "$OUT"
echo "program;library;exit_code;error_lines;first_error" > "$CSV"
total=0; ok=0
for dir in generated generated_ext; do
  for st in "$ROOT/results/$dir"/*.st; do
    [ -e "$st" ] || continue
    name="$(basename "$st" .st)"
    tag="$dir/$name"
    work="$OUT/$dir/$name"
    mkdir -p "$work"
    # Флаги как в OpenPLC_v3 (scripts/compile_program.sh): -f -l -p -r -R -a; -I — стандартная библиотека.
    "$IEC2C_BIN" -f -l -p -r -R -a -I "$LIB" -T "$work" "$st" > "$work/iec2c.log" 2>&1
    rc=$?
    errs=$(grep -ci "error" "$work/iec2c.log" || true)
    first=$(grep -i -m1 "error" "$work/iec2c.log" | tr ';' ',' | cut -c1-200)
    echo "$name;$dir;$rc;$errs;$first" >> "$CSV"
    total=$((total + 1))
    if [ "$rc" -eq 0 ]; then ok=$((ok + 1)); echo "OK    $tag"; else echo "ОШИБКА $tag (см. $work/iec2c.log)"; fi
  done
done
echo "Скомпилировано без ошибок: $ok из $total. Итог — $CSV"
[ "$ok" -eq "$total" ]
