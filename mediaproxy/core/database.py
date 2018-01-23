import web
import os
import traceback
import logging
logger = logging.getLogger('Database')
class Database:
    def __init__(self, config):
        self.config = config
        self.db = None
        
    def load(self):
        if not self.config.get('database', 'dbtype'):
            return False
            
        mode = self.config.install_check()
        databasepath = self.config.pathes_get(mode)[0]
        
        try:
            dbtype = self.config.get('database', 'dbtype')
            dbname = self.config.get('database', 'dbname')
            host = self.config.get('database', 'host')
            port = self.config.get('database', 'port')
            socket = self.config.get('database', 'socket')
            user = self.config.get('database', 'user')
            password = self.config.get('database', 'password')

            logger.info('Database Type: %s'%dbtype)

            if dbtype == 'sqlite':
                self.db = web.database(dbn=dbtype,db=os.path.join(databasepath,'database.db'))
            else:
                self.db = web.database(dbn=dbtype,db=dbname, host=host, user=user, pw=password)
            
            #~ sql = "CREATE TABLE IF NOT EXISTS settings (setting TEXT, value TEXT)"
            #~ self.database.query(sql)
            sql = "CREATE TABLE IF NOT EXISTS channels (CID TEXT, NAME TEXT, TYPE TEXT, ID TEXT, PATH TEXT, LOGIN TEXT, ACTIVE BOOL)"
            self.db.query(sql)
            logger.info('Loaded Database (%s)'%dbtype)
            return True
        except:

            traceback.print_exc()
            return False
