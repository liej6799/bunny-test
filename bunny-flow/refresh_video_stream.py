
from datetime import timedelta
from bunnybackend.backends.postgres import RefreshVideoPostgres, RefreshVideoStreamPostgres, TargetPostgres, VideoLibraryPostgres, VideoPostgres
from bunnybackend.common.flow import _load
from bunnybackend.common.transform import escape_string
from bunnybackend.types import VideoAPI
from prefect import task, flow, get_run_logger
import asyncio
import prefect
from prefect.task_runners import ConcurrentTaskRunner

from bunnybackend.common.flow import *
from prefect.cache_policies import TASK_SOURCE


@task
def get_database():
    return [(RefreshVideoStreamPostgres(TargetPostgres()), REFRESH_VIDEO_STREAM),
            (VideoPostgres(TargetPostgres()), VIDEO)]


@flow(task_runner=ConcurrentTaskRunner())
async def flow(exchanges):
    flow_name = REFRESH_VIDEO_STREAM
    flow_id = prefect.context.get_run_context().flow_run.dict().get('id')
    start_flow.submit(flow_id, flow_name)

    db_conns = get_database.submit()
    e_res_1 =  get_extract_database([conn for conn in db_conns.result() if conn[1] in [VIDEO]])


    tr_res = [transform([ex.result() for ex in e_res_1 if ex.result()], types)
            for types in [VIDEO]]
    
    video_id = [a[0][0].id for a in tr_res][0]
    library_id = [a[0][0].video_library_id for a in tr_res][0]

    print(video_id, library_id)
    exchanges = get_all_exhanges(init_paramteter(exchanges))
    feeds = get_feeds(exchanges,  {'flow_id':flow_id, 'flow_name':flow_name, 'payload': {'library_id': library_id, 'video_id': video_id}}) 
    conns = get_conn(feeds, flow_name)         
    extract = get_extract(conns)
    transform_data = get_transform(extract, flow_name)
    
    get_load(prepare_load(transform_data, db_conns))

    end_flow(flow_id, flow_name)

@task(cache_policy=TASK_SOURCE)
def transform(data, type):
    if type == VIDEO:
        return transform_video(data), type
 
def transform_video(msg):
    return list(set([VideoAPI(id=(j['id']), video_library_id=(j['video_library_id'])) for i in msg if i[1] == VIDEO for j in i[0]]))

if __name__ == '__main__':
    asyncio.run(flow("BUNNY"))

