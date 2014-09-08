import random, string

from jinja2 import Environment, PackageLoader

TEMPLATE_ENVIRONMENT = None
def init_template_environment():
    global TEMPLATE_ENVIRONMENT
    if not TEMPLATE_ENVIRONMENT:
        TEMPLATE_ENVIRONMENT = Environment(loader=PackageLoader("homeweb", "templates"))

class apply_template(object):
    ''' Apply template decorator '''
    def __init__(self, tmpl_name):
        if not TEMPLATE_ENVIRONMENT:
            init_template_environment()
        self.template = TEMPLATE_ENVIRONMENT.get_template(tmpl_name)

    def __call__(self, func):
        def _apply_template(*args, **kwargs):
            result = func(*args, **kwargs)
            if type(result) is str:
                return result
            elif type(result) is dict:
                return self.template.render(**result)
            else:
                return result
        return _apply_template

def write_return(func):
    ''' Apply self.write to whatever function is decorated '''
    def _write_return(_self, *args, **kwargs):
        result = func(_self, *args, **kwargs)
        if type(result) in (str, bytes):
            _self.write(result)
    return _write_return

DEFAULT_UID_CHARS = string.ascii_lowercase + string.digits
def get_random_uid(is_good=None, length=5, chars=[]):
    chars = chars or DEFAULT_UID_CHARS
    if is_good is None:
        is_good = lambda x: True  # If no "good" condition given, assume it's fine
    uid = ''
    while not (uid and is_good(uid)):
        uid = []
        for i in range(length):
            uid.append(random.choice(chars))
        uid = ''.join(uid)
    return uid