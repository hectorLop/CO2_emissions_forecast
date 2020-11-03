from flask import Flask
from source.data_collector.data_collector import DataCollector
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
data_collector = DataCollector()

@app.route("/")
def hello_world() -> str:
    return 'Hello this is the data colletor API!'

@app.route('/update_db')
def update_db() -> str:
    """
    Update the database to keep it up to date
    """
    print("UPDATING DATABASE")
    data_collector.collect_outdated_data()

    return 'OK'

def collect_data() -> str:
    """
    Collects emissions data
    """
    print('Collecting data...')
    data_collector.collect_data()

    return 'OK'

def schedule_data_collection() -> None:
    """
    Schedule a job to collect emissions data each 6 hours
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=collect_data, trigger='interval', minutes=360)
    scheduler.start()

    print('SCHEDULER created')

if __name__ == '__main__':
    app.run(host='localhost', port=8000)
    schedule_data_collection()