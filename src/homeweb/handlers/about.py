from ipaddress import ip_address
from tornado.web import RequestHandler

from homeweb.log import ERROR_LOG_NAME
from homeweb.util import apply_template, write_return

import logging
ERROR = logging.getLogger(ERROR_LOG_NAME)

class AboutYouHandler(RequestHandler):

    @write_return
    @apply_template('about_you.html')
    def get(self):
        ip = ip_address(self.request.remote_ip)
        user_agent = self.request.headers['user-agent']
        ERROR.info( (ip, user_agent) )

        return {'ip': ip,
                'user_agent': user_agent,
                }

class AboutMeHandler(RequestHandler):
    @write_return
    @apply_template('about_me.html')
    def get(self):
        return {}
