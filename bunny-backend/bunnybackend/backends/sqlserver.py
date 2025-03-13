

# from typing import Tuple
# from bunnybackend.defines import *
# from datetime import datetime as dt
# from bunnybackend.config import Config
# import json
# import pyodbc

# class CredsSQLServer():
#     def __init__(self):
#         pass

# class TargetSQLServer(CredsSQLServer):
#     id = SQLSERVER

#     def __init__(self, config=None):
#         if config is None:
#             config = 'config.yaml'

#         self.config = Config(config=config)
#         keys = self.config[self.id.lower()]
#         self.host = keys.host
#         self.user = keys.user
#         self.pw = keys.pw
#         self.db = keys.db
#         self.port = keys.port


# class SQLServer():
#     def __init__(self, conn: CredsSQLServer):
#         self.table = self.default_table
#         self.raw_table = TABLE + RAW

#         self.host = conn.host
#         self.user = conn.user
#         self.pw = conn.pw
#         self.db = conn.db
#         self.port = conn.port
#         self.driver = '{SQL Server}'

#     def _raw(self, data: Tuple):
#         timestamp, data = data
#         return f"('{timestamp}','{json.dumps(data, default=str)}')"

#     async def _connect(self):
#         self.dsn = f"DRIVER={self.driver};SERVER={self.host};DATABASE={self.db};UID={self.user};PWD={self.pw};Encrypt=no"
#         self.conn = await pyodbc.connect(dsn = self.dsn)

#     async def read(self):
#         await self._connect()
#         args_str = self._read()
#         async with self.conn.transaction():
#             try:
#                 return await self.conn.fetch(f"SELECT {args_str} FROM {self.table}")
#             except Exception as a:
#                 print(a)
#                 # when restarting a subscription, some exchanges will re-publish a few messages
#                 pass

#     async def write(self, updates: list):
#         await self._connect()

#         batch = []
        
#         for data in updates:
#             data = data.to_dict(numeric_type=float)
#             ts = dt.utcfromtimestamp(
#                 data['timestamp']) if data['timestamp'] else None
#             batch.append((ts, data))

#         args_str = ([self._write(u) for u in batch])
#         # args_raw_str = ','.join([self._raw(u) for u in batch])
#         self.n = ', '.join([f'${i+1}' for i in range(len(args_str[0]))])
#         self.col = self._col()
#         print(self.n)
#         print(self.col)
#         print(args_str)
#         loop = asyncio.get_event_loop()


#         async with aioodbc.create_pool(dsn=self.dsn, loop=loop) as pool:
#             async with pool.acquire() as conn:
#                 async with conn.cursor() as cur:
#                     await cur.executemany(f'INSERT INTO {self.table}{self.col} VALUES({self.n}) ON CONFLICT DO NOTHING', args_str)
       
              
#         # async with self.conn.transaction():
#         #     try:
#         #         await self.conn.executemany(f'INSERT INTO {self.table}{self.col} VALUES({self.n}) ON CONFLICT DO NOTHING', args_str)
#         #         # await self.conn.execute(f"INSERT INTO {self.raw_table} VALUES {args_raw_str}")
#         #     except Exception as a:
#         #         print(a)
#         #         # when restarting a subscription, some exchanges will re-publish a few messages
#         #         pass


# class RefreshVideoLibrarySQLServer(SQLServer):
#     default_table = TABLE + REFRESH_VIDEO_LIBRARY

#     def _read(self):
#         return f"id,name,video_count,traffic_usage,storage_usage,date_created,timestamp"

#     def _col(self):
#         return f"(id,name,video_count,traffic_usage,storage_usage,date_created,timestamp)"

#     def _write(self, data: Tuple):
#         timestamp, data = data
#         return (data['id'], data['name'], data['video_count'], data['traffic_usage'], data['storage_usage'],data['date_created'],timestamp)

