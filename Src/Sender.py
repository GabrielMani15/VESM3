
try:
    from machine import Pin
    from time import sleep
    import dht
    import network
    import espnow
    
    from machine import Pin, ADC
    from time import sleep
except ImportError:
    print("Import failed")

temputure_Sensor_Pin = 18
temputure_Sensor = dht.DHT11(Pin(temputure_Sensor_Pin))

#|temputure section Aproved
def get_Temp():
    temputure_Sensor.measure()
    heat = temputure_Sensor.temperature()
    return "{}".format(heat)

#Section|

# A WLAN interface must be active
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()   

#Check channel
sta.config(channel=5)
print("Channel:", sta.config("channel"))

#Starting bridge connection
e = espnow.ESPNow()
e.active(True)
peer = b'4\x85\x18\xa7nP'
e.add_peer(peer)

#Packing func just puts the items in a list
def shipping_Packet(tempValue,lightValue) -> list[str]:
    return [tempValue, lightValue]

print("Started")
while True:
    #Get lightValues
    light_Sensor = ADC(Pin(17))
    light_Sensor.atten(ADC.ATTN_11DB)
    light_Sensor_Value = light_Sensor.read()
    
    #Get temp
    temp = get_Temp()
    
    #Send data
    box = shipping_Packet(temp, light_Sensor_Value)
    e.send(peer,b'{}'.format(box))
    
    #Wait 2 sec
    sleep(2)
    
