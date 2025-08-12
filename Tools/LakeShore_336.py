import serial
import time

try:
    from Tools.Instrument import SerialInstrument
except:
    from Instrument import SerialInstrument



class temperatureController(SerialInstrument):
    def __init__(self, name, port:str):
        super().__init__(name, 'lakeshore_336', port, baudrate = 57600, 
                                bytesize = serial.SEVENBITS, 
                                parity=serial.PARITY_ODD, 
                                stopbits = serial.STOPBITS_ONE)

    def clear(self):
        self.write("*CLS")
        
    def identification(self):
        return self.query("*IDN?")
    
    def temp_read(self, channel:str): # channel 'A' - 'D'
        command = "KRDG? " + channel
        temp = self.query(command)
        print(temp)
        temp = temp.replace("+","")
        temp = temp.replace("\r","")
        temp = temp.replace("\n","")
        
        temp = float(temp)
        return temp
    
    def temp_read_all(self):
        command = "KRDG? A;KRDG? B;KRDG? C;KRDG? D"
        temp = self.query(command)
        temp = temp.replace("+","")
        temp = temp.replace("\r","")
        temp = temp.replace("\n","")
        temp = temp.split(";")
        i = 0
        while i < len(temp):
            temp[i] = float(temp[i])
            i += 1
        print(temp)
        return temp
    
    def resist_read(self, channel:str): # channel 'A' - 'D'
        command = "SRDG? " + channel
        resistance = self.query(command)
        print(resistance)
        resistance = resistance.replace("+","")
        resistance = resistance.replace("\r","")
        resistance = resistance.replace("\n","")
        
        resistance = float(resistance)
        return resistance
    
    def resist_read_all(self):
        command = "SRDG? A;SRDG? B;SRDG? C;SRDG? D"
        resistance = self.query(command)
        resistance = resistance.replace("+","")
        resistance = resistance.replace("\r","")
        resistance = resistance.replace("\n","")
        resistance = resistance.split(";")
        i = 0
        while i < len(resistance):
            resistance[i] = float(resistance[i])
            i += 1
        print(resistance)
        return resistance

if __name__ == "__main__":
    device = temperatureController('test', 'COM4')
    count = 0
    while count < 5:
        temp = device.resist_read_all()
        count += 1
        time.sleep(0.8)
    device.close()
    
        


















