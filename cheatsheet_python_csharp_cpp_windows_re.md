# Практическая шпаргалка: Python → C# → C++ → Windows API → память/CPU → отладка → Reverse Engineering → игровые проекты

> **Формат:** кратко о том, зачем существует каждая технология, что именно писать, какие команды запускать, где искать ошибки и когда делать `git commit`. Это **дополнение** к большому дорожному плану, а не замена практике. Целевая система: Windows 10/11 x64, PowerShell, VS Code/Zed и Visual Studio.
>
> **Сквозной пример:** собственная маленькая офлайн-игра **LabGame**, у которой есть HP, позиция и файл сохранения. Из неё вырастут инспектор сохранений, интерфейс, нативная библиотека, Windows-диагностика, отладка и анализ собственной сборки. Работаем только со своим кодом и программами, на исследование которых есть разрешение.

## 0. Карта всего пути за 60 секунд

| Шаг | Что даёт | Что уметь на выходе | Результат |
|---|---|---|---|
| Git + терминал | Не терять код, откатывать ошибки | `status`, `add`, `commit`, `diff`, `branch` | Репозиторий и история |
| Python | Быстро делать логику и инструменты | функции, JSON, байты, тесты | CLI-инспектор сохранений |
| C# / .NET | Удобные полноценные Windows-программы | классы, файлы, события, UI | GUI-инспектор |
| C++ | Контроль структуры данных и низкоуровневого кода | память, RAII, `struct`, сборка | Ядро симуляции |
| Windows API | Работать с возможностями ОС | окна, процессы, модули, ошибки | Монитор **своего** процесса |
| Память + CPU | Понимать, что происходит под капотом | стек/куча, адреса, регистры, байты | Карта состояния программы |
| Отладка | Искать настоящие причины ошибок | breakpoints, watch, call stack | Починка ошибки |
| Reverse Engineering | Читать поведение бинарника | PE, строки, символы, Ghidra, x64dbg | Анализ своей Release-сборки |
| Итоговый проект | Соединить навыки | архитектура, тесты, сборки, документация | LabGame + DevTools |

**Не перепрыгивай через основы:** `int`, `float`, `bool`, циклы и функции — не «теория для галочки». Тип определяет, **сколько байт**, **как они читаются** и **какие операции допустимы**. `float` может неточно хранить десятичные дроби; указатель не является самим значением.

---

# 1. Терминал, редактор, окружение — самая первая база

## Терминал (PowerShell)

Терминал запускает программы и команды. Редактор (Zed/VS Code) редактирует текст; терминал исполняет `python`, `dotnet`, `git`, `cmake`.

```powershell
pwd                     # где находишься
ls                      # файлы и папки (аналог dir)
mkdir lab-course        # создать папку
cd lab-course           # перейти в неё
New-Item notes.md       # создать файл
Get-Content notes.md    # показать содержимое
python --version        # проверить Python
py --version            # стандартный Windows Python launcher, если установлен
git --version           # проверить Git
dotnet --version        # проверить .NET SDK
```

**ВАЖНО:** `./script.sh` — Bash-скрипт, а не PowerShell. В PowerShell используются скрипты `.ps1`, например `./setup.ps1` (их выполнение может ограничиваться политикой исполнения; не отключай защиту глобально ради случайного скрипта). У программы в текущей папке обычно пишут `./program.exe` или `.\program.exe`.

**Пути:** `.` = текущая папка, `..` = родительская. Пробелы в пути требуют кавычек: `cd "C:\My Projects"`.

**Ссылки:** [PowerShell](https://learn.microsoft.com/powershell/), [VS Code](https://code.visualstudio.com/docs), [Zed](https://zed.dev/docs), [Windows Terminal](https://learn.microsoft.com/windows/terminal/).

### Практика и коммит

Сделай файл `notes.md` с командами, которые запустились на твоём ПК. Сохрани в Git коммитом `docs: record terminal setup` (см. ниже).

---

# 2. Git и GitHub — весь минимум, с которым уже можно работать

**Git** = история изменений на компьютере. **GitHub** = сайт для удалённых Git-репозиториев и совместной работы. Git **не сохраняет изменения автоматически**. Коммит — снимок подготовленных изменений, а не магическая резервная копия облака.

## Первое создание проекта

```powershell
mkdir lab-course
cd lab-course
git init
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
New-Item README.md
git status
git add README.md
git commit -m "docs: add project README"
git log --oneline
```

`git add` = поставить изменения в очередь (staging). `git commit` = сохранить эту очередь в историю. После изменения файла нужно **снова** `git add`.

## Команды, которые нужны постоянно

| Команда | Когда использовать |
|---|---|
| `git status` | Узнать, что изменено и что попадёт в коммит |
| `git diff` | Посмотреть **ещё не подготовленные** изменения |
| `git diff --staged` | Посмотреть **уже подготовленные** изменения |
| `git add path/to/file` | Выбрать конкретный файл |
| `git add -A` | Подготовить все изменения (сначала проверь `status`) |
| `git commit -m "feat: ..."` | Зафиксировать законченное маленькое изменение |
| `git log --oneline --graph --all` | Показать историю |
| `git switch -c feature/gui` | Создать ветку и переключиться в неё |
| `git switch main` | Вернуться на основную ветку (если она называется `main`) |
| `git merge feature/gui` | Влить ветку в текущую |
| `git restore file.py` | **Отменить** незакоммиченные правки файла — осторожно! |
| `git restore --staged file.py` | Убрать из очереди, сохранив правки в файле |
| `git revert <hash>` | Создать новый коммит, отменяющий старый; безопасно для общей истории |
| `git clone <url>` | Скачать существующий репозиторий |
| `git pull` | Получить и объединить изменения удалённого репозитория |
| `git push -u origin main` | В первый раз отправить основную ветку |

### Типичный рабочий цикл

```powershell
git status
# редактируешь src/player.py
git diff
git add src/player.py
git diff --staged
git commit -m "feat: add player health rules"
git status
```

**Сообщения коммитов:** `feat:` новая возможность, `fix:` исправление, `refactor:` переработка без изменения поведения, `test:` тесты, `docs:` документация, `chore:` настройка. Это общепринятое соглашение, а не требование Git.

### `.gitignore` — что НЕ коммитить

Создай `.gitignore` в корне:

```gitignore
# Python
.venv/
__pycache__/
.pytest_cache/
# .NET / C++
bin/
obj/
build/
.vs/
# редакторы и ОС
.DS_Store
# локальные секреты и конфигурация
.env
*.pfx
```

**Никогда не коммить** пароли, API-ключи, токены, личные документы, случайные бинарники. Если секрет уже попал в коммит, одного удаления из последнего файла недостаточно: секрет надо отозвать и перевыпустить.

### GitHub — один раз настроить

1. Создай пустой репозиторий на GitHub.
2. В локальной папке:

```powershell
git branch -M main
git remote add origin https://github.com/USERNAME/lab-course.git
git push -u origin main
```

Адрес **замени на свой**, GitHub может попросить авторизацию через браузер или credential manager. `git push` **публикует** твой код в выбранном репозитории; не путай private и public.

**Проверка:** внеси ошибку в README, зафиксируй, затем отмени её `git revert <hash>` — увидишь отдельный коммит-откат. Не применяй `reset --hard` к незнакомым изменениям.

**Ресурсы:** [Pro Git — бесплатно](https://git-scm.com/book/en/v2), [документация Git](https://git-scm.com/docs), [GitHub Hello World](https://docs.github.com/en/get-started/start-your-journey/hello-world), [.gitignore шаблоны](https://github.com/github/gitignore).

---

# 3. Python — быстрые утилиты и логика

**Зачем:** писать прототипы, обработчики файлов, автоматизацию и тестовые инструменты. Python хорош для скорости разработки, но не заменяет C++ там, где надо понимать размещение данных в нативной памяти.

## Основы на одном примере

```python
hp = 100             # int: целое число
speed = 2.5          # float: дробное число
paused = False       # bool
name = "LabPlayer"   # str

if hp <= 0:
    print("Game over")
elif hp < 30:
    print("Low health")
else:
    print(f"{name}: HP={hp}")

for tick in range(3):
    print("Tick", tick)
```

`=` присваивает, `==` сравнивает; `and`/`or` работают с условиями. Отступы в Python — **часть синтаксиса**. `range(3)` даёт `0, 1, 2`.

## Функция + проверка ошибок

```python
def damage(hp: int, amount: int) -> int:
    if amount < 0:
        raise ValueError("Damage cannot be negative")
    return max(0, hp - amount)

print(damage(100, 35))  # 65
```

`def` создаёт функцию; `return` возвращает значение; аннотации `: int` помогают редактору и читателю, но сами по себе **не проверяют тип автоматически**.

## Словарь, класс и сохранение JSON

```python
import json
from pathlib import Path

player = {"hp": 90, "x": 1.5, "y": -2.0}
path = Path("save.json")
path.write_text(json.dumps(player, indent=2), encoding="utf-8")
loaded = json.loads(path.read_text(encoding="utf-8"))
print(loaded["hp"])
```

`dict` связывает ключи и значения; JSON — **текстовый** формат. Проверь наличие и корректность полей прежде, чем доверять прочитанному файлу. Не используй `pickle` для чужих/непроверенных файлов.

## Бинарные данные: самое полезное для будущего RE

```python
import struct

blob = struct.pack("<If", 100, 12.5)  # < little-endian, I uint32, f float32
print(blob.hex(" "))
hp, x = struct.unpack("<If", blob)
print(hp, x)
```

В примере **8 байт**: 4 для беззнакового целого (`I`), 4 для 32-битного вещественного (`f`). Система координат и числа должны иметь согласованный формат на чтении и записи. Для нативного C++ `int` не обещает определённый размер на любой платформе — поэтому ниже будет `std::int32_t`.

## Окружение, зависимости, тесты

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install pytest
python -m pytest
```

Если политика PowerShell не даёт активировать venv, **можно обойтись без активации**: `.\.venv\Scripts\python.exe -m pip install pytest` и `.\.venv\Scripts\python.exe -m pytest`. Не нужен глобальный обход защит.

Файл `test_player.py`:

```python
from player import damage

def test_damage():
    assert damage(100, 35) == 65
    assert damage(10, 100) == 0
```

`assert` проверяет ожидаемый результат. **Не путай** тесты и продакшн-валидацию входных данных.

### Что ещё выучить и зачем

| Тема | Одно предложение |
|---|---|
| `list`, `tuple`, `set` | Последовательность, неизменяемая последовательность, множество уникальных значений |
| `try/except` | Обрабатывает ожидаемые исключения (не глуши всё через `except: pass`) |
| `with open(...)` | Закрывает файл даже при исключении |
| `pathlib` | Переносимая работа с путями |
| `argparse` | Параметры командной строки (`--file`, `--verbose`) |
| `logging` | Настраиваемые сообщения для диагностики вместо десятков `print` |
| `dataclass` | Удобное описание небольших объектов-данных |
| модули / `import` | Разделение проекта по файлам |
| `venv` / `pip` | Изоляция внешних библиотек для конкретного проекта |

### Git-история этапа

```text
feat: add player health functions
feat: save player state to JSON
feat: add little-endian binary save format
test: verify damage and save roundtrip
fix: reject truncated save files
docs: add save format specification
```

**Мини-проект:** `save_inspector.py`: аргумент `--file`, чтение своего файла, проверка длины, вывод HP/X, обработка повреждённого файла. **Пройдено:** умеешь объяснить каждый байт собственного сохранения.

**Ссылки:** [Python Tutorial](https://docs.python.org/3/tutorial/), [`struct`](https://docs.python.org/3/library/struct.html), [`pathlib`](https://docs.python.org/3/library/pathlib.html), [`argparse`](https://docs.python.org/3/library/argparse.html), [`venv`](https://docs.python.org/3/library/venv.html), [pytest](https://docs.pytest.org/en/stable/).

---

# 4. C# / .NET — полноценные Windows-приложения

**Зачем:** быстро делать графические интерфейсы, удобные инструменты и логику с типами. **.NET** — платформа и библиотеки, **C#** — язык, **SDK** — инструменты сборки, `dotnet` — команда.

## Создать и запустить проект

```powershell
dotnet new console -n LabInspector
cd LabInspector
dotnet run
dotnet build -c Release
```

`dotnet run` компилирует и запускает; `dotnet build` только собирает. `.csproj` описывает проект и зависимости; папки `bin/`, `obj/` генерируются автоматически.

## Переменные, свойства, классы, методы

```csharp
using System;

var player = new Player();
player.Damage(20);
Console.WriteLine($"HP={player.Health}, X={player.X}");

public class Player
{
    public int Health { get; private set; } = 100;
    public float X { get; set; } = 0.0f;

    public void Damage(int amount)
    {
        if (amount < 0) throw new ArgumentOutOfRangeException(nameof(amount));
        Health = Math.Max(0, Health - amount);
    }
}
```

**Уточнение:** при использовании top-level statements объявление `Player` стоит **после** исполняемых операторов; также можно вынести класс в отдельный `Player.cs`. `private set` запрещает другим классам напрямую ставить произвольный HP. `throw` сигнализирует ошибку.

## Чтение файла и JSON

```csharp
using System.Text.Json;

var json = File.ReadAllText("save.json");
var state = JsonSerializer.Deserialize<PlayerSave>(json)
    ?? throw new InvalidDataException("Empty save");
Console.WriteLine(state.Health);

public record PlayerSave(int Health, float X, float Y);
```

Помести `record` в отдельный `PlayerSave.cs` (или ниже top-level кода). `record` — компактный тип для данных. Пути относительно *рабочей директории*, а не обязательно директории `.exe`.

## WPF / WinForms / Avalonia: в чём разница?

| UI | Когда выбирать |
|---|---|
| **WinForms** | Быстро собрать обычное Windows-окно с кнопками и таблицей |
| **WPF** | Более гибкий Windows UI, XAML и привязка данных |
| **Avalonia** | Похожий по идее XAML UI, но кроссплатформенный |

Самый простой старт **на Windows**:

```powershell
dotnet new winforms -n LabInspectorGui
cd LabInspectorGui
dotnet run
```

WinForms шаблон/цель требуют Windows SDK/окружение с поддержкой Windows Desktop. В Visual Studio удобнее создавать формы визуальным дизайнером.

Минимальное действие кнопки (в классе формы):

```csharp
private void buttonLoad_Click(object sender, EventArgs e)
{
    using var dialog = new OpenFileDialog
    {
        Filter = "Save files (*.json)|*.json|All files (*.*)|*.*"
    };
    if (dialog.ShowDialog() != DialogResult.OK) return;
    labelStatus.Text = File.ReadAllText(dialog.FileName);
}
```

Это **пример обработчика**, не весь файл приложения; `buttonLoad` и `labelStatus` сначала создай в дизайнере и подключи событие `Click`.

## Тонкости C#

- `int` = знаковое 32-битное целое; `float` = 32-битное дробное число; `double` = 64-битное.
- `string` может быть `null` в зависимости от контекста; включи nullable reference types и учитывай предупреждения.
- `List<T>` — список, `Dictionary<TKey,TValue>` — словарь; `T` — тип элемента.
- `using var stream = ...` освобождает ресурсы (`IDisposable`) — это не то же, что `using Namespace;`.
- `async/await` удобны для операций ввода-вывода, но **не делают автоматически всё многопоточным**.
- Для UI нельзя блокировать главный поток длительными операциями; иначе окно зависнет.
- `try/catch` не должен скрывать ошибку. Покажи понятное сообщение и сохрани диагностическую информацию.

### Git-коммиты

```text
feat: create .NET console inspector
feat: load JSON and validate player data
feat: add WinForms file picker
fix: handle malformed save files
refactor: move save parsing to separate service
```

**Мини-проект:** GUI для своих `.json`/`.sav`, вывод HP, позиции, размера файла и сообщений об ошибке.

**Ссылки:** [C# guide](https://learn.microsoft.com/dotnet/csharp/), [.NET CLI](https://learn.microsoft.com/dotnet/core/tools/), [WinForms](https://learn.microsoft.com/dotnet/desktop/winforms/), [WPF](https://learn.microsoft.com/dotnet/desktop/wpf/), [System.Text.Json](https://learn.microsoft.com/dotnet/standard/serialization/system-text-json/overview), [Avalonia](https://docs.avaloniaui.net/).

---

# 5. C++ — нативный код, указатели, контроль ресурсов

**Зачем:** понимать структуры данных, память и машинный код. Сложнее Python/C#, зато даёт прямую связь с тем, что увидишь в отладчике и дизассемблере.

## Компиляция: важное различие

`.cpp` = исходный текст. **Компилятор** превращает его в объектный код; **линкер** собирает исполняемый файл и связывает библиотеки. `Debug` — для отладки, `Release` — обычно с оптимизацией (не гарантия безопасности).

Для Windows поставь Visual Studio Community с компонентом **Desktop development with C++**, чтобы получить MSVC и Developer PowerShell. `cl` работает из соответствующего developer shell, не из любой произвольной PowerShell-сессии.

```powershell
# В Developer PowerShell for VS:
cl /std:c++20 /EHsc /W4 main.cpp
.\main.exe
```

**Маленькая программа (`main.cpp`):**

```cpp
#include <cstdint>
#include <iostream>

struct Player {
    std::int32_t hp{100};
    float x{1.5f};
    float y{-2.0f};
};

int main() {
    Player p;
    p.hp -= 25;
    std::cout << "HP=" << p.hp << ", x=" << p.x << '\n';
    std::cout << "bytes=" << sizeof(p) << '\n';
}
```

## Указатель: что означают `&` и `*`

```cpp
int hp = 100;
int* address = &hp;   // & — взять адрес; int* — указатель на int
*address = 75;       // * — разыменовать и изменить значение по адресу
std::cout << hp;      // 75
```

- `hp` — **само значение**, `&hp` — адрес, `*address` — значение по адресу.
- `nullptr` — нулевой указатель, разыменовывать нельзя.
- После завершения жизни объекта его адрес может стать **недействительным** (`dangling pointer`).
- `sizeof(pointer)` на типичном x64 равен 8, а `sizeof(int)` обычно 4 — это **разные вещи**.

## Стек, куча, RAII

```cpp
#include <memory>
#include <vector>

int local = 5;                                // локальный объект
std::vector<int> values{1, 2, 3};            // динамический буфер под контролем vector
std::unique_ptr<int> owned = std::make_unique<int>(42); // управляемое владение
```

**RAII:** ресурс управляется временем жизни объекта. Предпочитай `std::vector`, `std::string`, `std::unique_ptr` вместо голых `new/delete`, пока не научишься обосновывать иное. Нельзя брать `&values[0]`, если вектор пуст; после его перераспределения старые указатели/итераторы могут стать недействительными.

## Передача по значению и ссылке

```cpp
void heal(Player& p, int amount) {
    if (amount > 0) p.hp += amount;
}

Player p;
heal(p, 10);  // меняет исходный p
```

Передача `Player p` (без `&`) создала бы копию. `const Player&` — ссылка без права изменять объект через неё.

## Почему структура может занимать больше суммы полей

```cpp
struct Demo {
    char flag;
    std::int32_t health;
};
static_assert(sizeof(std::int32_t) == 4);
```

Ожидаемо на обычном MSVC x64 `sizeof(Demo)` часто **8**, а не 5: между полями бывают байты выравнивания (**padding**). Конкретный layout зависит от ABI и настроек. Не записывай сырую структуру в файл без продуманного стабильного формата.

## CMake вместо ручной команды

`CMakeLists.txt`:

```cmake
cmake_minimum_required(VERSION 3.20)
project(LabCore LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
add_executable(labcore main.cpp)
```

```powershell
cmake -S . -B build
cmake --build build --config Debug
```

Для многоконфигурационных генераторов (Visual Studio) `--config` существенно. Ветка `Release` не всегда создаётся в той же папке, что `Debug`.

## На этом этапе понять

| Понятие | Зачем |
|---|---|
| `struct` / `class` | Структура собственных данных, поля, методы, доступ |
| `.h` / `.cpp` | Объявления отдельно от реализаций |
| `#include` | Подключение объявлений (не равнозначно установке библиотеки) |
| namespace | Избежать конфликтов названий |
| `std::int32_t` / `std::uint32_t` | Явная разрядность значений |
| `std::size_t` | Размеры и индексы; не путать с произвольным `int` |
| `std::vector`, `std::string` | Безопаснее управлять памятью |
| `const` | Запрет изменений через данный интерфейс |
| сборка / линковка | Почему появляется `unresolved external symbol` |
| UB (undefined behavior) | Некоторые ошибки не обязаны немедленно падать |

### Git-коммиты

```text
build: add CMake project
feat: add native Player structure
feat: implement movement simulation
refactor: replace owning raw pointer with vector
test: verify state serialization roundtrip
fix: guard against invalid indices
```

**Мини-проект:** нативная симуляция игрока и стабильный формат сохранения; добавь тесты переходов HP и координат.

**Ссылки:** [LearnCpp](https://www.learncpp.com/), [C++ reference](https://en.cppreference.com/w/), [CMake Tutorial](https://cmake.org/cmake/help/latest/guide/tutorial/), [MSVC C++](https://learn.microsoft.com/cpp/), [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines).

---

# 6. Windows API и устройство приложения

**Windows API (WinAPI)** — интерфейсы ОС: окна, файлы, процессы, потоки, память, модули и т.д. Windows headers/API требуют правильного платформенного SDK. **Win32** — историческое название семейства API и не означает, что программа обязана быть 32-битной.

## Создать обычное окно средствами WinAPI

```cpp
#define UNICODE
#define _UNICODE
#include <windows.h>

LRESULT CALLBACK WindowProc(HWND hwnd, UINT message, WPARAM wp, LPARAM lp) {
    if (message == WM_DESTROY) {
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProcW(hwnd, message, wp, lp);
}

int WINAPI wWinMain(HINSTANCE instance, HINSTANCE, PWSTR, int show) {
    constexpr wchar_t CLASS_NAME[] = L"LabWindow";
    WNDCLASSW wc{};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = instance;
    wc.lpszClassName = CLASS_NAME;
    RegisterClassW(&wc);

    HWND hwnd = CreateWindowExW(0, CLASS_NAME, L"LabGame Tools",
        WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT,
        600, 400, nullptr, nullptr, instance, nullptr);
    if (!hwnd) return 1;
    ShowWindow(hwnd, show);

    MSG msg{};
    while (GetMessageW(&msg, nullptr, 0, 0) > 0) {
        TranslateMessage(&msg);
        DispatchMessageW(&msg);
    }
    return static_cast<int>(msg.wParam);
}
```

Запуск через проект типа Windows Desktop Application (или соответствующую настройку линкера `/SUBSYSTEM:WINDOWS`), Unicode. Это *минимальное демонстрационное окно*: в рабочей версии проверь результат `RegisterClassW` и обрабатывай ошибки `GetMessageW` (`-1`).

**Разбор:** `HWND` — дескриптор окна; `WM_DESTROY` — сообщение уничтожения; `WindowProc` — функция обработки сообщений; message loop поддерживает отзывчивость GUI.

## Работать с информацией о **своём** процессе

```cpp
#include <windows.h>
#include <iostream>

int main() {
    std::cout << "PID=" << GetCurrentProcessId() << '\n';
    std::cout << "TID=" << GetCurrentThreadId() << '\n';
    SYSTEM_INFO info{};
    GetSystemInfo(&info);
    std::cout << "Page size=" << info.dwPageSize << '\n';
}
```

**PID** = идентификатор процесса, **TID** = идентификатор потока, **page size** = системный размер страницы виртуальной памяти. PID может со временем переиспользоваться; сам по себе это не разрешение на доступ к ресурсам другого процесса.

## Что учить дальше (в правильном порядке)

1. **Файлы:** `CreateFileW`, `ReadFile`, `WriteFile`, `CloseHandle` — читать/писать свои данные, всегда закрывать дескрипторы.
2. **Ошибки:** `GetLastError`, `FormatMessageW` — искать причину отказа API; вызывать `GetLastError` сразу после документированного неуспешного вызова.
3. **Процессы/потоки:** `GetCurrentProcessId`, `CreateProcessW`, `CreateThread` — сначала научись жизненному циклу **своей** программы.
4. **DLL:** экспорт/импорт функций, `LoadLibraryW`, `GetProcAddress`, `FreeLibrary` — на тестовой библиотеке, которую создал сам.
5. **Виртуальная память:** страницы, защита доступа, резервирование/коммит (`VirtualAlloc`, `VirtualFree`) — только в собственном процессе.
6. **PE:** заголовки EXE/DLL, секции, импорты, архитектура x86/x64, ASLR.

**Частые ошибки:** `HANDLE` не равен PID; `CloseHandle` не подходит для **любого** ресурса (например, у библиотек `FreeLibrary`); ANSI `*A` и Unicode `*W` — разные варианты API; WinAPI `BOOL` — не C++ `bool`.

### Git-коммиты

```text
feat: display own process and thread IDs
feat: add WinAPI diagnostics window
fix: report errors from failed OS calls
feat: load own example plugin DLL
```

**Мини-проект:** `LabMonitor` показывает PID собственного процесса, размер страницы, архитектуру, время работы и состояние твоего приложения; ничего не внедряет в чужие программы.

**Ссылки:** [Windows API index](https://learn.microsoft.com/windows/win32/api/), [Windows processes and threads](https://learn.microsoft.com/windows/win32/procthread/processes-and-threads), [Memory management](https://learn.microsoft.com/windows/win32/memory/memory-management), [PE format](https://learn.microsoft.com/windows/win32/debug/pe-format), [DLLs](https://learn.microsoft.com/windows/win32/dlls/dynamic-link-libraries).

---

# 7. Память, числа, CPU и Assembly — без бессмысленной зубрёжки

## Ментальная модель

- **Байт** = 8 бит. Биты принимают `0`/`1`. Hex — короткая запись байтов: `FF` = 255.
- **Little-endian**: младший байт многобайтового числа идёт первым. Например, `0x12345678` в памяти x86-64: `78 56 34 12`.
- **Virtual address**: адрес в виртуальном адресном пространстве процесса; не равен напрямую физическому адресу RAM.
- **Stack** обычно используется для кадров вызовов и локальных данных; **heap** — динамическая память; это полезная модель, но реальное размещение оптимизатор может менять.
- **CPU register**: маленькое именованное хранилище в процессоре; x64: `RAX`, `RBX`, `RCX`, `RDX`, `RSP`, `RBP`, `RIP`.
- **Инструкция**: единичная операция процессора, например `mov`, `add`, `cmp`, `jmp`, `call`, `ret`.

## Почему `int` и `float` нельзя пропускать

| Тип / пример | Типичный размер | Как интерпретируется |
|---|---:|---|
| `std::uint8_t` | 1 байт | 0…255 |
| `std::int32_t` | 4 байта | целое число со знаком |
| `std::uint32_t` | 4 байта | беззнаковое целое |
| `float` (IEEE 754 binary32) | 4 байта | знак, порядок, мантисса |
| `double` (IEEE 754 binary64) | 8 байт | дробное большей точности |
| указатель на обычной x64 Windows | 8 байт | адрес объекта/функции |

Размеры `float`/`double` здесь характерны для современных платформ Windows, но форматы/размеры всегда сверяй с целевой ABI. Содержимое памяти само **не помечено** как «здоровье» или «скорость»; смысл задаёт код, тип и контекст.

```cpp
#include <bit>
#include <cstdint>
#include <iostream>

int main() {
    float speed = 1.0f;
    std::uint32_t bits = std::bit_cast<std::uint32_t>(speed);
    std::cout << std::hex << bits << '\n'; // типичный IEEE 754: 3f800000
}
```

`bit_cast` читает **битовое представление**, а не преобразует число математически (`static_cast<uint32_t>(1.0f)` дало бы `1`). Не перепутай hex-представление числа с порядком байтов в памяти.

## Регистры и вызовы на Windows x64

- `RIP` — адрес следующей инструкции; `RSP` — указатель стека.
- По стандартному соглашению Windows x64 первые **целочисленные/указательные** аргументы передаются через `RCX`, `RDX`, `R8`, `R9`; аргументы floating-point используют XMM-регистры согласно правилам ABI.
- Важны `call`, `ret`, prologue/epilogue, сохранённые регистры, выравнивание стека, shadow space.
- Это **ABI**, а не универсальное правило для Linux: там другие соглашения вызова.

### Крошечная иллюстрация Assembly (псевдо-фрагмент x64)

```asm
mov eax, 100   ; положить 100 в EAX
sub eax, 25    ; вычесть 25 -> 75
cmp eax, 0     ; сравнить с нулём
je  is_zero    ; перейти, если равно
```

Реальный скомпилированный C++ может выглядеть **совсем иначе** из-за оптимизаций. Нельзя утверждать, что одна конкретная последовательность инструкций обязательно соответствует одной строке исходника.

## Какие термины узнать

`address`, `offset`, `alignment`, `padding`, `stack frame`, `heap allocation`, `page`, `access violation`, `ASLR`, `DEP/NX`, `call stack`, `symbol`, `endianness`, `ABI`, `32-bit vs 64-bit`. Умей пересказать **своими словами** и показать на своём примере.

### Практика и коммиты

Сделай `memory_lab.cpp`, который печатает `sizeof`, `alignof`, адрес локальной переменной, адрес поля структуры и hex-представление `float`. Не сохраняй и не используй эти адреса после завершения программы.

```text
feat: inspect primitive type sizes
feat: print field offsets and alignments
feat: demonstrate float bit representation
docs: explain x64 stack and registers
```

**Ссылки:** [Microsoft x64 calling convention](https://learn.microsoft.com/cpp/build/x64-calling-convention), [x64 software conventions](https://learn.microsoft.com/cpp/build/x64-software-conventions), [Virtual memory](https://learn.microsoft.com/windows/win32/memory/virtual-memory), [C++ `std::bit_cast`](https://en.cppreference.com/w/cpp/numeric/bit_cast), [Intel Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html).

---

# 8. Отладка — перестать гадать, почему код сломался

**Debugger** останавливает программу и показывает текущее состояние. **Логи** объясняют последовательность событий без пошаговой остановки. **Тесты** проверяют ожидаемое поведение автоматически. Нужны все три инструмента.

## Breakpoint, step, watch, call stack

| Инструмент | Что происходит |
|---|---|
| Breakpoint | Выполнение останавливается в выбранном месте |
| Step Over | Выполнить текущую строку, не заходя внутрь вызываемой функции |
| Step Into | Зайти внутрь функции |
| Step Out | Закончить текущую функцию и вернуться к вызывающему коду |
| Watch | Следить за выражением / переменной |
| Locals | Посмотреть доступные локальные переменные |
| Call Stack | Увидеть цепочку вызовов функций |
| Conditional breakpoint | Остановиться при выполнении условия |

## Намеренно ошибочный код: найди проблему

```python
def average_score(scores):
    return sum(scores) / len(scores)

print(average_score([]))  # ZeroDivisionError
```

1. Запусти под дебаггером, поставь breakpoint на `return`.
2. Проверь `scores` и `len(scores)`.
3. Реши правило для пустого списка, например явно `raise ValueError`.
4. Добавь тест и коммит `fix: reject empty score list`.

## Отладка C++: разница Debug vs Release

Собирать с символами отладки: в MSVC Debug-проекте они обычно есть; для Release настройки проверяй отдельно. `.pdb` связывает машинный код с именами, исходниками и строками. При оптимизации часть значений «исчезнет» или переместится в регистры — это **нормально**.

```cpp
#include <vector>
#include <iostream>

int main() {
    std::vector<int> items{10, 20};
    std::cout << items.at(5) << '\n'; // ожидаем исключение out_of_range
}
```

`at()` проверяет границы и бросает исключение. `operator[]` такой гарантии не даёт, и выход за границы — UB. Используй этот пример, чтобы увидеть стек вызовов и обработку исключения в Visual Studio.

## Чем пользоваться

- **VS Code / Zed:** базовые точки останова Python/.NET (конкретные возможности зависят от расширений и версии).
- **Visual Studio Debugger:** очень удобен для C#/C++ и символов.
- **WinDbg:** серьёзная диагностика Windows-программ и дампов.
- **x64dbg:** динамический анализ пользовательских Windows-приложений (начни со своего тестового `.exe`).

**Схема поиска багов:** воспроизведи → запиши ожидание и факт → найди минимальный пример → breakpoint/логи → исправь **причину** → тест → Git-коммит.

### Git-коммиты

```text
test: reproduce empty input failure
fix: handle empty input explicitly
test: cover invalid vector indices
docs: add debugging checklist
```

**Ссылки:** [VS Debugging](https://learn.microsoft.com/visualstudio/debugger/), [WinDbg](https://learn.microsoft.com/windows-hardware/drivers/debugger/), [x64dbg](https://x64dbg.com/), [Python pdb](https://docs.python.org/3/library/pdb.html).

---

# 9. Reverse Engineering — изучение работы собранных программ

**Reverse Engineering (RE)** = восстановление свойств и поведения программы по её бинарнику/наблюдениям. Дизассемблер показывает инструкции; декомпилятор даёт **приблизительный** C-подобный текст — не точный исходник. Начни с собственного кода, где можешь сравнить предположение с оригиналом.

## Рабочая схема без гадания

1. Напиши маленькую программу с функциями `damage`, `move_player`, `save`.
2. Собери `Debug` и `Release` для x64, сохрани исходники.
3. Запусти обе версии на тестовых данных, запиши наблюдаемое поведение.
4. Открой **свой EXE** в Ghidra: посмотри PE-заголовки, секции, строки, imports.
5. Изучи список функций, граф вызовов, decompiler; переименуй обнаруженные функции **в своей базе анализа**.
6. Сопоставь дизассемблирование и декомпиляцию с исходником. Объясни отличия Debug/Release.
7. В x64dbg открой свою тестовую программу; попробуй breakpoint и inspect registers/call stack.
8. Оформи отчёт: «какую гипотезу проверял, на какие наблюдения опирался, какие есть ограничения».

**Не требуется:** обход античитов, внедрение кода в чужие онлайн-игры, скрытое управление сторонним ПО. Эти действия не нужны для приобретения базовых навыков RE.

## Как читать основные элементы PE

| Элемент | Что показывает |
|---|---|
| DOS/PE headers | Что это за Windows-бинарник, архитектура, общая структура |
| `.text` | Обычно исполняемый код |
| `.rdata` | Обычно константы/читаемые данные |
| `.data` | Обычно изменяемые глобальные данные |
| import table | Внешние функции/библиотеки, которые использует приложение |
| export table | Функции/символы, которые бинарник предоставляет наружу |
| relocations | Информация, нужная для переноса адресов при загрузке |

Названия секций **соглашение**, не строгая гарантия; packer и компилятор могут организовать их иначе. ASLR делает адреса запуска нестабильными. PDB может дать имена/типы только если символы доступны.

## Ghidra: коротко по кнопкам

- Создай Project → Import File → выбери **свой** `.exe` → Analyze.
- **Symbol Tree** — функции/метки, **Listing** — адреса и инструкции, **Decompiler** — псевдокод.
- Двойной щелчок по имени/адресу — перейти; переименование отражает твою гипотезу, не «доказательство» её истинности.
- **Strings** — подсказки к поведению программы, но не полный список её функций.
- Не открывай неизвестные бинарники вне изолированной исследовательской среды и не запускай сомнительные файлы.

## Эксперимент для понимания оптимизаций

`lab.cpp`:

```cpp
#include <cstdint>

std::int32_t apply_damage(std::int32_t hp, std::int32_t damage) {
    return (damage <= 0) ? hp : ((damage >= hp) ? 0 : hp - damage);
}

int main() {
    volatile std::int32_t result = apply_damage(100, 25);
    return result == 75 ? 0 : 1;
}
```

Сравни Release и Debug. Оптимизатор может встроить функцию или вычислить значение заранее. `volatile` не гарантирует сохранения конкретного вызова или исходного вида машинного кода.

### Git-коммиты

```text
feat: add sample reverse-engineering target
build: produce debug and release artifacts
docs: map PE sections and imported functions
docs: compare decompiled code to original source
```

**Мини-проект:** `RE-report.md` для собственной программы: таблица функций, PE-секций, отличие сборок и скриншоты результатов.

**Ссылки:** [Ghidra project](https://github.com/NationalSecurityAgency/ghidra), [Ghidra docs](https://ghidra-sre.org/), [x64dbg docs](https://help.x64dbg.com/), [PE format](https://learn.microsoft.com/windows/win32/debug/pe-format), [Cutter](https://cutter.re/).

---

# 10. Собственная игровая песочница и инструменты разработчика

**Цель:** собери настоящий законченный продукт, но с полным контролем над исходниками и разрешением на тестирование. Он объединит темы лучше, чем случайные кусочки кода.

## Компоненты проекта

```text
lab-course/
├── README.md
├── .gitignore
├── docs/
│   ├── architecture.md
│   ├── save-format.md
│   └── re-report.md
├── python-tools/        # конвертер/инспектор сохранений
├── csharp-gui/          # WinForms/WPF панель инструментов
├── cpp-game/            # офлайн-симулятор с управляемыми правилами
├── windows-monitor/     # диагностика своей программы
└── tests/               # тестовые данные и сценарии
```

## Что значит «игровые devtools» на практике

- **Developer console:** `help`, `status`, `damage 10`, `heal 10`, `teleport 5 8`, `pause`, `resume` — команды внутри **своей игры**.
- **Debug HUD:** HP, координаты, FPS/tick rate, текущий режим — читаются напрямую из твоего состояния.
- **Save Inspector:** показывает и проверяет формат своего сохранения.
- **Game settings:** разрешённые тестовые флаги, например `invulnerable` или `infinite_stamina` внутри своего симулятора.
- **Logger:** файл событий, ошибок, обновлений состояния.
- **Test panel:** кнопки Reset, Load, Save, SpawnTestItem в GUI.
- **Diagnostics:** версия сборки, PID текущей программы, сведения о среде, тайминги.

## Пример безопасной команды собственной игры

```python
class Game:
    def __init__(self):
        self.hp = 100
        self.invulnerable = False

    def execute_dev_command(self, command: str) -> str:
        parts = command.strip().split()
        if not parts:
            return "Empty command"
        if parts == ["status"]:
            return f"HP={self.hp}, invulnerable={self.invulnerable}"
        if parts == ["invulnerable", "on"]:
            self.invulnerable = True
            return "Invulnerable ON"
        if parts == ["invulnerable", "off"]:
            self.invulnerable = False
            return "Invulnerable OFF"
        return "Unknown command"

lab = Game()
print(lab.execute_dev_command("status"))
print(lab.execute_dev_command("invulnerable on"))
```

Для реального продукта команды на изменение состояния доступны **только в локальном developer-режиме**. Добавь проверки входных данных, справку по командам, логирование и тесты. Для работы с файлами/сетью никогда не исполняй введённую строку как произвольный Python-код через `eval`/`exec`.

## План этапов: каждый шаг = проверяемый коммит

| Этап | Что реализовать | Пример коммита |
|---|---|---|
| 1 | Состояние `Player`, HP, позиция | `feat: add game state model` |
| 2 | Тики и команды перемещения | `feat: implement simulation loop` |
| 3 | Сохранение / загрузка | `feat: persist game state to JSON` |
| 4 | Бинарный формат с версией | `feat: add versioned binary save format` |
| 5 | Python CLI-инспектор | `feat: build save inspection tool` |
| 6 | C# GUI с таблицей параметров | `feat: add desktop inspector GUI` |
| 7 | C++ симулятор | `feat: port simulation core to C++` |
| 8 | WinAPI диагностика | `feat: show own process diagnostics` |
| 9 | Debug console и HUD | `feat: add local developer console` |
| 10 | Тесты ошибок и повреждённых файлов | `test: add invalid save cases` |
| 11 | Анализ Release в Ghidra | `docs: add binary analysis report` |
| 12 | Версия, README, скриншоты, сборка | `release: prepare v1.0.0` |

**Что считать «полноценным»:** воспроизводимая сборка, понятный README, минимальные тесты, обработка неверного ввода, лицензии библиотек, список известных ограничений, скриншоты, теги Git-релиза.

### Финальные команды Git

```powershell
git status
git add -A
git commit -m "release: prepare v1.0.0"
git tag v1.0.0
git push
git push origin v1.0.0
```

`tag` отмечает конкретный коммит; он **не создаёт автоматически** установщик, артефакты и страницу релиза. Чтобы выпускать сборки автоматически, отдельно изучи GitHub Actions.

**Ссылки:** [GitHub Actions](https://docs.github.com/en/actions), [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases), [CMake](https://cmake.org/cmake/help/latest/), [pytest](https://docs.pytest.org/).

---

# 11. Важные уточнения, которые экономят недели

## Частые заблуждения

1. **«Знать синтаксис = уметь программировать» — нет.** Важнее уметь делить задачу на функции, проверять входные данные и искать причину ошибки.
2. **`int` и `float` не мелочь.** Это разные представления байтов; `0.1 + 0.2 == 0.3` (в Python и на типичных double) может оказаться ложным из-за погрешности.
3. **C# не «упрощённый C++».** Это отдельный язык с другой моделью памяти и runtime.
4. **`&` и `*` в C++ имеют разные значения в зависимости от контекста.** `int&` при объявлении — ссылка; `&x` в выражении — адрес.
5. **Виртуальная память — не просто физическая RAM.** У процесса своё адресное пространство, существуют отображённые файлы и защита страниц.
6. **Адрес и offset — не одно и то же.** Адрес указывает место в пространстве памяти; offset — смещение относительно чего-то.
7. **Вывод декомпилятора — не исходник.** Имена, типы, циклы и порядок операций могут быть реконструированы неправильно.
8. **Debug и Release ведут себя по-разному при UB.** Если ошибка «исчезла» в Debug, это ещё не исправление.
9. **Секреты нельзя выкладывать в Git.** Даже private-репозиторий не заменяет управление секретами.
10. **Коммит — не backup облака.** Только после `push` история оказывается на удалённом сервере; и он тоже не единственный резервный носитель.
11. **Права и безопасность:** изучай чужие бинарники/игры только с разрешения; сторонние сервисы и античиты имеют свои правила.
12. **Не отключай Windows Defender/UAC или ограничения запуска ради непонятного туториала.** Если требуется это сделать — выясни причину и найди безопасную альтернативу.

## Таблица распространённых ошибок

| Видишь | Обычно означает | Что проверить |
|---|---|---|
| `python is not recognized` | Python нет в PATH/некорректная установка | `py --version`, установку Python |
| `ModuleNotFoundError` | Не установлен пакет **в текущем Python-окружении** | `python -m pip show PACKAGE`, выбранный интерпретатор |
| `SyntaxError` / `IndentationError` | Синтаксис Python или отступы | строку ошибки и соседние строки |
| `CS0103` | C# имя недоступно в текущем контексте | опечатка, область видимости, `using` |
| `CS0246` | Тип или namespace не найден | зависимость, `using`, имя |
| `LNK2019` | Линкер не нашёл реализацию символа | добавлен ли `.cpp`/библиотека, совпадают ли сигнатуры |
| `C1083` | Компилятор не смог открыть файл | `#include`, include path, SDK |
| `Access violation` | Недопустимый доступ к памяти | невалидный указатель, границы, lifetime |
| `git: nothing to commit` | Нет новых подготовленных изменений | `git status`, `git diff` |
| `non-fast-forward` при push | У удалённой ветки есть новые коммиты | `git fetch`, проверь историю перед объединением |
| Программа исчезает сразу | Консоль завершается после окончания | запуск через терминал / точка останова |

---

# 12. Шпаргалка «что учить / что пока не учить»

| Изучить обязательно сначала | Отложить до реальной необходимости |
|---|---|
| Типы, `if`, циклы, функции, ошибки | Архитектура драйверов ядра |
| Файлы, JSON, байты, `struct` | Собственный компилятор |
| Git, ветки, коммиты и тесты | Сложный Git rebase на старте |
| C# классы, .NET CLI, простые UI | Огромные enterprise-фреймворки |
| C++ ссылки, указатели, RAII, STL | Шаблонная метапрограмма C++ |
| Windows API, процессы, DLL, PE | Неподписанные драйверы и kernel hooking |
| Стек, куча, x64, ABI, CPU-регистры | Микроархитектура CPU и SIMD-оптимизации |
| Breakpoints, watch, symbols | Сложные трассировочные системы |
| Ghidra, дизассемблер, исследование своего EXE | Упаковщики, обфускация и способы обхода защит |

## Быстрая самопроверка по главам

- [ ] Могу объяснить разницу между `git add`, `commit` и `push`.
- [ ] Могу написать Python-функцию с проверкой входных данных и тестом.
- [ ] Могу объяснить, из каких байтов состоит моё сохранение.
- [ ] Могу открыть JSON в C# и показать значения в GUI.
- [ ] Могу объяснить C++ `&`, `*`, `nullptr`, `vector`, `sizeof`, `alignof`.
- [ ] Могу собрать C++ Debug/Release через CMake.
- [ ] Могу вывести PID собственной Windows-программы.
- [ ] Могу объяснить hex, little-endian, стек/кучу и назначение `RIP`.
- [ ] Могу поставить breakpoint и прочитать call stack.
- [ ] Могу открыть свой EXE в Ghidra и различить imports/sections/functions.
- [ ] Могу показать работающую LabGame с GUI/консолью, документацией и тестами.

---

# 13. Дневной распорядок и использование справочника

**Одна учебная сессия (60–90 мин):** 10 минут повторить вчерашний код → 35–60 минут сделать одну фичу руками → 10 минут проверить ошибки и тесты → 5 минут сделать осмысленный коммит → 5 минут записать, что понял и что осталось непонятным.

**Порядок при новой теме:** прочитай короткое объяснение выше → перепечатай пример → измени значение или условие → сломай код намеренно и найди ошибку → сохрани исправление → только потом открывай длинную документацию по конкретному вопросу.

**Официальные документы полезны как справочники, а не как обязательная книга от корки до корки.** Сохрани этот `.md` рядом с большим дорожным планом; отмечай галочками освоенные пункты.

**Предложение по времени:** Git/терминал 3–5 дней; Python 4–6 недель; C# 4–6; C++ 8–12; Windows API 4–6; память/CPU 3–5; отладка 2–3; RE 4–6; итоговый проект 6–10 недель. Это ориентиры, а не дедлайны.
