import schedule
import time
import json
import threading
from utilities import utils
from utilities.wordle_cheat import save_user_data


def run_continuously(interval=30):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def reset_wordle_counts():
    print("resetting daily wordle attempts!")
    with open("wordle_user_data.json") as f:
        user_data = json.load(f)

    for user in user_data:
        user_data[user] = 0

    # Save the reset data back to file
    save_user_data()


def increment_booba():
    utils.days_since_booba += 1


async def start_scheduled_tasks():
    print("scheduling tasks...")
    stop_run_continuously = run_continuously()


schedule.every().day.at("00:00").do(reset_wordle_counts)
schedule.every().day.at("00:00").do(increment_booba)
