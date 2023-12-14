try:
    import network
    ssid = ''
    password = ''
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print('Ip address of the network is:', sta_if.ifconfig())
    
except Exception as err:
    print("Boot failed",err)
