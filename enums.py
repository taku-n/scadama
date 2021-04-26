from enum import Enum, Flag, auto

# ENUM_ACCOUNT_*
# English:  https://www.mql5.com/en/docs/constants/environment_state/accountinformation
# Japanese: https://www.mql5.com/ja/docs/constants/environment_state/accountinformation

class ENUM_ACCOUNT_TRADE_MODE(Enum):    # AccountInfo.trade_mode
    ACCOUNT_TRADE_MODE_DEMO    = 0
    ACCOUNT_TRADE_MODE_CONTEST = auto()
    ACCOUNT_TRADE_MODE_REAL    = auto()

class ENUM_ACCOUNT_STOPOUT_MODE(Enum):  # AccountInfo.margin_so_mode
    ACCOUNT_STOPOUT_MODE_PERCENT = 0
    ACCOUNT_STOPOUT_MODE_MONEY   = auto()

class ENUM_ACCOUNT_MARGIN_MODE(Enum):   # AccountInfo.margin_mode
    ACCOUNT_MARGIN_MODE_RETAIL_NETTING = 0
    ACCOUNT_MARGIN_MODE_EXCHANGE       = auto()
    ACCOUNT_MARGIN_MODE_RETAIL_HEDGING = auto()


# English:  https://www.mql5.com/en/docs/constants/environment_state/marketinfoconstants
# Japanese: https://www.mql5.com/ja/docs/constants/environment_state/marketinfoconstants

class ENUM_SYMBOL_CHART_MODE(Enum):       # SymbolInfo.chart_mode
    SYMBOL_CHART_MODE_BID  = 0
    SYMBOL_CHART_MODE_LAST = auto()

class SYMBOL_ORDER_MODE(Flag):            # SymbolInfo.order_mode
    SYMBOL_ORDER_MARKET     = auto()  #  1
    SYMBOL_ORDER_LIMIT      = auto()  #  2
    SYMBOL_ORDER_STOP       = auto()  #  4
    SYMBOL_ORDER_STOP_LIMIT = auto()  #  8
    SYMBOL_ORDER_SL         = auto()  # 16
    SYMBOL_ORDER_TP         = auto()  # 32
    SYMBOL_ORDER_CLOSEBY    = auto()  # 64

class ENUM_SYMBOL_TRADE_MODE(Enum):       # SymbolInfo.trade_mode
    SYMBOL_TRADE_MODE_DISABLED  = 0
    SYMBOL_TRADE_MODE_LONGONLY  = auto()
    SYMBOL_TRADE_MODE_SHORTONLY = auto()
    SYMBOL_TRADE_MODE_CLOSEONLY = auto()
    SYMBOL_TRADE_MODE_FULL      = auto()

class ENUM_SYMBOL_TRADE_EXECUTION(Enum):  # SymbolInfo.trade_exemode
    SYMBOL_TRADE_EXECUTION_REQUEST  = 0       # deviation of order_send() works.
    SYMBOL_TRADE_EXECUTION_INSTANT  = auto()  # deviation of order_send() works.
    SYMBOL_TRADE_EXECUTION_MARKET   = auto()  # deviation of order_send() does not work.
    SYMBOL_TRADE_EXECUTION_EXCHANGE = auto()  # deviation of order_send() does not work.


# ENUM_ORDER_*
# English:  https://www.mql5.com/en/docs/constants/tradingconstants/orderproperties
# Japanese: https://www.mql5.com/ja/docs/constants/tradingconstants/orderproperties

class ENUM_ORDER_TYPE(Enum):  # TradePosition.type
    ORDER_TYPE_BUY             = 0
    ORDER_TYPE_SELL            = auto()
    ORDER_TYPE_BUY_LIMIT       = auto()
    ORDER_TYPE_SELL_LIMIT      = auto()
    ORDER_TYPE_BUY_STOP        = auto()
    ORDER_TYPE_SELL_STOP       = auto()
    ORDER_TYPE_BUY_STOP_LIMIT  = auto()
    ORDER_TYPE_SELL_STOP_LIMIT = auto()
    ORDER_TYPE_CLOSE_BY        = auto()
