import json, requests, time

from tornado.web import RequestHandler

from homeweb.config import get_config
from homeweb.util import get_random_uid
from homeweb.util import apply_template, write_return

def make_padded_id(uid):
    return "Codebox++%s" % uid

class CodeboxHandler(RequestHandler):
    ENVIRONMENTS = {
        'python2': {
            'sbtype': 'legacypython',
            'text': 'Python 2.7',
            'ace': 'ace/mode/python',
            'fname': 'test.py',
            },
        'python3': {
            'sbtype': 'python',
            'text': 'Python 3.x',
            'ace': 'ace/mode/python',
            'fname': 'test.py',
            },
        'pascal': {
            'sbtype': 'pascal',
            'text': 'Pascal (GPC)',
            'ace': 'ace/mode/pascal',
            'fname': 'test.pas',
            },
        'php5': {
            'sbtype': 'php5',
            'text': 'PHP 5',
            'ace': 'ace/mode/php',
            'fname': 'test.php',
            },
        'scala': {
            'sbtype': 'scala',
            'text': 'Scala',
            'ace': 'ace/mode/scala',
            'fname': 'test.scala',
            },
        'java8': {
            'sbtype': 'java8',
            'text': 'Java 8',
            'ace': 'ace/mode/java',
            'fname': 'test.java',
            },
        'c': {
            'sbtype': 'c',
            'text': 'C (GCC)',
            'ace': 'ace/mode/c_cpp',
            'fname': 'test.c',
            },
        }

    @write_return
    @apply_template("demos/codebox.html")
    def get(self):
        response = {}
        response['environments'] = sorted(CodeboxHandler.ENVIRONMENTS.items())
        return response

    def post(self):
        self.set_header('Content-type', 'text/plain')
        self.write('Environment ID: %s\n' % self.get_argument('env_choice'))
        self.write(self.get_argument('code'))
        code = self.get_argument('code')
        env_id = self.get_argument('env_choice')
        env = CodeboxHandler.ENVIRONMENTS[env_id]

        apiurl = get_config().get('codebox', 'api')
    
        data = {'filename': env['fname'],
                'source': code,
                'sbtype': env['sbtype']}
        
        jobsubmit = requests.post(apiurl+'job/new', data=data)
        job_id = jobsubmit.json()['job_id']

        self.write('\n-------------\n\n')
        self.write(jobsubmit.json())
        
        memcache = get_config().get_memcache_client()
        uid = get_random_uid(lambda x: not memcache.get(make_padded_id(x)))
        padded_uid = make_padded_id(uid)

        memcache.set(padded_uid, {
                'job_id': job_id,
                'result': None,
                'state': 'sent',
                'code': code,
                'env_id': env_id,
                })

        self.redirect('/demos/codebox_result/%s' % uid)
        '''
        while True:
            jobget = requests.get(apiurl+'job/get/'+job_id)
            data = jobget.json()
            if data['run_done']:
                self.write('\n============\n\n')
                self.write(data['run_result'])
                break
            else:
                time.sleep(1)
        '''

class CodeboxResultHandler(RequestHandler):
    @write_return
    @apply_template("demos/codebox_result.html")
    def get(self, uid=None):
        if not uid:
            self.set_status(400)
            return "Must specify a request ID"
        padded_uid = make_padded_id(uid)
        
        memcache = get_config().get_memcache_client()
        data = self.update_status(uid)
        if not data:
            self.set_status(404)
            return "Invalid request ID"
        
        return {
            "env": CodeboxHandler.ENVIRONMENTS[data['env_id']],
            "code": data['code'],
            "update": json.dumps({
                "error": "error" in data['state'],
                "state": data['state'],
                "result": data['result'],
                }),
            }

    @write_return
    def post(self, uid=None):
        if not uid:
            self.set_status(400)
            return "Must specify a request ID"
        data = self.update_status(uid)
        if not data:
            self.set_status(404)
            return "Invalid request ID"

        self.set_header("Content-type", "application/json")
        return json.dumps({
                "error": "error" in data['state'],
                "state": data['state'],
                "result": data['result'],
                })
    
    def update_status(self, uid):
        memcache = get_config().get_memcache_client()
        padded_uid = make_padded_id(uid)
        req_data = memcache.get(padded_uid)
        if not req_data:
            return None
        if req_data['result']:
            return req_data  #If it already has a result, it's done

        apiurl = get_config().get('codebox', 'api')

        jobget = requests.get(apiurl+'job/get/'+req_data['job_id'])
        cb_data = jobget.json()

        req_data['state'] = 'sent'
        if not cb_data['build_done']:
            req_data['state'] = 'building'
        elif not cb_data['run_done']:
            req_data['state'] = 'running'
        else:
            req_data['state'] = 'done'
            
        if cb_data['build_exception']:
            req_data['state'] = 'error/build'
            req_data['result'] = "Build exception:\n%s\n%s" % (cb_data['build_exception'], cb_data['build_result'])

        elif cb_data['run_exception']:
            req_data['state'] = 'error/run'
            req_data['result'] = "Runtime exception:\n%s" % (cb_data['run_exception'])
            
        else:
            # All is well
            if cb_data['run_done']:
                req_data['state'] = 'done'
                req_data['result'] = cb_data['run_result']['logs']

        memcache.set(padded_uid, req_data)
        return req_data
        
        
