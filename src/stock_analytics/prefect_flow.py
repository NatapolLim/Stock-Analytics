from prefect import flow, task, get_run_logger
from prefect.context import get_run_context
import time

from stock_analytics.prefect_flows.test_flow_1 import flow_1
from stock_analytics.prefect_flows.test_flow_2 import flow_2

if __name__=='__main__':
    flow_1.serve(name='test_flow_1', cron='*/1 * * * *', tags=['flow1'])
    flow_2.serve(name='test_flow_2', cron='*/1 * * * *', tags=['flow2'], parameters={"input": "wowo from in put"})