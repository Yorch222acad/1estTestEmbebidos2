import cv2
import serial
from time import sleep

# Configuración de UART para enviar comandos
ser = serial.Serial('/dev/ttyACM0', 9600)
ser.reset_input_buffer()

droidcam_url = "http://10.204.219.56:4747/video"
cap = cv2.VideoCapture(droidcam_url)

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

while True:
    try:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo obtener el fotograma.")
            break

        # Convertir la imagen a formato HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Rango ajustado para detectar el color rojo en el espacio HSV
        lower_red1 = (0, 120, 100)   # Rango 1 del rojo
        upper_red1 = (10, 255, 255)
        lower_red2 = (170, 120, 100) # Rango 2 del rojo (rojos más cercanos a los valores extremos)
        upper_red2 = (180, 255, 255)

        # Rango ajustado para detectar color verde
        lower_green = (90, 100, 100)
        upper_green = (150, 255, 255)

        # Crear las máscaras para los colores rojo y verde
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)

        # Unir las dos máscaras de rojo
        mask = cv2.bitwise_or(mask_red1, mask_red2, mask_green)

        # Contar los píxeles rojos y verdes
        red_pixels = cv2.countNonZero(mask)
        green_pixels = cv2.countNonZero(mask)

        # Si se detecta suficiente color rojo
        if red_pixels > 500:
            ser.write(b"DutyCycle 50\n")  # Media velocidad
            sleep(0.05)
            ser.write(b"avanzar\n")
            print("enviado: avanzar")

        # Si se detecta suficiente color verde
        elif green_pixels > 500:
            ser.write(b"DutyCycle 50\n")  # Media velocidad
            sleep(0.05)
            ser.write(b"retroceder\n")
            print("enviado: retroceder")

        # Mostrar la imagen original y los resultados filtrados para rojo y verde
        cv2.imshow('Original', frame)

        # Salir si se presiona 'q'
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    except Exception as e:
        print(e)
        break

# Cerrar la ventana de OpenCV al terminar
cap.release()
cv2.destroyAllWindows()