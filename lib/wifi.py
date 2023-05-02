import network

def connect_wifi(ssid, password):
    #Connect to your network
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    while station.isconnected() == False:
        pass
    print('Connection successful')
    print(station.ifconfig())
  
def wifi_status():
    station = network.WLAN(network.STA_IF)
    return station.isconnected()
   