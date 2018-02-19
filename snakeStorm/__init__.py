"""
Storm API Library

An attempt at a psuedo-clean room implementation of a Storm API Library to learn python

Jason Gillman Jr. <jason@rrfaae.com>
"""
import json
import requests

__all__ = ['Client']

APIVERSION = 'bleed'
APIBASE = {
    'public': 'https://api.stormondemand.com',
    'internal': 'https://api.int.liquidweb.com',
}
APIPORT = 443

DOCBASE = {
    'public': 'https://cart.liquidweb.com/storm/api/docs',
    'internal': 'https://billing.int.liquidweb.com/mysql/content/admin/api/internal/docs',
}


def get_api_methods(api_version=APIVERSION, environment='public', need_creds=False, creds=None):
    """
    Return a dictionary of methods and associated parameters and outputs
    """

    method_dict = {}
    request_args = {
        'url': DOCBASE[environment] + '/' + api_version + '/docs.json'
    }
    if need_creds:
        request_args['auth'] = creds
    api_docs = requests.get(**request_args).json()
    for group_name, group in api_docs.items():
        for method_name, method_specs in group['__methods'].items():
            full_method = group_name.lower() + '/' + method_name.lower()
            method_dict[full_method] = {
                'description': method_specs['__description'],
                'parameters': [],
                'outputs': [],
            }

            for param in (method_specs['__input'] or {}).keys():
                method_dict[full_method]['parameters'].append(param)

            for output in (method_specs['__output'] or {}).keys():
                method_dict[full_method]['outputs'].append(output)

    return method_dict


class Client:
    """
    The main Client class
    """
    def __getattr__(self, item):
        pass

    def __init__(self, username, password, api_version=APIVERSION, api_base=APIBASE['public'], api_port=APIPORT,
                 environment='public', need_doc_creds=False):
        self.username = username
        self.password = password
        self.environment = environment
        self.api_version = APIVERSION
        self.base_uri = api_base + ':' + str(api_port) + '/' + api_version
        self.api_methods = get_api_methods(self.api_version, self.environment, creds=(self.username, self.password),
                                           need_creds=need_doc_creds)
        self.endpoint = MethodGroup()

        # Build out the endpoints
        for method, method_data in self.api_methods.items():
            method_components = method.split('/')
            current_location = self.endpoint

            # Build the "groups"
            while len(method_components) > 1:
                component = method_components.pop(0)
                if not hasattr(current_location, component):
                    setattr(current_location, component, MethodGroup())
                current_location = getattr(current_location, component)

            # Actual Method
            component = method_components.pop(0)
            setattr(current_location, component, Method(
                username=self.username,
                password=self.password,
                base_uri=self.base_uri,
                method_path=method,
                method_definition=method_data
            ))


class Method:
    """
    Method Class
    """
    def __call__(self, **kwargs):
        return self.request(**kwargs)

    def __init__(self, username, password, base_uri, method_path, method_definition):
        self._username = username
        self._password = password
        self._call_uri = base_uri + '/' + method_path

        self.description = method_definition['description']
        self.parameters = {}
        self.raw_result = None
        self.result = None
        self.result_text = None
        self.request_error = False

    def set_params(self, **kwargs):
        """
        Set the method parameters
        Don't clear if nothing entered
        """
        if len(kwargs) > 0:
            self.parameters = kwargs

    def clear_params(self):
        """
        Clear out set parameters
        """
        self.parameters = {}

    def request(self, **kwargs):
        """
        Make the API request
        Return whether the request was successful or not
        """
        request_args = {
            'url': self._call_uri,
            'auth': (self._username, self._password),
        }
        if len(self.parameters) > 0:
            request_args['data'] = json.dumps({'params': self.parameters})

        # kwargs will override
        if len(kwargs) > 0:
            request_args['data'] = json.dumps({'params': kwargs})

        self.raw_result = requests.post(**request_args)
        self.result_text = self.raw_result.text

        try:
            self.result = self.raw_result.json()
            self.request_error = (self.raw_result.status_code != requests.codes.ok) or 'error' in self.result
        except Exception:
            self.request_error = True

        return not self.request_error


class MethodGroup:
    """
    This is just an empty definition to facilitate creating the "grouping" attributes
    """
    pass
