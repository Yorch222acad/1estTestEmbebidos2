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
    # Variables locales (usar dict para paso por referencia):
    state = {
        'mtr1Stt': False,
        'mtr2Stt': False,
        'adelante': False,
        'atras': False,
        'izquierda': False,
        'derecha': False,
        'det1': True,
        'det2': True,
    }
    duty = 30000

    try:
        while True:
            led0.value(0)
            
            #-----------------------
            state = UartHandler(state)
            #-----------------------
            distance = 20
            if 0 <= distance < 10:
                led4.value(1)
                if state['mtr1Stt']:
                    Pwm1.duty_u16(0)
                    dir1.value(1)
                    dir2.value(0)
                if state['mtr2Stt']:
                    Pwm2.duty_u16(0)
                    dir3.value(1)
                    dir4.value(0)
            else:
                led4.value(0)
                if state['mtr1Stt'] == True and state['mtr2Stt'] == False:
                    Pwm1.duty_u16(duty)
                    dir1.value(1)  # adelante
                    dir2.value(0)
                elif state['mtr2Stt'] == True and state['mtr1Stt'] == False:
                    Pwm2.duty_u16(duty)
                    dir3.value(1)
                    dir4.value(0)
                elif state['mtr1Stt'] and state['mtr2Stt']:
                    if state['det1'] == False:
                        if state['adelante']:
                            Pwm1.duty_u16(duty)
                            dir1.value(1)
                            dir2.value(0)
                            Pwm2.duty_u16(duty)
                            dir3.value(1)
                            dir4.value(0)
                        elif state['atras']:
                            Pwm1.duty_u16(duty)
                            dir1.value(0)
                            dir2.value(1)
                            Pwm2.duty_u16(duty)
                            dir3.value(0)
                            dir4.value(1)
                    if state['det2'] == False:
                        if state['izquierda']:
                            Pwm1.duty_u16(duty)
                            dir1.value(0)
                            dir2.value(1)
                            Pwm2.duty_u16(duty)
                            dir3.value(1)
                            dir4.value(0)
                        elif state['derecha']:
                            Pwm1.duty_u16(duty)
                            dir1.value(1)
                            dir2.value(0)
                            Pwm2.duty_u16(duty)
                            dir3.value(0)
                            dir4.value(1)
                    if state['det1'] == True and state['det2'] == True:
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
def UartHandler(state):
    if poll.poll(0):
        led0.value(1)
        linea = sys.stdin.readline().strip()

        # ---- Movimientos ----
        if linea == "Ad":
            led1.toggle()
            state['adelante'] = True
            state['det1'] = False
        elif linea == "At":
            led1.toggle()
            state['atras'] = True
            state['det1'] = False
        elif linea == "I":
            led1.toggle()
            state['izquierda'] = True
            state['det2'] = False
        elif linea == "D":
            led1.toggle()
            state['derecha'] = True
            state['det2'] = False
        elif linea == "D1":
            led1.toggle()
            state['adelante'] = False
            state['atras'] = False
            state['det1'] = True
        elif linea == "D2":
            led1.toggle()
            state['izquierda'] = False
            state['derecha'] = False
            state['det2'] = True

    return state

#-----------------------------------------------------------------------

#======================================================
if __name__ == "__main__":
    main()