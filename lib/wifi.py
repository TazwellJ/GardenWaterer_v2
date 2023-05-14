import network

class WiFi:

    def __init__(self,ssid,password):
        self.ssid = ssid
        self.password = password      
        self.station = network.WLAN(network.STA_IF)
        
    def connect_wifi(self):
        #Connect to your network
        self.station.active(True)
        self.station.connect(self.ssid, self.password)
        while self.station.isconnected() == False:
            pass
        print('Connection successful')
        print(self.station.ifconfig())
  
    def wifi_status(self):
        # Make sense of the wlan.status() numbers that are returned
        status = self.station.status()
        if status == network.STAT_IDLE:
            return 'STAT_IDLE'
        elif status == network.STAT_CONNECTING:
            return 'STAT_CONNECTING'
        elif status == network.STAT_WRONG_PASSWORD:
            return 'STAT_WRONG_PASSWORD'
        elif status == network.STAT_NO_AP_FOUND:
            return 'STAT_NO_AP_FOUND'
        elif status == network.STAT_CONNECT_FAIL:
            return 'STAT_CONNECT_FAIL'
        elif status == network.STAT_GOT_IP:
            return 'STAT_GOT_IP'
        else:
            return "Unknown wlan status: {}".format(status)
    
    def connected(self):
        if self.station.isconnected() == True:
            return True
        else:
            return False
        