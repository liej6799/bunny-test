
from bunnybackend.defines import *
from prefect import task, flow, get_run_logger

from bunnybackend.exchanges import Bunny


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
def _initiate(exchange):
 
    if exchange == BUNNY:
        return Bunny(config='config.yaml')

@task
def _initiate_connection(feed, type):
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
    await conn[0].write(data)

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


def get_feeds(exchanges):
    return [_initiate.submit(exchange) for exchange in exchanges]


def get_conn(feeds, type):

    return [_initiate_connection.submit(feed.result(), type) for feed in feeds]


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


async def get_extract_database(conns, wait=None):
    return [await _extract_database.submit(conn, wait_for=wait) for conn in conns]

async def get_refresh(conns):
    return [await _refresh.submit(conn) for conn in conns]