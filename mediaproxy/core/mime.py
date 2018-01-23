import mimetypes
mimetypes.init()

html5_types = []
html5_types.append('video/mp4')
html5_types.append('video/ogg')
html5_types.append('video/webm')
html5_types.append('audio/aac')
html5_types.append('audio/mp4')
html5_types.append('audio/mpeg')
html5_types.append('audio/ogg')
html5_types.append('audio/wav')
html5_types.append('audio/webm')


types = []
types.append(('video/x-matroska','.mkv'))
types.append(('text/x-nfo','.nfo'))

for entry in types:
    mimetypes.add_type(*entry)
    
    
def guess_extension(mime):
    if not mime:
        return None
    return mimetypes.guess_extension(mime,strict=False)
    
def guess_type(name):
    if not name:
        return None
    if '.' in  name:
        if name.startswith('.'):
            name = 'test%s'%name
    else:
        return None
    return mimetypes.guess_type(name,strict=False)[0]
    
    
def get_player(mime):
    if mime in html5_types:
        return 'html5_player'
    


#if __name__ == '__main__':
    #print guess_extension('video/x-matroska')
    #print guess_type('.avi')
    #print guess_type('test.mkv')
    


