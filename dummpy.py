from time import sleep
from threading import Event
from concurrent.futures import ThreadPoolExecutor

# mock target task function
def work(event):
    # pretend read data for a long time
    for _ in range(10):
        # pretend to read some data
        sleep(1)
        # check if the task should stop
        if event.is_set():
            return

# create an event used to stop running tasks
event = Event()
# create a thread pool
with ThreadPoolExecutor() as executor:
    # execute one task
    future = executor.submit(work, event)
    # wait a moment
    print('The task is running...')
    sleep(2)
    # cancel the task, just in case it is not yet running
    future.cancel()
    # stop the running task using the flag
    print('Stopping the task...')
    event.set()
    # waiting for all tasks to complete
    print('Waiting...')
print('All done.')