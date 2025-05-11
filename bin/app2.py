import sys
import serial
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal

# Thread class for reading serial data
class SerialReaderThread(QThread):
    new_data = pyqtSignal(str)

    def __init__(self, port, output_file):
        super().__init__()
        self.port = port
        self.output_file = output_file
        self.running = True

    def run(self):
        try:
            ser = serial.Serial(self.port, 9600)
            time.sleep(2)  # wait for Arduino reset
            with open(self.output_file, "w") as file:
                while self.running:
                    try:
                        line = ser.readline().decode().strip()
                        if line:
                            self.new_data.emit(f"[{self.port}] {line}")
                            file.write(line + "\n")
                            file.flush()
                    except serial.SerialException:
                        self.new_data.emit(f"[{self.port}] Arduino disconnected")
                        break
        except serial.SerialException:
            self.new_data.emit(f"[{self.port}] Unable to connect to Arduino")

    def stop(self):
        self.running = False
        self.quit()
        self.wait()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dual Arduino Logger")
        self.setFixedSize(600, 500)

        # Dark mode styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QTextEdit {
                background-color: #363636;
                color: #ffffff;
                border: 1px solid #555555;
            }
            QPushButton {
                background-color: #444444;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)

        # Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Widgets
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)

        self.button = QPushButton("Run Script")
        self.button.clicked.connect(self.run_script)
        layout.addWidget(self.button)

        # Threads (init to None)
        self.thread1 = None
        self.thread2 = None

    def run_script(self):
        # Prevent multiple starts
        if self.thread1 is not None or self.thread2 is not None:
            self.text_area.append("Script already running.")
            return

        # Define Arduino configs (adjust ports if needed)
        arduino1_port = "COM3"
        arduino2_port = "COM4"
        output1_file = "C:\\LAUN\\excel\\arduino1_output.csv"
        output2_file = "C:\\LAUN\\excel\\arduino2_output.csv"

        # Create and start threads
        self.thread1 = SerialReaderThread(arduino1_port, output1_file)
        self.thread2 = SerialReaderThread(arduino2_port, output2_file)

        self.thread1.new_data.connect(self.text_area.append)
        self.thread2.new_data.connect(self.text_area.append)

        self.thread1.start()
        self.thread2.start()

    def closeEvent(self, event):
        # Ensure threads are properly stopped when closing
        if self.thread1:
            self.thread1.stop()
        if self.thread2:
            self.thread2.stop()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
