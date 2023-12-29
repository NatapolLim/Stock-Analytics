from prefect import flow, task, get_run_logger
from prefect.context import get_run_context
import time

@task
def task_1(input: str) -> str:
    time.sleep(1)
    return input*2

@task
def task_2(input: str) -> str:
    time.sleep(1)
    return input[:3]

@flow(name='Test_flow', log_prints=True)
def flow_1(input: str='Hello World'):

    out1 = task_1(input)
    print(out1)

    out2 = task_2(out1)
    print(out2)

if __name__ == "__main__":
    # flow_1.serve(name='test_flow_1', cron='*/1 * * * *')
    flow_1("woprwjefopjwdg")