from microdot_asyncio import Microdot, Response,redirect
from machine import Pin
import network
import espnow

led = Pin(2, Pin.OUT)

def testerwep(temputure,light):
    if led.value() == 1:
        Value ="Off"
    else:
        Value ="On"
    
    page = """
            <!doctype html>
            <html>
            <head>
              <meta charset="UTF-8">
              <meta name="viewport" content="width=device-width, initial-scale=1.0">
              <script src="https://cdn.tailwindcss.com"></script>
            </head>
            <body>
              
                <main class="bg-black h-screen w-full overflow-hidden">

                  <div class="bg-gradient-to-r from-sky-500 to-sky-800 h-10 mr-10 ml-10 mt-8 blur-3xl "></div>

                  <div class="bg-slate-900 bg-opacity-40 w-full h-full max-h-96 max-w-lg m-auto mt-2 rounded-2xl">

                    <h3 class="text-center text-3xl pt-4 text-gray-400 font-bold">Vesm23</h3>

                    <div class="grid place-items-center gap-8 mt-6">

                      <button class="border-sky-500 border-2 rounded-xl h-10 w-60 text-center text-gray-300 font-semibold hover:bg-sky-600 hover:border-none hover:transition-all hover:text-white">

                        <a href="/CtnR">Turn """+ Value +""" the brightness sensor</a>
                      
                      </button>

                      <button class="border-sky-500 border-2 rounded-xl h-10 w-60 text-center text-gray-300 hover:text-white font-semibold hover:bg-sky-600 hover:border-none hover:transition-all">

                        <a href="/NDR">Reqaust new data</a>

                      </button>
                      
                       <div class="text-gray-400 border-2 border-sky-500 rounded-xl pt-1 pb-1 pr-5 pl-5 hover:text-white hover:font-semibold">

                            <h3>Light data : """+ light +""" </h3>

                        </div>
                      
                      <section>

                        <div class="bg-black bg-opacity-25 h-full w-full col-span-1 flex justify-center items-center rounded-2xl">

                        <div class="border-l-4 border-t-4 border-sky-500 h-12 w-12 rounded-full grid place-items-center">

                          <h3 class="text-2xl text-white hover:text-gray-300">"""+ temputure +"""  </h3>

                        </div>

                      </div>

                      </section>

                    </div>
                  </div>

                </main>
            </body>
            </html>
            """
    return page

app = Microdot()
Response.default_content_type = 'text/html'

def stabilze_STA():
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    #sta.disconnect() 
    sta.config(channel=5)
    print("Channel:", sta.config("channel"))
    return sta

def bridge():
    e = espnow.ESPNow()
    e.active(True)
    return e

def datalink():
    stabilze_STA()
    e = bridge()
    host, msg = e.recv(500)
    if msg:
        temp = msg.decode()
        print("Message recived",temp)
        e.active(False)
        return temp
    
global ck    
ck = None


@app.route('/')
def index(request):
    heat = None
    stabilze_STA()
    e = bridge()
    host, temp = e.recv(3500)
    if temp:
        data = temp.decode()
        tempt,light = data[2:4],data[7:-1]
        print("Tempt",tempt)
        print("Light",light)
    if ck == True:
        html = testerwep(tempt,light)
        print(ck)
    else:
        html = testerwep(tempt,"Off")
        print(ck)
    return html

@app.route('/CtnR')
def theoffroute(request):
    global ck
    if led.value() == 1:
        led.value(0)
        ck = False
    else:
        led.value(1)
        ck = True
    return redirect("/")

@app.route("/NDR")
def thenewdata(request):
    return redirect("/")

app.run(port=80)
