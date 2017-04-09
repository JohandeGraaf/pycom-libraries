from network import Bluetooth
from network import LoRa
import socket
import binascii
import struct
import time
import config
import pycom

# Setup the LoRaWAN part 

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

# Setup the Bluetooth part 

hexValue = "";

bluetooth = Bluetooth()
bluetooth.set_advertisement(name='LoPy01', service_uuid=b'1234567890123456')

def conn_cb (bt_o):
    events = bt_o.events()
    if  events & Bluetooth.CLIENT_CONNECTED:
        print("Client connected")
        hexValue = "";
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("Client disconnected")

bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)

bluetooth.advertise(True)

srv1 = bluetooth.service(uuid=b'1234567890123456', isprimary=True)

chr1 = srv1.characteristic(uuid=b'ab34567890123456', value=5)

def char1_cb(chr):
    print("Write request with value = {}".format(chr.value()))
    hexValue = chr.value()
    s.send(bytes(hexValue))
    print('sending hexValue to LoRaWAN')
        
char1_cb = chr1.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=char1_cb)

srv2 = bluetooth.service(uuid=1234, isprimary=True)

chr2 = srv2.characteristic(uuid=4567)



