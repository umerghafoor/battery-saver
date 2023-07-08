# battery_monitor.py

import psutil
from plyer import notification


class BatteryMonitor:
    def __init__(self, threshold):
        self.threshold = threshold

    def check_battery_level(self):
        battery = psutil.sensors_battery()
        battery_percent = battery.percent if battery else "Unknown"
        print(f"Battery level: {battery_percent}%")

        # Check if battery level is greater than threshold
        if battery_percent != "Unknown" and battery_percent > self.threshold:
            notification.notify(
                title="Battery Alert",
                message=f"Battery level is more than {self.threshold}% ({battery_percent}%)",
                timeout=10
            )

    def update_battery_label(self):
        battery = psutil.sensors_battery()
        battery_percent = battery.percent if battery else "Unknown"
        return battery_percent

    def set_threshold(self, threshold):
        self.threshold = threshold
