# class Zerodha():
#     def __init__(self):
#         self.headers = ['instrument_token','exchange_token','tradingsymbol',
#                    'name','last_price','expiry',
#                    'strike','tick_size','lot_size',
#                    'instrument_type','segment','exchange'
#         ]

#     def map_icici(self, data):
#         # {"Token","ShortName","Series",
#         #         "CompanyName","TickSize","LotSize",
#         #         "ScripCode","MarketLot","BCastFlag",
#         #         "AVMBuyMargin","AVMSellMargin","ScripID",
#         #         "ScripName","GroupName","NdFlag",
#         #         "NDSDate","NDEDate","SuspStatus",
#         #         "avmflag","SuspensionReason","Suspensiondate",
#         #         "DateOfListing","DateOfDeListing","IssuePrice",
#         #         "FaceValue","ISINCode","52WeeksHigh",
#         #         "52WeeksLow","LifeTimeHigh","LifeTimeLow",
#         #         "HighDate","LowDate","MarginPercentage","ExchangeCode"
#         # }

#         nse_map = {
#             'instrument_token': data['token'],
#             'exchange_token': data['token'],
#             'tradingsymbol': data['symbol'],
#             'name': data['CompanyName'],
#             'last_price': data['FaceValue'],
#             'expiry': data['ExpiryDate'],
#             'strike': '',
#             'tick_size': data['ticksize'],
#             'lot_size': data['Lotsize'],
#             'instrument_type': data['InstrumentType'],
#             'segment': data['Series'],
#             'exchange': data['Series']
#         }
#         return nse_map
    
#     def map_angel(self, data):
#         angel_map = {
#             'instrument_token': data['token'],
#             'exchange_token': '',
#             'tradingsymbol': data['symbol'],
#             'name': 'name',
#             'last_price': '',
#             'expiry': data['expiry'],
#             'strike': data['strike'],
#             'tick_size': data['tick_size'],
#             'lot_size': data['lotsize'],
#             'instrument_type': data['instrumenttype'],
#             'segment': f"{data['exch_seg'][0]}{data['symbols'][-2:]}-{data['instrumenttype']}",
#             'exchange': f"{data['exch_seg'][0]}{data['symbols'][-2:]}"
#         }

#         return angel_map
    
#     def map_kotak(self, data):
#         kotak_map = {
#             'instrument_token': data['instrumenttoken'],
#             'exchange_token': data['exchangetoken'],
#             'tradingsymbol': data['instrumentname'],
#             'name': data['name'],
#             'last_price': data['lastprice'],
#             'expiry': data['expiry'],
#             'strike': data['strike'],
#             'tick_size': data['ticksize'],
#             'lot_size': data['lotsize'],
#             'instrument_type': data['instrumenttype'],
#             'segment': ,
#             'exchange': 
#         }