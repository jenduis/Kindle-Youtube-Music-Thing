Ai wrote these, I don't trust them neither you should. 

# Kindle Music Dashboard Setup Guide

This guide provides the steps to configure a **Kindle Paperwhite 3** as a dedicated music display for the **YouTube Music Desktop App (ytmdesktop)**.

---

## 1. Windows Server Configuration

### Environment Setup

1. Install **Python 3.10** or higher on your Windows machine.
2. Install the YouTube Music Desktop App (v2.x).
3. Open your terminal and install the required Python libraries:
`pip install flask requests Pillow`

### Application Settings

1. Open the YouTube Music Desktop App.
2. Navigate to **Settings > Integrations > Companion Server**.
3. Enable the companion server on port **9863**.
4. Disable **Protect API with Password**.

### Obtaining the Authentication Token

The v2 API requires a specific handshake. To get your permanent token:

1. Run the `auth_helper.py` script (provided in the repository).
2. A popup will appear inside the YouTube Music Desktop App.
3. Select **Allow**.
4. Copy the long alphanumeric token string printed in your terminal.
5. Open `kindle_server.py` and paste this string into the `TOKEN` variable.

---

## 2. Kindle Device Configuration

### Prerequisites

* Your Kindle Paperwhite 3 must be jailbroken.
* **FBInk** must be installed to handle image rendering to the screen.
* **Kterm** or an SSH client must be available to run commands.

### Network Connection

1. Ensure both your PC and your Kindle are on the same local Wi-Fi network.
2. Find your PC's local IP address (e.g., 192.168.1.50).
3. Open the `music.sh` file provided in this repository.
4. Replace `192.168.1.XX` with your PC's actual local IP address.

---

## 3. Running the Dashboard

### Initialization

1. Start the server on your Windows PC by running:
`python kindle_server.py`
2. Start playing music in the YouTube Music Desktop App.
3. On your Kindle, open **Kterm** and navigate to the directory containing `music.sh`.
4. Execute the script:
`sh music.sh`

### Power Management

The script automatically disables the Kindle's screensaver timeout while running. To manually disable the screensaver at any time, type `~ds` into the Kindle's home screen search bar and press Enter. A device restart will re-enable standard power management.

---

## 4. Troubleshooting

### Connection and Authentication

* **401 Error:** If the Kindle displays an unauthorized message, the token is invalid. Delete the existing token in the YouTube Music App settings and re-run the `auth_helper.py` script.
* **429 Error:** This indicates the PC is requesting data too frequently. The server includes a 2-second cache to prevent this, but ensuring the Kindle script has a `sleep 5` command is recommended.

### Visual Issues

* **Missing Text:** If Japanese characters do not appear, ensure the `MS Gothic` font file (`msgothic.ttc`) is present in your Windows `C:\Windows\Fonts` directory.
* **Ghosting:** E-ink screens retain artifacts. The script is configured to use high-contrast grayscale to minimize this effect.
