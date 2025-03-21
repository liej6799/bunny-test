
from datetime import time
from bunnybackend.backends.postgres import FlowPostgres, TargetPostgres
from bunnybackend.defines import *
from bunnybackend.exchanges.common import Common
from bunnybackend.exchanges.hls import Hls
from bunnybackend.exchanges.videojs import VideoJS
from prefect import task, flow, get_run_logger
from bunnybackend.types import Flow
from bunnybackend.exchanges import Bunny
from prefect.task_runners import ConcurrentTaskRunner

def is_exchange_valid(exchanges):
    if [exchange for exchange in exchanges if exchange not in EXCHANGES_LIST]:
        return


def get_all_exhanges(exchanges):
    if exchanges == [ALL_EXCHANGES]:
        return EXCHANGES_LIST
    return exchanges


def has_method(o, name):
    return callable(getattr(o, name, None))

@task
def get_start_flow_database():
    return [(FlowPostgres(TargetPostgres()), START_FLOW)]

@task
def get_end_flow_database():
    return [(FlowPostgres(TargetPostgres()), END_FLOW)]

  

@task
def _initiate(exchange, payload, flow):
    if exchange == BUNNY:
        return Bunny(config='config.yaml',payload=payload,flow=flow)
    elif exchange == FLOW:
        return Common(config='config.yaml',payload=payload,flow=flow)
    elif exchange == VIDEOJS:
        return VideoJS(config='config.yaml',payload=payload,flow=flow)
    elif exchange == HLS:
        return Hls(config='config.yaml',payload=payload,flow=flow)

@task
def _initiate_connection(feed, type):
    print(feed, type)
    try:
        if feed is None:
            return None
        if feed[type] is None:
            return None
        return feed[type](), feed
    except AttributeError:
        return None


@task(retries=2, retry_delay_seconds=5)
def _extract(feed, method):
    return feed[method](), method, feed


@task
async def _extract_database(conn):
    return await conn[0].read(), conn[1]

@task
def _transform(feed, method, data, table):
    return feed.message_handler(method, data), table

@task
async def _load(conn, data):
    return await conn[0].write(data)

@task
async def _load_empty(conn):
    await conn[0].write_empty()

@task
async def _refresh(conn):
    await conn[0].refresh()

@task
async def _delete(conn, data):
    await conn[0].delete(data)


def init_paramteter(data):
    # need to convert to array
    if type(data) == str:
        return [data]
    return data

@task
def start_flow(flow_id, flow_name):
    db_conns = get_start_flow_database.submit()
    exchanges = get_all_exhanges(init_paramteter(FLOW))
    feeds = get_feeds_empty(exchanges, flow={'flow_id':flow_id, 'flow_name':flow_name})
    conns = get_conn(feeds, START_FLOW)         
    extract = get_extract(conns)
    transform = get_transform(extract, START_FLOW)
    get_load(prepare_load(transform, db_conns))

@task
def end_flow(flow_id, flow_name):
    db_conns = get_end_flow_database.submit()
    exchanges = get_all_exhanges(init_paramteter(FLOW))
    feeds = get_feeds_empty(exchanges, flow={'flow_id':flow_id, 'flow_name':flow_name})
    conns = get_conn(feeds, END_FLOW)         
    extract = get_extract(conns)
    transform = get_transform(extract, END_FLOW)
    get_load(prepare_load(transform, db_conns))


def get_feeds(exchanges, flow, payloads):

    return [_initiate.submit(exchange, x, flow) for exchange in exchanges for payload in payloads for x in payload[0]]


def get_feeds_empty(exchanges, flow):

    return [_initiate.submit(exchange, None, flow) for exchange in exchanges]


def get_conn(feeds, type):

    return [_initiate_connection.submit(feed.result(), type) for feed in feeds]


# @flow(task_runner=ConcurrentTaskRunner())
# def get_extract(conns):
#     run_tasks = [run.submit(*task) for task in batch]
#     results = []
#     for run_task in run_tasks:
#         results.append(run_task.result())
#     return results


def get_extract(conns):
    return [_extract.submit(conn.result()[1], method)
            for conn in conns if conn.result() is not None for method in conn.result()[0]]



def get_transform(extract, table):
    return [_transform.submit(e.result()[2], e.result()[1], e.result()[0], table) for e in extract]


def prepare_load(transform, db_conns):
    return [(conn, [res for raw in transform if raw.result() is not None if raw.result()[0] is not None if raw.result()[1] == conn[1] for res in raw.result()[0]])
            for conn in db_conns.result()]

def prepare_load_empty(db_conns):
    return [(conn, [{}]) for conn in db_conns.result()]

def prepare_refresh(db_conns):
    return [conn for conn in db_conns.result()]

def get_load(conns):
    return [_load.submit(conn[0], conn[1]) for conn in conns if conn[1] != []]

async def get_load_empty(conns):
    return [await _load_empty.submit(conn[0]) for conn in conns]


async def get_delete(conns, wait=None):
    return [await _delete.submit(conn[0], conn[1], wait_for=wait) for conn in conns if conn[1] != []]


def get_extract_database(conns, wait=None):
    return [_extract_database.submit(conn, wait_for=wait) for conn in conns]

async def get_refresh(conns):
    return [await _refresh.submit(conn) for conn in conns]