import requests
import hashlib
import json
from enum import Enum
import time
import hmac
import pandas as pd
pd.set_option('expand_frame_repr',False)


limit = 1000
end_time = int(time.time() // 60 * 60 * 1000)
print(end_time)
start_time = int(end_time - limit*60*1000)
print(start_time)

class Interval(Enum):
    MINUTE_1 = '1m'
    MINUTE_3 = '3m'
    MINUTE_5 = '5m'
    MINUTE_15 = '15m'
    MINUTE_30 = '30m'
    HOUR_1 = '1h'
    HOUR_2 = '2h'
    HOUR_4 = '4h'
    HOUR_6 = '6h'
    HOUR_8 = '8h'
    HOUR_12 = '12h'
    DAY_1 = '1d'
    DAY_3 = '3d'
    WEEK_1 = '1w'
    MONTH_1 = '1M'

class OrderType(Enum):
    LIMIT = 'LIMIT'
    MARKET = 'MARKET'
    STOP = 'STOP'

class Side(Enum):
    SELL = 'SELL'
    BUY = 'BUY'

class positionSide(Enum):
    LONG = 'LONG'
    SHORT = 'SHORT'

class timeInForce(Enum):
    GTC = 'GTC'
    IOC = 'IOC'
    FOK = 'FOK'
    GTX = 'GTX'

class RequestMethod(Enum):
    GET = 'get'
    POST = 'post'
    DELETE = 'delete'
    PUT = 'put'


class BinanceFuturehttpClient(object):
    def __init__(self, base_url=None, api_key=None, api_secret=None, timeout=5):
        # if base_url:
        #     self.base_url = base_url
        # else:
        #     self.base_url = 'https://fapi.binance.com'

        self.base_url = base_url if base_url else "https://fapi.binance.com"
        self.key = api_key
        self.secret = api_secret
        self.timeout = timeout
    
    def build_parameters(self, params:dict):
        
        return '&'.join([f"{key}={params[key]}" for key in params.keys()])
       

        # requery = ''
        # for key in params.keys():
        #     requery += f"{key}={params[key]}&"
        # requery = requery[0:-1]
        # return requery


    def request(self, method: RequestMethod, path, params=None, verify=False):
        url = self.base_url + path
       
        if params:

            url = url + '?' + self.build_parameters(params)

        if verify:
            query_str = self.build_parameters(params)
            signature = hmac.new(self.secret.encode('utf-8'), msg=query_str.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
            url += '&signature=' + signature 
        
        headers = {"X-MBX-APIKEY": self.key}
        # url = self.base_url + path + '?' + data
        # response_data=requests.post(url, headers, timeout=self.timeout).json()
        # return response_data

        return requests.request(method.value, url, headers=headers, timeout=self.timeout).json()




    def get_server_status(self):
        path = '/fapi/v1/ping'
        return self.request(RequestMethod.GET,path)
        
        # url = self.base_url + path
        # respone_data=requests.get(url,timeout=self.timeout).json()
        # return(respone_data)
    
    def get_server_time(self):
        path = '/fapi/v1/time'
        return self.request(RequestMethod.GET,path)

        # url = self.base_url + path
        # respone_data=requests.get(url,timeout=self.timeout).json()
        # return(respone_data)
       
    def get_exchange_info(self):
        path = '/fapi/v1/exchangeInfo'
        return self.request(RequestMethod.GET, path)

        # url = self.base_url + path
        # respone_data=requests.get(url,timeout=self.timeout).json()
        # return(respone_data)

    def get_market_depth(self,symbol,limit=5):
        path = '/fapi/v1/depth'
        url = self.base_url + path
        limits = [5, 10, 20, 50, 100, 500, 1000]
        if limit not in limits:
            # raise ValueError(f"{limit}is not in the limits")
            limit = 5
        params = {
            "symbol": symbol,
            "limit": limit
        }
        return self.request(RequestMethod.GET, path, params=params)
        # respone_data=requests.get(url,params=params,timeout=self.timeout).json()
        # return(respone_data)      

    def get_klines(self, symbol, interval:Interval, start_time=None, end_time=None, limit=500):
        path = '/fapi/v1/klines'

        params = {'symbol': symbol,
                 'interval': interval.value,
                 'limit': limit
        }

        if start_time:
            params['start_time'] = start_time

        if end_time:
            params['end_time'] = end_time

        return self.request(RequestMethod.GET, path, params=params)

    
        # url = self.base_url + path
        # respone_data=requests.get(url,params=params, timeout=self.timeout).json()
        # return(respone_data)

    def get_ticker_price(self, symbol=None):
        path = '/fapi/v1/ticker/price'
        url = self.base_url + path
        if symbol:
            params = {'symbol': symbol}

        return self.request(RequestMethod.GET, path, params=params)
        # respone_data=requests.get(url, params=params, timeout=self.timeout).json()
        # return(respone_data)

    def get_book_ticker(self, symbol=None):
        path = '/fapi/v1/ticker/bookTicker'
        # url = self.base_url + path
        params=None
        if symbol:
            params = {'symbol': symbol}

        return self.request(RequestMethod.GET, path, params=params)
        # respone_data=requests.get(url, params=params, timeout=self.timeout).json()
        # return(respone_data)

    def get_timestamp(self):
        return int(time.time() * 1000)
        

    def place_order(self, symbol, side: Side, type_: OrderType, positionSide: positionSide, quantity, price=None, stop_price=None, time_inforce=timeInForce.GTC, recv_Window=5000):
        path = '/fapi/v1/order'
        params = {
            'symbol':symbol,
            'side': side.value,
            'type': type_.value,
            'positionSide': positionSide.value,
            'quantity': quantity,
            'recvWindow':recv_Window,
            'timestamp': self.get_timestamp()
        }

        if type_ == OrderType.LIMIT:
            params['timeInForce'] = time_inforce.value
            if price > 0:
               params['price'] = price 
            else:
               raise ValueError('price 不能为空')

        if type_ == OrderType.STOP:
            if stop_price > 0:
                 params['stopPrice'] = stop_price
            else:
                 raise ValueError('stop price 不能小于0')
            if price > 0:
                params['price'] = price
            else:
                raise ValueError('price不能小于0')
        
        return self.request(RequestMethod.POST, path, params=params, verify=True)

        # query_str = ''
        # for key in params.keys():
        #      query_str += f'{key}={params[key]}&'

        # query_str = query_str[0:-1]

        # signature = hmac.new(self.secret.encode('utf-8'),msg=query_str.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        # data = query_str + '&signature' +signature 
        # headers = {"X-MBX-APIKEY": self.key}
        # url = self.base_url + path + '?' + data
        # response_data=requests.post(url, headers, timeout=self.timeout).json()
        # return response_data



    def get_order(self, symbol, order_id, rec_window=5000):
        path= '/fapi/v1/order'
        params={'symbol':symbol,
                'recWindow':rec_window,
                'timestamp': self.get_timestamp(),
                'orderId': order_id
                }
        
        return self.request(RequestMethod.GET, path, params=params, verify=True)

        # query_str = ''
        # for key in params.keys():
        #      query_str += f'{key}={params[key]}&'

        # query_str = query_str[0:-1]

        # signature = hmac.new(self.secret.encode('utf-8'),msg=query_str.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        # data = query_str + '&signature' +signature 
        # headers = {"X-MBX-APIKEY": self.key}
        # url = self.base_url + path + '?' + data
        # response_data=requests.get(url, headers, timeout=self.timeout).json()
        # return response_data


    def cancel_order(self, symbol, order_id,rec_window=5000):
        path= '/fapi/v1/order'
        params={'symbol':symbol,
                'recWindow':rec_window,
                'timestamp': self.get_timestamp(),
                'orderId': order_id
               }
        
        return self.request(RequestMethod.DELETE, path, params=params, verify=True)

        # query_str = query_str[0:-1]

        # signature = hmac.new(self.secret.encode('utf-8'),msg=query_str.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        # data = query_str + '&signature' +signature 
        # headers = {"X-MBX-APIKEY": self.key}
        # url = self.base_url + path + '?' + data
        # response_data=requests.delete(url, headers, timeout=self.timeout).json()
        # return response_data

    def get_open_orders(self, symbol, recv_window=5000):
        path = '/fapi/v1/openOrders'
        params = {'symbol': symbol,
                  "recvWindow": recv_window,
                  "timestamp": self.get_timestamp()
                  }

        return self.request(RequestMethod.GET, path, params=params, verify=True)


if __name__ == '__main__':
    key = "XXXXXXXXXXXXXXXXXX"
    secret = "FDFDDDDDDDDDDDDDDDDDDDd"
    bf = BinanceFuturehttpClient(api_key=key, api_secret=secret)
    
    
    # data = bf.get_server_status()
    # data = bf.get_server_time()
    # data = bf.get_exchange_info()
    # data = bf.get_market_depth('BTCUSDT','10')
    # data = bf.get_klines('BTCUSDT',Interval.MINUTE_15)
    # data = bf.get_ticker_price('ETHUSDT')
    # data = bf.get_book_ticker('BTCUSDT')
    # data = bf.place_order("BTCUSDT", side=Side.BUY, type_=OrderType.LIMIT, positionSide=positionSide.LONG, quantity=0.001, price=10000)
    # data = bf.get_order('BTCUSDT','38239729302')
    data = bf.get_open_orders('BTCUSDT')
    # data = bf.cancel_order('BTCUSDT','38239729302')
    print(data)
    
    
# Binance
