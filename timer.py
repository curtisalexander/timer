from collections import deque
from datetime import datetime
from datetime import timedelta

import argparse
import sys
import time


def countdown(timer, end):
    next_time = timer.popleft()

    while timer:
        diff = (next_time - datetime.now()).total_seconds()
        if diff <= 0:
            mins, secs = divmod((end - next_time).total_seconds(), 60)
            timeformat = f"{int(mins):02d}:{int(secs):02d} remaining"
            print(timeformat, end="\r")
            sys.stdout.flush()

            next_time = timer.popleft()
        else:
            # sliding scale for sleeping
            # based on an idea from the pause package
            # https://pypi.python.org/pypi/pause
            if diff <= 0.1:
                time.sleep(0.001)
            elif diff <= 0.5:
                time.sleep(0.01)
            elif diff <= 1.5:
                time.sleep(0.1)
            else:
                time.sleep(1)

    time.sleep(1)
    now_display = datetime.now().time().strftime("%H:%M:%S")
    print(f"\n\nGoodbye!  The time is now {now_display}\n\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Timer")
    parser.add_argument("-t", "--timer", help="Timer duration", required=True, type=int)
    parser.add_argument(
        "-u",
        "--unit",
        help="Unit (seconds or minutes)",
        required=True,
        choices=["seconds", "minutes"],
    )
    args = parser.parse_args()

    # how long will the timer last?
    if args.unit == "seconds":
        timer_seconds = args.timer
    else:
        timer_seconds = args.timer * 60

    start = datetime.now() + timedelta(seconds=2)
    start_display = start.time().strftime("%H:%M:%S")
    interval = timedelta(seconds=timer_seconds)
    end = start + interval
    end_display = end.time().strftime("%H:%M:%S")

    print(f"Start time is {start_display}")
    print(f"End time is {end_display}\n")

    print("---------")
    print("| Timer |")
    print("---------\n")

    timer = deque()
    for s in range((interval.seconds + 1)):
        timer.append(start + timedelta(seconds=(s)))

    countdown(timer, end)
