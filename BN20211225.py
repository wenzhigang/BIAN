import json
import requests
import hmac
import hashlib
import time



Base_url =  "https://fapi.binance.com"

# 测试服务器连通性 PING
r = requests.get(Base_url + "/fapi/v1/ping")  # 
# print(r.text)


# 获取服务器时间
t = requests.get(Base_url + "/fapi/v1/time")
# print(t.json())

# 获取交易规则和交易对

e = requests.get(Base_url + "/fapi/v1/exchangeInfo")
# print(e.json())

# 深度信息

d = requests.get(Base_url + "/fapi/v1/depth", params={"symbol":"BTCUSDT", "limit":"5"})
# print(d.json())

# 近期成交

Recent_trade = requests.get(Base_url + "/fapi/v1/trades", params={"symbol":"BTCUSDT","limit":"500"})
# print(Recent_trade.json())

# 查询历史成交(MARKET_DATA), 未完成，需要API Key

Hist_trade = requests.get(Base_url + "/fapi/v1/historicalTrades", params={"symbol":"BTCUSDT"})
# print(Hist_trade.json())

# 近期成交(归集)
agg_trade= requests.get(Base_url + "/fapi/v1/aggTrades", params={"symbol":"BTCUSDT"})
# print(agg_trade.json())

# K线数据
kline=requests.get(Base_url + "/fapi/v1/klines", params={"symbol":"BTCUSDT", "interval":"1m"})
# print(kline.json())

# 连续合约K线数据
Cont_kline=requests.get(Base_url + "/fapi/v1/continuousKlines", params={"pair":"BTCUSDT", "contractType":"PERPETUAL", "interval":"1m"})
# print(Cont_kline.json())

# 价格指数K线数据
indexPriceKlines=requests.get(Base_url + "/fapi/v1/indexPriceKlines", params={"pair":"BTCUSDT", "interval":"1m"})
# print(indexPriceKlines.json())

# 标记价格K线数据
markPriceKlines=requests.get(Base_url + "/fapi/v1/markPriceKlines", params={"symbol":"BTCUSDT", "interval":"1m"})
# print(markPriceKlines.json())

# 最新标记价格和资金费率 (不指定symbol，返回所有交易对信息)
premiumIndex=requests.get(Base_url + "/fapi/v1/premiumIndex", params={"symbol":"BTCUSDT"})
# print(premiumIndex.json())

# 查询资金费率历史
fundingRate=requests.get(Base_url + "/fapi/v1/fundingRate", params={"symbol":"BTCUSDT"})
# print(fundingRate.json())

# 24hr价格变动情况
hr=requests.get(Base_url + "/fapi/v1/ticker/24hr")
# print(hr.json())

# 最新价格
price=requests.get(Base_url + "/fapi/v1/ticker/price",params={"symbol":"BTCUSDT"})
# print(price.json())

# 当前最优挂单
bookTicker=requests.get(Base_url + "/fapi/v1/ticker/bookTicker")
# print(bookTicker.json())

# 获取未平仓合约数
openInterest=requests.get(Base_url + "/fapi/v1/openInterest", params={"symbol":"btcusdt"})
# print(openInterest.json())

# 合约持仓量
openInterestHist=requests.get(Base_url + "/futures/data/openInterestHist", params={"symbol":"btcusdt", "period":"5m"})
# print(openInterestHist.json())

# 大户账户数多空比
topLongShortAccountRatio=requests.get(Base_url + "/futures/data/topLongShortAccountRatio", params={"symbol":"btcusdt", "period":"5m"})
# print(topLongShortAccountRatio.json())

# 大户持仓量多空比
topLongShortPositionRatio=requests.get(Base_url + "/futures/data/topLongShortPositionRatio", params={"symbol":"btcusdt", "period":"5m"})
# print(topLongShortPositionRatio.json())

# 多空持仓人数比
globalLongShortAccountRatio=requests.get(Base_url + "/futures/data/globalLongShortAccountRatio", params={"symbol":"ethusdt","period":"5m"})
# print(globalLongShortAccountRatio.json())  

# 合约主动买卖量
takerlongshortRatio=requests.get(Base_url + "/futures/data/takerlongshortRatio", params={"symbol":"ltcusdt","period":"5m"})
# print(takerlongshortRatio.json())

# 杠杆代币历史净值K线
lvtKlines=requests.get(Base_url + "/fapi/v1/lvtKlines", params={"symbol":"BTCUP", "interval":"5m"})
# print(lvtKlines.json())

# 综合指数交易对信息
indexInfo=requests.get(Base_url + "/fapi/v1/indexInfo")
# print(indexInfo.json())

# 多资产模式资产汇率指数
assetIndex=requests.get(Base_url + "/fapi/v1/assetIndex").json()
# print(assetIndex)


# --------------------------------------------------------------------------------------------------------
# #
# # 测试下单接口 (TRADE)
testTrade=requests.post(Base_url + "/fapi/v1/order/test")
# print(testTrade.json())

apiKey="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
secretKey="BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
signature = hmac.new(apiKey.encode('utf-8'),secretKey.encode('utf-8'),hashlib.sha256).hexdigest()
timestamp=int(time.time()*1000)
# print(timestamp)
params={"symbol":"BTCUSDT", 
        "type":"LIMIT",
        "quantity":"0.001",
        "price":"20000", 
        "timeInForce":"GTC", 
        "recvWindow":"5000",
        "timestamp":timestamp,
        "signature":signature
        }
# print(params)
url=Base_url + "/fapi/v1/order"
order=requests.post(url,  headers={"X-MBX-APIKEY":apiKey}, params=params) 
# # $ curl -H "X-MBX-APIKEY: dbefbc809e3e83c283a984c3a1459732ea7db1360ca80c5c2c8867408d28cc83" -X POST 'https://fapi.binance.com/fapi/v1/order?symbol=BTCUSDT&side=BUY&type=LIMIT&quantity=1&price=9000&timeInForce=GTC&recvWindow=5000&timestamp=1591702613943&signature= 3c661234138461fcc7a7d8746c6558c9842d4e10870d2ecbedf7777cad694af9'
print(order.json())