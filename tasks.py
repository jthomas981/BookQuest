# your_app/tasks.py

from background_task import background
import requests
import datetime

@background(schedule=30)  # Schedule this task to run every 30 seconds
def reload_website():
    url = 'https://bookquest-h8cl.onrender.com/' 
    try:
        response = requests.get(url)
        print(f'Reloaded at {datetime.datetime.now()}: Status Code {response.status_code}')
    except Exception as e:
        print(f'Error reloading at {datetime.datetime.now()}: {e}')
