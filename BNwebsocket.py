import json
import websocket
import threading 


def on_open(wsapp):
    print('on open')
    data={
            "method": "SUBSCRIBE",
            "params":
            [
            # "btcusdt@aggTrade"
             "btcusdt@depth5"
            ],
            "id": 1
            }
    wsapp.send(json.dumps(data))

def on_message(wsapp, message):
    print("on message")
    print(message)

def on_error(wsapp, error):
    print(error)

def on_close(wsapp):
    print("on close")

def run():
    # websocket.enableTrace(True)
    wsapp_url = "wss://stream.binance.com:9443/ws"  
    wsapp = websocket.WebSocketApp(wsapp_url, 
                                    on_open=on_open, 
                                    on_message=on_message, 
                                    on_error=on_error, 
                                    on_close=on_close)
    wsapp.run_forever(ping_interval=15)

if __name__ == '__main__':
    t1 = threading.Thread(target=run)
    t1.start()
    print("hello world.")

