import RPi.GPIO as GPIO
import time
from AlphaBot import AlphaBot

SERVO = 27
TRIG_DX = 17 #13
ECHO_DX = 5

TRIG_SX = 18
ECHO_SX = 24

Ab = AlphaBot()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SERVO, GPIO.OUT, initial=GPIO.LOW) 
GPIO.setup(TRIG_DX,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ECHO_DX,GPIO.IN)
GPIO.setup(TRIG_SX,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ECHO_SX,GPIO.IN)
p = GPIO.PWM(SERVO,50)
p.start(0)

def ServoAngle(angle):
	p.ChangeDutyCycle(2.5 + 10.0 * angle / 180)

def Distance_DX():
	GPIO.output(TRIG_DX,GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(TRIG_DX,GPIO.LOW)
	while not GPIO.input(ECHO_DX):
		pass
	t1 = time.time()
	while GPIO.input(ECHO_DX):
		pass
	t2 = time.time()
	return (t2-t1)*34000/2

def Distance_SX():
	GPIO.output(TRIG_SX,GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(TRIG_SX,GPIO.LOW)
	while not GPIO.input(ECHO_SX):
		pass
	t1 = time.time()
	while GPIO.input(ECHO_SX):
		pass
	t2 = time.time()
	return (t2-t1)*34000/2

ServoAngle(90)		
#print("Ultrasonic_Obstacle_Avoidance")
try:
	while True:
		middleDistance_DX = Distance_DX() / 10
		middleDistance_SX = Distance_SX() / 10

		print("MiddleDistance DESTRA = %0.2f cm"%middleDistance_DX)
		print("MiddleDistance SINISTRA = %0.2f cm"%middleDistance_SX)

		
		Ab.forward()
		
		if (middleDistance_DX <= 3 and middleDistance_SX <= 3):
			print("Ostacolo Davanti")
			Ab.backward()
			time.sleep(0.3)
			Ab.forward()
			if(middleDistance_DX > middleDistance_SX):
				print("Ostacolo Sinistra")
				Ab.backward()
				time.sleep(0.3)	
				Ab.right()
				time.sleep(0.3)
				Ab.forward()
			elif(middleDistance_DX < middleDistance_SX):
				print("Ostacolo Destra")
				Ab.backward()
				time.sleep(0.3)
				Ab.left()
				time.sleep(0.3)
				Ab.forward()
		elif(middleDistance_DX <= 3):
			print("Ostacolo Sinistra")
			Ab.backward()
			time.sleep(0.3)
			Ab.right()
			time.sleep(0.3)
			Ab.forward()
		elif(middleDistance_SX <= 3):
			print("Ostacolo Destra")
			Ab.backward()
			time.sleep(0.3)
			Ab.left()
			time.sleep(0.3)
			Ab.forward()
		else:
			print("No Ostacoli")
			Ab.forward()
			time.sleep(0.5)

		"""if middleDistance <= 20:
			Ab.stop()
#			time.sleep(0.5)
			ServoAngle(5)
			time.sleep(1)
			rightDistance = Distance()
			print("RightDistance = %0.2f cm"%rightDistance)
#			time.sleep(0.5)
			ServoAngle(180)
			time.sleep(1)
			leftDistance = Distance()
			print("LeftDistance = %0.2f cm"%leftDistance)
#			time.sleep(0.5)	
			ServoAngle(90)
			time.sleep(1)
			if rightDistance <20 and leftDistance < 20:
				Ab.backward()
				time.sleep(0.3)
				Ab.stop()
			elif rightDistance >= leftDistance:
				Ab.right()
				time.sleep(0.3)
				Ab.stop()
			else:
				Ab.left()
				time.sleep(0.3)
				Ab.stop()
			time.sleep(0.3)
		else:
			Ab.forward()
			time.sleep(0.02)"""

except KeyboardInterrupt:
	GPIO.cleanup();
