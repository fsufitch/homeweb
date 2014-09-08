import json, memcache

DEFAULT_CONFPATH = '/etc/homeweb.json'
CONF = None

def get_config(generate=False, confpath=None):
    global CONF
    if not CONF:
        if not generate:
            raise Exception("Config not initialized!")
        else:
            if not confpath:
                confpath = DEFAULT_CONFPATH
            CONF = Configuration(confpath)
    return CONF

class Configuration(object):
    def __init__(self, confpath):
        self.memcache = None
        with open(confpath) as f:
            self.raw = json.loads(f.read())

    def get(self, *args):
        if not args:
            raise TypeError("Must specify at least one configuration path argument")
        current_conf = self.raw
        for arg in args:
            current_conf = current_conf.get(arg)
            if not current_conf:
                return None
        return current_conf

    def get_memcache_client(self):
        if not self.memcache:
            servers = self.get('memcache', 'servers')
            if not servers:
                servers = ['localhost']
            self.memcache = memcache.Client(servers)
        return self.memcache