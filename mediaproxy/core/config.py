#~ # coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import with_statement

import os
import sys
import logging
from six.moves import configparser
import threading
import codecs

logger = logging.getLogger('Config')

class Config:
    def __init__(self, workingpath, name):
        self.name = name
        self.wp = workingpath
        self.datapath = None
        self.cfg = configparser.RawConfigParser()
        self.cfg.save = self.save
        self.lock = threading.Lock()
        self.mode = self.install_check()
        if self.mode:
            self.load(self.mode)
        
    def install_check(self):
        returnv = None
        datapath, inipath = self.pathes_get('portable')
        logger.debug('Check for File: %s'%inipath)
        if os.path.isfile(inipath):
            returnv = 'portable'
            
        inipath = self.pathes_get('local')[1]
        logger.debug('Check for File: %s'%inipath)
        if os.path.isfile(inipath):
            returnv = 'local'
        logger.info('Install Check returns: %s'%returnv)
        self.mode = returnv
        return returnv
        
    def load(self,mode):
        inipath = self.pathes_get(mode)[1]
        self.lock.acquire()
        self.cfg.read(inipath)
        self.lock.release()
        
    def save(self,mode=None):
        self.lock.acquire()
        if not mode:
            mode = self.mode
        
        folderpath,inipath = self.pathes_get(mode)
        logger.info('Create Folder: %s'%folderpath)
        if not os.path.isdir(folderpath):
            os.makedirs(folderpath)
        
        with codecs.open(inipath,'wb', "utf8") as inifile:
            self.cfg.write(inifile)
        
        if not self.mode:
            self.install_check()
        self.lock.release()
        
    def reset(self):
        self.cfg = configparser.RawConfigParser()
        import shutil
        pathes = []
        pathes.append(self.pathes_get('portable')[0])
        pathes.append(self.pathes_get('local')[0])
        
        for path in pathes:
            logger.info('Cleaning up %s'%path)
            shutil.rmtree(path,True)

    def pathes_get(self, mode):
        logger.info('Get Pathes %s'%mode)
        if mode == 'portable':
            folderpath = os.path.join(self.wp,'data')
            filepath = os.path.join(folderpath,'%s.ini'%self.name)
            return (folderpath,filepath)
        elif mode == 'local':
            folderpath = os.path.expanduser('~/.config/%s'%self.name)
            filepath = os.path.join(folderpath,'%s.ini'%self.name)
            return (folderpath,filepath)
        else:
            return None
            
    def set(self,section,option,value):
        if not self.cfg.has_section(section):
            self.cfg.add_section(section)
        self.cfg.set(section,option,value)

    def get(self,section,option):
        if not self.mode:
            return None
            
        if not self.cfg.has_section(section):
            return None
            
        if not self.cfg.has_option(section,option):
            return None
            
        return self.cfg.get(section,option)

    def cfg_create(self,lang):
        try:
            self.cfg.add_section(self.name)
        except:
            pass
        self.cfg.set(self.name, 'language', lang)
        
import unittest
class TestFS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import logging
        logging.basicConfig(format="[%(levelname)-7s] (%(name)s) %(asctime)s.%(msecs)-3d Thread:%(thread)s/%(module)s[%(lineno)-3d]/%(funcName)-10s  %(message)-8s ", level=logging.DEBUG)
        workingpath = os.path.dirname(os.path.realpath(__file__))
        cls._cfg = Config(workingpath,'test')
        cls._cfg.reset()
        
        
    @classmethod
    def tearDownClass(cls):
        cls._cfg.reset()


    def test_1_save_portable(cls):
        cls._cfg.save('portable')
        assert cls._cfg.install_check() == 'local'
        
    #~ def test_2_reset(cls):
        #~ cls._cfg.reset()
        #~ assert cls._cfg.install_check() == None
        
    #~ def test_3_save_portable(cls):
        #~ cls._cfg.save('local')
        #~ assert cls._cfg.install_check() == 'local'
        
    #~ def test_4_reset(cls):
        #~ cls._cfg.reset()
        #~ assert cls._cfg.install_check() == None
        
    def test_5_add_get(cls):
        cls._cfg.set('test','nr','1')
        assert cls._cfg.get('test','nr') == '1'
        cls._cfg.set('test','nr',u'1')
        assert cls._cfg.get('test','nr') == '1'
        cls._cfg.save('portable')
        
    def test_6_restart_get(cls):
        workingpath = os.path.dirname(os.path.realpath(__file__))
        cls._cfg = Config(workingpath,'test')
        assert cls._cfg.get('test','nr') == '1'
        
if __name__ == '__main__':
    unittest.main()
    #~ print  u'e' + b'\u0301'
        
        
        
        
