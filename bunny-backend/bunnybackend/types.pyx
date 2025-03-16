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

    cdef readonly object api_key
    cdef readonly object read_only_api_key

    cdef readonly object date_created

    cdef readonly object timestamp
    cdef readonly object raw

    def __init__(self, id, flow_id, name, video_count, traffic_usage, storage_usage, date_created, api_key, read_only_api_key, timestamp, raw=None):

        self.id = id
        self.flow_id = flow_id
        self.name = name
        self.video_count = video_count
        self.traffic_usage = traffic_usage

        self.storage_usage = storage_usage
        self.date_created = date_created

        self.api_key = api_key
        self.read_only_api_key = read_only_api_key

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

            data['api_key'],
            data['read_only_api_key'],                        
            data['timestamp']
        )

    cpdef dict to_dict(self, numeric_type=None, none_to=False):
        if numeric_type is None:
            data = {'id': self.id, 'flow_id': self.flow_id, 'name': self.name, 'video_count': self.video_count, 'traffic_usage': self.traffic_usage, 'storage_usage': self.storage_usage, 'date_created': self.date_created, 'api_key': self.api_key, 'read_only_api_key': self.read_only_api_key, 'timestamp': self.timestamp}
        else:
            data = {'id': self.id, 'flow_id': self.flow_id, 'name': self.name, 'video_count': self.video_count, 'traffic_usage': self.traffic_usage, 'storage_usage': self.storage_usage, 'date_created': self.date_created, 'api_key': self.api_key, 'read_only_api_key': self.read_only_api_key, 'timestamp': self.timestamp}

        return data if not none_to else convert_none_values(data, none_to)

    def __repr__(self):
        return f"id: {self.id} flow_id: {self.flow_id} name: {self.name} video_count: {self.video_count} traffic_usage: {self.traffic_usage} storage_usage: {self.storage_usage} date_created: {self.date_created} api_key: {self.api_key} read_only_api_key: {self.read_only_api_key} timestamp: {self.timestamp}"

    def __eq__(self, cmp):
        return self.id == cmp.id and self.flow_id == cmp.flow_id and self.name == cmp.name and self.video_count == cmp.video_count and self.traffic_usage == cmp.traffic_usage and self.storage_usage == cmp.storage_usage and self.date_created == cmp.date_created and self.api_key == cmp.api_key and self.read_only_api_key == cmp.read_only_api_key and self.timestamp == cmp.timestamp

    def __hash__(self):
        return hash(self.__repr__())



cdef class VideoLibraryAPI:
    # common
    cdef readonly object id
    cdef readonly object api_key
    cdef readonly object read_only_api_key

    def __init__(self, id, api_key, read_only_api_key):

        self.id = id
        self.api_key = api_key
        self.read_only_api_key = read_only_api_key

  

    @staticmethod
    def from_dict(data: dict) -> VideoLibraryAPI:
        return VideoLibraryAPI(
            data['id'],

            data['api_key'],
            data['read_only_api_key']                     
  
        )

    cpdef dict to_dict(self, numeric_type=None, none_to=False):
        if numeric_type is None:
            data = {'id': self.id, 'api_key': self.api_key, 'read_only_api_key': self.read_only_api_key }
        else:
            data = {'id': self.id, 'api_key': self.api_key, 'read_only_api_key': self.read_only_api_key }

        return data if not none_to else convert_none_values(data, none_to)

    def __repr__(self):
        return f"id: {self.id} api_key: {self.api_key} read_only_api_key: {self.read_only_api_key}"

    def __eq__(self, cmp):
        return self.id == cmp.id and self.api_key == cmp.api_key and self.read_only_api_key == cmp.read_only_api_key 

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
    def from_dict(data: dict) -> Flow:
        return Flow(
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
 


 

cdef class Video:
    # common
    cdef readonly object id
    cdef readonly object video_library_id
    cdef readonly object flow_id
    cdef readonly object name
    cdef readonly object date_upload
    cdef readonly object views
    cdef readonly object encode_process
    cdef readonly object storage_size

    cdef readonly object timestamp
    cdef readonly object raw

    def __init__(self, id, video_library_id, flow_id, name, date_upload, views, encode_process, storage_size, timestamp, raw=None):
        self.id = id
        self.video_library_id = video_library_id
        self.flow_id = flow_id
        self.name = name
        self.date_upload = date_upload
        self.views = views
        self.encode_process = encode_process
        self.storage_size = storage_size
        self.timestamp = timestamp
        self.raw = raw

    

    @staticmethod
    def from_dict(data: dict) -> Video:
        return Video(
            data['id'],
            data['video_library_id'],
            data['flow_id'],
            data['name'],
            data['date_upload'],
            data['views'],
            data['encode_process'],
            data['storage_size'],
            data['timestamp']            
        )

    cpdef dict to_dict(self, numeric_type=None, none_to=False):
        if numeric_type is None:
            data = {'id': self.id, 'video_library_id': self.video_library_id, 'flow_id': self.flow_id, 'name': self.name, 'date_upload': self.date_upload, 'views': self.views, 'encode_process': self.encode_process, 'storage_size': self.storage_size, 'timestamp': self.timestamp}
        else:
            data = {'id': self.id, 'video_library_id': self.video_library_id, 'flow_id': self.flow_id, 'name': self.name, 'date_upload': self.date_upload, 'views': self.views, 'encode_process': self.encode_process, 'storage_size': self.storage_size, 'timestamp': self.timestamp }

        return data if not none_to else convert_none_values(data, none_to)

    def __repr__(self):
        return f"id: {self.id} video_library_id: {self.video_library_id} flow_id: {self.flow_id} self.name: {self.name} date_upload: {self.date_upload} views: {self.views} encode_process: {self.encode_process} storage_size: {self.storage_size} timestamp: {self.timestamp}"

    def __eq__(self, cmp):
        return self.id == cmp.id and self.video_library_id == cmp.video_library_id and self.flow_id == cmp.flow_id and self.name == cmp.name and self.date_upload == cmp.date_upload and self.views == cmp.views and self.encode_process == cmp.encode_process and self.storage_size == cmp.storage_size and self.timestamp == cmp.timestamp

    def __hash__(self):
        return hash(self.__repr__())




cdef class VideoAPI:
    # common
    cdef readonly object id
    cdef readonly object video_library_id

    def __init__(self, id, video_library_id):

        self.id = id
        self.video_library_id = video_library_id


    @staticmethod
    def from_dict(data: dict) -> VideoAPI:
        return VideoAPI(
            data['id'],
            data['video_library_id']              
        )

    cpdef dict to_dict(self, numeric_type=None, none_to=False):
        if numeric_type is None:
            data = {'id': self.id, 'video_library_id': self.video_library_id }
        else:
            data = {'id': self.id, 'video_library_id': self.video_library_id }

        return data if not none_to else convert_none_values(data, none_to)

    def __repr__(self):
        return f"id: {self.id} video_library_id: {self.video_library_id} "

    def __eq__(self, cmp):
        return self.id == cmp.id and self.video_library_id == cmp.video_library_id

    def __hash__(self):
        return hash(self.__repr__())




cdef class VideoStream:
    # common
    cdef readonly object id
    cdef readonly object video_library_id
    cdef readonly object flow_id

    cdef readonly object captions_path
    cdef readonly object seek_path
    cdef readonly object thumbnail_path
    cdef readonly object fallback_url
    cdef readonly object video_playlist_url
    cdef readonly object preview_url

    cdef readonly object timestamp
    cdef readonly object raw

    def __init__(self, id, video_library_id, flow_id, captions_path, seek_path, thumbnail_path, fallback_url, video_playlist_url, preview_url, timestamp, raw=None):
        self.id = id
        self.video_library_id = video_library_id
        self.flow_id = flow_id

        self.captions_path = captions_path
        self.seek_path = seek_path
        self.thumbnail_path = thumbnail_path
        self.fallback_url = fallback_url
        self.video_playlist_url = video_playlist_url
        self.preview_url = preview_url
        
        self.timestamp = timestamp
        self.raw = raw

    @staticmethod
    def from_dict(data: dict) -> VideoStream:
        return VideoStream(
            data['id'],
            data['video_library_id'],
            data['flow_id'],
            data['captions_path'],
            data['seek_path'],
            data['thumbnail_path'],
            data['fallback_url'],
            data['video_playlist_url'],
            data['preview_url'],
            data['timestamp']            
        )

    cpdef dict to_dict(self, numeric_type=None, none_to=False):
        if numeric_type is None:
            data = {'id': self.id, 'video_library_id': self.video_library_id, 'flow_id': self.flow_id, 'captions_path': self.captions_path, 'seek_path': self.seek_path, 'thumbnail_path': self.thumbnail_path, 'fallback_url': self.fallback_url, 'video_playlist_url': self.video_playlist_url, 'preview_url': self.preview_url, 'timestamp': self.timestamp}
        else:
            data = {'id': self.id, 'video_library_id': self.video_library_id, 'flow_id': self.flow_id, 'captions_path': self.captions_path, 'seek_path': self.seek_path, 'thumbnail_path': self.thumbnail_path, 'fallback_url': self.fallback_url, 'video_playlist_url': self.video_playlist_url, 'preview_url': self.preview_url, 'timestamp': self.timestamp}
        
        return data if not none_to else convert_none_values(data, none_to)

    def __repr__(self):
        return f"id: {self.id} video_library_id: {self.video_library_id} flow_id: {self.flow_id} captions_path: {self.captions_path} seek_path: {self.seek_path} thumbnail_path: {self.thumbnail_path} fallback_url: {self.fallback_url} video_playlist_url: {self.video_playlist_url} preview_url: {self.preview_url} timestamp: {self.timestamp}"
   

    def __eq__(self, cmp):
        return self.id == cmp.id and self.video_library_id == cmp.video_library_id and self.flow_id == cmp.flow_id and self.captions_path == cmp.captions_path and self.seek_path == cmp.seek_path and self.thumbnail_path == cmp.thumbnail_path and self.fallback_url == cmp.fallback_url and self.video_playlist_url == cmp.video_playlist_url and self.preview_url == cmp.preview_url and self.timestamp == cmp.timestamp        


    def __hash__(self):
        return hash(self.__repr__())

