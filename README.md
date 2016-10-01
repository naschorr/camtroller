# camtroller
OctoPrint plugin (with CLI) that lets you move and rotate your webcam

Note: This project is designed around the [28BYJ-48 stepper motor and ULN2003 driver board](https://smile.amazon.com/USPRO-Stepper-28BYJ-48-4-Phase-ULN2003/dp/B00JB22IQC). It should also work for other steppers and drivers, however you'll probably have to tweak some stuff. 

Another Note: Actual handy plugin installation and functionality is coming soon. For now, feel free to use these config settings to manipulate your webcam from the web interface's "System" dropdown.

Also check out my [other OctoPrint script](https://github.com/naschorr/octopi-webcam-toggle) for toggling your webcam from the web interface!

## Installation
- `git clone` this repo into your `~/scripts/` directory on your OctoPi
  - Alternatively, just drop `camtroller.py` into your `~/scripts/` directory.
- Insert the lines from `camtroller.yaml` into the `~/.octoprint/config.yaml` file under the `system:` `actions:` section. (See below image)
  - If you did just put `camtroller.py` into the scripts directory, then you'll have to remove the `/camtroller` subdirectory from the  the `command:` lines in `camtroller.yaml`.

![config.yaml example](https://raw.githubusercontent.com/naschorr/camtroller/master/resources/config_yaml_example.png)

## Usage
![rotate webcam example](https://raw.githubusercontent.com/naschorr/camtroller/master/resources/rotate_webcam_ui.png)

At the top of the page, just click on the 'System' dropdown. Then, hit any of the pitch or yaw buttons to rotate the webcam. Check out the 'Control' tab to see the changes. If you're not seeing anything, make sure that the mjpg_streamer is configured and running (configs located in `/boot/octopi.txt`, and `sudo service webcamd restart` respectively).
