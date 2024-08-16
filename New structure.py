import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore

class WebcamApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Webcam Application")

        self.camera_label = QLabel("Camera Frame")
        self.camera_frame = QLabel()
        self.camera_frame.setFixedSize(640, 480)
        self.camera_layout = QVBoxLayout()
        self.camera_layout.addWidget(self.camera_label)
        self.camera_layout.addWidget(self.camera_frame)

        self.captured_label = QLabel("Captured Image")
        self.captured_frame = QLabel()
        self.captured_frame.setFixedSize(640, 480)
        self.captured_layout = QVBoxLayout()
        self.captured_layout.addWidget(self.captured_label)
        self.captured_layout.addWidget(self.captured_frame)

        self.rgb_values_panel = QGroupBox("RGB Values")
        self.rgb_values_layout = QVBoxLayout()
        # Add widgets for displaying RGB values here
        self.rgb_values_panel.setLayout(self.rgb_values_layout)

        self.controls_layout = QHBoxLayout()
        self.capture_button = QPushButton("Capture Image")
        self.save_button = QPushButton("Save Image")
        self.exit_button = QPushButton("Exit")
        self.controls_layout.addWidget(self.capture_button)
        self.controls_layout.addWidget(self.save_button)
        self.controls_layout.addWidget(self.exit_button)

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.camera_layout)
        self.layout.addLayout(self.captured_layout)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.layout)
        main_layout.addWidget(self.rgb_values_panel)
        main_layout.addLayout(self.controls_layout)

        self.setLayout(main_layout)

        self.webcam = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(10)

    def update_frame(self):
        ret, frame = self.webcam.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.camera_frame.setPixmap(QPixmap.fromImage(q_img))

    def capture_image(self):
        ret, frame = self.webcam.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            q_img = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
            self.captured_frame.setPixmap(QPixmap.fromImage(q_img))

    def save_image(self):
        # Implement save image functionality here
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WebcamApp()
    win.show()
    sys.exit(app.exec_())
