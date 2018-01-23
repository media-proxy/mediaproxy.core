#~ # coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import with_statement

from yapsy.PluginManager import PluginManager
import logging
import sys
from .categories import channel, scraper

from yapsy.PluginManager import PluginManagerSingleton
from yapsy.VersionedPluginManager import VersionedPluginManager
#~ from OnlinePluginManager import OnlinePluginManager
from yapsy.ConfigurablePluginManager import ConfigurablePluginManager


from yapsy.IPlugin import IPlugin

class Plugins:
    def __init__(self,configparser,loadpathes=["plugins"],installpath=None,language='en'):
        self.language = language
        self.configparser = configparser
        self.loadpathes = loadpathes
        if len(loadpathes) == 1 and installpath is None:
            self.installpath = loadpathes[0]
        else:
            self.installpath = installpath
        self.manager = None
        self.extension = "mediaproxy"
        self.categories = {}
        self.categories["Channels"] = channel
        self.categories["Scrapers"] = scraper
        self.load()

    def load(self):
        PluginManagerSingleton.setBehaviour([
            VersionedPluginManager,ConfigurablePluginManager,
        ])#OnlinePluginManager
        self.manager = PluginManagerSingleton.get()

        #~ if self.installpath:
            #~ self.manager.setInstallDir(self.installpath)

        self.manager.setConfigParser(self.configparser,self.configparser.save)
        self.manager.setPluginPlaces(self.loadpathes)
        self.manager.setPluginInfoExtension(self.extension)
        self.manager.setCategoriesFilter(self.categories)
        self.manager.collectPlugins()
        
    def list_plugins(self,categorie=None,only_active=False):
        if categorie:
            try:
                plugins = self.manager.getPluginsOfCategory(categorie)
            except KeyError:
                return []
        else:
            plugins = self.manager.getAllPlugins()
            
        outlist = []
        for plugin in plugins:
            if not plugin.is_activated and only_active:
                continue
            pdict = {}
            pdict['id'] = '%s.%s'%(plugin.category,plugin.name)
            pdict['name'] = plugin.name

            pdict['description'] = plugin.name
            pdict['category'] = plugin.category
            pdict['plugin'] = plugin
            if self.language:
                if plugin.details.has_section(self.language):
                    pdict['name'] = plugin.details.get(self.language,'Name')
                    pdict['description'] = plugin.details.get(self.language,'Description')
                    pdict['version'] = plugin.version
            #~ print "%s - %s"%(pdict['id'],plugin.version)
            outlist.append(pdict)
        return outlist
        
    def activatePluginByID(self,ID):
        self.manager.activatePluginByName(ID.split('.')[1],category_name=ID.split('.')[0],save_state=True)
    
    def deactivatePluginByID(self,ID):
        self.manager.deactivatePluginByName(ID.split('.')[1],category_name=ID.split('.')[0],save_state=True)
        
    def getPluginByName(self, name, category='channels'):
        return self.manager.getPluginByName(name, category=category)
        
            

if __name__ == "__main__":
    import ConfigParser
    c = ConfigParser.ConfigParser()
    def saveconfig():
        print ('Save')
    c.save_config =  saveconfig
    p = Plugins(c)

    print (p.list_plugins())
    print (p.manager.installFromZIP('folder.zip'))
    print (p.load())
    print (p.list_plugins())
    #~ print p.list_online()
    
    
    
    
    #~ assert p.list_plugins(only_active=True) == []
    #~ p.activatePluginByID('Channels.Folder')
#~ 
    #~ print p.list_plugins(only_active=True)
    #~ p.deactivatePluginByID('Channels.Folder')
    #~ assert p.list_plugins(only_active=True) == []
    #~ print p.list_plugins(only_active=True)

