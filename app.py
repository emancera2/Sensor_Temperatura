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
#Servicio Web encargado de pintar la los graficos del sensor
def web_page():  
    html = """
<html>
<head>
<title>Medidor de humedad y temperatura</title>
</head>            
<body>
<center>
<iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1447645/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=15&type=spline"></iframe>
<br>
<br>
<iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1454840/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=10&type=spline"></iframe>
</center>
</body>            
</html>  """
    return html
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind(('', 80))
tcp_socket.listen(3)

#------------------------------------------------
#Muestra la pagina y actualiza constantemente
def MostrarPG():
    while True:
        conn, addr = tcp_socket.accept()
        print('Nueva conexion desde:  %s' % str(addr))
        request = conn.recv(1024)
        print('Solicitud = %s' % str(request))    
        #Mostrar Página
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
_thread.start_new_thread(MostrarPG,())        
#------------------------------------------------
#Escritura sobre las API ThingSpeak
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
    url1="https://api.thingspeak.com/update?api_key=UF6WR2PQ8W3EFKS5&field1="
    url1 += str(t)
    r1 = urequests.get(url1)
    print(r1.json())
    url2="https://api.thingspeak.com/update?api_key=6ZLA92ULEGMRBEWU&field1="
    url2 += str(h)
    r2 = urequests.get(url2)
    print(r2.json())
#------------------------------------------------  