import six
class templator_wrapper:
    def __init__(self, r):
        self.renderer = r

    def __getattr__(self, key):
        def wrapper(*args, **kwargs): 
            return self.__return_body_(key,*args,**kwargs)
        return wrapper

    def __return_body_(self,template,*args,**kwargs):
        exec ("renderfunc = self.renderer.%s"%template)
        if six.PY2:
            return renderfunc(*args, **kwargs).__body__
        else:
            return locals()['renderfunc'](*args,**kwargs).__body__
