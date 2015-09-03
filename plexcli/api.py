"""
Some API handling code.
"""

import requests
import syndicate
import syndicate.client
import syndicate.data
from syndicate.adapters.sync import HeaderAuth

xmldecode = syndicate.data.serializers['xml'].decode

# CRAZY DEBUG XXX
def debug():
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    import logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
#debug()
# /CRAZY DEBUG XXX


class AuthFailure(SystemExit):
    pass


class PlexAuth(HeaderAuth):
    """ Get the auth token by hitting the sign_in.xml endpoint. """

    token_header = 'X-Plex-Token'

    def __init__(self, api, params):
        self.api = api
        self.params = params
        headers = {"X-Plex-Client-Identifier": 'plexcli'}
        if not params.get('auth_token'):
            auth = params['username'], params['password']
        else:
            headers[self.token_header] = params.get('auth_token')
            auth = None
        print(params)
        print(headers)
        signin = requests.post('%s/users/sign_in.xml' % self.api.uri,
                               auth=auth, headers=headers)
        signin_xml = xmldecode(signin.content)
        if signin.status_code != 201:
            errors = [x.text for x in signin_xml.iter('error')]
            raise AuthFailure('\n'.join(errors))
        api.state['auth'] = auth = {
            "token": signin_xml.attrib['authenticationToken'],
            "username": signin_xml.attrib['username'],
            "email": signin_xml.attrib['email']
        }
        headers[self.token_header] = auth['token']
        super().__init__(headers)


class PlexService(syndicate.Service):

    site = 'https://plex.tv'

    def default_data_getter(self, response):
        if response.error:
            raise response.error
        else:
            return response.content

    def __init__(self, state):
        self.state = state
        super().__init__(uri='<reset_by_connect>', serializer='xml',
                         trailing_slash=False)

    def connect(self, uri, auth_params):
        self.uri = uri or self.site
        self.authenticate(auth_params)

    def authenticate(self, params):
        auth = PlexAuth(self, params)
        self.adapter.auth = auth

    def do(self, *args, **kwargs):
        """ Wrap some session and error handling around all API actions. """
        try:
            return super().do(*args, **kwargs)
        except syndicate.client.ResponseError as e:
            self.handle_error(e)

    def handle_error(self, error):
        """ Pretty print error messages and exit. """
        print('XXX: handle error', error)
        print('XXX: handle error', error)
        print('XXX: handle error', error)
        raise SystemExit("Error: %s" % error)
