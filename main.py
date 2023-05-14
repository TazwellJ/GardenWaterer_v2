from machine import Pin,SoftI2C
import utime
import urequests
from wifi import WiFi
import _thread
import chirp
from secrets import secrets

# GPIO pinout
# 0 - I2C SDA Pin
# 1 - I2C SCL Pin

# 14 - reservoir water level sensor (upper)
# 15 - reservoir water level sensor (lower)

HTTP_HEADERS = {'Content-Type': 'application/json'}
THINGSPEAK_WRITE_API_KEY = secrets["ts_api_key"]  

ssid = secrets["wifi_ssid"]
password = secrets["wifi_pass"]

numPlants = 2
resActive = True

mode_byte = 0

# I2C device addresses
relAddr = 0x20 # relay board
mst1Addr = 0x21 # moisture sensor 1
mst2Addr = 0x22 # moisture sensor 2
mst3Addr = 0x23 # moisture sensor 3

#Initialize reservoir pump state
pres = 0

#Initialize I2C bus
i2c = SoftI2C(scl=Pin(1),sda=Pin(0),freq=100000)


# By default, the Chirp sensors have an address of 0x20.  If you use an I2C multiplexor you won't need to change it.
# I'm not currently using a multiplexor so this code is for 3 individual sensors.  A script to change the address
# can be found in the Tools subfolder.

# Plant 1
m1 = 0 # Initialize moisture sensor 1 value for ThingSpeak
p1 = 0 # Initialize pump 1 value for ThingSpeak
if numPlants >= 1:
    mst1 = chirp.Chirp(bus=i2c,address=mst1Addr,min_moist=250,max_moist=500)
    p1chan = 3 # relay board channel for pump 1
    mst1prev = mst1.moist_percent # get initial value for use in the low pass filter
    while mst1.busy:
        pass
    print(mst1prev)

# Plant 2
m2 = 0 # Initialize moisture sensor 2 value for ThingSpeak
p2 = 0 # Initialize pump 2 value for ThingSpeak
if numPlants >= 2:
    mst2 = chirp.Chirp(bus=i2c,address=mst2Addr,min_moist=250,max_moist=500)
    p2chan = 2 # relay board channel for pump 2
    mst2prev = mst2.moist_percent # get initial value for use in the low pass filter
    while mst2.busy:
        pass
    print(mst2prev)
    
# Plant 3
m3 = 0 # Initialize moisture sensor 1 value for ThingSpeak
p3 = 0 # Initialize pump 3 value for ThingSpeak
if numPlants == 3:
    mst3 = chirp.Chirp(bus=i2c,address=mst3Addr,min_moist=250,max_moist=500)
    p3chan = 3 # relay board channel for pump 3
    mst3prev = mst2.moist_percent # get initial value for use in the low pass filter
    while mst3.busy:
        pass
    print(mst3prev)
    
# The low pass filter is used to smooth out anomalous readings that would result in erroneously triggering the pumps
# You can change the multipliers as long as the two values add up to 1
def LowPassFilter(prev_val,curr_val):
    newval = round((prev_val * 0.65) + (curr_val * 0.35),1)
    return newval

# This is the code to turn the relays on and off
def ch_mode(addr, channel, mode):   
    global mode_byte
    
    if channel == 1:
        channel = 7
    elif channel == 2:
        channel = 6
    elif channel == 3:    
        channel = 5
    elif channel == 4:
        channel = 4

    mode_byte &= ~(1<<(channel))
    mode_byte |= mode<<channel
    
    buf = [~mode_byte]
    barr = bytearray(buf)
    i2c.writeto(addr,barr)

def checkReservoirLevel():
    # Reservoir
    global pres
    presChan = 4 # relay board channel for reservoir pump
    WLS1 = Pin(14, Pin.IN, Pin.PULL_UP) #water level sensor - upper
    WLS2 = Pin(15, Pin.IN, Pin.PULL_UP) #water level sensor - lower

    while True:
        # check water supply level in reservoir and trigger pump to start when low and stop when full
        # both sensors must read the same value to result in a state change of the pump
        v1 = WLS1.value()
        v2 = WLS2.value()
        if v1 and v2: # both sensors down - reservoir is empty
            ch_mode(relAddr,presChan,1)
            pres = 1
        elif not v1 and not v2: # both sensors up - reservoir is full
            ch_mode(relAddr,presChan,0)
            pres = 0
        for x in range (0,14): # This loop causes the thread to wait for 15 minutes between polls
            utime.sleep(900)

# Connect to wifi
w = WiFi(ssid, password)
w.connect_wifi()

# start Reservoir polling thread
if resActive == True:
    _thread.start_new_thread(checkReservoirLevel, ())
else:
    pres = 0

# main program loop
while True:
    if numPlants >= 1:
        # read moisture sensor 1 and activate/deactivate pump relay when necessary
        last = mst1.moist_percent
        while mst1.busy:
            pass
        m1 = LowPassFilter(mst1prev, mst1.moist_percent)
        if m1 < 40:
            ch_mode(relAddr,p1chan,1)
            p1 = 1
        elif m1 >= 70 and p1 == 1:
            ch_mode(relAddr,p1chan,0)
            p1 = 0
        print(m1)
        mst1prev = m1
        utime.sleep(0.5)
        
    if numPlants >= 2:
        # read moisture sensor 2 and activate/deactivate pump relay when necessary
        last = mst2.moist_percent
        while mst2.busy:
            pass
        m2 = LowPassFilter(mst2prev, mst2.moist_percent)
        if m2 < 40:
            ch_mode(relAddr,p2chan,1)
            p2 = 1
        elif m2 >= 70 and p2 == 1:
            ch_mode(relAddr,p2chan,0)
            p2 = 0
        print(m2)
        mst2prev = m2
        utime.sleep(0.5)
        
    if numPlants == 3:
        # read moisture sensor 3 and activate/deactivate pump relay when necessary
        last = mst3.moist_percent
        while mst3.busy:
            pass
        m3 = LowPassFilter(mst3prev, mst3.moist_percent)
        if m3 < 40:
            ch_mode(relAddr,p3chan,1)
            p3 = 1
        elif m3 >= 70 and p3 == 1:
            ch_mode(relAddr,p3chan,0)
            p3 = 0
        print(m3)
        mst3prev = m3
        utime.sleep(0.5)
    
    if w.connected() == False:
        print("Reconnecting to wifi")
        w.connect_wifi()

    # upload data to ThingSpeak channel
    sensor_data = {'field1':m1, 'field2':m2, 'field3':m3, 'field4':p1, 'field5':p2, 'field6':p3, 'field7':pres}
    request = urequests.post( 'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY, json = sensor_data, headers = HTTP_HEADERS )  
    request.close()
        
    utime.sleep(300)
