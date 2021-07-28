from machine import Pin
import utime as t

class LedRGB:
    
    def __init__(self,verde,azul,rojo):
        self.Azul = Pin(2, Pin.OUT)
        self.Rojo = Pin(4, Pin.OUT)
        self.Verde = Pin(15, Pin.OUT)
            
    def rojo(self):
        self.Rojo.on()
    
    def azul(self):
        self.Azul.on()
    
    def violeta(self):
        self.Rojo.on()
        self.Azul.on()
    
    def verde(self):
        self.Verde.on()
    
    def apagado(self):
        self.Rojo.off()
        self.Azul.off()
        self.Verde.off()

       