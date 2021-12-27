import json
from typing_extensions import runtime_checkable
import requests
import hmac
import hashlib
import time

Base_url =  "https://fapi.binance.com"

def para2string(params):     #根据params（一个参数字典）生成字符串函数
    s=''
    for k in params.keys():
        s+=k
        s+='='
        s+=(str(params[k]))
        s+='&'
    return s[:-1]

def signature(params):
    signature=hmac.new(secretKey.encode('utf-8'),msg=para2string(params).encode('utf-8'),digestmod=hashlib.sha256).hexdigest()
    return signature

def getUrl(path,params):
    url=Base_url + path + '?' + para2string(params)
    return url

if __name__ == '__main__':
    
    apiKey=""
    secretKey=""
    timestamp=int(time.time()*1000)
    headers={'X-MBX-APIKEY':apiKey}

# 下单 (TRADE)      
    orderParams={"symbol":"BNBUSDT", 
            "side":"BUY",
            "type":"LIMIT",
            "quantity":1,
            "price":"60", 
            "timeInForce":"GTC", 
            "recvWindow":"5000",
            "timestamp":timestamp
            }
    orderParams['signature']=signature(orderParams)
    path="/fapi/v1/order"
    # Order=requests.post(url=getUrl(path, orderParams),headers=headers).json()
    # print(Order)
    

# 更改持仓模式(TRADE)

    DualParams={"dualSidePosition":"false", 
                "timestamp":timestamp
               }
    DualParams['signature']=signature(DualParams)
    path="/fapi/v1/positionSide/dual"
    # Dual=requests.post(url=getUrl(path, DualParams),headers=headers).json()
    # print(Dual)

# 查询持仓模式(TRADE)

    DisDualParams={"timestamp":timestamp}
    DisDualParams['signature']=signature(DisDualParams)
    path="/fapi/v1/positionSide/dual"
    # DisDual=requests.get(url=getUrl(path, DisDualParams),headers=headers).json()
    # print(DisDual)

# 查询联合保证金模式(USER_DATA)

    DisMultiAssetsMarginParams={"timestamp":timestamp}
    DisMultiAssetsMarginParams['signature']=signature(DisMultiAssetsMarginParams)
    path="/fapi/v1/multiAssetsMargin"
    # DisMultiAssetsMargin=requests.get(url=getUrl(path, DisMultiAssetsMarginParams),headers=headers).json()
    # print(DisMultiAssetsMargin)

# 批量下单 (TRADE)     
# {'code': -1102, 'msg': "Mandatory parameter 'timestamp' was not sent, was empty/null, or malformed."}
    # batchOrdersParams={
    #               "batchOrders": [
    #                   {
    #                    "symbol":"BNBUSDT", 
    #                    "side":"BUY",
    #                    "type":"LIMIT",
    #                    "quantity":1,
    #                    "price":"101",
    #                    "timeInForce":"GTC", 
    #                    },
    #                    {
    #                    "symbol":"BNBUSDT", 
    #                    "side":"BUY",
    #                    "type":"LIMIT",
    #                    "quantity":1,
    #                    "price":"102", 
    #                    "timeInForce":"GTC"
    #                    },
    #                 ]
    #             } 
    # # batchOrdersParams["timestamp"]=signature(timestamp)
    # # print(batchOrdersParams)
    # batchOrdersParams['signature']=signature(batchOrdersParams)
    # path="/fapi/v1/batchOrders"
    # batchOrder=requests.post(url=getUrl(path, batchOrdersParams),headers=headers).json()
    # print(batchOrder)

#  查询订单 (USER_DATA)    id:36868606949
    DisOrderParams={"symbol":"BNBUSDT", 
                    "orderId":36868606949,
                    "timestamp":timestamp
            }
    DisOrderParams['signature']=signature(DisOrderParams)
    path="/fapi/v1/order"
    # DisOrder=requests.get(url=getUrl(path, DisOrderParams),headers=headers).json()
    # print(DisOrder)

# 撤销订单 (TRADE)
    DelOrderParams={"symbol":"BNBUSDT", 
                    "orderId":36868606949,
                    "timestamp":timestamp
            }
    DelOrderParams['signature']=signature(DelOrderParams)
    path="/fapi/v1/order"
    # DelOrder=requests.delete(url=getUrl(path, DelOrderParams),headers=headers).json()
    # print(DelOrder)

# 查询当前挂单 (USER_DATA)
    OpenOrderParams={"symbol":"BNBUSDT", 
                    "orderId":36864141568,
                    "timestamp":timestamp
            }
    OpenOrderParams['signature']=signature(OpenOrderParams)
    path="/fapi/v1/order"
    # OpenOrder=requests.delete(url=getUrl(path, OpenOrderParams),headers=headers).json()
    # print(OpenOrder)

# 查询所有订单(包括历史订单) (USER_DATA)
    DisAllOrdersParams={"symbol":"BNBUSDT", 
                        "timestamp":timestamp
            }
    DisAllOrdersParams['signature']=signature(DisAllOrdersParams)
    path="/fapi/v1/allOrders"
    # DisAllOrders=requests.get(url=getUrl(path, DisAllOrdersParams),headers=headers).json()
    # print(DisAllOrders)

# 账户余额V2 (USER_DATA)
    BalanceParams={
                    "timestamp":timestamp
            }
    BalanceParams['signature']=signature(BalanceParams)
    path="/fapi/v2/balance"
    # balance=requests.get(url=getUrl(path, BalanceParams),headers=headers).json()
    # print(balance)

# 账户信息V2 (USER_DATA)
    accountParams={
                    "timestamp":timestamp
            }
    accountParams['signature']=signature(accountParams)
    path="/fapi/v2/account"
    # account=requests.get(url=getUrl(path, accountParams),headers=headers).json()
    # print(account)

# 账户成交历史 (USER_DATA)
    userTradesParams={"symbol":"BNBUSDT", 
                    "timestamp":timestamp
            }
    userTradesParams['signature']=signature(userTradesParams)
    path="/fapi/v1/userTrades"
    # userTrades=requests.get(url=getUrl(path, userTradesParams),headers=headers).json()
    # print(userTrades)

# 用户手续费率 (USER_DATA)
    commissionRateParams={"symbol":"BNBUSDT", 
                    "timestamp":timestamp
            }
    commissionRateParams['signature']=signature(commissionRateParams)
    path="/fapi/v1/commissionRate"
    # commissionRate=requests.get(url=getUrl(path, commissionRateParams),headers=headers).json()
    # print(commissionRate)

# 用户 API 交易量化规则指标 (USER_DATA)
    apiTradingStatusParams={
                    "timestamp":timestamp
            }
    apiTradingStatusParams['signature']=signature(apiTradingStatusParams)
    path="/fapi/v1/apiTradingStatus"
    # apiTradingStatus=requests.get(url=getUrl(path, apiTradingStatusParams),headers=headers).json()
    # print(apiTradingStatus)

# 获取账户损益资金流水(USER_DATA)
    incomeParams={
                    "timestamp":timestamp
            }
    incomeParams['signature']=signature(incomeParams)
    path="/fapi/v1/income"
    # income=requests.get(url=getUrl(path, incomeParams),headers=headers).json()
    # print(income)

# 杠杆分层标准 (USER_DATA)
    leverageBracketParams={
                    "timestamp":timestamp
            }
    leverageBracketParams['signature']=signature(leverageBracketParams)
    path="/fapi/v1/leverageBracket"
    # leverageBracket=requests.get(url=getUrl(path, leverageBracketParams),headers=headers).json()
    # print(leverageBracket)

# 用户强平单历史 (USER_DATA)
    forceOrdersParams={
                    "timestamp":timestamp
            }
    forceOrdersParams['signature']=signature(forceOrdersParams)
    path="/fapi/v1/forceOrders"
    forceOrders=requests.get(url=getUrl(path, forceOrdersParams),headers=headers).json()
    print(forceOrders)
