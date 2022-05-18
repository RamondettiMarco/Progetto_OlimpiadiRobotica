#!/usr/bin/python
# _*_ coding: utf-8 -*-
#server tpc

#copia del server sull'alphabot

import socket as sck
import threading as thr
import time
import RPi.GPIO as GPIO
import sqlite3 #libreria data base
import subprocess

TEMPO_PER_CURVARE_DI_90_GRADI = 0.5

TRIG_DX = 17 #13
ECHO_DX = 5

TRIG_SX = 18
ECHO_SX = 24
SERVO = 27

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
#GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(SERVO, GPIO.OUT, initial=GPIO.LOW) 
GPIO.setup(TRIG_DX,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ECHO_DX,GPIO.IN)
GPIO.setup(TRIG_SX,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ECHO_SX,GPIO.IN)
p = GPIO.PWM(SERVO,50)
p.start(0)

lista_client = []
clients = []

#classe thread

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

def obstacle(Ab):
    middleDistance_DX = Distance_DX() / 10
    middleDistance_SX = Distance_SX() / 10

    print("MiddleDistance DESTRA = %0.2f cm"%middleDistance_DX)
    print("MiddleDistance SINISTRA = %0.2f cm"%middleDistance_SX)
    
    if (middleDistance_DX <= 3 and middleDistance_SX <= 3):
        print("Ostacolo Davanti")
        Ab.backward()
        time.sleep(0.3)
        if(middleDistance_DX > middleDistance_SX):
            print("Ostacolo Sinistra")
            Ab.backward()
            time.sleep(0.3)	
            Ab.right()
            time.sleep(0.3)
        elif(middleDistance_DX < middleDistance_SX):
            print("Ostacolo Destra")
            Ab.backward()
            time.sleep(0.3)
            Ab.left()
            time.sleep(0.3)
    elif(middleDistance_DX <= 3):
        print("Ostacolo Sinistra")
        Ab.backward()
        time.sleep(0.3)
        Ab.right()
        time.sleep(0.3)
    elif(middleDistance_SX <= 3):
        print("Ostacolo Destra")
        Ab.backward()
        time.sleep(0.3)
        Ab.left()
        time.sleep(0.3)
    else:
        print("No Ostacoli")
        time.sleep(0.5)

#funzione che si avvia alla creazione della classe
def __init__(self, connessione, indirizzo ,alphabot):
    thr.Thread.__init__(self)   #costruttore super (java)
    self.connessione = connessione
    self.indirizzo=indirizzo
    self.alphabot=alphabot          #per usare la classe del robot all'interno del thread
    self.running = True


class AlphaBot(object):  #classe dell'Alfabot
    
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA  = 20  #velocità in girare
        self.PB  = 20   #velocità per girare

        #motori
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

    def backward(self, speed = 50):  #avanti a velocità 60
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)


        
    def stop(self):     #fermare i motori
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def forward(self , speed = 50):   #indietro velocità 60
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        
        

    def left(self, speed = 30):     #girare a sinistra velocità settata in precedenza
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
    
    
    def right(self, speed = 30):    #destra con la velocità settata in precedenza
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        
    def set_pwm_a(self, value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def set_pwm_b(self, value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)    
        
    def set_motor(self, left, right):
        if (right >= 0) and (right <= 100):
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif (right < 0) and (right >= -100):
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if (left >= 0) and (left <= 100):
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif (left < 0) and (left >= -100):
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)

class BatteryCheck(thr.Thread):
    def __init__(self):
        thr.Thread.__init__(self)
        self.running = True
    #OVERRIDE
    def run(self):
        while self.running:
            # @@@@@@@@@ COMANDO SHELL @@@@@@@@@@ #
            output = subprocess.run(["vcgencmd", "get_throttled"], capture_output=True)
            # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

            dato = output.stdout.decode()
            dato = int(dato.split("=")[1].replace("\n", ""),16)

            if dato != 0:
                if len(clients) > 0:
                    # invio a tutti i client il messaggio di sostituire le batterie
                    for client in clients:
                        client.connection.sendall(f"Sostituire le BATTERIE! (dato:{dato})".encode())
                    time.sleep(10)

def main():
    # start thread per gestione batterie
    battery_check = BatteryCheck()
    battery_check.start()


    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM) 
    s.bind(('0.0.0.0', 3450))       #bind del server tcp
    s.listen()
    Ab = AlphaBot()      #inizzializzo alphabot

    running = True
   
    connessione, indirizzo = s.accept()   #connessioni dei client
    

    #client = Classe_Thread(connessione, indirizzo, Ab)
    #mettere codice run
    while running:     #ciclo infinito del programma
        messaggio = (connessione.recv(4096)).decode()          #ricevo il comando

        if messaggio == 'exit':             #per chiudere il programma e scollegare i client
            running = False

            lista_client.remove()
            
        else:
            print(messaggio)
            
            #prova sensori
            """ServoAngle(90)		
            #print("Ultrasonic_Obstacle_Avoidance")
            
            middleDistance = Distance()
            print("MiddleDistance = %0.2f cm"%middleDistance)
      
            if middleDistance <= 20:
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
            
            if messaggio.upper().startswith("W"): #avanti 
                #for i in range(5):
                obstacle(Ab)
                Ab.forward()
                obstacle(Ab)
                time.sleep(0.1)        #durata del movimento
                Ab.stop()
            if messaggio.upper().startswith("D"): #destra
                Ab.right()
                time.sleep(0.1)   
                Ab.stop()
                obstacle(Ab)
            if messaggio.upper().startswith("S"): #indietro
                obstacle(Ab)
                Ab.backward()
                time.sleep(0.1)   
                Ab.stop()
            if messaggio.upper().startswith("A"): #sinistra
                Ab.left()
                time.sleep(0.1)   
                Ab.stop()
                obstacle(Ab)
            if messaggio.upper().startswith("ESCI"): #fermo
                Ab.stop()
                obstacle(Ab)

    # chiusura thread battery_check
    battery_check.running = False
    time.sleep(0.5)
    battery_check.join()

    s.close()
   
main()
