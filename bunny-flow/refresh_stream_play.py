
from bunnybackend.backends.postgres import RefreshVideoLibraryPostgres, TargetPostgres
from bunnybackend.backends.stream import DemoStream
from bunnybackend.common.flow import _load
from prefect import task, flow, get_run_logger
from bunnybackend.types import PlayerModel
import asyncio
import prefect
from bunnybackend.defines import *
from prefect.task_runners import ConcurrentTaskRunner

from bunnybackend.common.flow import *

@task
def get_stream():
    return [(DemoStream(), STREAM_PLAY)]

@flow(task_runner=ConcurrentTaskRunner())
def flow(exchanges):
    flow_name = REFRESH_STREAM_PLAY
    flow_id = prefect.context.get_run_context().flow_run.dict().get('id')
    # start_flow.submit(flow_id, flow_name)


    exchanges = get_all_exhanges(init_paramteter(exchanges))
    e_res_1 = [{''},{}]

    db_conns = get_stream.submit()
    e_res_1 =  get_extract_database([conn for conn in db_conns.result() if conn[1] in [STREAM_PLAY]])


    tr_res = [transform([ex.result() for ex in e_res_1 if ex.result()], types)
        for types in [STREAM_PLAY]]
    

    feeds = get_feeds(exchanges, payloads=tr_res, flow={'flow_id':flow_id, 'flow_name':flow_name}) 
    
    conns = get_conn(feeds, flow_name)         
    extract = get_extract(conns)
    for i in extract:
        if i.result():
            print(i.result())

    # transform = get_transform(extract, flow_name)
  
    # get_load(prepare_load(transform, db_conns))

@task
def transform(data, type):
    if type == STREAM_PLAY:
        return transform_stream(data), type

def transform_stream(msg):

    return list(set([PlayerModel(stream=(j['STREAM']), browser=(j['BROWSER'])) for i in msg if i[1] == STREAM_PLAY for j in i[0]]))

if __name__ == '__main__':
    (flow("VIDEOJS"))

