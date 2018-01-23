#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from six.moves import configparser
import codecs
import logging
logger = logging.getLogger('translator')

class Translator:
    def __init__(self, workingpath, language=None):
        self.languagepath = os.path.join(workingpath,'languages')
        self.language = None
        self.config = None
        if language:
            self.set_language(language)
            
            
    def set_language(self,language):
            logger.info('Setting Language to %s'%language)
            language = language.lower()
            langfile = os.path.join(self.languagepath,"%s.lang"%language)
            if not os.path.isfile(langfile):
                return
            
            self.config = ConfigParser.RawConfigParser()
            with codecs.open(langfile,'r', "utf8") as langfp:
                self.config.readfp(langfp)
                
            self.language = language
        
    def translate(self,string):
        logger.debug('Translate %s'%string)
        #~ string = string.encode('utf-8')
        if not self.config:
            logger.info('No Config')
            return string
            
        if not self.config.has_section('translations'):
            logger.info('No Section')
            return string
            
        if not self.config.has_option('translations',string):
            logger.warning('Not Translated to %s "%s"'%(self.language,string))
            return string
        
        trans = self.config.get('translations',string)
        logger.debug('Return %s'%trans)
        return trans
        
    def list_translations(self):
        languages = []
        files = os.listdir(self.languagepath)
        for f in files:
            if f.endswith('.lang'):
                languages.append(f.split('.')[0].title())
        return languages
        
    def get_language(self,local=False):
        if not self.config:
            return None
        if local:
            return self.config.get('meta','name')
        else:
            return self.language.title()
        
