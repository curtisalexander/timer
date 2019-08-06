from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from datetime import timedelta

import argparse
import queue
import random
import time


def print_saying(count, saying):
    """ Just prints a saying - nothing more and nothing less.

    Parameters
    ----------
    count : count of printed saying

    saying : saying to print
    """
    now = datetime.now().time().strftime("%H:%M:%S")
    print(f"{count}: The time is now {now} ==> {saying}\n")


def process_queue(q, pool, func):
    """ Process a priority queue based on time

    The priority within the queue is the time at which the item can execute.

    Continually poll the queue, popping an item only when the current time is
    greater than the time at which the item is permitted to execute.

    Parameters
    ----------
    q : an instance of a priority queue

    pool : a thread pool

    func : the function to be executed by a thread in the threadpool

    Returns
    -------
    null
    """

    # get first item in the queue
    priority, count, saying = q.get()

    while True:
        diff = (priority - datetime.now()).total_seconds()

        if diff <= 0:
            pool.submit(func, (count + 1), saying)

            try:
                priority, count, saying = q.get(timeout=5.0)
            except queue.Empty:
                print("All done!  Congratulations on finishing!")
                break

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


def main(t_duration, s_duration, sayings):
    # start
    start = datetime.now() + timedelta(seconds=5)
    timer = timedelta(seconds=t_duration)

    print("Starting in 5 seconds...\n")

    # priority queue instance
    q = queue.PriorityQueue()

    # build up the priority queue
    for i in range((timer.seconds // s_duration) + 1):
        next_time = start + timedelta(seconds=(i * s_duration))
        q.put((next_time, i, random.choice(sayings)))

    # process the queue
    with ThreadPoolExecutor(max_workers=3) as pool:
        process_queue(q, pool, print_saying)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Timer")

    parser.add_argument(
        "-t", "--timer", help="Overall timer duration in minutes", type=int
    )

    parser.add_argument("-s", "--sayings", help="Sayings duration in minutes", type=int)

    args = parser.parse_args()

    # how long will the timer last?
    timer_duration_seconds = args.timer

    # how many seconds will elapse until printing encouragement
    sayings_duration_seconds = args.sayings

    # list of encouraging sayings
    sayings = [
        "Keep it up!",
        "Just a little bit longer.",
        "Focus, focus, focus!",
        "Wow, you are accomplishing so much!",
    ]

    main(timer_duration_seconds, sayings_duration_seconds, sayings)
