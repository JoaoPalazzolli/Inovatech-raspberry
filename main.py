import RPi.GPIO as GPIO
import time
import requests
import json


# Define as portas GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define os pinos do sensor de gás e fumaça
GAS_SENSOR_PIN = 21

# Define os pinos dos LEDs
LED_RED = 17
LED_GREEN = 22

# Define o pino do buzzer
BUZZER_PIN = 18

# Inicializa os pinos GPIO
def init_gpio():
    GPIO.setup(GAS_SENSOR_PIN, GPIO.IN)
    GPIO.setup(LED_RED, GPIO.OUT)
    GPIO.setup(LED_GREEN, GPIO.OUT)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Função para piscar o LED
def blink_led(pin, times):
    for _ in range(times):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.5)
        
        
# Função para ativar o buzzer (bip)
def buzz(pitch, duration):
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(delay)
        
def buzz_and_blink(pitch, duration):
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
        GPIO.output(BUZZER_PIN, True)
        GPIO.output(LED_GREEN, True)
        time.sleep(0.5)
        GPIO.output(BUZZER_PIN, False)
        GPIO.output(LED_GREEN, True)
        time.sleep(0.5)
        
def buzz2_and_blink2(pitch, duration):
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
        GPIO.output(BUZZER_PIN, True)
        GPIO.output(LED_RED, True)
        time.sleep(0.5)
        GPIO.output(BUZZER_PIN, False)
        GPIO.output(LED_RED, False)
        time.sleep(0.5)

def transfer_json(temperature, humidity, smoke):
    dados = {
        "temperatura": temperature,
        "umidade": humidity,
        "fumaca": smoke
        }
    
    return json.dumps(dados, indent=4)

    # Função principal
def main():
    
    init_gpio()

    time.sleep(2)
    
    while True:
        # Verifica se há gás ou fumaça
        if GPIO.input(GAS_SENSOR_PIN) == GPIO.HIGH:
                requests.post('https://inovatech-monitoramento-ar-backend.onrender.com/api/v1/monitoramento', transfer_json(10, 60, True))
                print('Detectou')
                GPIO.output(LED_GREEN, GPIO.LOW)
                buzz2_and_blink2(2, 5)
                time.sleep(0.5)
        else:
                GPIO.input(GAS_SENSOR_PIN) == GPIO.LOW
                requests.post('https://inovatech-monitoramento-ar-backend.onrender.com/api/v1/monitoramento', transfer_json(20, 65, False))
                print('Não detectou')
                buzz_and_blink(1, 1)
                
        time.sleep(1)
 

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
