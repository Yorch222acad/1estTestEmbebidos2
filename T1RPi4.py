# Librerías:
import RPi.GPIO as GPIO # GPIO
import serial # Comunicación Serial
from time import sleep # Retardo
import cv2

# Variables:
BtnBuzzer = 5 # Botón Buzzer
BtnMtr1 = 6 # Botón Motor 1
BtnMtr2 = 13 # Botón Motor 2
MdfDtCy = 19 # Botón Modificar Duty Cycle


droidcam_url = "http://172.20.10.3:4747/video"
cap = cv2.VideoCapture(droidcam_url)

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()


# Configuración:
GPIO.setmode(GPIO.BCM) # Pines (Modo de numeración BCM)
GPIO.setup(BtnBuzzer, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Buzzer
GPIO.setup(BtnMtr1, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Motor 1
GPIO.setup(BtnMtr2, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Motor 2
GPIO.setup(MdfDtCy, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Modificador Duty Cycle

# Configuración UART:
ser = serial.Serial('/dev/ttyACM0', 9600)
ser.reset_input_buffer()

# Función para ingresar el Duty Cycle por terminal:
def ingDtCy():
    DtCy = int(input("Ingrese el valor del Duty Cycle entre 0 - 100: "))
    while DtCy < 0 or DtCy > 100:
        print("Valor incorrecto")
        DtCy = int(input("Ingrese el valor del Duty Cycle entre 0 - 100: "))
    return DtCy




while True:
    try:
        # Envíar comandos por UART al presionar los botones:
        #------------------------------------------------{ Buzzer:
        if GPIO.input(BtnBuzzer) == GPIO.LOW:
            ser.write(b"buzzer\n")
            print("enviado: buzzer")
            sleep(0.2)
        #}-----------------------------------------------{ Motor 1:
        if GPIO.input(BtnMtr1) == GPIO.LOW:
            ser.write(b"motor1\n")
            print("enviado: motor1")
            sleep(0.2)
        #}-----------------------------------------------{ Motor 2:
        if GPIO.input(BtnMtr2) == GPIO.LOW:
            ser.write(b"motor2\n")
            print("enviado: motor2")
            sleep(0.2)
        #}-----------------------------------------------{ Modificar Duty Cycle:
        if GPIO.input(MdfDtCy) == GPIO.LOW:
            DtCy = ingDtCy()
            mensaje = "DutyCycle " + str(DtCy) + "\n"
            ser.write(mensaje.encode())
            print("enviado:", mensaje.strip())
            sleep(0.2)
        #}--
        # Recibir el Duty Cycle modificado desde Tiva:
        if ser.in_waiting > 0:
            value = ser.readline().decode('utf-8').rstrip()
            print("DutyCycle recibido ", value)

            ret, frame = cap.read()

        if not ret:
            print("Error: No se pudo obtener el fotograma.")
            break
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        lower_red = (0, 100, 100)
        upper_red = (10, 255, 255)
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        
        lower_green = (50, 100, 100)
        upper_green = (70, 255, 255)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        
        if cv2.countNonZero(mask_red) > 500:
            ser.write(b"motor2\n")
            print("enviado: Adelante")
            sleep(0.2)
        if cv2.countNonZero(mask_green) > 500:
            ser.write(b"motor2\n")
            print("enviado: Atras")
            sleep(0.2)
        
        cv2.imshow('Droicam', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break


    except Exception as e:
        print(e)

    


    
