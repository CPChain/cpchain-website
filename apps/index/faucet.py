import schedule
from . import views

# schedule.every().day.do(Faucet.update())
schedule.every(10).seconds.do(views.Faucet.update())

while True:
    schedule.run_pending()
