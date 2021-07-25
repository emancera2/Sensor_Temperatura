#Librerias
import time
from machine import Pin, SoftI2C
import network
import socket
import utime
import ssd1306
import claseRGB
import _thread
import dht
from time import sleep
import framebuf
import urequests
#------------------------------------------------
#Configuración inicial de WiFi
ssid = 'Harry Mancera'  #Nombre de la Red
password = '80352754*' #Contraseña de la red
wlan = network.WLAN(network.STA_IF)
#------------------------------------------------
wlan.active(True) #Activa el Wifi
wlan.connect(ssid, password) #Hace la conexión
#------------------------------------------------
#Configuración Pantalla OLED
# ESP32 Pin assignment
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
#------------------------------------------------
#Configuración sensor de temperatura.
sensort = dht.DHT11(Pin(13))
sleep(2)
sensort.measure()
#------------------------------------------------
#Configuración del LED RGB
rgb = claseRGB.LedRGB(2,4,15)
#------------------------------------------------
def ConexionRED():
    #Ciclo que valide en 5 segundos que se establezca la conexión
    for i in range(5):
        print(".")
        utime.sleep(1)
#------------------------------------------------
#Condición encargada de notificar si la conexión es Exitosa o no
    if wlan.isconnected() == True:#Conexión Exitosa
        rgb.verde() #En caso de ser exitosa enciende el led RGB verde
        utime.sleep(1)
        rgb.apagado()
        print(wlan.ifconfig()) #Muestra la IP y otros datos del Wi-Fi
        oled.text('Conexion OK', 10, 32) #Muestra mensaje en pantalla oled
        oled.show()
#------------------------------------------------
    else: #Conexión no Exitosa
        rgb.rojo() #En caso de no ser exitosa enciende el led RGB Rojo
        utime.sleep(1)
        rgb.apagado()
        print(wlan.ifconfig())
        oled.text('Conexion No/OK', 10, 32)#Muestra mensaje en pantalla oled
        oled.show()
_thread.start_new_thread(ConexionRED,())
#------------------------------------------------
while True:
    oled.fill(0)
    sleep(2)
    sensort.measure()
    t = sensort.temperature()
    h = sensort.humidity()
    oled.text('temp : '+str(t) + " C", 0,0,1)
    oled.text('humd : '+str(h) + " %", 0,10,1)
    oled.show()   
    utime.sleep(2)
    #url="https://api.thingspeak.com/update?api_key=YWA90E43Q1X709Q8&field1="
    url="https://api.thingspeak.com/update?api_key=UF6WR2PQ8W3EFKS5&field1="
    url += str(h)
    r = urequests.get(url)
    print(r.json())
#------------------------------------------------