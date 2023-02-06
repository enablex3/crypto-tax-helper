# Record Reader takes in arguments to process a crypto.com transactions record.
# Additional arguments required to display or record results

import csv

CRYPTO_COM = "Crypto.com"
BINANCE = "Binance"
BITRUE = "Bitrue"
KUCOIN = "KuCoin"

TYPES = [
    CRYPTO_COM,
    BINANCE,
    BITRUE,
    KUCOIN
]

CRYPTO_COM_INDICATORS = {
    "BUY": "Buy",
    "SELL": " ->",
    "SELL_IGNORE": ["USDC -> USD", "USDT -> USD"]
}

CRYPTO_COM_COLUMNS = {
    "TRANSACTION_DESCRIPTION": 1,
    "NATIVE_AMOUNT" : 7
}

class RecordReader:
    
    def __init__(self):
        self.record_content = []
        self.record_result = False
        self.type = TYPES[0] # change to be modular in the future
        self.buys = []
        self.sells = []
        self.proceeds = float(0)
        
    def load_file(self, file_path):
        with open(file_path, newline="") as CSV_FILE:
            record_file = csv.reader(CSV_FILE, quotechar="|")
            for row in record_file:
                self.record_content.append(row)
            
    def display_file_content(self):
        for row in self.record_content:
            print(row)
            
    def set_record_result(self, record_boolean):
        self.record_result = record_boolean
        
    def crypto_com_scan(self):
        for row in self.record_content:
            # each row is a list (csv columns)
            isBuy = False
            # determine if the description row contains purchase information
            transaction_description = row[CRYPTO_COM_COLUMNS["TRANSACTION_DESCRIPTION"]]
            if CRYPTO_COM_INDICATORS["BUY"] in transaction_description:
                # if we're looking at a row that can give us purchase info, then get the amount
                transaction_amount = row[CRYPTO_COM_COLUMNS["NATIVE_AMOUNT"]]
                # add the amount to the list of buys
                self.buys.append(float(transaction_amount))
            elif CRYPTO_COM_INDICATORS["SELL"] in transaction_description:
                # if we're looking at a valid sell, collect that information
                # double-check to make sure we're not collect stable coin sells
                if not transaction_description in CRYPTO_COM_INDICATORS["SELL_IGNORE"]:
                    transaction_amount = row[CRYPTO_COM_COLUMNS["NATIVE_AMOUNT"]]
                    self.sells.append(float(transaction_amount))
        # once we're all done, let's tally the amounts
        totalBuy = sum(self.buys)
        totalSell = sum(self.sells)
        self.gains = totalSell - totalBuy
        
    def get_proceeds(self):
        return self.gains, sum(self.buys), sum(self.sells)
    
    def generate_document(self):
        return None
                