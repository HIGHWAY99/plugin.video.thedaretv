import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,xbmc,xbmcplugin,xbmcgui,xbmcaddon,os
from metahandler import metahandlers
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
from universal import favorites
from universal import _common as univ_common
from thedareradio import *

#www.thedarewall.com (The Dare TV) - by The_Silencer 2013 v0.6.0


grab = metahandlers.MetaData(preparezip = False)
addon_id = 'plugin.video.thedaretv'
local = xbmcaddon.Addon(id=addon_id)
daretvpath = local.getAddonInfo('path')
addon = Addon(addon_id, sys.argv)
datapath = addon.get_profile()
art = daretvpath+'/art'
net = Net()
fav = favorites.Favorites('plugin.video.thedaretv', sys.argv)


#Metahandler
def GRABMETA(name,types):
	type = types
	EnableMeta = local.getSetting('Enable-Meta')
	if EnableMeta == 'true':
		if 'Movie' in type:
			meta = grab.get_meta('movie',name,'',None,None,overlay=6)
			infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year']}
		elif 'tvshow' in type:
			meta = grab.get_meta('tvshow',name,'','',None,overlay=6)
			infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'cast': meta['cast'],'studio': meta['studio'],'banner_url': meta['banner_url'],'backdrop_url': meta['backdrop_url'],'status': meta['status']}
	else: infoLabels=[]
	return infoLabels
                
#Main menu
def CATEGORIES():
	addDir('Movies','http://www.thedarewall.com/tv/new-movies',18,art_('Movies','Main Menu'),None,'') ## 'http://www.thedarewall.com/tv/templates/thedarewall/images/logo.png'
	addDir('TV-Shows','http://www.thedarewall.com/tv/',4,art_('TV Shows','Main Menu'),None,'') ## 'http://www.thedarewall.com/tv/templates/thedarewall/images/logo.png'
	fav.add_my_fav_directory(img=art_('Favorites','Main Menu')) ## os.path.join(art,'')
	addDir('Search','http://www.thedarewall.com/tv/',15,art_('Search','Main Menu'),None,'')
	addDir('Radio','http://www.thedarewall.com/mp3/radio.php',302,art_('Radio','Main Menu'),None,'') ## 'http://www.thedarewall.com/mp3/images/bgcont.png'
	addDir('Settings','http://',309,art_('Settings','Main Menu'),None,'')
	set_view('list')

def MOVIES():
	addDir('Latest Updated','http://www.thedarewall.com/tv/new-movies',5,art_('Latest Movies','Sub Menus'),None,'')
	addDir('BoxOffice','http://www.thedarewall.com/tv/movie-tags/boxoffice',5,art_('Box_Office','Sub Menus'),None,'')
	addDir('Genres','http://www.thedarewall.com/tv/',9,art_('Genres','Sub Menus'),None,'')
	addDir('Search','http://www.thedarewall.com/tv/',15,art_('Search','Sub Menus'),None,'')
	set_view('list')

def TV():
	addDir('Latest Updated','http://www.thedarewall.com/tv/new-shows',17,art_('Latest Shows','Sub Menus'),None,'')
	addDir('A-Z','http://www.thedarewall.com/tv/tv-shows',10,art_('A-Z Shows','Sub Menus'),None,'')
	#addDir('A-Z (abc)','http://www.thedarewall.com/tv/tv-shows/abc',10,art_('','Sub Menus'),None,'') ## might need to be done like TVAZ() after a-z is chosen.
	#addDir('A-Z (date)','http://www.thedarewall.com/tv/tv-shows/date',10,art_('','Sub Menus'),None,'')
	#addDir('A-Z (imdb)','http://www.thedarewall.com/tv/tv-shows/imdb_rating',10,art_('','Sub Menus'),None,'')
	addDir('All (abc)','http://www.thedarewall.com/tv/tv-shows/abc',11,art_('TV Shows','Main Menu'),None,'')
	addDir('All (date)','http://www.thedarewall.com/tv/tv-shows/date',11,art_('TV Shows','Main Menu'),None,'')
	addDir('All (imdb)','http://www.thedarewall.com/tv/tv-shows/imdb_rating',11,art_('TV Shows','Main Menu'),None,'')
	addDir('Search','http://www.thedarewall.com/tv/index.php',16,art_('Search','Sub Menus'),None,'')
	set_view('list')

#regex for A-Z list
def TVAZ(url):
	data=re.compile('<font color="white">Tv :</font></p></li>(.+?)</ul>',re.DOTALL).findall(net.http_GET(url).content)
	pattern = '<li><a href="(.+?)">(.+?)</a></li>'
	match = re.findall(pattern,str(data))
	for url,name in match:
		if (len(name) > 1): img=art_('#','Letters')
		else: img=art_(name,'Letters')
		addDir(name,'http://www.thedarewall.com'+url,11,img,None,'')
	set_view('list')

#regex for genres movies  
def MOVIEGEN(url):
	data=re.compile('<li class="dropdown"><a href="http://www.thedarewall.com/tv/movies" class="dropdown-toggle"><b class="caret"></b>&nbsp;&nbsp;Movies</a>.+?<ul class="dropdown-menu">(.+?)</ul>.+?</li>',re.DOTALL).findall(net.http_GET(url).content)
	pattern = '<li><a href="(.+?)">(.+?)</a></li>'
	match = re.findall(pattern,str(data))
	for url,name in match:
		addDir(name,url,5,art_(name,'Genres'),None,'')
	set_view('list')

#Routine to search for Movies
def SEARCH(url):
	EnableMeta = local.getSetting('Enable-Meta')
	keyb = xbmc.Keyboard('', 'Search The Dare TV for Movies')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		encode=urllib.quote(search)
		encode = encode.replace('%20', '+')
		print encode
		surl='http://www.thedarewall.com/tv/index.php?menu=search&query='+encode
		match=re.compile('</div>.+?<h5 class=".+?">.+?<a class="link" href="(.+?)" title="(.+?)">',re.DOTALL).findall(net.http_GET(surl).content)  
		for url,name in match:
			if EnableMeta == 'true': addDir(name.encode('UTF-8','ignore'),url,6,'','Movie','Movies')
			if EnableMeta == 'false': addDir(name.encode('UTF-8','ignore'),url,6,'',None,'Movies')
		set_view('movies')

#Routine to search for TV Shows
def SEARCHTV(url):
	EnableMeta = local.getSetting('Enable-Meta')
	keyb = xbmc.Keyboard('', 'Search The Dare TV for TV Shows')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		encode=urllib.quote(search)
		encode = encode.replace('%20', '+')
		print encode
		data = net.http_POST(url,{'menu' : 'search', 'query' : encode}).content
		match=re.compile('<h5>.+?<a class="link" href="(.+?)" title="(.+?)">.+?</h5>',re.DOTALL).findall(data)
		for url,name in match:
			if EnableMeta == 'true':  addDir(name,url,12,'','tvshow','TV-Shows')
			if EnableMeta == 'false': addDir(name,url,12,'',None,'TV-Shows')
		set_view('tvshows')

#regex for Movies            
def INDEX1(url):
	EnableMeta = local.getSetting('Enable-Meta')
	match=re.compile('</div>.+?<h5 class=".+?">.+?<a class="link" href="(.+?)" title="(.+?)">',re.DOTALL).findall(net.http_GET(url).content)
	nextpage=re.search('<li class=\'current\'>.+?<li><a href="(.+?)">&raquo;</a></li>',(net.http_GET(url).content))
	for url,name in match:
		if EnableMeta == 'true':  addDir(name.encode('UTF-8','ignore'),url,6,'','Movie','Movies')
		if EnableMeta == 'false': addDir(name.encode('UTF-8','ignore'),url,6,'',None,'Movies')
	if nextpage:
		url = nextpage.group(1)
		addDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]',url,5,art_('Next_Page','Sub Menus'),None,'')
	set_view('movies')

#regex for latest TV-Shows            
def INDEX2(url):
	EnableMeta = local.getSetting('Enable-Meta')
	match=re.compile('<a class="link" href="(.+?)" title="(.+?)">.+?</a>.+?<p class="left">(.+?)</p>',re.DOTALL).findall(net.http_GET(url).content)
	#nextpage=re.search('<li class=\'current\'>.+?<li><a href="(.+?)">&raquo;</a></li>',(net.http_GET(url).content))
	nextpage=re.search('</a></li>\s*<li><a href="(http://[0-9A-Za-z\-\_/\.]+)">&raquo;</a></li>',(net.http_GET(url).content))
	for url,name,extra in match:
		if EnableMeta == 'true': addDir("%s ~ %s"%(name.encode('UTF-8','ignore'),extra),url,6,'','tvshow','TV-Shows')
		if EnableMeta == 'false': addDir(name.encode('UTF-8','ignore'),url,6,'',None,'TV-Shows')
	if nextpage:
		url = nextpage.group(1)
		addDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]',url,7,art_('Next_Page','Sub Menus'),None,'')
	set_view('episodes')

#regex for TV-Shows            
def INDEX3(url):
	EnableMeta = local.getSetting('Enable-Meta')
	match=re.compile('<h5>.+?<a class="link" href="(.+?)" title="(.+?)">.+?</a>.+?</h5>',re.DOTALL).findall(net.http_GET(url).content)
	#nextpage=re.search('<li class=\'current\'>.+?<li><a href="(.+?)">&raquo;</a></li>',(net.http_GET(url).content))  ## didn't work
	nextpage=re.search('</a></li>\s*<li><a href="(http://[0-9A-Za-z\-\_/\.]+)">&raquo;</a></li>',(net.http_GET(url).content))  ## working fix
	for url,name in match:
		if EnableMeta == 'true': addDir(name.encode('UTF-8','ignore'),url,12,'','tvshows','TV-Shows')
		if EnableMeta == 'false': addDir(name.encode('UTF-8','ignore'),url,12,'',None,'TV-Shows')
	if nextpage:
		url = nextpage.group(1)
		addDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]',url,11,art_('Next_Page','Sub Menus'),None,'')
	set_view('tvshows')

#regex for seasons
def SEASONS(url):
	data=re.compile('<li class="noleftmargin current"><a href=".+?">All seasons</a></li>(.+?)</ul>',re.DOTALL).findall(net.http_GET(url).content)
	pattern = '<li ><a href=\'(.+?)\'>(.+?)</a></li>'
	match = re.findall(pattern,str(data))
	for url,name in match:
		addDir(name.encode('UTF-8','ignore'),url,13,'',None,'TV-Shows')
	set_view('seasons')

#regex for episodes
def EPISODES(url):
	match = re.compile('<h5 class="left">.+?<a class="link" href="(.+?)" title="(.+?)">.+?</h5>',re.DOTALL).findall(net.http_GET(url).content)
	for url,name in match:
		addDir(name.encode('UTF-8','ignore'),url,6,'',None,'TV-Shows')
	set_view('episodes')
                        
#regex for Hoster links
def VIDEOLINKS(url):
	match=re.compile('id="selector(.+?)"><span>(.+?)</span></a>',re.DOTALL).findall(net.http_GET(url).content)
	for click,name in match:
		nono = ['videomega.tv']
		if name not in nono:
			img=art_(name,'Hosters')
			#if (os.path.isfile(img)==False): img='http://www.google.com/s2/favicons\?domain='+name  ## the name lacks the .com/net/to/eu on the domain name to use google for the tiny favorite icon image.
			print 'img:  '+img
			addDir(name,url+'@'+click,26,img,None,'')
	set_view('list')

def ONCLICK(url,name):
	click = url.split('@')[1]
	url = url.split('@')[0]
	print name
	print click
	match=re.compile('embeds\['+click+'\] =.+?src="(.+?)"',re.DOTALL | re.IGNORECASE).findall(net.http_GET(url).content)
	for url in match:
		url = url.replace('http://www.thedarewall.com/thedarewall/embed.php?url=','')
		specialhost = ['Allmyvideos','Vidto-ipad']
		if name not in specialhost:
			print url
			addDir(name,url,7,'',None,'')
		else: addDir(name,url,8,'',None,'')
	set_view('list')
                                
#Routine to resolve host not in metahandlers (Vidto-ipad, Allmyvideos)
def SPECIALHOST(url,name):
	#Get Vidto-ipad final link
	if 'Vidto-ipad' in name:
		match=re.compile('').findall(net.http_GET(url).content)
		for url in match:
			addLink('Play',url,art_('Vidto-Ipad','Hosters'))
	#Get Allmyvideos final link
	if 'Allmyvideos' in name:
		match=re.compile('"file" : "(.+?)"').findall(net.http_GET(url).content)
		for url in match:
			addLink('Play',url,art_('#','Allmyvideos'))
	set_view('list')

#Pass url to urlresolver
def STREAM(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	streamlink = urlresolver.resolve(urllib2.urlopen(req).url)
	print streamlink
	addLink(name,streamlink,'')
	set_view('list')

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
	return param

def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
	return ok


def addDir(name,url,mode,iconimage,types,favtype):
	ok=True
	type = types
	if type != None: infoLabels = GRABMETA(name,types)
	else: infoLabels = {'title':name}
	try: img = infoLabels['cover_url']
	except: img= iconimage
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=img)
	liz.setInfo( type="Video", infoLabels= infoLabels)
	try: liz.setProperty( "Fanart_Image", infoLabels['backdrop_url'] )
	except: t=''
	contextMenuItems = []
	contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
	liz.addContextMenuItems(contextMenuItems, replaceItems=False)
	#Universal Favorites
	if 'Movies' in favtype:
		contextMenuItems.append(('Add to Favorites', fav.add_directory(name, u, section_title='Movies')))
		liz.addContextMenuItems(contextMenuItems, replaceItems=True)
	elif 'TV-Shows' in favtype:
		contextMenuItems.append(('Add to Favorites', fav.add_directory(name, u, section_title='TV-Shows')))
		liz.addContextMenuItems(contextMenuItems, replaceItems=True)
	else:
		contextMenuItems.append(('Add to Favorites', fav.add_directory(name, u, section_title='Other Favorites')))
		liz.addContextMenuItems(contextMenuItems, replaceItems=True)
	####################
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

params=get_params()
url=None; name=None; mode=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass

print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name)


if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: MOVIES()
elif mode==2: MOVIESAZ()
elif mode==3: MOVIESGEN()
elif mode==4: TV()
elif mode==5: INDEX1(url)
elif mode==6: VIDEOLINKS(url)
elif mode==7: STREAM(url)
elif mode==8: SPECIALHOST(url,name)
elif mode==9: MOVIEGEN(url)
elif mode==10: TVAZ(url)
elif mode==11: INDEX3(url)
elif mode==12: SEASONS(url)
elif mode==13: EPISODES(url)
elif mode==14: DIRECTORDIR()
elif mode==15: SEARCH(url)
elif mode==16: SEARCHTV(url)
elif mode==17: INDEX2(url)
elif mode==18: MOVIES()
elif mode==19: TVSHOWS()
elif mode==20: TVGEN(url)
elif mode==21: COUNTRIESTV(url)
elif mode==22: SEARCHTV(url)
elif mode==23: SEASONS(url,name)
elif mode==24: EPISODES(url,name)
elif mode==25: EPISODELINKS(url,name)
elif mode==26: ONCLICK(url,name)
elif mode==300:	RadioPlay(url)
elif mode==301:	RadioStations(url)
elif mode==302:	RadioCategories()
elif mode==302:	RadioCategories()
elif mode==309:	addon.addon.openSettings()


xbmcplugin.endOfDirectory(int(sys.argv[1]))
