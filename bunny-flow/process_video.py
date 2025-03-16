
import m3u8

playlist = m3u8.load('https://vz-f54b3be4-646.b-cdn.net/b8c08c53-03b7-4df1-a2cf-9d01b4dcf4fb/playlist.m3u8')
print(playlist.dumps())

