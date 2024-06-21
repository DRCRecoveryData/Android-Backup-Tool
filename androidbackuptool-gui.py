import sys
import os
import subprocess
from tarfile import is_tarfile
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QProgressBar, QPlainTextEdit, QMessageBox, QCheckBox
from PyQt6.QtCore import QThread, pyqtSignal

# Constants for AB to Tar conversion
AB_HEADER = b"ANDROID BACKUP"
TAR_HEADER = b"\x1f\x8b\x08\x00\x00\x00\x00\x00"
IGNORE_OFFSET = 24

class LogicalBackupApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Android Backup Tool")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.backup_label = QLabel("Backup Directory:")
        self.backup_path_edit = QLineEdit()
        self.browse_button = QPushButton("Browse", self)
        self.browse_button.setObjectName("browseButton")
        self.browse_button.clicked.connect(self.browse_backup_directory)

        self.convert_checkbox = QCheckBox("Convert to tar file")
        self.extract_checkbox = QCheckBox("Extract tar file")

        self.execute_button = QPushButton("Apply", self)
        self.execute_button.setObjectName("blueButton")
        self.execute_button.clicked.connect(self.execute_command)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)

        layout.addWidget(self.backup_label)
        layout.addWidget(self.backup_path_edit)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.convert_checkbox)
        layout.addWidget(self.extract_checkbox)
        layout.addWidget(self.execute_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.log_box)

        self.setLayout(layout)

        self.setStyleSheet("""
        QPushButton#blueButton, #browseButton {
            background-color: #3498db;
            border: none;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 4px;
        }
        QPushButton#blueButton:hover, #browseButton:hover {
            background-color: #2980b9;
        }
        """)

        self.worker = None

    def browse_backup_directory(self):
        backup_directory = QFileDialog.getExistingDirectory(self, "Select Backup Directory")
        if backup_directory:
            self.backup_path_edit.setText(backup_directory)

    def execute_command(self):
        backup_directory = self.backup_path_edit.text()

        if not backup_directory:
            self.show_message("Error", "Please select a backup directory.")
            return

        self.worker = LogicalBackupWorker(backup_directory, self.convert_checkbox.isChecked(), self.extract_checkbox.isChecked())
        self.worker.log_updated.connect(self.update_log)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.backup_finished.connect(self.show_backup_completed_popup)
        self.worker.start()

    def update_log(self, message):
        self.log_box.appendPlainText(message)

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def show_backup_completed_popup(self, message):
        QMessageBox.information(self, "Backup Completed", message)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

class LogicalBackupWorker(QThread):
    progress_updated = pyqtSignal(int)
    log_updated = pyqtSignal(str)
    backup_finished = pyqtSignal(str)

    def __init__(self, backup_directory, convert, extract):
        super().__init__()
        self.backup_directory = backup_directory
        self.convert = convert
        self.extract = extract

    def run(self):
        try:
            devices = self.list_connected_devices()
            self.progress_updated.emit(10)
            if devices:
                device_serial = self.get_device_serial(devices)
                self.progress_updated.emit(20)
                if device_serial:
                    backup_file = self.backup_android(device_serial, self.backup_directory)
                    self.progress_updated.emit(50)
                    if backup_file:
                        if self.convert:
                            tar_file = self.extract_tar_from_ab(backup_file, self.backup_directory)
                            self.progress_updated.emit(75)
                            if tar_file and self.extract:
                                self.extract_tar_file(tar_file, self.backup_directory)
                                self.progress_updated.emit(100)
                        self.copy_files_from_sdcard(device_serial, self.backup_directory)
            else:
                self.log_updated.emit("No devices connected. Please connect a device and try again.")
                self.progress_updated.emit(0)
        except Exception as e:
            self.log_updated.emit(f"Error: {e}")
            self.progress_updated.emit(0)
        self.backup_finished.emit("Backup process completed.")

    def list_connected_devices(self):
        adb_path = 'adb'
        process = subprocess.Popen([adb_path, 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            self.log_updated.emit(f"Error occurred: {stderr.decode('utf-8')}")
            return None
        
        devices_output = stdout.decode('utf-8').strip().split('\n')
        devices = [line.split()[0] for line in devices_output if 'device' in line and 'devices' not in line]
        
        if not devices:
            self.log_updated.emit("No devices found")
            return None
        
        self.log_updated.emit("Connected devices:")
        for device in devices:
            self.log_updated.emit(device)
        return devices

    def get_device_serial(self, devices):
        if devices:
            return devices[0]
        return None

    def backup_android(self, device_serial, backup_dir):
        adb_path = 'adb'
        backup_file = os.path.join(backup_dir, "backup.ab")
        
        adb_command = [adb_path, '-s', device_serial, 'backup', '-all', '-f', backup_file]
        
        self.log_updated.emit("Please unlock your phone and confirm the backup operation.")
        
        try:
            process = subprocess.Popen(adb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self.log_updated.emit(f"Error occurred: {stderr.decode('utf-8')}")
            else:
                self.log_updated.emit(f"Backup completed successfully. File saved as {backup_file}")
                return backup_file
        
        except Exception as e:
            self.log_updated.emit(f"An error occurred: {str(e)}")
        
        return None

    def extract_tar_from_ab(self, path_to_ab, output_dir=None):
        if output_dir is None:
            output_dir = os.path.dirname(path_to_ab)

        try:
            ab_data = open(path_to_ab, 'rb')
        except:
            self.log_updated.emit(f"Unable to open AB file at {path_to_ab}")
            return False

        ab_bytes_to_remove = ab_data.read(24)

        if ab_bytes_to_remove[:14] == AB_HEADER:
            self.log_updated.emit("AB Header checked and intact")
        else:
            self.log_updated.emit("AB Header not found; is it definitely the right file?")
            return False

        output_path = self.build_tar_filepath(path_to_ab, output_dir)

        try:
            output_file = open(output_path, 'wb')
        except:
            self.log_updated.emit(f"Unable to open file at {output_path}")
            return False

        self.log_updated.emit("Writing tar header..")
        output_file.write(TAR_HEADER)

        self.log_updated.emit("Writing rest of AB file..")
        output_file.write(ab_data.read())

        self.log_updated.emit("..done.")
        self.log_updated.emit("Closing files..")

        output_file.close()
        ab_data.close()

        try:
            test_val = is_tarfile(output_path)
            self.log_updated.emit("Output verified OK")
            return output_path
        except:
            self.log_updated.emit("Verification failed; maybe it's encrypted?")
            return False

    def build_tar_filepath(self, input_path, output_dir):
        output_filename = "backup.tar"
        self.log_updated.emit(f"Output filename: {output_filename}")
        output_filepath = os.path.join(output_dir, output_filename)
        return output_filepath

    def extract_tar_file(self, tar_file, output_dir):
        try:
            extract_dir = os.path.join(output_dir, os.path.splitext(os.path.basename(tar_file))[0])
            os.makedirs(extract_dir, exist_ok=True)
            
            process = subprocess.Popen(['tar', '-xvf', tar_file, '-C', extract_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self.log_updated.emit(f"Error occurred during extraction: {stderr.decode('utf-8', 'ignore')}")
            else:
                self.log_updated.emit(f"Extraction of {tar_file} completed successfully to {extract_dir}.")
        except Exception as e:
            self.log_updated.emit(f"An error occurred during extraction: {str(e)}")

    def copy_files_from_sdcard(self, device_serial, backup_dir):
        adb_path = 'adb'
        sdcard_path = '/sdcard/'

        self.log_updated.emit(f"Fetching files from {sdcard_path} on the device to {backup_dir}.")

        try:
            process = subprocess.Popen([adb_path, '-s', device_serial, 'pull', sdcard_path, backup_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                self.log_updated.emit(f"Error occurred during file retrieval from device: {stderr.decode('utf-8')}")
            else:
                self.log_updated.emit(f"Files retrieved successfully from {sdcard_path} on the device to {backup_dir}.")

        except Exception as e:
            self.log_updated.emit(f"An error occurred during file retrieval from device: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LogicalBackupApp()
    window.show()
    sys.exit(app.exec())
