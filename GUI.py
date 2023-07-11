from PyQt6.QtGui import QPainter, QRegion, QMouseEvent
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QApplication, QLabel, QSlider, QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QSystemTrayIcon, QMenu
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QIcon
from battery_monitor import BatteryMonitor


class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super(CustomTitleBar, self).__init__()
        self.parent = parent
        self.draggable = True
        self.dragging_threshold = 5
        self.mousePressPos = None
        self.mouseMovePos = None

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel("Battery Saver")

        btn_size = 32

        self.btn_close = QPushButton("x")
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setFixedSize(btn_size, btn_size)

        self.btn_min = QPushButton("-")
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(btn_size, btn_size)

        self.title.setFixedHeight(35)
        self.title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_close)

        self.setLayout(self.layout)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mousePressPos = event.globalPosition().toPoint()
            self.mouseMovePos = event.globalPosition().toPoint()

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton and self.draggable:
            # Adjust the window position based on the drag distance
            diff = event.globalPosition().toPoint() - self.mouseMovePos
            newPos = self.parent.pos() + diff
            self.parent.move(newPos)

            self.mouseMovePos = event.globalPosition().toPoint()

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if (
            event.button() == Qt.MouseButton.LeftButton
            and self.mousePressPos is not None
        ):
            # Check if the mouse movement exceeded the dragging threshold
            diff = event.globalPosition().toPoint() - self.mousePressPos
            if diff.manhattanLength() > self.dragging_threshold:
                event.ignore()
                return

        super().mouseReleaseEvent(event)

    def btn_close_clicked(self):
        self.parent.close()

    def btn_min_clicked(self):
        self.parent.showMinimized()
        self.parent.hide()
        self.draggable = False


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.Window |
                            Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setGeometry(4, 4, 200, 500)

        def set_style_sheet(filename):
            with open(filename, "r") as f:
                style = f.read()
                self.setStyleSheet(style)

        # Implementation of System tray
        tray_icon = QSystemTrayIcon(self)
        tray_icon.setIcon(QIcon("icon.png"))
        tray_icon.setVisible(True)

        tray_menu = QMenu(self)
        restore_action = QAction("Restore", self)
        quit_action = QAction("Quit", self)
        tray_menu.addAction(restore_action)
        tray_menu.addAction(quit_action)

        def restore_window():
            self.show()

        restore_action.triggered.connect(restore_window)
        quit_action.triggered.connect(QApplication.quit)

        tray_icon.setContextMenu(tray_menu)

        self.show()

        # Create a custom title bar widget
        title_bar = CustomTitleBar(self)
        layout = QVBoxLayout(self)
        layout.addWidget(title_bar)

        # All widgets
        battery_monitor = BatteryMonitor(threshold=90)

        battery_label = QLabel("Battery Level: -", self)
        battery_threshold = QLabel("Battery threshold: 90%")
        slider = QSlider(Qt.Orientation.Vertical)
        slider.setRange(0, 100)
        slider.setValue(90)

        update_button = QPushButton("Update Battery")
        loop_time_label = QLabel("Loop Time (seconds):")
        loop_time_entry = QLineEdit("60")
        loop_time_entry.setAlignment(Qt.AlignmentFlag.AlignCenter)

        current_css_file = "style.css"
        set_style_sheet(current_css_file)

        layout.addWidget(battery_label)
        layout.addWidget(slider, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(battery_threshold)
        layout.addWidget(update_button)
        layout.addWidget(loop_time_label)
        layout.addWidget(loop_time_entry)

        def update_battery_label():
            battery_percent = battery_monitor.update_battery_label()
            battery_label.setText(f"Battery Level : {battery_percent}%")
            loop_time = int(loop_time_entry.text())
            QTimer.singleShot(loop_time * 1000, update_battery_label)

        def on_slider_changed(value):
            threshold_value = slider.value()
            battery_monitor.set_threshold(threshold_value)
            battery_threshold.setText(
                f"Battery threshold : {threshold_value}%")

        def check_battery_level():
            battery_monitor.check_battery_level()
            loop_time = int(loop_time_entry.text())
            QTimer.singleShot(loop_time * 1000, check_battery_level)

        slider.valueChanged.connect(on_slider_changed)
        update_button.clicked.connect(check_battery_level)

        update_battery_label()
        check_battery_level()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(Qt.GlobalColor.white)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def shape(self):
        shape = QRegion(self.rect(), QRegion.RegionType.Ellipse)
        return shape
