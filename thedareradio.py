### ############################################################################################################
###	#	
### # Project: 			#		TheDareWall.com - by The_Silencer 2013.
### # Project: 			#		TheDareRadio - by The Highway 2013.
### # Authors: 			#		The_Silencer, The Highway
### # Version:			#		v_._._
### # Description: 	#		http://www.thedarewall.com
###	#	
### ############################################################################################################
### ############################################################################################################
import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,xbmc,xbmcplugin,xbmcgui,xbmcaddon,os,sys
from metahandler import metahandlers
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
from universal import favorites
from universal import _common as univ_common

### ############################################################################################################
### ############################################################################################################

addon_id = 'plugin.video.thedaretv'
local = xbmcaddon.Addon(id=addon_id)
daretvpath = local.getAddonInfo('path')
addon = Addon(addon_id, sys.argv)
datapath = addon.get_profile()
art = daretvpath+'/art'
net = Net()
fav = favorites.Favorites('plugin.video.thedaretv', sys.argv)
artRadio='http://www.thedarewall.com/mp3/images/bgcont.png'

### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##### Play #####
def RadioPlay(url): ### mode=300
	play=xbmc.Player(xbmc.PLAYER_CORE_AUTO) ### xbmc.PLAYER_CORE_AUTO | xbmc.PLAYER_CORE_DVDPLAYER | xbmc.PLAYER_CORE_MPLAYER | xbmc.PLAYER_CORE_PAPLAYER
	play.play(url)
	addon.resolve_url(url)
##### /\ ##### Play #####

##### Common Functions #####
def eod(): addon.end_of_directory()
def set_view(content='none',view_mode=50):
	h=int(sys.argv[1])
	if (content is not 'none'): xbmcplugin.setContent(h, content)
	### set content type so library shows more views and info
	#if (tfalse(addst("auto-view"))==True):
	#	xbmc.executebuiltin("Container.SetViewMode(%s)" % view_mode)
##### /\ ##### Common Functions #####


##### Browse Radio Stations #####
def RadioStations(url): ### mode=301
	html=net.http_GET(url).content
	s='>\s*<span\s+id="radiop">\s*</span>\s*&nbsp;\s*(.+?)</div>\';[\n]'+"\s*var\s+so\s+=\s+new\s+SWFObject\('http.+?.swf','\D+','\d+','\d+','\d+','#\d+'\);[\n]\s*so.addParam\('.+?'\s*,\s*'.+?'\);[\n]\s*so.addParam\('.+?'\s*,\s*'.+?'\);[\n]\s*so.addParam\('.+?'\s*,\s*'.+?'\);[\n]\s*so.addVariable\('src'\s*,\s*'(.+?)'\)"
	matches=re.compile(s).findall(html)
	if (not matches): eod(); return
	ItemCount=len(matches)
	for name, path in matches:
		try:		img=re.compile('<img src="(http://.+?)" alt="'+name+'"').findall(html)[0]
		except:	img=artRadio
		labs={'title':name}; pars={'mode':300,'url':path}
		contextMenuItems=[]; 
		#contextMenuItems.append(('Download', ''))
		addon.add_directory(pars, labs, img=img, contextmenu_items=contextMenuItems, total_items=ItemCount)
	set_view('list'); eod()
##### /\ ##### Browse Radio Stations #####

##### Browse Radio Categories #####
def RadioCategories(url='http://www.thedarewall.com/mp3/radio.php', prefix='http://www.thedarewall.com/mp3/radio.php'): ### mode=302
	html=net.http_GET(url).content; s='<div\s+id="tabtop"\s+style="background:\s*#282828;">\s*<a\s+href="(\?genre=.+?)">(.+?)</a>\s*</div>' ## works
	matches=re.compile(s).findall(html)
	if (not matches): eod(); return
	ItemCount=len(matches)
	for path, name in matches:
		labs={'title':name}; pars={'mode':301,'url':prefix+path}
		contextMenuItems=[]; 
		#contextMenuItems.append(('Download', ''))
		addon.add_directory(pars, labs, img=artRadio, contextmenu_items=contextMenuItems, total_items=ItemCount)
	set_view('list'); eod()
##### /\ ##### Browse Radio Categories #####



