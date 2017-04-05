from network import LoRa
import socket
import binascii
import struct
import time
import config

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)

# create an ABP authentication params
dev_eui = binascii.unhexlify(config.DEV_EUI.replace(' ',''))
app_eui = binascii.unhexlify(config.APP_EUI.replace(' ',''))
app_key = binascii.unhexlify(config.APP_KEY.replace(' ',''))

# set the 3 default channels to the same frequency
lora.add_channel(0, frequency=868100000, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=868100000, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=868100000, dr_min=0, dr_max=5)

# join a network using OTAA
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not joined yet...')

# remove all the non-default channels
for i in range(3, 16):
    lora.remove_channel(i)

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
s.setblocking(False)

i = 0

while True:     # runs forever
    if (i >= 10):
        i = 0
    i = i + 1    
    sensor = '' + str(i)
    uart1.write(str(i)+'\n')
    time.sleep(3)
    if uart1.any() > 0:
        sensor = uart1.readall() # read the response from the Circuit Playground
        pycom.rgbled(0x007f700) # green
        s.send(bytes(sensor))
    print('count: ' + str(i))
    print('sending: ')
    print(sensor)    
    time.sleep(.5)    
    pycom.rgbled(0)	
    time.sleep(3.5)
    rx = s.recv(256)
    if rx:
        pycom.rgbled(0x00007F) # blue    
        print(rx)
        time.sleep(1)    
        pycom.rgbled(0)
    time.sleep(30)