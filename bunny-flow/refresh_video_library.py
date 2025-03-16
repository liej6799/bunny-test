
from bunnybackend.backends.postgres import RefreshVideoLibraryPostgres, TargetPostgres
from bunnybackend.common.flow import _load
from prefect import task, flow, get_run_logger
import asyncio
import prefect
from prefect.task_runners import ConcurrentTaskRunner

from bunnybackend.common.flow import *

@task
def get_database():
    return [(RefreshVideoLibraryPostgres(TargetPostgres()), REFRESH_VIDEO_LIBRARY)]

@flow(task_runner=ConcurrentTaskRunner())
async def flow(exchanges):
    flow_name = REFRESH_VIDEO_LIBRARY
    flow_id = prefect.context.get_run_context().flow_run.dict().get('id')
    start_flow.submit(flow_id, flow_name)

    exchanges = get_all_exhanges(init_paramteter(exchanges))
    feeds = get_feeds_empty(exchanges, flow={'flow_id':flow_id, 'flow_name':flow_name}) 
    db_conns = get_database.submit()
    conns = get_conn(feeds, flow_name)         
    extract = get_extract(conns)
    transform = get_transform(extract, flow_name)
    get_load(prepare_load(transform, db_conns))

    

    end_flow(flow_id, flow_name)

if __name__ == '__main__':
    asyncio.run(flow("BUNNY"))

