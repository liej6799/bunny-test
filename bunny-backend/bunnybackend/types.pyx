'''
Copyright (C) 2017-2023 Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''
cimport cython
from decimal import Decimal

cdef extern from *:
    """
    #ifdef CYTHON_WITHOUT_ASSERTIONS
    #define _COMPILED_WITH_ASSERTIONS 0
    #else
    #define _COMPILED_WITH_ASSERTIONS 1
    #endif
    """
    cdef bint _COMPILED_WITH_ASSERTIONS
COMPILED_WITH_ASSERTIONS = _COMPILED_WITH_ASSERTIONS

cdef dict convert_none_values(d: dict, s: str):
    for key, value in d.items():
        if value is None:
            d[key] = s
    return d



cdef class RefreshVideoLibrary:
    # common
    cdef readonly object id
    cdef readonly object flow_id
    cdef readonly object name
    cdef readonly object video_count

    cdef readonly object traffic_usage
    cdef readonly object storage_usage

    cdef readonly object date_created

    cdef readonly object timestamp
    cdef readonly object raw

    def __init__(self, id, flow_id, name, video_count, traffic_usage, storage_usage, date_created, timestamp, raw=None):

        self.id = id
        self.flow_id = flow_id
        self.name = name
        self.video_count = video_count
        self.traffic_usage = traffic_usage

        self.storage_usage = storage_usage
        self.date_created = date_created

        self.timestamp = timestamp
        self.raw = raw

    @staticmethod
    def from_dict(data: dict) -> RefreshVideoLibrary:
        return RefreshVideoLibrary(
            data['id'],
            data['flow_id'],
            data['name'],
            data['video_count'],
            data['traffic_usage'],

            data['storage_usage'],
            data['date_created'],
            data['timestamp']
        )

    cpdef dict to_dict(self, numeric_type=None, none_to=False):
        if numeric_type is None:
            data = {'id': self.id, 'flow_id': self.flow_id, 'name': self.name, 'video_count': self.video_count, 'traffic_usage': self.traffic_usage, 'storage_usage': self.storage_usage, 'date_created': self.date_created, 'timestamp': self.timestamp}
        else:
            data = {'id': self.id, 'flow_id': self.flow_id, 'name': self.name, 'video_count': self.video_count, 'traffic_usage': self.traffic_usage, 'storage_usage': self.storage_usage, 'date_created': self.date_created, 'timestamp': self.timestamp}

        return data if not none_to else convert_none_values(data, none_to)

    def __repr__(self):
        return f"id: {self.id} flow_id: {self.flow_id} name: {self.name} video_count: {self.video_count} traffic_usage: {self.traffic_usage} storage_usage: {self.storage_usage} date_created: {self.date_created}  timestamp: {self.timestamp}"

    def __eq__(self, cmp):
        return self.id == cmp.id and self.flow_id == cmp.flow_id and self.name == cmp.name and self.video_count == cmp.video_count and self.traffic_usage == cmp.traffic_usage and self.storage_usage == cmp.storage_usage and self.date_created == cmp.date_created and self.timestamp == cmp.timestamp

    def __hash__(self):
        return hash(self.__repr__())



cdef class Flow:
    # common
    cdef readonly object flow_name
    cdef readonly object flow_id
    cdef readonly object status
    cdef readonly object timestamp

    def __init__(self, flow_name, flow_id, status, timestamp):
        self.flow_name = flow_name
        self.flow_id = flow_id
        self.status = status
        self.timestamp = timestamp


    @staticmethod
    def from_dict(data: dict) -> RefreshVideoLibrary:
        return RefreshVideoLibrary(
            data['flow_name'],
            data['flow_id'],
            data['status'],
            data['timestamp'],
        )

    cpdef dict to_dict(self, numeric_type=None, none_to=False):
        if numeric_type is None:
            data = {'flow_name': self.flow_name, 'flow_id': self.flow_id, 'status': self.status, 'timestamp': self.timestamp }
        else:
            data = {'flow_name': self.flow_name, 'flow_id': self.flow_id, 'status': self.status, 'timestamp': self.timestamp }

        return data if not none_to else convert_none_values(data, none_to)

    def __repr__(self):
        return f"flow_name: {self.flow_name} flow_id: {self.flow_id} status: {self.status} timestamp: {self.timestamp} "

    def __eq__(self, cmp):
        return self.flow_name == cmp.flow_name and self.flow_id == cmp.flow_id and self.status == cmp.status and self.timestamp == cmp.timestamp

    def __hash__(self):
        return hash(self.__repr__())
 