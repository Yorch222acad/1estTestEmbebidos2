# Importaciones:
#-----------------------------{ Mínimas
from machine import Pin, PWM
#}----------------------------{ Uart
import sys  # Uart vía USB
import select  # UART no bloqueante
#}----------------------------{ Otros
import utime
#}--

#======================================================
# Variables globales:
tIter = 0
frecuencia = 1000

# Configuraciones de pines:
#-------------------------{ Leds
led0 = Pin("LED", Pin.OUT)  # Led integrado
led1 = Pin(10, Pin.OUT)  # Actividad UART
led2 = Pin(11, Pin.OUT)
led3 = Pin(12, Pin.OUT)
led4 = Pin(13, Pin.OUT)
#}------------------------{ Buzzer
Buzzer = Pin(16, Pin.OUT)
#}------------------------{ PWM
Pwm1 = PWM(Pin(14))
dir1 = Pin(3, Pin.OUT)
dir2 = Pin(2, Pin.OUT)
Pwm2 = PWM(Pin(15))
dir3 = Pin(4, Pin.OUT)
dir4 = Pin(5, Pin.OUT)

Pwm1.freq(frecuencia)
Pwm2.freq(frecuencia)
#}------------------------{ Ultrasonico
trig = Pin(18, Pin.OUT)
echo = Pin(19, Pin.IN)
#}--

# Configuración UART no bloqueante
poll = select.poll()
poll.register(sys.stdin, select.POLLIN)

#======================================================
def main():
    # Variables locales:
    #----------------------{ Buzzer
    BuzzerState = False
    #}---------------------{ Motores
    mtr1Stt = True
    mtr2Stt = True
    duty = 30000
    adelante = False
    atras = False
    izquierda = False
    derecha = False
    det1 = True
    det2 = True
    #}---------------------{ Ultrasonico
    try:
        while True:
            led0.value(0)
            
            #-----------------------
            adelante, atras, izquierda, derecha, det1, det2 = UartHandler(
                adelante, atras, izquierda, derecha, det1, det2
            )
            #-----------------------
            distance = 20
            if 0 <= distance < 10:
                led4.value(1)
                if mtr1Stt:
                    Pwm1.duty_u16(0)
                    dir1.value(1)
                    dir2.value(0)
                if mtr2Stt:
                    Pwm2.duty_u16(0)
                    dir3.value(1)
                    dir4.value(0)
            else:
                led4.value(0)
                if mtr1Stt == True and mtr2Stt == False:
                    Pwm1.duty_u16(duty)
                    dir1.value(1)  # adelante
                    dir2.value(0)
                elif mtr2Stt == True and mtr1Stt == False:
                    Pwm2.duty_u16(duty)
                    dir3.value(1)
                    dir4.value(0)
                elif mtr1Stt and mtr2Stt:
                    if det1 == False:
                        if adelante:
                            Pwm1.duty_u16(duty)
                            dir1.value(1)
                            dir2.value(0)
                            Pwm2.duty_u16(duty)
                            dir3.value(1)
                            dir4.value(0)
                        elif atras:
                            Pwm1.duty_u16(duty)
                            dir1.value(0)
                            dir2.value(1)
                            Pwm2.duty_u16(duty)
                            dir3.value(0)
                            dir4.value(1)
                    if det2 == False:
                        if izquierda:
                            Pwm1.duty_u16(duty)
                            dir1.value(0)
                            dir2.value(1)
                            Pwm2.duty_u16(duty)
                            dir3.value(1)
                            dir4.value(0)
                        elif derecha:
                            Pwm1.duty_u16(duty)
                            dir1.value(1)
                            dir2.value(0)
                            Pwm2.duty_u16(duty)
                            dir3.value(0)
                            dir4.value(1)
                    if det1 == True and det2 == True:
                        Pwm1.duty_u16(0)
                        dir1.value(0)
                        dir2.value(0)
                        Pwm2.duty_u16(0)
                        dir3.value(0)
                        dir4.value(0)
                else:
                    print("Motores desactivados")

    except Exception as e:
        led0.toggle()
        utime.sleep_ms(200)
        led0.toggle()
        utime.sleep_ms(200)

#======================================================
def interactiveDelay(time_sec):
    global tIter
    if tIter == 0:
        tIter = utime.ticks_add(utime.ticks_ms(), int(time_sec * 1000))
    if utime.ticks_diff(tIter, utime.ticks_ms()) <= 0:
        tIter = 0
        return True
    return False

#-----------------------------------------------------------------------
def UartHandler(adelante, atras, izquierda, derecha, det1, det2):
    if poll.poll(0):
        led0.value(1)
        linea = sys.stdin.readline().strip()

        # ---- Movimientos ----
        if linea == "adelante":
            led1.toggle()
            adelante = True
            det1 = False
        elif linea == "atras":
            led1.toggle()
            atras = True
            det1 = False
        elif linea == "izquierda":
            led1.toggle()
            izquierda = True
            det2 = False
        elif linea == "derecha":
            led1.toggle()
            derecha = True
            det2 = False
        elif linea == "det1":
            led1.toggle()
            adelante = False
            atras = False
            det1 = True
        elif linea == "det2":
            led1.toggle()
            izquierda = False
            derecha = False
            det2 = True

    return adelante, atras, izquierda, derecha, det1, det2

#-----------------------------------------------------------------------

#======================================================
if __name__ == "__main__":
    main()