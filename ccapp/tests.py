from django.test import TestCase,TransactionTestCase
from .tasks import *
from .prices import *
from django.core.cache import cache
from celery.contrib.testing.worker import start_worker
from ccticker.celery import app
# Create your tests here.
from django.test import SimpleTestCase

import pytest
from channels.testing import HttpCommunicator
from .consumers import TickerConsumer

@pytest.mark.asyncio
async def test_my_consumer():
    communicator = HttpCommunicator(TickerConsumer, "GET", "/test/")
    response = await communicator.get_response()
    self.assertEqual(response["body"] , b"test response")
    self.assertEqual(response["status"],200)

class ProjectTests(TestCase):

    def test_homepage(self):
        response = self.client.get('/tickers/')
        self.assertEqual(response.status_code, 200)

    def test_binance_api(self):
    	b = Binance('https://api.binance.com/api/v3/ticker/bookTicker')
    	resp = b.get_data('BTCUSDT')
    	self.assertTrue(resp)
    	resp = b.get_data('ETHUSDT')
    	self.assertTrue(resp)

    def test_kraken_api(self):
    	b = Kraken('https://api.kraken.com/0/public/Ticker')
    	resp = b.get_data('XXBTZUSD')
    	self.assertTrue(resp)
    	resp = b.get_data('XETHZUSD')
    	self.assertTrue(resp)

    def test_redis_cache(self):
    	cache.set("test", 1)
    	self.assertEqual(cache.get("test"),1)



class UpdatePricesTaskTestCase(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.celery_worker = start_worker(app)
        cls.celery_worker.__enter__()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.celery_worker.__exit__(None, None, None)
    def setUp(self):
        super().setUp()
        self.task = update_cc_prices.delay() # whatever your method and args are
        self.results = self.task.get()
    def test_success(self):
        assert self.task.state == "SUCCESS"


