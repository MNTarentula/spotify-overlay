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

## Requirements

* Windows
* Spotify
* Spotify must be open before launching the overlay.
* The Spotify main window must be larger than **200 × 200 pixels**.

The overlay uses Windows APIs through Python `ctypes` to detect and follow the Spotify window.

## Installation

Download the `.exe` file from the **Releases** section and run it.

**Python is not required.** The released executable contains everything needed to run the overlay.

## Known Limitations

* Tested on **Windows 11** only.
* Other Windows versions have not been tested, although they should work.
* If the Spotify process is renamed, the overlay may not work.
* Spotify can be minimized or hidden after the overlay is launched.
* Spotify must be open when the overlay is launched.
* The Spotify main window must be larger than **200 × 200 pixels**.

## Reporting Problems

If you find a problem, feel free to report it to me through **Discord or email**.

When reporting a problem, please include:

* What happened.
* What you expected to happen.
* If possible, how to reproduce the problem.

## License

See the repository for license information.
