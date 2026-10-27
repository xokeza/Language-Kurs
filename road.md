# Полный маршрут: Python → C# → C++ → Windows API → память и CPU → отладка → Reverse Engineering → игровые инструменты

**Уровень:** от нуля до уверенного самостоятельного разработчика.  
**Цель:** создавать Windows-программы, инструменты диагностики, анализировать собственные бинарные файлы и разрабатывать игровые инструменты для **собственных или разрешённых офлайн-проектов**.  
**Темп:** 8–12 часов в неделю, приблизительно 10–16 месяцев. Срок ориентировочный: важнее реальные навыки, чем календарь.  
**Правило:** 30% чтения / 70% кода, экспериментов и заметок.

> [!IMPORTANT]
> Здесь нет инструкций по обходу античитов, скрытому внедрению в чужие процессы, взлому онлайн-игр или вмешательству в чужие игровые сервисы. Вместо этого итоговый проект — полноценная офлайн-песочница с собственными диагностическими и игровыми инструментами: от HUD и консоли до отдельной панели управления. Навыки C++, WinAPI, отладки и RE при этом изучаются по-настоящему.

---

## 0. Ответ на вопрос: нужны ли `int`, `float` и другие типы?

**Да, обязательно — и именно для твоего направления.** Не нужно заучивать таблицу типов, но надо понимать, что они означают в памяти.

| Понятие | Где пригодится | Минимум знаний |
|---|---|---|
| `int` / `uint32_t` | счётчик здоровья, патроны, ID, флаги | целые числа, знаковость, размер |
| `float` | координаты, скорость, угол, дистанция | приблизительное хранение вещественных значений |
| `double` | расчёты с большей точностью | отличие от `float` |
| `bool` | `isPaused`, `godMode` в **своей** игре | `true/false` и представление состояния |
| `char`, `byte` | сырые байты и строки | кодировки, байтовые массивы |
| `size_t`, `uintptr_t` | размеры буферов, адреса | связь с архитектурой x64 |
| `struct`, `class` | структуры игровых сущностей | поля, выравнивание, объектная модель |
| указатель | доступ к переменным через адрес | `&`, `*`, `nullptr`, время жизни |

Пример C++:

```cpp
#include <cstdint>

struct PlayerState {
    std::int32_t health = 100;
    float x = 12.5f;
    float y = -4.0f;
    bool invulnerable = false;
};
```

Задача: объясни, почему здоровье представлено целым числом, а координаты — `float`. Потом выведи `sizeof(PlayerState)` и выясни, почему результат не обязан равняться сумме размеров полей (подсказка: **padding / alignment**).

### Что *можно* отложить

Сложную математику, графику DirectX, метапрограммирование шаблонов, SIMD, драйверы ядра и многопоточную оптимизацию. Они нужны для отдельных специализаций, но не в первую неделю.

---

## 1. Подготовка рабочего окружения (1–3 дня)

**Что установить:**

1. [Python](https://www.python.org/downloads/) и [официальная документация](https://docs.python.org/3/).
2. [Visual Studio Code](https://code.visualstudio.com/) или [Zed](https://zed.dev/) — редактор; для C++ в Windows удобно также [Visual Studio Community](https://visualstudio.microsoft.com/vs/community/) с компонентом *Desktop development with C++*.
3. [.NET SDK](https://dotnet.microsoft.com/download) для C#.
4. [Git](https://git-scm.com/downloads) и [Git Book](https://git-scm.com/book/en/v2).
5. [CMake](https://cmake.org/download/) — на этапе C++.
6. [Windows Terminal](https://learn.microsoft.com/windows/terminal/) и PowerShell.

**Настрой:** создай каталог `dev-learning` и внутри `python/`, `csharp/`, `cpp/`, `windows/`, `re-lab/`, `game-lab/`.

**Навыки:** терминал, `cd`, `dir`/`ls`, переменные среды, относительный/абсолютный путь, `git init`, `git add`, `git commit`, `.gitignore`, Markdown. Не запускай неизвестные исполняемые файлы ради тренировки.

**Проверка:** можешь создать репозиторий, запустить Hello World на Python/C# и объяснить, где находится исходник и что делает компилятор/интерпретатор.

---

## 2. Python — автоматизация и мышление программиста (4–6 недель)

### Неделя 1. Базовая логика

- Переменные, `int`, `float`, `bool`, `str`, `None`; сравнения и преобразования.
- `if/elif/else`, `and`, `or`, `not`.
- `for`, `while`, `range`, `break`, `continue`.
- `print`, `input`, f-строки.
- Практика: меню текстовой игры с HP, координатами, инвентарём.

### Неделя 2. Функции и коллекции

- `def`, аргументы, `return`, локальные переменные.
- `list`, `dict`, `tuple`, `set`; циклы по коллекциям.
- `try/except`, простое логирование.
- Практика: симулятор 10 игровых персонажей с уникальными параметрами.

### Неделя 3. Файлы и форматы

- `pathlib`, чтение и запись `.txt`, `.json`, `.csv`.
- `struct` (модуль Python) и `int.to_bytes` / `int.from_bytes`.
- Понятия little-endian, byte offset, hex dump.
- Практика: собственный формат бинарного сохранения: магическое число, версия, HP, X/Y.

### Неделя 4. Структура программы

- Модули, `import`, пакеты, виртуальные окружения, `pip`.
- Классы и `dataclass` для представления состояний.
- Аннотации типов, документация функций, `pytest`.
- Практика: утилита, читающая и валидирующая бинарное сохранение **твоей** игры.

### Недели 5–6. Полировка

- `argparse`, `logging`, обработка ошибок, тесты краевых случаев.
- GitHub README, релизы, рефакторинг.
- Проект **Save Inspector**: CLI, читающий собственный `.sav` и показывающий поля, размеры и значения; отдельный модуль тестирует несовместимые версии.

**Ресурсы:**

- [Официальный Python Tutorial](https://docs.python.org/3/tutorial/)
- [Python: `struct`](https://docs.python.org/3/library/struct.html)
- [Python: `pathlib`](https://docs.python.org/3/library/pathlib.html)
- [Python: `argparse`](https://docs.python.org/3/library/argparse.html)
- [pytest — getting started](https://docs.pytest.org/en/stable/getting-started.html)
- [Automate the Boring Stuff with Python](https://automatetheboringstuff.com/)

**Контроль:** сам, без копирования, напиши парсер своего бинарного файла и пять тестов к нему.

---

## 3. C# и .NET — Windows-приложения и интерфейсы (5–7 недель)

### Неделя 1. Перенос логики с Python

- `Console.WriteLine`, `Console.ReadLine`, переменные, типы, `if`, `switch`, циклы.
- Методы, параметры, возвращаемые значения, обработка исключений.
- Собери CLI-версию Save Inspector на C#.

### Неделя 2. ООП и модели данных

- `class`, `struct`, `record`, свойства, конструкторы.
- Интерфейсы, наследование (без злоупотребления), композиция.
- `List<T>`, `Dictionary<TKey,TValue>`, `enum`.
- Проект: модель игровых сущностей с разделением логики и хранения.

### Неделя 3. Файлы и сериализация

- `File`, `Stream`, `BinaryReader`, `BinaryWriter`.
- JSON, кодировки UTF-8/UTF-16, `Span<T>` на концептуальном уровне.
- Проект: редактор **собственного** формата сохранений с резервной копией и проверками.

### Неделя 4. Desktop UI

- Windows Forms — быстрый старт, либо WPF — UI и привязка данных.
- События, обработчики, layout, асинхронность `async/await`.
- Проект: окно с полями HP/скорости/координатами, сохранение в JSON.

### Недели 5–7. Интеграция

- .NET runtime и garbage collector, сравнение с нативным C++.
- HTTP API на базовом уровне, `HttpClient`, отмена операций.
- Логи, конфигурация, пользовательские настройки, публикация приложения.
- Проект **Game Lab Control Panel**: UI изменяет настройки **твоей игры** через JSON или документированный локальный API.

**Ресурсы:**

- [Microsoft Learn: C#](https://learn.microsoft.com/dotnet/csharp/)
- [C# для начинающих](https://learn.microsoft.com/dotnet/csharp/getting-started/)
- [Практические упражнения C#](https://microsoftlearning.github.io/mslearn-csharp-programming/)
- [Windows Forms](https://learn.microsoft.com/dotnet/desktop/winforms/)
- [WPF](https://learn.microsoft.com/dotnet/desktop/wpf/)
- [Асинхронное программирование в C#](https://learn.microsoft.com/dotnet/csharp/asynchronous-programming/)

**Контроль:** собери настольную утилиту с GUI, валидацией данных, логами и сохранением настроек.

---

## 4. C++ — нативный код и управление памятью (8–12 недель)

### Недели 1–2. Язык и компиляция

- `#include`, `main`, заголовки `.h/.hpp`, исходники `.cpp`.
- `int`, `float`, `double`, `bool`, `char`, `std::string`.
- `if`, циклы, функции, ссылки (`&`), `const`.
- Компилятор, линкер, `.obj`, `.exe`, `Debug` и `Release`.
- Практика: текстовый симулятор PlayerState.

### Недели 3–4. Адреса, указатели и память

- Stack vs heap; время жизни объектов.
- `&value`, `*pointer`, `nullptr`, массивы и адресная арифметика.
- `new/delete` для понимания, но в коде предпочитать RAII.
- `std::vector`, `std::array`, `std::unique_ptr`, `std::shared_ptr`.
- `sizeof`, `alignof`, padding, `std::uint32_t`, `std::uintptr_t`.
- Практика: визуализатор структуры объектов с адресами собственных переменных.

### Недели 5–6. Архитектура проекта

- `class`, `struct`, `enum class`, перегрузка, `const` methods.
- Конструктор, деструктор, RAII, правило пяти/нуля.
- Исключения и коды ошибок, namespaces.
- Модульный проект: `GameState`, `Player`, `Simulation`, `Serializer`.

### Недели 7–8. Бинарные данные

- `std::byte`, `std::span`, работа с потоками файлов.
- Hex, endian, структуры, бинарная сериализация по полям (не записывать сырую память структуры без понимания ABI/padding).
- Undefined behavior, выход за границы, use-after-free (анализировать и исправлять, не создавать эксплойты).
- Практика: совместимый формат сохранения для Python/C#/C++.

### Недели 9–12. Профессиональные основы

- CMake, warning levels, статический анализ, sanitizers там, где доступны.
- `std::thread`, mutex и race condition — основы.
- Unit tests, `gtest` или Catch2.
- Оптимизация по профилировщику, а не догадкам.
- Финал: небольшая офлайн-игра с движением и состоянием, на которую позднее будет опираться весь курс.

**Ресурсы:**

- [LearnCpp — последовательный курс](https://www.learncpp.com/)
- [cppreference — справочник](https://en.cppreference.com/w/cpp)
- [Microsoft C++ documentation](https://learn.microsoft.com/cpp/)
- [CMake Tutorial](https://cmake.org/cmake/help/latest/guide/tutorial/index.html)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [GoogleTest](https://google.github.io/googletest/)

**Контроль:** объясни, почему возвращать адрес локальной переменной нельзя; когда нужен `unique_ptr`; почему два поля могут иметь разные смещения и что значит `0x10`.

---

## 5. Windows API и устройство приложений (5–7 недель)

### Неделя 1. Windows user mode

- Процесс, поток, дескриптор (handle), права доступа, PID.
- Win32 API, `HWND`, `HANDLE`, `DWORD`, `LPCWSTR` — как читать документацию.
- Unicode в Windows: wide strings, UTF-16.
- Практика: своё окно Win32 с сообщениями и кнопкой.

### Неделя 2. Message loop и события

- Окна, `WndProc`, сообщения, `WM_PAINT`, `WM_CLOSE`.
- `GetLastError`, коды ошибок, безопасная очистка ресурсов.
- Практика: окно диагностики с таймером обновления состояния своей программы.

### Неделя 3. Процессы и модули

- Как Windows запускает `.exe`; разница EXE/DLL.
- Модуль, путь к файлу, версия, архитектура x86/x64.
- Process Explorer и инструменты мониторинга — наблюдение за **своими** процессами.
- Практика: инспектор метаданных и производительности запущенной тобой программы.

### Неделя 4. PE-формат

- DOS header, PE signature, COFF header, optional header.
- Секции `.text`, `.data`, `.rdata`, таблица импортов, экспорты.
- RVA vs file offset vs VA; ASLR на концептуальном уровне.
- Практика: PE-inspector, показывающий секции и импорты исполняемого файла собственного проекта.

### Недели 5–7. Обмен данными между своими приложениями

- Files, named pipes, localhost sockets: когда и зачем.
- Ограничения прав и безопасность команд.
- Практика: твоя C#-панель отправляет разрешённые команды твоей C++-игре через локальный документированный интерфейс; игра проверяет команды.

**Ресурсы:**

- [Windows desktop development](https://learn.microsoft.com/windows/win32/)
- [Windows API index](https://learn.microsoft.com/windows/win32/api/)
- [Process and threads](https://learn.microsoft.com/windows/win32/procthread/processes-and-threads)
- [PE format](https://learn.microsoft.com/windows/win32/debug/pe-format)
- [Windows internals documentation](https://learn.microsoft.com/windows/)
- [Sysinternals Suite](https://learn.microsoft.com/sysinternals/downloads/sysinternals-suite)

**Контроль:** различаешь PID, handle, module, virtual address и file offset; можешь объяснить, что показывает PE-inspector.

---

## 6. Память, процессор, ASM x64 (5–7 недель)

### Неделя 1. Как представляются данные

- Бит, байт, hex, little-endian, signed/unsigned.
- IEEE 754: почему `float` хранит 1.5 не так, как `int` хранит 1.
- ASCII, UTF-8, UTF-16; массивы байтов.
- Практика: выведи байтовое представление своих `int` и `float`.

### Неделя 2. Виртуальная память

- Virtual memory, pages, stack, heap, read/write/execute permissions.
- Address space, ASLR, guard pages; ошибки доступа к памяти.
- Практика: карта **собственного** процесса на уровне разрешённых диагностических инструментов.

### Недели 3–4. Процессор и инструкции

- Регистры `RAX`, `RBX`, `RCX`, `RDX`, `RSP`, `RBP`, `RIP`.
- `mov`, `lea`, `cmp`, `test`, `jmp`, условные переходы, `call`, `ret`.
- Флаги CPU, stack frames и соглашения вызова Windows x64.
- Практика: скомпилировать `sum(a,b)`, открыть disassembly, сопоставить исходные строки и инструкции.

### Недели 5–7. Компилятор и оптимизация

- Debug vs Release; inlining; почему локальная переменная может не иметь простого адреса.
- Символы и PDB; разница исходного кода и машинного кода.
- Практика: исследование трёх своих функций в Debug/Release, отчёт со скриншотами и аннотациями.

**Ресурсы:**

- [Intel Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html)
- [x64 calling convention (Microsoft)](https://learn.microsoft.com/cpp/build/x64-calling-convention)
- [x64 architecture (Microsoft)](https://learn.microsoft.com/windows-hardware/drivers/debugger/x64-architecture)
- [IEEE 754 overview](https://en.wikipedia.org/wiki/IEEE_754)

**Контроль:** можешь на бумаге объяснить `RIP`, stack frame и переход при сравнении двух чисел.

---

## 7. Отладка и исследование поведения (4–6 недель)

### Этап 1. Дебаггер IDE

- Breakpoints, step into/over/out, watch, locals, call stack.
- Отладка C# и C++ в Visual Studio.
- Практика: специально введи ошибку в **свою** программу и найди её с помощью breakpoint.

### Этап 2. WinDbg и x64dbg

- Прикрепление отладчика к собственной тестовой программе.
- Регистры, стек, call stack, модули, символы, просмотр своего кода в дизассемблере.
- Условные breakpoints и логирование событий в собственном приложении.
- Практика: выяснить, где собственная функция `ApplyDamage` меняет `PlayerState.health`.

### Этап 3. Диагностика

- Crash dump, исключения, символы PDB.
- Наблюдение утечек памяти, анализ времени выполнения.
- Практика: отчет о баге — ожидаемое поведение, фактическое, минимальный воспроизводимый пример, исправление.

**Ресурсы:**

- [Visual Studio debugger docs](https://learn.microsoft.com/visualstudio/debugger/)
- [WinDbg documentation](https://learn.microsoft.com/windows-hardware/drivers/debugger/)
- [x64dbg](https://x64dbg.com/)
- [x64dbg manual](https://help.x64dbg.com/en/latest/index.html)
- [Debugging tools for Windows](https://learn.microsoft.com/windows-hardware/drivers/debugger/debugger-download-tools)

**Контроль:** найдёшь причину ошибки в собственной игре, даже если видишь её впервые, и сможешь документировать ход расследования.

---

## 8. Reverse engineering — анализ своих бинарников и учебных образцов (6–9 недель)

**Рабочая среда:** собственные исполняемые файлы, открытые учебные образцы или программы, на анализ которых у тебя есть разрешение. Не запускай сомнительные образцы на основном компьютере.

### Недели 1–2. Статический анализ

- Disassembler vs decompiler: отличия и ограничения.
- Функции, строки, импорты, символы, контрольный поток.
- Ghidra: импорт, listing, decompiler, xrefs, function graph.
- Практика: собери свой бинарник без отладочных символов, попробуй восстановить назначение трёх функций.

### Недели 3–4. Динамический анализ

- Сопоставление наблюдаемого поведения с функциями.
- Breakpoints в собственном приложении, входные значения, точки ветвления.
- Практика: восстановить логику проверки уровня и изменения счёта в своей игрушке.

### Недели 5–6. Форматы, версии, сравнения

- Строки, таблицы, константы; как распознавать структуру данных.
- Сравнение двух сборок собственного приложения.
- Отчёт с гипотезами и проверками: что известно, а что лишь предполагается.

### Недели 7–9. Автоматизация анализа

- Скрипты Ghidra (при необходимости), структурирование заметок.
- Мини-исследование: «из бинарника без исходников восстановить схему функции начисления очков».
- Не полагайся слепо на decompiler — проверяй вывод через тесты.

**Ресурсы:**

- [Ghidra — официальный проект](https://github.com/NationalSecurityAgency/ghidra)
- [Ghidra — Introduction to Ghidra](https://ghidra.re/ghidra_docs/GhidraClass/Beginner/Introduction_to_Ghidra_Student_Guide.html)
- [Ghidra docs](https://ghidra-sre.org/)
- [OpenSecurityTraining2 — курсы по низкоуровневым темам](https://opensecuritytraining.info/)
- [Compiler Explorer](https://godbolt.org/)

**Контроль:** по своему `.exe` без исходников можешь определить входную точку, найти интересующую функцию, объяснить её логику и проверить предположение экспериментом.

---

## 9. Итоговая ветка: полноценные игровые инструменты (8–12 недель)

Ты не просто делаешь «кнопку +100 HP», а строишь систему из **игры**, **отдельной панели**, **диагностики** и **тестов**. Все изменения происходят через специально предусмотренный интерфейс собственной офлайн-песочницы, а не обход защиты сторонних игр.

### Проект A. Game Sandbox (C++)

Функции:
- Игровой цикл; координаты, скорость, HP, ресурсы, противники-боты.
- `PlayerState`, управление состоянием, сохранение/загрузка.
- Переключение режимов *developer/test* в локальной сборке.
- Event log: урон, передвижение, смена сцены.
- Подготовка обычной и диагностической сборки.

**Приёмка:** можно играть, сохранить прогресс, восстановить его и воспроизвести ошибку.

### Проект B. Developer Console (C++)

Команды в **своей игре**:

```text
help
show player
set player.health 100
set player.speed 6.5
teleport 10 20
spawn dummy
pause
resume
```

Добавь валидацию типов и диапазонов, подсказки, журнал команд и отключение консоли в обычной сборке.

### Проект C. Game Control Panel (C#)

- Красивый интерфейс: вкладки Player, World, Debug, Logs.
- Слайдер скорости, поля координат, кнопка восстановления здоровья.
- Подключение к **своему** локальному серверу команд внутри игры через localhost или named pipe.
- Передача структурированного JSON и явная обработка ошибок.
- Отдельная кнопка «Сбросить настройки» и статус соединения.

### Проект D. Game Telemetry HUD (C++/C#)

- Показ FPS, позиции, текущего HP, времени кадра.
- Графики по данным, которые **твоя игра сама экспортирует**.
- Запись CSV и сравнение двух запусков.
- Система уведомлений о состоянии и отладочные показатели.

### Проект E. Binary Lab (C++ + Ghidra + debugger)

- Собери отдельно учебную программу с формулами урона и начислением очков.
- Удали символы из учебной сборки, не потеряв исходники у себя.
- По статическому анализу восстанови схемы расчётов.
- Подтверди выводы отладкой; сравни Debug и Release.
- Создай отчёт `reverse_notes.md` со схемами и результатами.

### Финальный проект F. «Game Lab Toolkit»

Структура репозитория:

```text
game-lab-toolkit/
  README.md
  docs/
    architecture.md
    memory_layout.md
    reverse_notes.md
  game-cpp/
    src/
    include/
    tests/
  control-panel-csharp/
  save-inspector-python/
  assets/
  examples/
```

**Минимальные требования:** запускается с нуля по README; код разделён на модули; настройки сохраняются; есть обработка ошибок; 15+ тестов; схема API; видео-демо; история Git-коммитов.

**Опционально:** графическое окно игры с [SDL](https://www.libsdl.org/) или [raylib](https://www.raylib.com/). Для UI панели — WPF или WinForms. Для профилирования — инструменты Visual Studio.

---

## 10. Опциональные специализации (только после основ)

| Направление | Что добавить | Проект |
|---|---|---|
| Windows developer tools | ETW, логирование, мониторинг ресурсов | диагностическая панель своего приложения |
| Game tools | ECS, UI, графика, математика векторов | редактор уровней своего проекта |
| Reverse engineering | ABI, оптимизации компиляторов, Ghidra scripting | сравнение версий своего бинарника |
| Performance | CPU profiler, cache, SIMD | ускорение симуляции по измерениям |
| Secure development | memory safety, fuzzing, input validation | устранение ошибок в своём парсере |

---

## 11. Реальный график на 48 недель

| Недели | Раздел | Главный результат |
|---|---|---|
| 1 | Окружение, Git | репозиторий и три Hello World |
| 2–6 | Python | Save Inspector CLI |
| 7–12 | C# | панель Windows и редактор собственного сейва |
| 13–22 | C++ | GameState, сериализация, маленькая игра |
| 23–27 | Windows API | окно Win32, PE-inspector, локальный API |
| 28–32 | Память/ASM | отчёт об адресах, типах и дизассемблировании |
| 33–37 | Отладка | баг-репорты и дампы своих приложений |
| 38–43 | Reverse Engineering | анализ учебных бинарников |
| 44–48 | Game Lab Toolkit | комплект игровых инструментов |

Если какая-то фаза требует больше времени, **не перескакивай**. 48 недель — базовый план; для более глубокого уровня нормально учиться 60–70 недель.

### Недельный ритм (10 часов)

- 2 ч — читаешь документацию и делаешь короткие заметки.
- 5 ч — реализуешь задачи и новые функции.
- 2 ч — ищешь и исправляешь ошибки, отлаживаешь.
- 1 ч — тесты, Git, README, итоги недели.

### Критерии перехода (обязательные)

- **Python → C#:** пишешь функции и работаешь с файлами без подсказок.
- **C# → C++:** понимаешь типы, классы, исключения и устройство desktop GUI.
- **C++ → Windows API:** уверенно пользуешься указателями и RAII.
- **Windows API → память/ASM:** различаешь виртуальный адрес, модуль, поток, секцию PE.
- **Память/ASM → отладка:** знаешь регистры, стек, основные инструкции.
- **Отладка → RE:** умеешь самостоятельно находить причину ошибки по стеку и переменным.
- **RE → финал:** умеешь объяснить поведение собственной программы по бинарнику и тестам.

---

## 12. 35 практических задач от лёгких к сложным

**Python (1–7):**

1. Выведи HP и координаты персонажа.
2. Реализуй получение урона и лечение с ограничением максимального HP.
3. Сделай перемещение по командам `w/a/s/d`.
4. Запиши состояние в JSON.
5. Считай сохранение и проверь корректность полей.
6. Сделай бинарный сейв с версией формата.
7. Напиши 5 автоматических тестов парсера.

**C# (8–14):**

8. Перепиши симулятор на C#.
9. Сделай класс игрока и инвентарь.
10. Прочитай формат JSON от Python.
11. Создай WinForms/WPF-окно.
12. Добавь изменение параметров в своём сохранении.
13. Сделай лог ошибок и историю изменений.
14. Напиши приложение, которое не падает от неправильных данных.

**C++ (15–22):**

15. Собери проект из нескольких `.cpp` и `.hpp`.
16. Сделай `PlayerState` и выведи `sizeof`.
17. Выведи адреса собственных полей и их смещения.
18. Сравни `float` и `int` на уровне байтов.
19. Замени ручное выделение ресурсов на RAII.
20. Реализуй безопасный парсер своего формата.
21. Добавь 10 тестов.
22. Сделай игровую симуляцию с ботом и журналом событий.

**Windows и отладка (23–29):**

23. Открой своё Win32-окно.
24. Реализуй корректное закрытие окна и обработку ошибок.
25. Получи метаданные о собственном исполняемом файле.
26. Покажи секции собственного PE-файла.
27. Поставь breakpoint на `ApplyDamage`.
28. Сопоставь C++-строку и несколько инструкций x64.
29. Найди и исправь собственную ошибку через call stack.

**RE и финал (30–35):**

30. Импортируй свой `.exe` в Ghidra.
31. Восстанови смысл трёх функций без отладочных символов.
32. Сопоставь найденные функции с исходниками.
33. Добавь developer console с проверкой команд.
34. Свяжи C#-панель со своей C++-игрой через локальный API.
35. Опубликуй учебный репозиторий с документацией и демонстрацией.

---

## 13. Как учиться, чтобы не застрять

**Порядок для каждой темы:** 1) прочитай концепцию; 2) перепиши минимальный пример; 3) измени его; 4) сломай и почини; 5) создай свой проект без пошаговой подсказки; 6) объясни своими словами.

**Дневник ошибок:**

```md
## Ошибка
Что хотел получить:
Что получил:
Минимальный код для воспроизведения:
Гипотеза:
Как проверил:
Исправление:
Чему научился:
```

**Правило поиска:** сначала официальная документация, затем статьи и видео; если две статьи противоречат друг другу, проверяй кодом и документацией актуальной версии.

**Как проверять уровень:** если можешь воспроизвести проект через неделю без видео, объяснить каждую строку и написать тест — тему усвоил. Если нет, повторяй практику, а не просто смотри ещё ролики.

---

## 14. Большой справочник ссылок

### Основы и исходный код
- Python: https://docs.python.org/3/tutorial/
- C#: https://learn.microsoft.com/dotnet/csharp/
- C++: https://www.learncpp.com/
- C++ reference: https://en.cppreference.com/w/cpp
- Git book: https://git-scm.com/book/en/v2
- GitHub Skills: https://skills.github.com/
- Compiler Explorer: https://godbolt.org/

### Windows и native
- Win32: https://learn.microsoft.com/windows/win32/
- Win32 API index: https://learn.microsoft.com/windows/win32/api/
- PE format: https://learn.microsoft.com/windows/win32/debug/pe-format
- x64 calling convention: https://learn.microsoft.com/cpp/build/x64-calling-convention
- Sysinternals: https://learn.microsoft.com/sysinternals/
- Microsoft C++: https://learn.microsoft.com/cpp/

### Отладка и реверсинг
- Visual Studio debugging: https://learn.microsoft.com/visualstudio/debugger/
- WinDbg: https://learn.microsoft.com/windows-hardware/drivers/debugger/
- x64dbg: https://x64dbg.com/
- x64dbg docs: https://help.x64dbg.com/en/latest/index.html
- Ghidra: https://github.com/NationalSecurityAgency/ghidra
- Ghidra beginner guide: https://ghidra.re/ghidra_docs/GhidraClass/Beginner/Introduction_to_Ghidra_Student_Guide.html
- Intel instruction-set manuals: https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html

### Проектирование игровых инструментов
- raylib: https://www.raylib.com/
- SDL: https://www.libsdl.org/
- WPF: https://learn.microsoft.com/dotnet/desktop/wpf/
- Windows Forms: https://learn.microsoft.com/dotnet/desktop/winforms/
- CMake tutorial: https://cmake.org/cmake/help/latest/guide/tutorial/index.html
- GoogleTest: https://google.github.io/googletest/

---

## 15. Первое занятие — сделай сегодня

Создай `python/day01_player.py`:

```python
health = 100
speed = 4.5
x = 0.0

print(f"HP: {health}; speed: {speed}; x: {x}")

damage = 25
health = max(0, health - damage)
x += speed

print(f"После удара HP: {health}; новая x: {x}")
```

**Твоя задача без подсказки:** добавь `max_health`, команду лечения, запрет отрицательного здоровья и проверку, что скорость неотрицательная. Затем сохрани состояние в JSON. Если получилось — переходи к первому недельному модулю.

**Конечный ориентир:** не знание сотни названий API, а способность самостоятельно спроектировать программу, наблюдать её поведение, находить ошибки и объяснять её работу вплоть до байтов и инструкций CPU.
