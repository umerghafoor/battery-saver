# Battery Saver App
The Battery Saver App is a PyQt6-based application that helps prevent overcharging of the device's battery. It continuously monitors the battery level and sends a notification when the battery reaches a specified threshold, reminding the user to unplug the charger and prevent overcharging.

## Features
- Battery level monitoring: The app continuously monitors the battery level of the device.
- Overcharging prevention: Users can set a battery level threshold for notifications to prevent overcharging.
- System tray integration: The app runs in the system tray, allowing users to access the main window easily.
- Notification: When the battery level exceeds the set threshold, the app sends a notification to the user, reminding them to unplug the charger.
## Installation
Clone the repository or download the source code files.
Install the required dependencies using pip:
```
pip install pyqt6
pip install psutil
pip install plyer
```
## Usage
To run the Battery Saver App, execute the following command in the project directory:

shell
Copy code
```
python pyqt.pyw
```
The app will start running and appear in the system tray. To access the main window, click on the app icon in the system tray.

In the main window, you will find the following elements:

- Battery Level: Displays the current battery level.
- Battery threshold: Displays the set battery threshold.
- Slider: Allows you to set the battery threshold by adjusting the slider.
- Update Battery button: Manually checks the battery level.
- Loop Time (seconds): Specifies the time interval for automatic battery level checks.

Adjust the slider to set the desired battery threshold to prevent overcharging. When the battery level exceeds the set threshold, the app will send a notification, reminding you to unplug the charger.

You can also update the battery level manually by clicking the Update Battery button. The app will continuously monitor the battery level based on the loop time specified.

To quit the application, right-click on the app icon in the system tray and select Quit.


## License
ProductivityPause is open source project licensed under the [MIT License](LICENSE).

## Contact
For any questions, feedback, or inquiries, please reach out to umerghaforr@gmail.com.