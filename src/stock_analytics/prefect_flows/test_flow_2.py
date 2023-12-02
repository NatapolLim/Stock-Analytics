from prefect import flow, task, get_run_logger
from prefect.context import get_run_context
import time

@task(tags=['task1'])
def task_1(input: str) -> str:
    time.sleep(2)
    return input*2

@task(tags=["task2"])
def task_2(input: str) -> str:
    time.sleep(2)
    return input[:3]

@flow(name='Test_flow_2', log_prints=True, flow_run_name="run_flow2")
def flow_2(input: str='YOYO flow 2'):
    context = get_run_context()
    print('Context', context.flow_run, context.flow_run_states)

    out1 = task_1(input)
    print(out1)

    out2 = task_2(out1)
    print(out2)

if __name__ == "__main__":
    flow_2.serve(name='test_flow_2', cron='*/1 * * * *', tags=['flow2'], parameters={"input": "wowo from in put"})