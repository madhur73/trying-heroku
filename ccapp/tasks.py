from celery import shared_task
from .prices import Prices
from django.core.cache import cache
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from ccticker.celery import app
'''
@shared_task
def example_task():
    import logging
    k = Kraken(KRAKEN_URL)
    b = Binnance(BINNANCE_URL)
    logging.info(k.get_btc_prices())
    logging.info(b.get_btc_prices())
'''
@shared_task
def update_cc_prices():
	prices_obj 	= Prices()
	cryptocoins = ['ETH', 'BTC']
	sources		= ['BIN','KRA']
	response 	= prices_obj.get_current_prices(cryptocoins, sources)
	channel_layer = get_channel_layer()
	for cryptocoin in cryptocoins:
		for source in sources:
			latest_price = response[cryptocoin][source]
			ticker_code = cryptocoin + source
			if cache.get(ticker_code) != latest_price:
				cache.set(ticker_code, response[cryptocoin][source])
				async_to_sync(channel_layer.group_send)(
					ticker_code,
					{
						'type': 'price_update',
						'price': latest_price,
					}
				)
@app.task(name='celery.ping')
def ping():
    # type: () -> str
    """Simple task that just returns 'pong'."""
    return 'pong'