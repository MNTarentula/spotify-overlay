# Spotify Overlay

A small Windows overlay for controlling Spotify with global hotkeys.

## Features

* ⏭️ Skip to the next song with a global hotkey.
* ⏮️ Go back to the previous song with a global hotkey.
* 🔄 Reopen Spotify with a global hotkey.
* ⌨️ Customize the hotkeys from inside the overlay.
* 🎵 Works with Spotify without requiring Spotify Premium or any additional Spotify features.

## Setting Up Hotkeys

1. Launch the overlay **after Spotify is already open**.
2. In the Spotify window, look near the arrow buttons at the top.
3. You should see a **K** button.
4. Click the **K** button to open the hotkey settings.
5. Click **Set** next to the action you want to change.
6. Press the key you want to use.
7. The new hotkey will be set and can be used globally.
<img width="468" height="267" alt="image" src="https://github.com/user-attachments/assets/7186f337-17ed-4fa7-9756-338933ebfb12" />

## Requirements

* Windows
* Spotify
* Spotify must be open before launching the overlay.
* The Spotify main window must be larger than **200 × 200 pixels**.

The overlay uses Windows APIs through Python `ctypes` to detect and follow the Spotify window.

## Installation

Download the `.exe` file from the **Releases** section and run it.

**Python is not required.** The released executable contains everything needed to run the overlay.

## Editing the Code

If you want to modify the overlay, you can clone or download the repository and edit the Python source directly.

### 1. Install Python

Install **Python 3.12 or a compatible Python version**.

Make sure Python is available from the terminal:

```powershell
python --version
```

### 2. Install the dependencies

Install the required packages:

```powershell
pip install PySide6 psutil pywin32
```

The project also uses Windows APIs through Python `ctypes`, which is included with Python.

### 3. Understand the project structure

The main files are:

```text
Main.py
src/
├── GUI.py
├── reopenSpotify.py
└── skip_song.py

data.json
Main.spec
```

#### `Main.py`

The main entry point of the application.

It connects the different parts of the program and starts the overlay.

If you want to understand how the application starts and how its main systems are connected, start here.

#### `src/GUI.py`

Contains the overlay's graphical interface.

This is where the buttons, settings menu, window positioning, and other GUI-related behavior are handled.

If you want to change how the overlay looks or behaves visually, this is the main file to inspect.

#### `src/skip_song.py`

Contains the functionality used for controlling Spotify playback, such as skipping to the next or previous song.

#### `src/reopenSpotify.py`

Contains the functionality for opening and closing/reopening Spotify.

#### `data.json`

Stores the user's configured hotkeys.

Do not delete this file if you want to keep your saved hotkey configuration.

#### `Main.spec`

PyInstaller's build configuration.

This is used when creating the executable.

---

## Running the Source Code

After installing the dependencies, you can run the project directly without building an executable:

```powershell
python Main.py
```

This is useful when developing because you can change the code and test the changes immediately.

---

## Building Your Own EXE

After modifying the code, you can build your own executable using PyInstaller:

```powershell
python -m PyInstaller --noconsole --onefile --clean Main.py
```

The resulting executable will be created inside:

```text
dist/
```

If you want to use the existing PyInstaller configuration, you can also build from the `.spec` file:

```powershell
python -m PyInstaller Main.spec
```

After building, make sure `data.json` is placed next to the executable if you want the saved hotkey configuration to work.

---

## How the Overlay Works

The overlay is designed specifically around the Windows Spotify desktop application.

The program finds the Spotify window and uses Windows APIs to monitor its position and state. The overlay can then follow the Spotify window when it moves or changes size.

The project uses:

* **PySide6** for the graphical interface.
* **psutil** for process information.
* **pywin32** for Windows process/window functionality.
* **ctypes** for direct access to Windows APIs.
* **PyInstaller** for creating the standalone executable.

The Windows API parts are some of the more complicated parts of the project. If you are trying to learn from the code, `GUI.py` and the window-handling logic are good places to start.

---

## Changing the Project

You are free to experiment with the code.

A simple development workflow is:

```text
1. Clone/download the repository
        ↓
2. Install the dependencies
        ↓
3. Change the Python source
        ↓
4. Run `python Main.py`
        ↓
5. Test your changes
        ↓
6. Build with PyInstaller if needed
        ↓
7. Test the new EXE
```

You do not need to rebuild the EXE every time you change something. Running `python Main.py` is much faster during development.

**Python is not required.** The released executable contains everything needed to run the overlay.

## Known Limitations

* Tested on **Windows 11** only.
* Other Windows versions have not been tested, although they should work.
* If the Spotify process is renamed, the overlay may not work.
* Spotify can be minimized or hidden after the overlay is launched.
* Spotify must be open when the overlay is launched.
* The Spotify main window must be larger than **200 × 200 pixels**.

## Reporting Problems

If you find a problem, feel free to report it to me through **Discord: tarntola264**.

When reporting a problem, please include:

* What happened.
* What you expected to happen.
* If possible, how to reproduce the problem.

