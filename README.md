# 📸 Screenshoter

> Лёгкий и быстрый инструмент для создания скриншотов на Windows

[![Platform](https://img.shields.io/badge/platform-Windows-blue?style=for-the-badge&logo=windows)](#)
[![Python](https://img.shields.io/badge/python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](#)
[![PyPI](https://img.shields.io/badge/status-ready-success?style=for-the-badge)](#)

---

## 🇷🇺 Русская версия

### ✨ Возможности

- **Мгновенный скриншот** — нажмите `PrintScreen` для захвата экрана
- **Выбор области** — выделите нужный участок экрана мышью
- **Трей-иконка** — удобный доступ через системный трей
- **Предпросмотр** — просмотр скриншота перед сохранением
- **Копирование в буфер** — быстрая вставка в любой мессенджер или редактор
- **Сохранение в PNG** — сохранение с временной меткой в удобном формате
- **Автозагрузка** — возможность запуска вместе с Windows

### 🚀 Установка

#### Из исходного кода

```bash
# Клонируйте репозиторий
git clone https://github.com/medellin17/screenshoter.git
cd screenshoter

# Установите зависимости
pip install -r requirements.txt

# Запустите приложение
python main.py
```

#### Создание исполняемого файла

```bash
# Соберите .exe файл
build.bat

# Готовый файл появится в папке dist/
```

### 📖 Использование

| Действие | Описание |
|----------|----------|
| `PrintScreen` | Сделать скриншот всего экрана |
| `ЛКМ + Drag` | Выделить область для скриншота |
| `Esc` | Отменить выделение / Закрыть окно |
| Трей-иконка | Меню с опциями скриншота и выхода |

### 🏗️ Архитектура

```
📁 screenshoter/
├── 📄 main.py        # Главное приложение, TrayManager, UI
├── 📄 capture.py     # Захват экрана через mss
├── 📄 clipboard.py   # Копирование в буфер обмена (Windows API)
├── 📄 preview.py     # Окно предпросмотра скриншота
├── 📄 overlay.py     # Полноэкранный оверлей для выделения
├── 📄 autostart.py   # Управление автозагрузкой Windows
├── 📄 app.py         # Базовый Tkinter-класс
└── 📄 build.bat      # Скрипт сборки .exe
```

### 📦 Зависимости

| Пакет | Назначение |
|-------|------------|
| [mss](https://github.com/BoboTiG/python-mss) | Захват экрана |
| [Pillow](https://pillow.readthedocs.io/) | Обработка изображений |
| [pynput](https://github.com/moses-palmer/pynput) | Глобальный хоткей `PrintScreen` |
| [pywin32](https://github.com/mhammond/pywin32) | Работа с буфером обмена Windows |
| [pystray](https://github.com/moses-palmer/pystray) | Системный трей |

### 🔧 Требования

- **ОС:** Windows 10/11
- **Python:** 3.8+
- **Разрешение:** Любое (поддержка Fullscreen и multi-monitor)

---

## EN English Version

### ✨ Features

- **Instant Screenshot** — press `PrintScreen` to capture the entire screen
- **Region Selection** — highlight the desired screen area with your mouse
- **Tray Icon** — convenient access via the system tray
- **Preview** — review screenshots before saving
- **Clipboard Copy** — quick paste into any messenger or editor
- **Save as PNG** — save with timestamp in a convenient format
- **Autostart** — option to launch with Windows

### 🚀 Installation

#### From Source

```bash
# Clone the repository
git clone https://github.com/medellin17/screenshoter.git
cd screenshoter

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

#### Build Executable

```bash
# Build the .exe file
build.bat

# The output will be in the dist/ folder
```

### 📖 Usage

| Action | Description |
|--------|-------------|
| `PrintScreen` | Capture the entire screen |
| `LMB + Drag` | Select a region for screenshot |
| `Esc` | Cancel selection / Close window |
| Tray Icon | Menu with screenshot & exit options |

### 🏗️ Architecture

```
📁 screenshoter/
├── 📄 main.py        # Main app, TrayManager, UI
├── 📄 capture.py     # Screen capture via mss
├── 📄 clipboard.py   # Windows clipboard operations
├── 📄 preview.py     # Screenshot preview window
├── 📄 overlay.py     # Fullscreen selection overlay
├── 📄 autostart.py   # Windows autostart management
├── 📄 app.py         # Base Tkinter class
└── 📄 build.bat      # .exe build script
```

### 📦 Dependencies

| Package | Purpose |
|---------|---------|
| [mss](https://github.com/BoboTiG/python-mss) | Screen capture |
| [Pillow](https://pillow.readthedocs.io/) | Image processing |
| [pynput](https://github.com/moses-palmer/pynput) | Global `PrintScreen` hotkey |
| [pywin32](https://github.com/mhammond/pywin32) | Windows clipboard API |
| [pystray](https://github.com/moses-palmer/pystray) | System tray icon |

### 🔧 Requirements

- **OS:** Windows 10/11
- **Python:** 3.8+
- **Resolution:** Any (supports fullscreen and multi-monitor)

---

## 📝 Лицензия / License

MIT License. Подробнее — см. [LICENSE](LICENSE)

---

<div align="center">

**powered by medellin17** | [Открыть issue](../../issues) | [Сделать PR](../../pulls)

</div>
