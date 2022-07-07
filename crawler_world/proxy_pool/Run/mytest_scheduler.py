from apscheduler.schedulers.background import BackgroundScheduler
import time


def job1():
    print('job1...')


def job2():
    print('job2...')


scheduler = BackgroundScheduler()
scheduler.add_job(job1, 'interval', minutes=30, id="fetch_proxy")
scheduler.add_job(job2, "interval", minutes=1)  # 每分钟检查一次
scheduler.start()

while True:
    time.sleep(5)
