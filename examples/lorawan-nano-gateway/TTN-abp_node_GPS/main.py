from micropyGPS import MicropyGPS
from machine import UART
from network import LoRa
import socket
import binascii
import struct
import time
import config
import tools
    
# Initialize GPS
com = UART(1,pins=(config.TX, config.RX),  baudrate=9600) 
my_gps = MicropyGPS()

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)

# create an ABP authentication params
dev_addr = struct.unpack(">l", binascii.unhexlify(config.DEV_ADDR.replace(' ','')))[0]
nwk_swkey = binascii.unhexlify(config.NWK_SWKEY.replace(' ',''))
app_swkey = binascii.unhexlify(config.APP_SWKEY.replace(' ',''))

# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# remove all the non-default channels
for i in range(3, 16):
    lora.remove_channel(i)

# set the 3 default channels to the same frequency
lora.add_channel(0, frequency=868100000, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=868100000, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=868100000, dr_min=0, dr_max=5)

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
s.setblocking(False)

while True: 
    pycom.rgbled(0x007f700) # green
    if com.any():
        my_sentence = com.readline()
        for x in my_sentence:
            my_gps.update(chr(x)) 
        gps_array = tools.convert_latlon(my_gps.latitude[0] + (my_gps.latitude[1] / 60), my_gps.longitude[0] + (my_gps.longitude[1] / 60))
        print(gps_array)
        s.send(gps_array)  
    time.sleep(.5)    
    pycom.rgbled(0)	
    time.sleep(60)