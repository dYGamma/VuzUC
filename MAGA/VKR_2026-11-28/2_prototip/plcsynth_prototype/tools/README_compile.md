# Проверка сгенерированных программ сторонними компиляторами

Цель — подтвердить, что 24 сгенерированные программы (12 схем × базовая и расширенная библиотеки)
принимаются компиляторами, которыми пользуются на практике: matiec (в составе OpenPLC и Beremiz) и CODESYS.
Результат вносится в опыт И1 строкой «компиляция: N из 24 без ошибок».

Программы: `results/generated/*.st` и `*.xml` (базовая библиотека), `results/generated_ext/*.st` и `*.xml`
(расширенная). Если прототип менялся, сначала пересоздайте их: `cd experiments && python run_all.py --skip-i6`.

## Способ 1. OpenPLC Runtime через веб-интерфейс (проще всего)

1. Установите OpenPLC Runtime v3 по инструкции проекта OpenPLC (Linux: `git clone https://github.com/thiagoralves/OpenPLC_v3.git && cd OpenPLC_v3 && ./install.sh linux`,
   или Docker). Откройте `http://localhost:8080`, вход openplc / openplc.
2. Programs → Upload Program → выберите файл `.st` → Upload Program → Launch program.
3. Откроется журнал компиляции. «Compilation finished successfully!» — программа принята matiec
   и собрана в исполняемый модуль. Ошибка — скопируйте первые строки журнала.
4. Повторите для каждого файла и заполните таблицу результатов (ниже).

Одна программа за раз — так устроен OpenPLC; на 24 файла уходит около получаса.

## Способ 2. matiec из командной строки (все 24 файла сразу)

После установки OpenPLC_v3 компилятор уже собран (`iec2c` в папке `webserver/` или
`utils/matiec_src/`). Можно собрать и отдельно: исходники matiec — в составе OpenPLC_v3
(`utils/matiec_src`) или Beremiz; сборка `autoreconf -i && ./configure && make`.

```bash
cd plcsynth_prototype                       # корень архива
IEC2C=~/OpenPLC_v3/webserver/iec2c MATIEC_LIB=~/OpenPLC_v3/utils/matiec_src/lib ./tools/compile_check.sh
```

Скрипт вызывает `iec2c -f -l -p -r -R -a -I <lib> -T <папка> файл.st` — с теми же флагами, что
OpenPLC при компиляции, — и пишет `results/compile_matiec.csv` и журналы `results/compile_matiec/`.
Код возврата 0 у всех файлов = все программы приняты. Без переменных `IEC2C` и `MATIEC_LIB` скрипт
ищет компилятор в PATH и в типовых папках OpenPLC_v3.

Компиляция в C (iec2c) — первый этап; второй (gcc) выполняет OpenPLC при загрузке программы, поэтому
полная проверка — способ 1. Для отчёта достаточно способа 2 на всех файлах и способа 1 на двух-трёх.

## Способ 3. CODESYS (Windows)

1. Установите CODESYS Development System V3.5 (бесплатно, store.codesys.com) — в комплекте есть
   программный контроллер CODESYS Control Win V3.
2. File → New Project → Standard project, устройство CODESYS Control Win V3, язык PLC_PRG — ST.
3. Project → Import PLCopenXML… → выберите `results/generated/NN_имя.xml` → отметьте все объекты → OK.
   Если в проекте уже есть объекты с такими именами, CODESYS спросит, заменить ли их.
4. В Task Configuration → MainTask добавьте вызов программы `main` (Add Call), чтобы она компилировалась
   как часть приложения.
5. Build → Build (F11). В окне сообщений — число ошибок и предупреждений. 0 ошибок = программа принята.
6. Для следующего файла удобнее создавать новый проект (или удалять импортированные объекты).

## Таблица результатов

Заполните `results/compile_external.csv` (шаблон — `tools/compile_external_TEMPLATE.csv`):

| program | library | tool | tool_version | errors | warnings | first_error |
|---|---|---|---|---|---|---|
| 01_motor_direct | base | matiec (OpenPLC v3) | … | 0 | 0 | |

Что делать при ошибке: сохраните журнал, укажите строку и текст первой ошибки. Ошибка компилятора
на сгенерированном коде — результат опыта (дефект генератора или ФБ), его исправляют и перезапускают
все опыты (`run_all.py`), как это было сделано с FB_Valve и FB_DigitalInput (`results/defects/`).

## Что уже проверено без внешних компиляторов

- Все 24 программы проходят собственный анализатор ST (синтаксис, типы, имена без учёта регистра).
- Совпадение имён с ключевыми словами, типами, стандартными функциями и блоками ищется без учёта
  регистра, как требует IEC 61131-3 (так найден дефект `tOn`/`TON`).
- Вложенных комментариев нет (matiec без флага `-n` их не допускает); идентификаторы и код — ASCII,
  русский текст только в комментариях.
- Адреса укладываются в области OpenPLC: %IX/%QX до 99.7, %IW/%QW до 1023; аналоговые каналы —
  тип INT.
