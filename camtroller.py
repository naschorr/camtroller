from __future__ import print_function
import RPi.GPIO as GPIO
import time
import threading
import click

## String literals
BOARD = "board"
BCM = "bcm"
YAW = "yaw"
PITCH = "pitch"

## Defaults
WAIT_TIME = 0.00244
DIR = 1	# 1 for CW, -1 for CCW
PIN_MODE = BOARD
PITCH_PINS = (40, 38, 36, 32)
YAW_PINS = (37, 35, 33, 31)

class StepperController:
	STEPS_PER_REV = 4076		# 28byj-48 Stepper
	STEP_PHASES =  [[1,0,0,1],      # Half stepping on ULN2003
	                [1,0,0,0],
			[1,1,0,0],
			[0,1,0,0],
	                [0,1,1,0],
                	[0,0,1,0],
        	        [0,0,1,1],
	                [0,0,0,1]]

	def __init__(self, pins):
		self.thisPhase = 0
		self.pins = pins

	@property
	def thisPhase(self):
		return self._thisPhase

	@thisPhase.setter
	def thisPhase(self, value):
		self._thisPhase = value

	@property
	def pins(self):
		return self._pins

	@pins.setter
	def pins(self, value):
		self._pins = value

	def doStep(self, direction=DIR):
		currentSteps = self.STEP_PHASES[self.thisPhase]
       		for pin in range(len(self.pins)):
	       	        GPIO.output(self.pins[pin], currentSteps[pin])

		self.thisPhase = (self.thisPhase + direction) % len(self.STEP_PHASES)

	def stepDegrees(self, degrees, waitTime=WAIT_TIME):
		steps = int((self.STEPS_PER_REV/360.0) * abs(degrees))
	        direction = 1 if degrees > 0 else -1
		for stepIndex in range(steps):
	                self.doStep(direction)
	                time.sleep(waitTime)

	def threadedStepDegrees(self, degrees, waitTime=WAIT_TIME):
		thread = threading.Thread(target=self.stepDegrees, args=(degrees, waitTime))
		thread.start()
		return thread


def init(pin_mode, yaw_pins, pitch_pins):
	if(pin_mode == BCM):
		GPIO.setmode(GPIO.BCM)		
	else:	# Otherwise it's in board mode.
		GPIO.setmode(GPIO.BOARD)

	try:
		GPIO.setup(pitch_pins, GPIO.OUT)
	except ValueError as ve:
		print(ve, "The supplied pitch stepper pins {0} are invalid. Consult the pinout, and make sure your pin-mode is correct. Error text: {1}\nDefaulting to pins {2}.".format(pitch_pins, ve, PITCH_PINS))
		pitch_pins = PITCH_PINS
		GPIO.setup(PITCH_PINS, GPIO.OUT)

	try:
                GPIO.setup(yaw_pins, GPIO.OUT)
        except ValueError as ve:
                print("The supplied yaw stepper pins {0} are invalid. Consult the pinout, and make sure your pin-mode is correct. Error text: {1}.\nDefaulting to pins {2}.".format(yaw_pins, ve, YAW_PINS))
		yaw_pins = YAW_PINS
                GPIO.setup(YAW_PINS, GPIO.OUT)

	## Return successfully initialized StepperController objects (with consistent pins!)
	return StepperController(yaw_pins), StepperController(pitch_pins)


@click.command()
@click.option('--yaw', '-y', type=float, help='Number of degrees to yaw the camera')
@click.option('--pitch', '-p', type=float, help='Number of degrees to pitch the camera')
@click.option('--pin-mode', default=PIN_MODE, type=click.Choice([BOARD, BCM]), help='Selects the pin selection mode. Defaults to {0}'.format(PIN_MODE))
@click.option('--yaw-pins', default=YAW_PINS, type=(int, int, int, int), help='Pins to control the yaw stepper.')
@click.option('--pitch-pins', default=PITCH_PINS, type=(int, int, int, int), help='Pins to control the pitch stepper.')
def main(yaw, pitch, pin_mode, yaw_pins, pitch_pins):
	yawStepper, pitchStepper = init(pin_mode, yaw_pins, pitch_pins)

	try:
		if(yaw and pitch):
			yawStepper.stepDegrees(yaw)
			pitchStepper.threadedStepDegrees(pitch).join()
		elif(yaw):
			yawStepper.stepDegrees(yaw)
		elif(pitch):
			pitchStepper.stepDegrees(pitch)
	except KeyboardInterrupt as ki:
		print("Interrupt detected. Going to clean up the GPIO and exit. Error text: {0}.".format(ki))
	finally:
		GPIO.cleanup()


if(__name__ == "__main__"):
	main()
