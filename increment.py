import random
import string

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from sh import sh as shell


def run(cmd):
    "A wrapper for running commands"

    print("command:")
    print(cmd)                 # <-- runs
    result = shell("-c", cmd)  # <-- starts but doesn't finish
    print("result:")           # <-- doesn't run
    print(result)
    return result


def get_task(delay):

    @task(task_id=str(delay).replace('.','_'))
    def wait():
        pod_name = "".join(random.choice(string.ascii_letters) for i in range(7)).lower()
        run(f"kubectl run {pod_name} --rm -n freezebug --restart=Never -i --image=bash -- sleep {delay}")

    return wait()

@dag(
    schedule_interval=None,
    start_date=days_ago(1),
    default_args={"owner": "airflow"},
    catchup=False,
)
def increment():

    # create successively longer tasks
    prev_task = get_task(0)
    for i in range(1, 20):
        current_task = get_task(i / 10)
        prev_task >> current_task
        prev_task = current_task


incr = increment()
