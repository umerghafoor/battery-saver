import sys
from PyQt6.QtCore import Qt, QTimer,QPoint
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QSlider, QPushButton, QVBoxLayout, QWidget, QLineEdit,QHBoxLayout,QFrame
from battery_monitor import BatteryMonitor

class CustomTitleBar(QWidget):

    def __init__(self, parent):
        super(CustomTitleBar, self).__init__()
        self.parent = parent
        print(self.parent.width())
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10,5,5,5)
        self.title = QLabel("Battery Saver")

        btn_size = 25

        self.btn_close = QPushButton("x")
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setFixedSize(btn_size,btn_size)

        self.btn_min = QPushButton("-")
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(btn_size, btn_size)

        self.title.setFixedHeight(35)
        self.title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_close)


        self.setLayout(self.layout)

        self.start = QPoint(0, 0)
        self.pressing = False

    def resizeEvent(self, QResizeEvent):
        super(CustomTitleBar, self).resizeEvent(QResizeEvent)
        self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.parent.width(),
                                self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False


    def btn_close_clicked(self):
        self.parent.close()

    def btn_max_clicked(self):
        self.parent.showMaximized()

    def btn_min_clicked(self):
        self.parent.showMinimized()
        self.draggable = False

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Battery Monitor")

# Set the window flags to create a frameless window
window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
window.setFixedHeight(500)
window.setFixedWidth(200)

# Create a custom title bar
title_bar = CustomTitleBar(window)
window.setMenuWidget(title_bar)

battery_monitor = BatteryMonitor(threshold=90)

battery_label = QLabel("Battery Level: -")
battery_threshold = QLabel("Battery threshold: 90%")
slider = QSlider(Qt.Orientation.Vertical)
slider.setRange(0, 100)
slider.setValue(90)

update_button = QPushButton("Update Battery")
loop_time_label = QLabel("Loop Time (seconds):")
loop_time_entry = QLineEdit("60")
loop_time_entry.setAlignment(Qt.AlignmentFlag.AlignCenter)


layout = QVBoxLayout()
layout.addWidget(battery_label)
layout.addWidget(slider, alignment=Qt.AlignmentFlag.AlignHCenter)
layout.addWidget(battery_threshold)
layout.addWidget(update_button)
layout.addWidget(loop_time_label)
layout.addWidget(loop_time_entry)

widget = QWidget()
widget.setLayout(layout)
window.setCentralWidget(widget)

# Apply styling using a separate CSS file
with open("style.css", "r") as f:
    style = f.read()
    app.setStyleSheet(style)

def update_battery_label():
    battery_percent = battery_monitor.update_battery_label()
    battery_label.setText(f"Battery Level : {battery_percent}%")
    loop_time = int(loop_time_entry.text())
    QTimer.singleShot(loop_time * 1000, update_battery_label)


def on_slider_changed(value):
    threshold_value = slider.value()
    battery_monitor.set_threshold(threshold_value)
    battery_threshold.setText(f"Battery threshold : {threshold_value}%")


def check_battery_level():
    battery_monitor.check_battery_level()
    loop_time = int(loop_time_entry.text())
    QTimer.singleShot(loop_time * 1000, check_battery_level)


slider.valueChanged.connect(on_slider_changed)
update_button.clicked.connect(check_battery_level)

update_battery_label()
check_battery_level()

window.show()
sys.exit(app.exec())
