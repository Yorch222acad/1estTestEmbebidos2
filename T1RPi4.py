# Librerías:
import RPi.GPIO as GPIO # GPIO
import serial # Comunicación Serial
from time import sleep, time  # Retardo
import select  # Para lectura no bloqueante
import sys   # <-'

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
try:
    ser = serial.Serial('/dev/ttyACM0', 9600)
    ser.reset_input_buffer()
except Exception as e:
    print(f"Error al abrir puerto serial: {e}")
    exit()

# Variables para debounce manual:
last_press = {BtnBuzzer:0, BtnMtr1:0, BtnMtr2:0, MdfDtCy:0}
debounce_time = 0.2  # segundos

# Función para ingresar el Duty Cycle por terminal:
def ingDtCy():
    DtCy = int(input("Ingrese el valor del Duty Cycle entre 0 - 100: "))
    while DtCy < 0 or DtCy > 100:
        print("Valor incorrecto")
        DtCy = int(input("Ingrese el valor del Duty Cycle entre 0 - 100: "))
    return DtCy

def ingDeegre():
    while True:
        try:
            Degree = int(input("Ingrese el valor del grado entre 0 - 360: "))
            if 0 <= Degree <= 360:
                return Degree
            print("Valor incorrecto")
        except ValueError:
            print("Por favor ingrese un número válido")

def mostrar_menu():
    print("\n--- Menú de Control ---")
    print("1. Activar Buzzer")
    print("2. Activar Motor 1")
    print("3. Activar Motor 2")
    print("4. Modificar Duty Cycle")
    print("5. Modificar Grados")

mostrar_menu()
print("Seleccione una opción (1-5): ")
try:
    while True:
        now = time()

        # Detectar si hay entrada de usuario disponible en stdin (sin bloquear)
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            opcion = sys.stdin.readline().strip()  # leer línea sin detener el programa
            if opcion not in ['1', '2', '3', '4', '5']:
                print("Opción inválida. Por favor seleccione entre 1-5")
                continue
            mostrar_menu()
            print("\nSeleccione una opción (1-5): ")
        else:
            opcion = None  # nada ingresado

        #---------------------------------------------------------------------------------

        if opcion != None:
            #------------------------------------------------{ Buzzer:
            if GPIO.input(BtnBuzzer) == GPIO.LOW or opcion == '1' and now - last_press[BtnBuzzer] > debounce_time:
                ser.write(b"buzzer\n")
                print("enviado: buzzer")
                last_press[BtnBuzzer] = now
            #}-----------------------------------------------{ Motor 1:
            elif GPIO.input(BtnMtr1) == GPIO.LOW or opcion == '2' and now - last_press[BtnMtr1] > debounce_time:
                ser.write(b"motor1\n")
                print("enviado: motor1")
                last_press[BtnMtr1] = now
            #}-----------------------------------------------{ Motor 2:
            elif GPIO.input(BtnMtr2) == GPIO.LOW or opcion == '3' and now - last_press[BtnMtr2] > debounce_time:
                ser.write(b"motor2\n")
                print("enviado: motor2")
                last_press[BtnMtr2] = now
            #}-----------------------------------------------{ Modificar Duty Cycle:
            elif GPIO.input(MdfDtCy) == GPIO.LOW or opcion == '4' and now - last_press[MdfDtCy] > debounce_time:
                DtCy = ingDtCy()
                mensaje = "DutyCycle " + str(DtCy) + "\n"
                ser.write(mensaje.encode())
                print("enviado:", mensaje.strip())
                last_press[MdfDtCy] = now
            #}-----------------------------------------------{ Modificar Grados:
            elif opcion == '5':
                Degree = ingDeegre()
                mensaje = f"Degree {Degree}\n"
                ser.write(mensaje.encode())
                print("enviado:", mensaje.strip())          
            #}--
            opcion = None  # reset opción después de procesar

        # Recibir el Duty Cycle modificado desde Tiva:
        if ser.in_waiting > 0:
            value = ser.readline().decode('utf-8').rstrip()
            print("DutyCycle recibido ", value)
except Exception as e:
        print(e)