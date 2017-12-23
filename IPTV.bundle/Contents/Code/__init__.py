# Copyright © 2013-2016 Valdas Vaitiekaitis

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# Version 1.2.2

from datetime import datetime, timedelta # https://docs.python.org/2/library/datetime.html
import xml.etree.ElementTree # https://docs.python.org/2/library/xml.etree.elementtree.html
import time
import calendar

TITLE = 'EvFree Fullerton'
PREFIX = '/video/iptv'
GROUPS = {}
STREAMS = {}
GUIDE = {}

def Start():
    ObjectContainer.title1 = TITLE
    ObjectContainer.art = R('art-default.jpg')
    DirectoryObject.thumb = R('icon-folder.png')
    DirectoryObject.art = R('art-default.jpg')
    VideoClipObject.art = R('art-default.png')

@handler(PREFIX, TITLE)
def MainMenu():
    oc = ObjectContainer()
    oc.add(CreateVideoClipObject(
	url = 'http://plexserver.fefcful.org:8090/live/worshipcenter/index.m3u8',
#	url = 'rtmp://plexserver.fefcful.org/live/worshipcenter',
	title = 'Worship Center Live',
	thumb = 'http://plexserver.fefcful.org:8090/EVF_logo.png',
	summary = ' '
	))
    oc.add(CreateVideoClipObject(
        url = 'http://plexserver.fefcful.org:8090/live/signage/index.m3u8',
        title = 'Blvd Signage',
        thumb = 'http://plexserver.fefcful.org:8090/EVF_logo.png',
        summary = ' '
        ))
#    oc.add(CreateVideoClipObject(
#	url = 'http://plexserver.fefcful.org:8090/live/quadtest/index.m3u8',
#	title = 'Campus Cameras',
#	thumb = 'http://plexserver.fefcful.org:8090/EVF_logo.png',
#	summary = ' '
#	))
    return oc

@route(PREFIX + '/createvideoclipobject')
def CreateVideoClipObject(url, title, thumb, summary, container = False, includeBandwidths = 0):
    vco = VideoClipObject(
        key = Callback(CreateVideoClipObject, url = url, title = title, thumb = thumb, summary = summary, container = True, includeBandwidths = 0),
        rating_key = title,
        url = url,
        title = title,
        thumb = GetThumb(thumb),
        summary = summary,
        items = [
            MediaObject(
                #container = Container.MP4,     # MP4, MKV, MOV, AVI
                #video_codec = VideoCodec.H264, # H264
                #audio_codec = AudioCodec.AAC,  # ACC, MP3
                #audio_channels = 2,            # 2, 6
                parts = [
                    PartObject(
                        key = GetVideoURL(url = url)
                    )
                ],
                optimized_for_streaming = True
            )
        ]
    )
    if container:
        return ObjectContainer(objects = [vco])
    else:
        return vco
    return vco

def GetVideoURL(url, live = True):
    if url.startswith('rtmp') and Prefs['rtmp']:
        #Log.Debug('*' * 80)
        #Log.Debug('* url before processing: %s' % url)
        #if url.find(' ') > -1:
        #    playpath = GetAttribute(url, 'playpath', '=', ' ')
        #    swfurl = GetAttribute(url, 'swfurl', '=', ' ')
        #    pageurl = GetAttribute(url, 'pageurl', '=', ' ')
        #    url = url[0:url.find(' ')]
        #    Log.Debug('* url_after: %s' % RTMPVideoURL(url = url, playpath = playpath, swfurl = swfurl, pageurl = pageurl, live = live))
        #    Log.Debug('*' * 80)
        #    return RTMPVideoURL(url = url, playpath = playpath, swfurl = swfurl, pageurl = pageurl, live = live)
        #else:
        #    Log.Debug('* url_after: %s' % RTMPVideoURL(url = url, live = live))
        #    Log.Debug('*' * 80)
        #    return RTMPVideoURL(url = url, live = live)
        #Log.Debug('* url after processing: %s' % RTMPVideoURL(url = url, live = live))
        #Log.Debug('*' * 80)
        return RTMPVideoURL(url = url, live = live)
    #elif url.startswith('mms') and Prefs['mms']:
    #    return WindowsMediaVideoURL(url = url)
    else:
        return HTTPLiveStreamURL(url = url)

def GetThumb(thumb, default = 'EVF_logo.png'):
    if thumb and thumb.startswith('http'):
        return thumb
    elif thumb and thumb != '':
        return R(thumb)
    else:
        return R(default)

def GetAttribute(text, attribute, delimiter1 = '="', delimiter2 = '"', default = ''):
    x = text.find(attribute)
    if x > -1:
        y = text.find(delimiter1, x + len(attribute)) + len(delimiter1)
        z = text.find(delimiter2, y)
        if z == -1:
            z = len(text)
        return unicode(text[y:z].strip())
    else:
        return default

def GetGuide(channel):
    summary = ''
    #if Prefs['xmltv'].startswith('http://') or Prefs['xmltv'].startswith('https://'):
    #    xmltv = HTTP.Request(Prefs['xmltv']).content
    #else:
    #    xmltv = Resource.Load(Prefs['xmltv'], binary = True)
    #if xmltv != '':
    if channel in GUIDE.keys():
        current_time = datetime.today()
        try:
            guide_hours = int(Prefs['guide_hours'])
        except:
            guide_hours = 8
        #root = xml.etree.ElementTree.fromstring(xmltv)
        #for programme in root.findall("./programme[@channel='" + channel + "']"):
        #    start_time = datetime.strptime(programme.get('start')[:12], '%Y%m%d%H%M')
        #    stop_time = datetime.strptime(programme.get('stop')[:12], '%Y%m%d%H%M')
        #    if start_time <= current_time + timedelta(hours = guide_hours) and stop_time > current_time:
        #        summary = summary + '\n' + start_time.strftime('%H:%M') + ' ' + programme.find('title').text
        items_list = GUIDE[channel].values()
        for item in items_list:
            if item['start'] <= current_time + timedelta(hours = guide_hours) and item['stop'] > current_time:
                summary = summary + '\n' + item['start'].strftime('%H:%M') + ' ' + item['title']
    return summary
