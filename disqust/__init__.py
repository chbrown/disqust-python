# become as Python3-like as possible:
from __future__ import division, absolute_import, print_function, unicode_literals
# for HTTP communications
from requests import Session
# deque with a maxlen argument creates a fixed-length queue such that old items
# just fall off the front when new items are added
from collections import deque


class Client(object):
    def __init__(self, **params):
        '''
        Create a new requests.Session, set the default timeout to 5 seconds,
        and store the given ``params`` for merging with the params provided to
        the json() method.
        '''
        self.session = Session()
        self.session.timeout = 5
        self.default_params = params
        self.responses = deque((), 10)

    @property
    def last_response(self):
        '''
        Return the last response added to the ``responses`` deque,
        or None if no responses are available.
        '''
        if len(self.responses) > 0:
            return self.responses[-1]

    @property
    def rate_limit_remaining(self):
        '''
        Return the number of remaining API calls, according to the headers of
        the last response, or None if there are no responses or the headers do
        not indicate a limit.
        '''
        last_response = self.last_response
        if last_response is not None:
            return last_response.headers.get('X-Ratelimit-Remaining')

    def json(self, name, method='GET', **params):
        url = 'https://disqus.com/api/3.0/{}.json'.format(name)
        response = self.session.request(method, url, params=dict(self.default_params, **params))
        self.responses.append(response)
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()

    def iter_json(self, name, method='GET', **params):
        '''
        Iterate forward through pages of responses, each as would be returned by
        calling json() with the same arguments, but successively uses the 'next'
        field of the response's cursor object to formulate a new request, until
        the cursor indicates no more pages are available.

        You'll probably want to set the limit=n param, which for most things
        (posts/list, forums/listThreads) maxes out at 100, but defaults to 25.

        The cursor object looks like:

            {hasPrev: false, prev: null,
             hasNext: true, next: "1320872487989935:0:0",
             total: null}

        The API documentation notes that the 'total' field is rarely filled in.
        '''
        # It appears that the following parameters are obsolete (the API
        # documentation doesn't mention them, and they seem to all have exactly
        # the same values as the fields that the documentation does mention)
        # * more (=> hasNext)
        # * prev (=> hasPrev)
        # * id (=> next)
        while True:
            result = self.json(name, method, **params)
            yield result
            if not result['cursor']['hasNext']:
                break
            # otherwise, set the cursor parameter and continue
            params['cursor'] = result['cursor']['next']

    def iter_results(self, name, method='GET', **params):
        '''
        Paginate forward through all results, as with iter_json(), but iterate
        over the items in each page's 'response' field, instead of the full page
        objects.
        '''
        for page in self.iter_json(name, method, **params):
            for item in page['response']:
                yield item
