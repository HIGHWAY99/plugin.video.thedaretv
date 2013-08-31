import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,xbmc,xbmcplugin,xbmcgui,xbmcaddon,os
from metahandler import metahandlers
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
from universal import favorites
from universal import _common as univ_common
from thedareradio import *

#www.thedarewall.com (The Dare TV) - by The_Silencer 2013 v0.3


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
                        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                          'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
                          'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year']}
                elif 'tvshow' in type:
                        meta = grab.get_meta('tvshow',name,'','',None,overlay=6)
                        infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                              'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],
                              'cast': meta['cast'],'studio': meta['studio'],'banner_url': meta['banner_url'],
                              'backdrop_url': meta['backdrop_url'],'status': meta['status']}
        return infoLabels
                
#Main menu
def CATEGORIES():
        addDir('Movies','http://www.thedarewall.com/tv/new-movies',18,'http://www.thedarewall.com/tv/templates/thedarewall/images/logo.png',None,'')
        addDir('TV-Shows','http://www.thedarewall.com/tv/',4,'http://www.thedarewall.com/tv/templates/thedarewall/images/logo.png',None,'')
        fav.add_my_fav_directory(img=os.path.join(art,''))
        addDir('Search','http://www.thedarewall.com/tv/',15,'',None,'')
        addDir('Radio','http://www.thedarewall.com/mp3/radio.php',302,'http://www.thedarewall.com/mp3/images/bgcont.png',None,'')
        addDir('Settings','http://',309,'',None,'')

def MOVIES():
        addDir('Latest Updated','http://www.thedarewall.com/tv/new-movies',5,'',None,'')
        addDir('BoxOffice','http://www.thedarewall.com/tv/movie-tags/boxoffice',5,'',None,'')
        addDir('Genres','http://www.thedarewall.com/tv/',9,'',None,'')
        addDir('Search','http://www.thedarewall.com/tv/',15,'',None,'')

def TV():
        addDir('Latest Updated','http://www.thedarewall.com/tv/new-shows',17,'',None,'')
        addDir('A-Z','http://www.thedarewall.com/tv/tv-shows',10,'',None,'')
        addDir('Search','http://www.thedarewall.com/tv/index.php',16,'',None,'')

#regex for A-Z list
def TVAZ(url):
        data=re.compile('<font color="white">Tv :</font></p></li>(.+?)</ul>',re.DOTALL).findall(net.http_GET(url).content)
        pattern = '<li><a href="(.+?)">(.+?)</a></li>'
        match = re.findall(pattern,str(data))
        for url,name in match:
                        addDir(name,'http://www.thedarewall.com'+url,11,'',None,'')

#regex for genres movies  
def MOVIEGEN(url):
        data=re.compile('<li class="dropdown"><a href="http://www.thedarewall.com/tv/movies" class="dropdown-toggle"><b class="caret"></b>&nbsp;&nbsp;Movies</a>.+?<ul class="dropdown-menu">(.+?)</ul>.+?</li>',re.DOTALL).findall(net.http_GET(url).content)
        pattern = '<li><a href="(.+?)">(.+?)</a></li>'
        match = re.findall(pattern,str(data))
        for url,name in match:
                        addDir(name,url,5,'',None,'')

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
                        if EnableMeta == 'true':
                               addDir(name.encode('UTF-8','ignore'),url,6,'','Movie','Movies')
                        if EnableMeta == 'false':
                               addDir(name.encode('UTF-8','ignore'),url,6,'',None,'Movies')

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
                        if EnableMeta == 'true':
                               addDir(name,url,12,'','tvshow','TV-Shows')
                        if EnableMeta == 'false':
                               addDir(name,url,12,'',None,'TV-Shows')

#regex for Movies            
def INDEX1(url):
        EnableMeta = local.getSetting('Enable-Meta')
        match=re.compile('</div>.+?<h5 class=".+?">.+?<a class="link" href="(.+?)" title="(.+?)">',re.DOTALL).findall(net.http_GET(url).content)
        nextpage=re.search('<li class=\'current\'>.+?<li><a href="(.+?)">&raquo;</a></li>',(net.http_GET(url).content))
        for url,name in match:
                if EnableMeta == 'true':
                        addDir(name.encode('UTF-8','ignore'),url,6,'','Movie','Movies')
                if EnableMeta == 'false':
                        addDir(name.encode('UTF-8','ignore'),url,6,'',None,'Movies')
        if nextpage:
                url = nextpage.group(1)
                addDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]',url,5,'',None,'')

#regex for latest TV-Shows            
def INDEX2(url):
        EnableMeta = local.getSetting('Enable-Meta')
        match=re.compile('<a class="link" href="(.+?)" title="(.+?)">.+?</a>.+?<p class="left">(.+?)</p>',re.DOTALL).findall(net.http_GET(url).content)
        nextpage=re.search('<li class=\'current\'>.+?<li><a href="(.+?)">&raquo;</a></li>',(net.http_GET(url).content))
        for url,name,extra in match:
                if EnableMeta == 'true':
                        addDir("%s ~ %s"%(name.encode('UTF-8','ignore'),extra),url,6,'','tvshow','TV-Shows')
                if EnableMeta == 'false':
                        addDir(name.encode('UTF-8','ignore'),url,6,'',None,'TV-Shows')
        if nextpage:
                url = nextpage.group(1)
                addDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]',url,5,'',None,'')

#regex for TV-Shows            
def INDEX3(url):
        EnableMeta = local.getSetting('Enable-Meta')
        match=re.compile('<h5>.+?<a class="link" href="(.+?)" title="(.+?)">.+?</a>.+?</h5>',re.DOTALL).findall(net.http_GET(url).content)
        nextpage=re.search('<li class=\'current\'>.+?<li><a href="(.+?)">&raquo;</a></li>',(net.http_GET(url).content))
        for url,name in match:
                if EnableMeta == 'true':
                        addDir(name.encode('UTF-8','ignore'),url,12,'','tvshows','TV-Shows')
                if EnableMeta == 'false':
                        addDir(name.encode('UTF-8','ignore'),url,12,'',None,'TV-Shows')
        if nextpage:
                url = nextpage.group(1)
                addDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]',url,5,'',None,'')

#regex for seasons
def SEASONS(url):
        data=re.compile('<li class="noleftmargin current"><a href=".+?">All seasons</a></li>(.+?)</ul>',re.DOTALL).findall(net.http_GET(url).content)
        pattern = '<li ><a href=\'(.+?)\'>(.+?)</a></li>'
        match = re.findall(pattern,str(data))
        for url,name in match:
                addDir(name.encode('UTF-8','ignore'),url,13,'',None,'TV-Shows')

#regex for episodes
def EPISODES(url):
        match = re.compile('<h5 class="left">.+?<a class="link" href="(.+?)" title="(.+?)">.+?</h5>',re.DOTALL).findall(net.http_GET(url).content)
        for url,name in match:
                addDir(name.encode('UTF-8','ignore'),url,6,'',None,'TV-Shows')
                        
#regex for Hoster links
def VIDEOLINKS(url):
        match=re.compile('id="selector(.+?)"><span>(.+?)</span></a>',re.DOTALL).findall(net.http_GET(url).content)
        for click,name in match:
                nono = ['videomega.tv']
                if name not in nono:
                        addDir(name,url+'@'+click,26,'',None,'')

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
                        else:
                                addDir(name,url,8,'',None,'')
                                
#Routine to resolve host not in metahandlers (Vidto-ipad, Allmyvideos)
def SPECIALHOST(url,name):
        #Get Vidto-ipad final link
        if 'Vidto-ipad' in name:
                match=re.compile('').findall(net.http_GET(url).content)
                for url in match:
                        addLink('Play',url,'')
                
        #Get Allmyvideos final link
        if 'Allmyvideos' in name:
                match=re.compile('"file" : "(.+?)"').findall(net.http_GET(url).content)
                for url in match:
                        addLink('Play',url,'')

#Pass url to urlresolver
def STREAM(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        streamlink = urlresolver.resolve(urllib2.urlopen(req).url)
        print streamlink
        addLink(name,streamlink,'')

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
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
        if type != None:
                infoLabels = GRABMETA(name,types)
        else: infoLabels = {'title':name}
        try: img = infoLabels['cover_url']
        except: img= iconimage
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=img)
        liz.setInfo( type="Video", infoLabels= infoLabels)

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
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)


if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
        
elif mode==1:
        MOVIES()

elif mode==2:
        MOVIESAZ()

elif mode==3:
        MOVIESGEN()

elif mode==4:
        TV()

elif mode==5:
        print ""+url
        INDEX1(url)

elif mode==6:
        print ""+url
        VIDEOLINKS(url)

elif mode==7:
        print ""+url
        STREAM(url)

elif mode==8:
        print ""+url
        SPECIALHOST(url,name)

elif mode==9:
        print ""+url
        MOVIEGEN(url)

elif mode==10:
        print ""+url
        TVAZ(url)

elif mode==11:
        print ""+url
        INDEX3(url)

elif mode==12:
        print ""+url
        SEASONS(url)

elif mode==13:
        print ""+url
        EPISODES(url)

elif mode==14:
        DIRECTORDIR()

elif mode==15:
        print ""+url
        SEARCH(url)

elif mode==16:
        print ""+url
        SEARCHTV(url)

elif mode==17:
        print ""+url
        INDEX2(url)
        
elif mode==18:
        MOVIES()

elif mode==19:
        TVSHOWS()
        
elif mode==20:
        print ""+url
        TVGEN(url)

elif mode==21:
        print ""+url
        COUNTRIESTV(url)

elif mode==22:
        print ""+url
        SEARCHTV(url)

elif mode==23:
        print ""+url
        SEASONS(url,name)

elif mode==24:
        print ""+url
        EPISODES(url,name)

elif mode==25:
        print ""+url
        EPISODELINKS(url,name)

elif mode==26:
        print ""+url
        ONCLICK(url,name)
        
elif mode==300:	RadioPlay(url)
elif mode==301:	RadioStations(url)
elif mode==302:	RadioCategories()
elif mode==302:	RadioCategories()
elif mode==309:	addon.addon.openSettings()


xbmcplugin.endOfDirectory(int(sys.argv[1]))
