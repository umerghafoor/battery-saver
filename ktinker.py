import tkinter as tk
from threading import Thread
from battery_monitor import BatteryMonitor

class BatteryApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Battery Monitor")

        self.battery_monitor = BatteryMonitor(threshold=90)

        self.battery_label = tk.Label(self.root, text="Battery Level: -")
        self.slider = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, length=200)
        self.slider.set(90)  # Set initial threshold value to 90

        self.update_button = tk.Button(self.root, text="Update Battery", command=self.check_battery_level)
        self.loop_time_label = tk.Label(self.root, text="Loop Time (seconds):")
        self.loop_time_entry = tk.Entry(self.root)
        self.loop_time_entry.insert(tk.END, "60")

        self.apply_styles()

        self.battery_label.pack(padx=10, pady=10)
        self.slider.pack(padx=10, pady=5)
        self.update_button.pack(padx=10, pady=5)
        self.loop_time_label.pack(padx=10, pady=5)
        self.loop_time_entry.pack(padx=10, pady=5)

        self.slider.bind("<ButtonRelease-1>", self.on_slider_changed)

        self.update_battery_label()
        self.check_battery_level()

        self.root.mainloop()

    def apply_styles(self):
        style = {}

        # self.battery_label.configure(**style["battery_label"])
        # self.slider.configure(**style["slider"])
        # self.update_button.configure(**style["update_button"])
        # self.loop_time_label.configure(**style["loop_time_label"])
        # self.loop_time_entry.configure(**style["loop_time_entry"])

    def update_battery_label(self):
        battery_percent = self.battery_monitor.update_battery_label()
        self.battery_label.config(text=f"Battery Level: {battery_percent}%")
        loop_time = int(self.loop_time_entry.get())
        self.root.after(loop_time * 1000, self.update_battery_label)

    def on_slider_changed(self, event):
        threshold_value = self.slider.get()
        self.battery_monitor.set_threshold(threshold_value)

    def check_battery_level(self):
        self.battery_monitor.check_battery_level()
        loop_time = int(self.loop_time_entry.get())
        self.root.after(loop_time * 1000, self.check_battery_level)

if __name__ == "__main__":
    BatteryApp()
