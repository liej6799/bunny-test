
from bunnybackend.backends.postgres import RefreshVideoLibraryPostgres, TargetPostgres
from bunnybackend.common.flow import _load
from prefect import task, flow, get_run_logger
import asyncio
from prefect.task_runners import ConcurrentTaskRunner

from bunnybackend.common.flow import *

@task
def get_database():
    return [(RefreshVideoLibraryPostgres(TargetPostgres()), REFRESH_VIDEO_LIBRARY)]

@flow(task_runner=ConcurrentTaskRunner())
async def flow(exchanges):
    id = REFRESH_VIDEO_LIBRARY
    exchanges = get_all_exhanges(init_paramteter(exchanges))

    feeds = get_feeds(exchanges)
    db_conns = get_database.submit()
    conns = get_conn(feeds, id)         
    extract = get_extract(conns)
    transform = get_transform(extract, id)
    get_load(prepare_load(transform, db_conns))

if __name__ == '__main__':
    asyncio.run(flow("BUNNY"))

