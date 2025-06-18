# AutoBackup 📂⏱️➡️📂

AutoBackup is a simple automatic folder backup tool that synchronizes changes every few seconds.

## 🚀 Features

- **Auto-detect changes:** Automatically detects new, modified, or deleted files.
- **Preserves folder structure:** Keeps the directory hierarchy intact.
- **Multiple backup support:** Configure and run several backups at once via a JSON configuration file.
- **Color-coded console output:** Uses the Rich library for informative and pretty output.
- **Configurable retry mechanism:** Adjust reattempts and delays for files that may be temporarily locked.

## ⚙️ Requirements

- Python 3.x
- [Rich](https://github.com/willmcgugan/rich) library (for pretty console output)
- [Watchdog](https://github.com/gorakhargosh/watchdog) library

## 📥 Installation

Install the required packages with pip:

```bash
pip install rich watchdog
```

## 🔧 Usage

### 1. Backup with Source and Target Paths

Run the backup tool by specifying the source and target folders:

```bash
python autobackup.py [SOURCE_FOLDER] [TARGET_FOLDER]
```

Example:

```bash
python autobackup.py "C:\Users\YourName\Documents" "D:\Backups\Documents_backup"
```

Press Ctrl+C to stop the backup.

### 2. Backup with JSON Configuration

Create a JSON configuration file (e.g., `config.json`) that contains multiple backup definitions:

```json
{
    "backups": [
        {
            "source": "C:\\Users\\YourName\\Desktop\\Source1",
            "target": "C:\\Users\\YourName\\Desktop\\Backup1"
        },
        {
            "source": "C:\\Users\\YourName\\Desktop\\Source2",
            "target": "C:\\Users\\YourName\\Desktop\\Backup2"
        }
    ]
}
```

Run the backup tool with the JSON configuration:

```bash
python autobackup.py config.json
```

Press Ctrl+C to stop the backups.

### 3. Handling Locked Files

If files are locked (for example, by an editor) and cannot be copied immediately, the tool will retry copying for a configurable number of attempts with a delay between retries. You can adjust these parameters in the source code if needed.

## ✨ Summary

AutoBackup is a lightweight, flexible tool to keep your folders in sync. Configure it once (either via command line or a JSON configuration file) and let it take care of the rest!

Happy backing up!

---

Follow me on Twitter: [@_bkir0](https://x.com/_bkir0)