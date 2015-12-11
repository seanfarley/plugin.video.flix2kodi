from __future__ import unicode_literals
from thread import start_new_thread
import xbmc, xbmcgui, xbmcaddon, xbmcplugin

import get
import utility
import os
import sys

def trailer(title, video_type):
    trailers = []
    content = get.trailer(video_type, title)
    if content:
        for match in content['results']:
            if match['site'] == 'YouTube':
                if match['iso_639_1']:
                    name = match['name'] + ' (' + match['iso_639_1'] + ')'
                else:
                    name = match['name']
                match = {'name': name, 'key': match['key']}
                trailers.append(match)
        if len(trailers) > 0:
            dialog = xbmcgui.Dialog()
            nr = dialog.select('Trailer', [match['name'] for match in trailers])
            if nr >= 0:
                selected_trailer = trailers[nr]
                match = 'PlayMedia(plugin://plugin.video.youtube/play/?video_id=%s)' % selected_trailer['key']
                xbmc.executebuiltin(match)
        else:
            utility.notification(utility.get_string(30305))
    else:
        utility.notification(utility.get_string(30305))
        pass


def video(url):
    player = FlixPlayer()
    player.play( url )
    return None


class FlixPlayer(xbmcgui.Window):

    def onAction(self, action):
        xbmc.log('Action: ' + `action.getId()`, level=xbmc.LOGERROR)
        if action.getId() == 92:
            os.system('/usr/bin/xdotool key alt+F4')
            self.close()
        if action.getId() == 7:
            os.system('/usr/bin/xdotool key space')
        if action.getId() == 1:
            os.system('/usr/bin/xdotool key Left Left Left space')
        if action.getId() == 2:
            os.system('/usr/bin/xdotool key Right Right Right space')

    def play ( self, url):
        start_new_thread(self.playInternal, (url,))
        self.doModal()
    def playInternal (self, url):
        xbmc.executebuiltin("PlayerControl(Stop)")
        xbmc.audioSuspend()
#        xbmc.enableNavSounds(False)
        addonPath = xbmcaddon.Addon().getAddonInfo("path")
        os.system('sh '+addonPath+'/resources/launchBrowser.sh https://www.netflix.com/watch/%s' % url)
        xbmc.audioResume()
#        xbmc.enableNavSounds(True)