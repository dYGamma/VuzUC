# Simulink-модели — инструкция

Все 7 моделей создаются программно через `build_task*.m`. Task 8 — теоретическое
(система ОДУ), Simulink-модель не требуется.

## Список build-скриптов

| Скрипт           | Создаёт           | Описание                                                    |
|------------------|-------------------|-------------------------------------------------------------|
| `build_task1.m`  | `task1_model.slx` | Исходная структурная схема рис.1                            |
| `build_task2.m`  | `task2_model.slx` | Та же схема + отдельный Scope для сигнала e(t)              |
| `build_task3.m`  | `task3_model.slx` | Регулятор Kp=4 + объект W из Task 1                         |
| `build_task4.m`  | `task4_model.slx` | 3 параллельных F(e) + переключатель + объект W              |
| `build_task5.m`  | `task5_model.slx` | Нелинейный логический регулятор (MATLAB Function) + объект W|
| `build_task6.m`  | `task6_model.slx` | ПИД + задержка 1.5с + ZOH в ОС + объект W                   |
| `build_task7.m`  | `task7_aim2.slx`  | АИМ-2 на MATLAB Function + синус                            |
| `build_all.m`    | все 7 файлов      | Запускает все builder'ы подряд                              |

## Как запустить в MATLAB Online

1. Загрузить папку `report/` в MATLAB Drive (drag & drop).
2. Перейти в `report/models/`, в Command Window:
   ```matlab
   build_all
   ```
3. Откроется/сохранится 7 файлов `.slx`. Открыть любой → нажать **Run** → дважды
   щёлкнуть Scope для просмотра графика.
4. Скрин Scope: щелчок ПКМ по графику → **Copy to clipboard** или экспортировать
   в PNG (значок камеры на тулбаре Scope).

## Замечания

- В `build_task4` параметр `Sel` (Constant блок) выбирает аппроксимацию:
  1 = кусочно-линейная, 2 = полином 3-й ст., 3 = степенная.
  Меняем значение в блоке Sel и запускаем повторно.
- `build_task5` требует наличия Stateflow API (sfroot) — есть в MATLAB Online basic.
- Все объекты W внутри моделей берут готовую ПФ из Task 1 (числитель/знаменатель
  жёстко вписаны в `Transfer Fcn` блок, чтобы модель работала автономно без
  предварительного запуска `task1_reduce.m`).

## Если что-то не запускается

- Ошибка «`sfroot.find` … parentheses» — используется MATLAB R2023a+; в моделях
  уже `sfroot()` с круглыми скобками.
- Предупреждение «model name is shadowing another name» — имя `.slx` совпадает с
  именем m-файла в воркспейсе; build-скрипты используют суффикс `_model` чтобы
  избежать конфликта (`task1_model.slx` вместо `task1.slx`).
- В basic-аккаунте MATLAB Online отсутствует Control System Toolbox функция
  `pidtune`. Все параметры ПИД (Task 6) в build-скриптах уже вписаны жёстко.
