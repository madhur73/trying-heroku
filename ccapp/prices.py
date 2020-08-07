import requests

BINNANCE_URL = 'https://api.binance.com/api/v3/ticker/bookTicker'
KRAKEN_URL = 'https://api.kraken.com/0/public/Ticker'

class Prices():

	def get_current_prices(self, cryptocoins, sources):
		prices = dict()
		kraken_obj = Kraken(KRAKEN_URL)
		binance_obj = Binance(BINNANCE_URL)
		for cryptocoin in cryptocoins:
			prices[cryptocoin] = dict()
			for source in sources:
				if source == "BIN":
					if cryptocoin == "BTC":
						prices[cryptocoin][source] = binance_obj.get_btc_prices()
					else:
						prices[cryptocoin][source] = binance_obj.get_eth_prices()
				else:
					if cryptocoin == "BTC":
						prices[cryptocoin][source] = kraken_obj.get_btc_prices()
					else:
						prices[cryptocoin][source] = kraken_obj.get_eth_prices()
		return prices


class Binance():

	def __init__(self, endpoint):
		self.url = endpoint

	def get_buy_price(self, resp):
		return resp['bidPrice']

	def get_sell_price(self, resp):
		return resp['askPrice']

	def get_data(self, symbol):
		resp = requests.get( self._url() + symbol)
		#print(resp.json())
		if resp.status_code != 200:
	    # self means something went wrong.
	 		#raise ApiError('GET /tasks/ {}'.format(resp.status_code))
	 		print("ApiError")

		return resp.json()

	def _url(self):
		return self.url +'?symbol='

	def get_btc_prices(self):
		res = {}
		resp_obj = self.get_data('BTCUSDT')
		res['buy'] = self.get_buy_price(resp_obj)
		res['sell'] = self.get_sell_price(resp_obj)
		return res

	def get_eth_prices(self):
		res = {}
		resp_obj = self.get_data('ETHUSDT')
		res['buy'] = self.get_buy_price(resp_obj)
		res['sell'] = self.get_sell_price(resp_obj)
		return res

class Kraken():

	def __init__(self, endpoint):
		self.url = endpoint

	def get_buy_price(self, resp):
		return resp['a'][0]

	def get_sell_price(self, resp):
		return resp['b'][0]

	def get_data(self, symbol):
		resp = requests.get( self._url() + symbol)
		#print(resp.json())
		if resp.status_code != 200 or (resp.json()['error'] is None):
	    # self means something went wrong.
	 		#raise ApiError('GET /tasks/ {}'.format(resp.status_code))
	 		print("ApiError")

		return resp.json()['result'][symbol]

	def _url(self):
		return self.url +'?pair='

	def get_btc_prices(self):
		res = {}
		resp_obj = self.get_data('XXBTZUSD')
		res['buy'] = self.get_buy_price(resp_obj)
		res['sell'] = self.get_sell_price(resp_obj)
		return res

	def get_eth_prices(self):
		res = {}
		resp_obj = self.get_data('XETHZUSD')
		res['buy'] = self.get_buy_price(resp_obj)
		res['sell'] = self.get_sell_price(resp_obj)
		return res
