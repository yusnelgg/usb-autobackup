# AutoBackup 📂⏱️➡️📂

Simple automatic folder backup tool that syncs changes every 5 seconds.

## 🚀 How to Use

1. First install the required package:
   ```bash
   pip install rich
    Run the backup tool:

    bash
    python autobackup.py [SOURCE_FOLDER] [TARGET_FOLDER]
    Example (backup your Documents):

    bash
    python autobackup.py ~/Documents ~/Backups/Documents_backup
    Press Ctrl+C to stop when done

✨ Features
    Auto-detects new and changed files

    Preserves folder structure

    Color-coded console output

    Lightweight and simple

⚙️ Requirements
    Python 3.x

    Rich library (for pretty output)