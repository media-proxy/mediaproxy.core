#~ # coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import with_statement

# SQLAlchemy, yapsy,bottle

import os
import uuid
import logging
from .logger import Logger
from .config import Config
from .plugin_manager import Plugins
import base64
logger = logging.getLogger('core')



class Core:
    plugins = None
    def __init__(self,datapath='data',log=None,level=None):

        if not log:
            log = 'stream'
            
        if not level:
            level = 1
        
        if log == 'stream':
            logginghandler = Logger()
            logginghandler.create_stream_logger(level=level)

        #Defining Pathes
        workingpath = os.path.dirname(os.path.realpath(__file__))
        self.workingpath = workingpath

        logger.info('Startup Core')
        logger.info('Workingpath: %s'%workingpath)

        ### Config
        if datapath:
            self.config = Config(datapath,'MediaProxy')
        else:
            self.config = Config(workingpath,'MediaProxy')

        if not self.config.mode:
            logger.info('Fresh Start, No Config File')
        else: 
            logger.info('Config in state: %s'%self.config.mode)

        ### Import dependencies requires extlibs
        from .plugin_manager import Plugins
        from .database import Database
        from fs.mountfs import MountFS

        ### Plugins
        if self.config.mode:
            self.plugins = Plugins(self.config.cfg,loadpathes=[os.path.join(datapath,'plugins')])
            
        self.filesystem = MountFS()
        
        ###Database
        self.database = Database(self.config)
        self.database.load()
        self.channels_populate()
        
    def channel_get(self,ctype=None):
        
        if not ctype:
            return self.filesystem
            
        else:
            
            from fs.mountfs import MountFS
            channel = MountFS()
            
            for path,fs in self.filesystem.mounts:

                
                if fs.exists(u'/'):
                    if 'mediaproxy.media' in fs.getinfo(u'/').raw:
                        logger.info('Check Channel: %s - %s'%(path,fs.getinfo(u'/').raw['mediaproxy.media']['type']))
                        if fs.getinfo(u'/').raw['mediaproxy.media']['type'] == ctype:
                            channel.mount(path,fs)

            return channel
            
        

    def channels(self):
        return self.filesystem.listdir(u'/')


    def load_meta(self,path,filesystem=None):
        logger.info('path: %s'%path)
        if filesystem:
            meta = filesystem.getinfo(path,'media')
        else:
            meta = self.filesystem.getinfo(path,'media')
        
        #~ print self.filesystem.getinfo(path,'media').raw
        filemeta = {}
        filemeta['path'] = path
        if meta.get('media','files'):
            filemeta['files'] = meta.get('media','files')
        else:
            filemeta['files'] = [path]
        filemeta['id'] = meta.get('media','id')
        filemeta['title'] = meta.get('media','title')
        filemeta['sorttitle'] = meta.get('media','sorttitle')
        filemeta['originaltitle'] = meta.get('media','originaltitle')
        filemeta['year'] = meta.get('media','year')
        filemeta['rating'] = meta.get('media','rating')
        filemeta['outline'] = meta.get('media','outline')
        filemeta['plot'] = meta.get('media','plot')
        filemeta['runtime'] = meta.get('media','runtime')
        filemeta['genre'] = meta.get('media','genre')
        filemeta['set'] = meta.get('media','set')
       
        if meta.get('media','thumb'):
            filemeta['thumb'] = base64.b64encode(meta.get('media','thumb'))
        else:
            filemeta['thumb'] = None
           
        if meta.get('media','plakat'):
            filemeta['plakat'] = base64.b64encode(meta.get('media','plakat'))
        else:
            filemeta['plakat'] = None
           
        filemeta['size'] = meta.get('media','size')


        if meta.get('meta','extension') and meta.get('media','mime'):
            filemeta['mime'] = meta.get('media','mime')
            filemeta['extension'] = meta.get('media','extension')
        elif meta.get('media','extension'):
            filemeta['extension'] = meta.get('media','extension')
            filemeta['mime'] = mime.guess_type(filemeta['extension'])
        elif meta.get('media','mime'):
            filemeta['mime'] = meta.get('media','mime')
            filemeta['extension'] = mime.guess_extension(filemeta['mime'])
        else:
            filemeta['mime'] = None
            filemeta['extension'] = None
        return filemeta

            
    def channels_populate(self):
        
        if not self.database.db:
            return
        channellist = list(self.database.db.select('channels'))
        
        for c in channellist:
            name = c.NAME
            cid = c.CID
            categorie, pluginname = c.ID.split('.')
            cplugin = self.plugins.getPluginByName(pluginname,categorie)
            if c.TYPE:
                categorie, pluginname = c.TYPE.split('.')
                splugin = self.plugins.getPluginByName(pluginname,categorie)
                
            try:
                fs = cplugin.plugin_object.load(c.PATH,c.LOGIN)
                if c.TYPE:
                    gfs = splugin.plugin_object.load(fs)
        #~ 
                    # ~ gfs.setinfo(u'',{'cid':cid})
                    # ~ gfs.setinfo(u'',{'status':'online'})
                else:
                     gfs = fs

                self.filesystem.mount('/'+name,gfs)
                    
            except:
                self.filesystem.makedir(u'/%s'%name)
                pass
        #~ 
        
    def setup_check(self):
        logger.info('Installed, %s'%self.config.mode)
        
        if not self.config.mode:
            return False
            
        if not self.config.get('database','dbtype'):
            return False
            
        return True

    def setup(self,mode):
        
        if self.setup_check():
            raise IOError('Already installed')
            
        if mode == 'portable':
            self.config.set('database','dbtype','sqlite')
            self.config.save('portable')

        self.plugins = Plugins(self.config.cfg)
        self.database.load()
        

    def plugins_list(self,categorie=None,only_active=False):
        return self.plugins.list_plugins(categorie=categorie,only_active=only_active)
        
    def plugin_activate(self,id):
            self.plugins.activatePluginByID(id)
            
    def plugin_deactivate(self,id):
            self.plugins.deactivatePluginByID(id)
            

    def channel_add(self,name,pluginid,scraperid,path,login):
        # ~ assert type(name) == unicode
        # ~ assert type(path) == unicode
        categorie, pluginname = pluginid.split('.')
        cplugin = self.plugins.getPluginByName(pluginname,categorie)
        if scraperid:
            categorie, pluginname = scraperid.split('.')
            splugin = self.plugins.getPluginByName(pluginname,categorie)
        
        cid = str(uuid.uuid4())
        
        fs = cplugin.plugin_object.load(path,login)
        if scraperid:
            gfs = splugin.plugin_object.load(fs)
        else:
            gfs = fs

        # ~ fs.setinfo(u'',{'cid':cid})
        

        if not gfs.isdir(u'/'):
            raise IOError('Filesystem not accessable')
        try:
            self.filesystem.mount(name,gfs)
        except:
            fs.close()
            raise IOError('Filesystem not includable')


        with self.database.db.transaction():
            self.database.db.insert('channels',CID=cid, NAME=name, TYPE=scraperid,  ID=pluginid, PATH=path, LOGIN=login, ACTIVE=1)
            
    def channel_info(self, path):
        return self.filesystem.getinfo(path).raw['mediaproxy']
        

class MixedFS:
    def __init__(self, fsdict):
        self.fsdict = fsdict
        
    def __getattr__(self, key):
        def wrapper(path, *args, **kwargs):
            
            
            
            splitpath = os.path.split(path)
            fs = self.fsdict[u'/'.join(splitpath[:2])]
            sub_path = u'/'.join(splitpath[:2])

            return fs(sub_path,*args,**kwargs)
        return wrapper
        

