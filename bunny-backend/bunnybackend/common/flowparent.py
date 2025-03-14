
from bunnybackend.common.flow import get_all_exhanges, get_feeds, init_paramteter
from bunnybackend.defines import FLOW
from prefect import task, flow, get_run_logger
from prefect.task_runners import ConcurrentTaskRunner


class FlowParent:
    @flow(task_runner=ConcurrentTaskRunner())
    def __init__ (self, exchanges):
        self.flow_id = 'awd'
        self.exchanges = exchanges
