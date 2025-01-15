# Android Backup Tool for Android Forensics

![2024-06-21_153832](https://github.com/DRCRecoveryData/Android-Backup-Tool/assets/85211068/8e2a0113-e87a-41e2-bf29-699d1f1df9df)

![Build Status](https://img.shields.io/github/actions/workflow/status/DRCRecoveryData/Android-Backup-Tool/build.yml)
![License](https://img.shields.io/github/license/DRCRecoveryData/Android-Backup-Tool)
![Version](https://img.shields.io/github/v/release/DRCRecoveryData/Android-Backup-Tool)

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [References](#references)
- [Contact](#contact)

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

## Installation

To install the Android Backup Tool:

1. Download the latest release from the [releases page](https://github.com/DRCRecoveryData/Android-Backup-Tool/releases).
2. Extract the contents to a directory.
3. Ensure you have Python installed. You can download it from [python.org](https://www.python.org/).
4. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
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

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

For issues or suggestions, please open an issue on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

- [Python Programming Language](https://www.python.org/)
- [PyQt6 Library](https://pypi.org/project/PyQt6/)

## Contact

For support or questions, please contact us at [hanaloginstruments@gmail.com](mailto:hanaloginstruments@gmail.com)
