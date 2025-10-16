# Librerías:
import RPi.GPIO as GPIO # GPIO
import serial # Comunicación Serial
from time import sleep # Retardo
import pygame # Bluetooth

# Variables:
BtnBuzzer = 5 # Botón Buzzer
BtnMtr1 = 6 # Botón Motor 1
BtnMtr2 = 13 # Botón Motor 2
MdfDtCy = 19 # Botón Modificar Duty Cycle

# Configuración:
GPIO.setmode(GPIO.BCM) # Pines (Modo de numeración BCM)
GPIO.setup(BtnBuzzer, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Buzzer
GPIO.setup(BtnMtr1, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Motor 1
GPIO.setup(BtnMtr2, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Motor 2
GPIO.setup(MdfDtCy, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Modificador Duty Cycle

# Configuración UART:
ser = serial.Serial('/dev/ttyACM0', 9600)
ser.reset_input_buffer()

# Configuración Bluetooth  :
pygame.init()
pygame.joystick.init()
#------------------------------
joystick = pygame.joystick.Joystick(0)
joystick.init()

print("Mando conectado:", joystick.get_name())
print("Número de ejes detectados:", joystick.get_numaxes())

while True:
    try:

        pygame.event.pump()
        eje_izq_y = joystick.get_axis(1)
        eje_der_x = joystick.get_axis(3)
        if eje_izq_y < -0.8 and eje_izq_y >= -1:
            ser.write(b"adelante\n")
            print(f"adelante")
            det1 = False
        elif eje_izq_y <= 1 and eje_izq_y > 0.8:
            ser.write(b"atras\n")
            print(f"atras")
            det1 = False
        else:
            ser.write(b"det1\n")
            det1 = True
        #------------------------------------------------
        if eje_der_x < -0.8 and eje_der_x >= -1:
            ser.write(b"izquierda\n")
            print(f"izquierda")
            det2 = False
        elif eje_der_x <= 1 and eje_der_x > 0.8:
            ser.write(b"derecha\n")
            print(f"derecha")
            det2 = False
        else:
            ser.write(b"det2\n")
            det2 = True
        #------------------------------------------------
        #------------------------------------------------
        if det1 and det2:
            ser.write(b"detenerse\n")
            print(f"detenerse")
        pygame.event.pump()

        # Recibir el Duty Cycle modificado desde Tiva:
        if ser.in_waiting > 0:
            value = ser.readline().decode('utf-8').rstrip()
            print("DutyCycle recibido ", value)
    except Exception as e:
        print(e)