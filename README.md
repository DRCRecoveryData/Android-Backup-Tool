# Android Backup Tool for Android Forensics

![2024-06-21_153832](https://github.com/DRCRecoveryData/Android-Backup-Tool/assets/85211068/8e2a0113-e87a-41e2-bf29-699d1f1df9df)


## Overview
This tool provides a graphical interface (GUI) application built with PyQt6 and Python, designed to facilitate logical backups of Android devices. It supports various commands to backup, convert `.ab` files to `.tar`, extract `.tar` files, and copy files from the device's SD card.

## Features
- **Backup**: Create full backups of Android devices to a specified directory.
- **Convert to tar**: Convert Android backup `.ab` files to `.tar`.
- **Extract tar**: Extract the contents of a `.tar` file.
- **Copy Files**: Copy files from the device's SD card to the backup directory.

## Requirements
- **Python**: Version 3.6 or higher
- **Dependencies**:
  - PyQt6

Install dependencies using pip:
```bash
pip install PyQt6
```

## Usage
1. **Clone the repository**:
   ```bash
   git clone https://github.com/DRCRecoveryData/Android-Backup-Tool.git
   cd Android-Backup-Tool
   ```

2. **Run the application**:
   ```bash
   python androidbackuptool-gui.py
   ```
   This will launch the GUI application where you can perform various operations.

3. **Select options** from the checkboxes (`Convert to tar`, `Extract tar`).

4. **Specify the Backup Directory**:
   - Click on **Browse** to select the directory where backups should be stored.

5. **Click Apply** to execute the selected command.

6. **Monitor Progress**:
   - The progress of operations (e.g., backup, conversion) will be displayed in the progress bar and log area.
   - Upon completion, a popup will notify you of the backup status.

## Notes
- Ensure `adb` is installed and accessible in your system's PATH for proper functionality of commands.

## Contributions
Contributions are welcome! If you find any issues or have suggestions for improvements, please create an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
