#Use MXP Tiny with H.254 Encoder v3.5.3 - always set to 29.97p
:begin
start "ffmpeg1" ffmpeg -i \\.\pipe\DeckLink.ts -f mpegts -c:v:0 h264 -c:a:1 aac -c:v copy -c:a aac -ac 2 -ar 48000 -b:a 128k -bufsize 2000k -f flv -rtmp_buffer 300 -rtmp_app live -rtmp_playpath worshipcenter rtmp://plexserver.fefcful.org/

