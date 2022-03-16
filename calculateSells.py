import csv, sys

"""
INDEXES:
0 - Timestamp
1 - Transaction Description
2 - Currency
3 - Amount
4 - To Currency
5 - To Amount
6 - Native Currency
7 - Native Amount
8 - Native Amount (in USD)
9 - Transaction Kind
"""

# Init dictionary for access column indexes for ease of use
columns = {
    "Timestamp": 0,
    "Transaction Description": 1,
    "Currency": 2,
    "Amount": 3,
    "To Currency": 4,
    "To Amount": 5,
    "Native Currency": 6,
    "Native Amount": 7,
    "Native Amount (in USD)": 8,
    "Transaction Kind": 9
}

try:
    crypto_transactions_file = sys.argv[1]
    fiat_transactions_file = sys.argv[2]
except Exception as e:
    print("Please provide both crypto and fiat transaction files as arguments")
    print("Example: python3 calculateSells.py <crypto_file.csv> <fiat_file.csv>")


# Init objects to track crypto and fiat transactions
# We want Timestamp, Amount, To Currency, Transaction Description (e.g., "CRYPTO-> USD", "CRYPTO -> USDT"), and Native Amount. We can ignore all others
# Our map will convert the above names to Date Acquired, Property Description (Amount + To Currency), Amount
crypto_transactions = {}
fiat_transactions = {}
csv_content = []

# Let's start with crypto transactions
with open('crypto-transactions.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        csv_content.append(row)

# Iterate csv_content and filter Buy Orders
# We want to skip the 1st row cause it contains the column headers
for record in csv_content[1:len(csv_content)]:
    if "-> USD" in record[columns["Transaction Description"]]:
        txid = "txid: {}".format(str(csv_content.index(record)))
        crypto_transactions[txid] = {}
        crypto_transactions[txid]["Date Acquired"] = record[columns["Timestamp"]]
        if record[columns["To Currency"]] != "":
            crypto_transactions[txid]["Property Description"] = record[columns["Amount"]] + " " + record[columns["To Currency"]]
        else:
            crypto_transactions[txid]["Property Description"] = record[columns["Amount"]] + " " + record[columns["Currency"]]
        crypto_transactions[txid]["Amount (USD)"] = float(record[columns["Native Amount"]])
    elif "-> USDT" in record[columns["Transaction Description"]]:
        txid = "txid: {}".format(str(csv_content.index(record)))
        crypto_transactions[txid] = {}
        crypto_transactions[txid]["Date Acquired"] = record[columns["Timestamp"]]
        if record[columns["To Currency"]] != "":
            crypto_transactions[txid]["Property Description"] = record[columns["Amount"]] + " " + record[columns["To Currency"]]
        else:
            crypto_transactions[txid]["Property Description"] = record[columns["Amount"]] + " " + record[columns["Currency"]]
        crypto_transactions[txid]["Amount (USD)"] = float(record[columns["Native Amount"]])

# Repeat for fiat transactions
with open('fiat-transactions.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        csv_content.append(row)

for record in csv_content[1:len(csv_content)]:
    if "-> USD" in record[columns["Transaction Description"]]:
        txid = "txid: {}".format(str(csv_content.index(record)))
        fiat_transactions[txid] = {}
        fiat_transactions[txid]["Date Acquired"] = record[columns["Timestamp"]]
        if record[columns["To Currency"]] != "":
            fiat_transactions[txid]["Property Description"] = record[columns["Amount"]] + " " + record[columns["To Currency"]]
        else:
            fiat_transactions[txid]["Property Description"] = record[columns["Amount"]] + " " + record[columns["Currency"]]
        fiat_transactions[txid]["Amount (USD)"] = float(record[columns["Native Amount"]])
    elif "-> USDT" in record[columns["Transaction Description"]]:
        txid = "txid: {}".format(str(csv_content.index(record)))
        fiat_transactions[txid] = {}
        fiat_transactions[txid]["Date Acquired"] = record[columns["Timestamp"]]
        if record[columns["To Currency"]] != "":
            fiat_transactions[txid]["Property Description"] = record[columns["Amount"]] + " " + record[columns["To Currency"]]
        else:
            fiat_transactions[txid]["Property Description"] = record[columns["Amount"]] + " " + record[columns["Currency"]]
        fiat_transactions[txid]["Amount (USD)"] = float(record[columns["Native Amount"]])

# Function for calculating total
def calculateTotal():
    total = 0

    for transactions in crypto_transactions.values():
        total += transactions["Amount (USD)"]

    for transactions in fiat_transactions.values():
        total += transactions["Amount (USD)"]

    return abs(total)

# Create new csv for all buy orders
with open('sells/cryptoComSells.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    # Begin by establishing the column headers ["Date Acquired", "Property Description", "Amount (USD)"]
    writer.writerow(["Date Acquired", "Property Description", "Amount (USD)"])
    for transaction in crypto_transactions.values():
        writer.writerow([transaction["Date Acquired"], transaction["Property Description"].replace("-", ""), abs(transaction["Amount (USD)"])])
    for transaction in fiat_transactions.values():
        writer.writerow([transaction["Date Acquired"], transaction["Property Description"].replace("-", ""), abs(transaction["Amount (USD)"])])
    writer.writerow(["  ", "  Total", calculateTotal()])
