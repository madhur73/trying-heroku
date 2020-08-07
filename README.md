<h1>Welcome to CryptoCoin Ticker!!!</h1>
You can view live version [here](https://intense-shelf-05236.herokuapp.com/tickers/)
<h3>How to run locally </h3>
* Configure your redis-server properly with version >=5, use [this](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04) for ubuntu.

* Run `pipenv install --skip-lock` to set up an environment with required dependencies
* Run `pipenv shell` to activate the environment in your shell
- Run `cd ccticker/`, `./manage.py migrate`, `./manage.py createsuperuser`,` ./manage.py runserver`
- Go to `http://localhost:8000/admin/django_celery_beat/periodictask/add/ and schedule ccapp.tasks.update_cc_prices` to run every ten seconds
- Open another tab in terminal activate the envrionment using `pipenv shell` 
- Run `cd ccticker/`, and run `celery -A ccticker worker -l info`
- Run `cd ccticker/` Open another tab with environment activated and run `celery -A ccticker beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler`
- Go to http://localhost:8000/tickers


Components used:
- Django
    - celery
    - WebSockets(ASGI)
    - channels
- Redis >= 5.0
- Heroku

<h2> System Design</h2>>
[](images/websocket-archi.png?raw=true)

