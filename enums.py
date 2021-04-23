from enum import Enum, auto

# English:  https://www.mql5.com/en/docs/constants/environment_state/accountinformation
# Japanese: https://www.mql5.com/ja/docs/constants/environment_state/accountinformation

class ENUM_ACCOUNT_TRADE_MODE(Enum):    # trade_mode
    ACCOUNT_TRADE_MODE_DEMO    = 0
    ACCOUNT_TRADE_MODE_CONTEST = auto()
    ACCOUNT_TRADE_MODE_REAL    = auto()

class ENUM_ACCOUNT_STOPOUT_MODE(Enum):  # margin_so_mode
    ACCOUNT_STOPOUT_MODE_PERCENT = 0
    ACCOUNT_STOPOUT_MODE_MONEY   = auto()

class ENUM_ACCOUNT_MARGIN_MODE(Enum):   # margin_mode
    ACCOUNT_MARGIN_MODE_RETAIL_NETTING = 0
    ACCOUNT_MARGIN_MODE_EXCHANGE       = auto()
    ACCOUNT_MARGIN_MODE_RETAIL_HEDGING = auto()


# English:  https://www.mql5.com/en/docs/constants/environment_state/marketinfoconstants
# Japanese: https://www.mql5.com/ja/docs/constants/environment_state/marketinfoconstants

class ENUM_SYMBOL_CHART_MODE(Enum):       # chart_mode
    SYMBOL_CHART_MODE_BID  = 0
    SYMBOL_CHART_MODE_LAST = auto()

class ENUM_SYMBOL_TRADE_MODE(Enum):       # trade_mode
    SYMBOL_TRADE_MODE_DISABLED  = 0
    SYMBOL_TRADE_MODE_LONGONLY  = auto()
    SYMBOL_TRADE_MODE_SHORTONLY = auto()
    SYMBOL_TRADE_MODE_CLOSEONLY = auto()
    SYMBOL_TRADE_MODE_FULL      = auto()

class ENUM_SYMBOL_TRADE_EXECUTION(Enum):  # trade_exemode
    SYMBOL_TRADE_EXECUTION_REQUEST  = 0       # deviation of order_send() works.
    SYMBOL_TRADE_EXECUTION_INSTANT  = auto()  # deviation of order_send() works.
    SYMBOL_TRADE_EXECUTION_MARKET   = auto()  # deviation of order_send() does not work.
    SYMBOL_TRADE_EXECUTION_EXCHANGE = auto()  # deviation of order_send() does not work.
