
import sys
import serial 
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Area Application")
        self.setFixedSize(500, 400)
        # Set dark mode style sheet
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

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create text area
        self.text_area = QTextEdit()
        layout.addWidget(self.text_area)

        # Create button
        self.button = QPushButton("Run Script")
        self.button.clicked.connect(self.run_script)
        layout.addWidget(self.button)

    def run_script(self):
        try:
            ser = serial.Serial("COM3", 9600)
            time.sleep(2)
            with open("C:\\LAUN\\excel\\output.csv", "w") as file:
                while True:
                    try:
                        line = ser.readline().decode().strip()
                        self.text_area.append(line)
                        file.write(line + "\n")
                        print(line)
                    except serial.SerialException:
                        self.text_area.append("Arduino disconnected")
                        break
        except serial.SerialException:
            self.text_area.append("Unable to connect to Arduino")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
