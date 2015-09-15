"""
Some API handling code.
"""

import requests
import syndicate
import syndicate.data
from syndicate.adapters.sync import HeaderAuth
from syndicate.client import ResponseError

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

    def __init__(self, api, params, signin):
        self.api = api
        self.params = params
        headers = {"X-Plex-Client-Identifier": 'plexcli'}
        if not params.get('auth_token'):
            auth = params['username'], params['password']
        else:
            headers[self.token_header] = params.get('auth_token')
            auth = None
        super().__init__(headers)
        if signin:
            self.signin(auth)

    def signin(self, auth):
        signin = requests.post('%s/users/sign_in.xml' % self.api.uri,
                               auth=auth, headers=self.headers)
        signin_xml = xmldecode(signin.content)
        if signin.status_code != 201:
            errors = [x.text for x in signin_xml.iter('error')]
            raise AuthFailure('\n'.join(errors) or signin.text)
        self.api.state['auth'] = auth = {
            "token": signin_xml.attrib['authenticationToken'],
            "username": signin_xml.attrib['username'],
            "email": signin_xml.attrib['email']
        }
        self.headers[self.token_header] = auth['token']


class PlexService(syndicate.Service):

    site = 'https://plex.tv'

    def default_data_getter(self, response):
        if response.error:
            raise response.error
        elif response.http_code not in (200, 201):
            raise ResponseError(response)
        else:
            return response.content

    def __init__(self, state):
        self.state = state
        super().__init__(uri='<reset_by_connect>', serializer='xml',
                         trailing_slash=False)

    def multi_connect(self, *args, **kwargs):
        """ Try connecting with a list of urls.  If none work we abort but
        return to our original state first. """
        uri_save = self.uri
        auth_save = self.adapter.auth
        try:
            self._multi_connect(*args, **kwargs)
        except BaseException as e:
            self.uri = uri_save
            self.adapter.auth = auth_save
            raise e

    def _multi_connect(self, urls, verbose=False, **auth):
        printer = print if verbose else lambda *_, **__: None
        for x in urls:
            printer("Trying connection to %s: " % x, end='', flush=True)
            try:
                self.connect(x, signin=False, **auth)
                self.get(timeout=1)  # Force connection attempt as test.
                printer('SUCCESS')
                break
            except IOError:
                printer('FAIL')
        else:
            raise IOError("ERROR: Could not connect to server(s)")

    def connect(self, uri, signin=True, **auth_params):
        self.uri = uri or self.site
        self.authenticate(auth_params, signin)

    def authenticate(self, params, signin):
        auth = PlexAuth(self, params, signin)
        self.adapter.auth = auth

    def do(self, *args, **kwargs):
        """ Wrap some session and error handling around all API actions. """
        try:
            return super().do(*args, **kwargs)
        except ResponseError as e:
            self.handle_error(e)

    def handle_error(self, error):
        """ Pretty print error messages and exit. """
        raise SystemExit("Error: %s" % error)
