# Install Historic-Crypto
# Documentation: https://pypi.org/project/Historic-Crypto/
# pip install Historic-Crypto

from Historic_Crypto import HistoricalData
from Historic_Crypto import Cryptocurrencies
from Historic_Crypto import LiveCryptoData

Cryptocurrencies().find_crypto_pairs()

data = Cryptocurrencies(coin_search = 'BTC', extended_output=False).find_crypto_pairs()

new = HistoricalData('BTC-USD',300,'2021-11-01-00-00', '2021-11-30-00-00').retrieve_data()

print(new)

# Converting to CSV File
bitcoinCSV = new.to_csv('BitcoinData_CSV_V1.csv')

# Converting to JSON File
# bitcoinJson = new.to_json('BitcoinData_JSON_V1.json')