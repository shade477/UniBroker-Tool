class Zerodha():
    def __init__(self):
        self.headers = ['instrument_token','exchange_token','tradingsymbol',
                   'name','last_price','expiry',
                   'strike','tick_size','lot_size',
                   'instrument_type','segment','exchange'
        ]

    def map_icici(self):
        # {"Token","ShortName","Series",
        #         "CompanyName","TickSize","LotSize",
        #         "ScripCode","MarketLot","BCastFlag",
        #         "AVMBuyMargin","AVMSellMargin","ScripID",
        #         "ScripName","GroupName","NdFlag",
        #         "NDSDate","NDEDate","SuspStatus",
        #         "avmflag","SuspensionReason","Suspensiondate",
        #         "DateOfListing","DateOfDeListing","IssuePrice",
        #         "FaceValue","ISINCode","52WeeksHigh",
        #         "52WeeksLow","LifeTimeHigh","LifeTimeLow",
        #         "HighDate","LowDate","MarginPercentage","ExchangeCode"
        # }

        nse_map = {
            'instrument_token': 'token',
            'exchange_token': 'token',
            'tradingsymbol': 'symbol',
            'name': 'CompanyName',
            'last_price': 'FaceValue',
            'expiry': 'ExpiryDate',
            'strike': '',
            'tick_size': 'ticksize',
            'lot_size': 'Lotsize',
            'instrument_type': 'InstrumentType',
            'segment': 
        }