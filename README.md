# Bell Giga Hub Wi-Fi Scheduler

This is an automated Python script that uses Playwright to log into a Bell Giga Hub modem's web administration page and turn the Wi-Fi ON and OFF at scheduled times. The script works by disabling all available Wi-Fi bands and should only be run on a machine with a direct ethernet connection.

The script is designed to be resilient, automatically retrying failed jobs until they succeed.

## Prerequisites

* Python 3.7+

## Setup and Installation

Follow these steps to set up and run the project on your local machine.

### 1. Create a Virtual Environment

It is highly recommended to use a Python virtual environment to manage project dependencies. This keeps your project's packages isolated from your global Python installation.

Navigate to the project's root directory and run:

**On macOS/Linux:**

```Shell
python3 -m venv venv
```

**On Windows:**

```Shell
python -m venv venv
```

### 2. Activate the Virtual Environment

Before installing dependencies, activate the newly created environment.

**On macOS/Linux:**

```Shell
source venv/bin/activate
```

**On Windows (PowerShell):**

```PowerShell
.\venv\Scripts\Activate.ps1
```

### 3. Install Requirements

With the virtual environment activated, install the required Python packages using the `requirements.txt` file.

```Shell
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

After installing the Python packages, you need to download the browser binaries that Playwright uses for automation.

```Shell
playwright install
```

## Configuration

The script requires a `credentials.txt` file in the root directory to store the modem's password and admin URL.

1. Create a file named `credentials.txt`.
2. Add the modem's password to the **first line**.
3. Add the modem's admin page URL to the **second line**.
4. Configure the schedule on line 86 and 87 of `modem_bot.py`

**Example** **`credentials.txt`:**

```
YourModemPasswordHere
http://192.168.2.1/
```

## Usage

To run the bot, simply execute the `modem_bot.py` script from the project's root directory:

```Shell
python modem_bot.py
```

The script will start the scheduler and run continuously. You will need to keep the terminal session open. The script will log its actions to the console, including when jobs are scheduled and when they are executed.
