#~ # coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import with_statement

from six.moves.urllib.request import pathname2url

import sys
import traceback
import logging
import locale
import os

from ..core import Core
mediaproxy = Core()
from .translator import Translator
from .templator_wrapper import templator_wrapper as Templator_Wrapper
from web import template, form
from bottle import route, run, redirect, static_file, get, post,request,response

logger = logging.getLogger('Server')

locale_enc = locale.getdefaultlocale()[1]
#Translator
translator = Translator(mediaproxy.workingpath,mediaproxy.config.get('main','language'))
_ = translator.translate

def pathencode(path):
    return pathname2url(path.encode('utf-8'))
#Render

template_globals = {}
template_globals['_'] = _
template_globals['path2url'] = pathencode

serverpath = os.path.dirname(os.path.realpath(__file__))

if mediaproxy.setup_check():
    render = Templator_Wrapper(template.render(os.path.join(serverpath,'template'),base='base',globals=template_globals))
else:
    render = Templator_Wrapper(template.render(os.path.join(serverpath,'template'),globals=template_globals))

def format_exception(exc):
    exc_string = ''.join(exc)
    exc_string = exc_string.decode(locale_enc)
    exc_string = exc_string.encode('ascii', 'xmlcharrefreplace')
    exc_string = exc_string.replace('\n','<br>')
    return exc_string

@route('/')
def root():
    if not mediaproxy.setup_check():
        redirect("/setup_language")
    redirect("/channels/")
        
@get('/setup_language')
def setup_lang_get():
    return render.setup_lang(['German'])

@post('/setup_language')
def setup_lang_post():
    lang = request.forms.get('language')
    translator.set_language(lang)
    redirect("/setup_mode?language=%s"%lang.lower())

@get('/setup_mode')
def setup_mode_get():
    return render.setup_mode()

@post('/setup_mode')
def setup_mode_post():
    mode = request.forms.get('mode')
    mediaproxy.setup(mode)
    mediaproxy.config.set('main','language',translator.get_language())
    mediaproxy.config.save()
    redirect("/")

@get('/channel_add')
def channel_add_get():
    basedata = {'folderlist':mediaproxy.channels()}
    cplugins = mediaproxy.plugins_list(categorie='Channels')
    splugins = mediaproxy.plugins_list(categorie='Scrapers')
    return render.channel_add(basedata,cplugins,splugins,None)
    
@post('/channel_add')
def channel_add_post():
    values = {}
    values['name'] = request.forms.get('name')
    values['path'] = request.forms.get('path')
    values['cplugin'] = request.forms.get('cplugin')
    values['splugin'] = request.forms.get('splugin')
    basedata = {'folderlist':mediaproxy.channels()}
    cplugins = mediaproxy.plugins_list(categorie='Channels')
    splugins = mediaproxy.plugins_list(categorie='Scrapers')
    try:
        mediaproxy.channel_add(values['name'],values['cplugin'],values['splugin'],values['path'],None)
        basedata['message']  = _('Channel added:') + ' %s'%values['name']
    except:
        etype, value, tb = sys.exc_info()
        basedata['error']  = str(traceback.format_exc(tb)).replace('\n','<br>')


    return render.channel_add(basedata,cplugins,splugins,values)


@route('/channels')
@route('/channels<path:path>')
def channels(path=''):
    logger.info(repr(request.urlparts))

    #path = path.decode('utf-8')
    basedata = {'path':path,'basepath':os.path.join(path, os.pardir)}
    logger.info(repr(path))
    logger.info(mediaproxy.filesystem.exists(path))
    if mediaproxy.filesystem.exists(path):
        logger.info(mediaproxy.filesystem.isdir(path))
        if mediaproxy.filesystem.isdir(path):
            try:
                clist = mediaproxy.filesystem.listdir(path)
                logger.info(repr(clist))

            except:
                basedata['error']  = format_exception(traceback.format_exc(sys.exc_info()[2]))
                clist = []
            if not path.endswith('/'):
                path = path + '/'
            return render.channel_list(basedata,pathencode(path),clist)
        else:
            try:
                meta = mediaproxy.filesystem.getinfo(path).raw
            except:
                basedata['error']  = format_exception(traceback.format_exc(sys.exc_info()[2]))
                meta = {}
            return render.channel_file(basedata,pathencode(path),meta)
    return render.notexist(basedata,pathencode(path))
    
@route('/tv')
@route('/tv<path:path>')
def tv(path=''):
    raise IOError("Not supported yet")
    channel = mediaproxy.channel_get('tv')
    basedata = {'path':path,'basepath':os.path.abspath(os.path.join(path, os.pardir))}
    basedata['error']  = 'Not Implemented jet'
    return render.notexist(basedata,path)
    
@route('/music')
@route('/music<path:path>')
def music(path=''):
    raise IOError("Not supported yet")
    channel = mediaproxy.channel_get('tv')
    basedata = {'path':path,'basepath':os.path.abspath(os.path.join(path, os.pardir))}
    basedata['error']  = 'Not Implemented jet'
    return render.notexist(basedata,path)
    
@route('/pictures')
@route('/pictures<path:path>')
def pictures(path=''):
    raise IOError("Not supported yet")
    channel = mediaproxy.channel_get('tv')
    basedata = {'path':path,'basepath':os.path.abspath(os.path.join(path, os.pardir))}
    basedata['error']  = 'Not Implemented jet'
    return render.notexist(basedata,path)
    
@route('/series')
@route('/series<path:path>')
def series(path=''):
    raise IOError("Not supported yet")
    channel = mediaproxy.channel_get('tv')
    basedata = {'path':path,'basepath':os.path.abspath(os.path.join(path, os.pardir))}
    basedata['error']  = 'Not Implemented jet'
    return render.notexist(basedata,path)
    
@route('/movies')
@route('/movies<path:path>')
def movies(path=''):
    channel = mediaproxy.channel_get('movie')
    basedata = {'path':path,'basepath':os.path.abspath(os.path.join(path, os.pardir))}
    try:
        if channel.exists(path):
            if channel.isdir(path):
                try:
                    clist = channel.listdir(path)
                    clist.sort()
                except:
                    basedata['error']  = format_exception(traceback.format_exc(sys.exc_info()[2]))
                    clist = []
                if not path.endswith('/'):
                    path = path + '/'
                return render.movie_list(basedata,path,clist)
            else:
                try:
                    meta = mediaproxy.load_meta(path,filesystem=channel)
                    if not 'title' in meta:
                        meta['title'] = os.path.basename(path)
                except:
                    basedata['error']  = format_exception(traceback.format_exc(sys.exc_info()[2]))
                    meta = {}
                return render.movie_file(basedata,path,meta)
    except:
        basedata['error']  = format_exception(traceback.format_exc(sys.exc_info()[2]))
    return render.notexist(basedata,path)
    
@route('/download<path:path>')
def download(path):
    #path = path.decode('utf-8')
    
    if mediaproxy.filesystem.isfile(path):
        response.set_header('Content-Length', mediaproxy.filesystem.getsize(path))
        response.set_header('Content-Type', 'application/octet-stream')
        fo = mediaproxy.filesystem.open(path,'rb')
        return fo
        

    #~ return render.listdir(basedata,path,clist)

@route('/images/<path:path>')
def images(path):
    print (path)
    return static_file(path, root='images/',mimetype='image/png')

@get('/favicon.ico')
def favicon():
    return static_file('server.ico', root='images/',mimetype='image/vnd.microsoft.icon')


