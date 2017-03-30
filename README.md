# disqust

Disqus API client.

The [Disqus API](https://disqus.com/api/docs/) is super-simple; you don't need their approved client, which is broken and lacks documentation of its arcane intended usage.

You probably don't even need this library.
Just creating a [`requests.Session`](http://docs.python-requests.org/en/master/user/advanced/#session-objects) object and setting `session.params = {'api_key': '...'}` would get you pretty far.
In fact, that is practically all that happens when using this library's `disqust.Client(api_key='...')` constructor.

But there are a couple of handy features this library provides:

* Automatic error raising and JSON parsing, via `client.json()`
* Iterating over successive pages, via `client.iter_results()`
* Storing a (fixed-length queue of) responses, which enables the `client.rate_limit_remaining` helper and other debugging niceties.


## Install

[![PyPI version](https://badge.fury.io/py/disqust.svg)](https://pypi.python.org/pypi/disqust)

With [`pip`](https://pip.pypa.io/en/stable/):

    pip install -U disqust

With [`setuptools`](https://github.com/pypa/setuptools):

    easy_install -U disqust

In either case, use `-U` / `--upgrade` to upgrade to the latest version in case you've already installed an older one.


## Example

We'll use the standard public API key that Disqus uses for its embedded integrations all over the web:

    export DISQUS_API_KEY=E8Uh5l5fHZ6gD8U3KycjAIAk46f68Zw7C6eW8WSjZvCLXebZ7p0r1yrYDrLilk2F

(I don't know if this is legit or condoned or reliable, but you can grab that key from any XHR request on any webpage that embeds Disqus comments.)

Then, start a Python REPL and configure the `client` instance:

    import os
    import disqust
    client = disqust.Client(api_key=os.environ['DISQUS_API_KEY'])

Show channel details (lots of fields manually elided from response):

    client.json('channels/details', channel='discussdisqus')
    >>> {u'code': 0,
         u'response': {u'adminOnly': False, u'dateAdded': u'2014-09-16T05:20:15',
          u'enableCuration': False, u'hidden': False, u'id': u'2', u'isAggregation': False,
          u'isCategory': False, u'name': u'Discuss Disqus',
          u'options': {u'banner_color': u'gray', u'banner_timestamp': 1476228709,
           u'categories': {u'API': u'Communicate with Disqus data from within your application.'},
           u'coverImage': {u'cache': u'//media.disquscdn.com/home/discussdisqus.jpg'},
           u'description': u'Ongoing topics of discussion about the Disqus product',
           u'favicon': u'//media.disquscdn.com/home/discussdisqus_favicon.png',
           u'modEmail': u'discuss-disqus@disqus.com',
           u'primaryTopics': [{u'description': u'Questions about how to install Disqus on your site.',
             u'displayName': u'Installation', u'identifier': u'installation'}]},
          u'owner_id': u'21035893',
          u'primaryForum': {u'category': u'Tech', u'createdAt': u'2014-08-29T15:49:20.880158',
           u'daysAlive': 90, u'daysThreadAlive': 90,
           u'description': u'<p>Ongoing topics of discussion about the Disqus product</p>',
           u'disableDisqusBranding': False, u'founder': u'164577566',
           u'guidelines': u'<p>You\u2019ve made it to Discuss Disqus \u2013\u2013 the go-to place ...',
           u'id': u'channel-discussdisqus',
           u'language': u'en', u'name': u'Discuss Disqus', u'settings': {u'adsEnabled': False},
           u'signedUrl': u'http://discussdisqus.disq.us',
           u'twitterName': u'disqus',
           u'url': u'http://discussdisqus.disq.us'},
          u'slug': u'discussdisqus'}}

Show user details (for the owner of the `discussdisqus` channel we just fetched):

    client.json('users/details', user='21035893')
    >>> {u'code': 0,
         u'response': {u'about': u"Product Support @Disqus \u2013\u2013 I'm in your inbox, ...",
          u'avatar': {u'isCustom': True,
           u'permalink': u'https://disqus.com/api/users/avatars/iamfrancisyo.jpg'},
          u'disable3rdPartyTrackers': False,
          u'id': u'21035893',
          u'isAnonymous': False,
          u'isPowerContributor': False,
          u'isPrimary': True,
          u'isPrivate': False,
          u'joinedAt': u'2012-01-10T21:38:08',
          u'location': u'San Francisco, CA',
          u'name': u'Daniel',
          u'numFollowers': 1225,
          u'numFollowing': 164,
          u'numForumsFollowing': 153,
          u'numLikesReceived': 2105,
          u'numPosts': 2071,
          u'profileUrl': u'https://disqus.com/by/iamfrancisyo/',
          u'reputation': 6.3932899999999995,
          u'reputationLabel': u'High',
          u'username': u'iamfrancisyo'}}

Fetch all the threads in a forum (this can take 5-7 minutes!) ... apparently there's no `channels/listThreads` endpoint like there is `forums/listThreads`, nor a `channel=xyz` parameter for the `threads/list` endpoint, but we can use the forum parameter like so:

    threads = list(client.iter_results('threads/list', forum='channel-discussdisqus', limit=100))
    len(threads)
    >>> 13357

Print the 10 most recent threads:

    for thread in threads[:10]:
        print('[{}] {}'.format(thread['createdAt'], thread['title']))
    >>> [2017-03-30T17:41:56] Bug Reports & Feedback: Comment migration fails for single page
    >>> [2017-03-30T16:48:08] Bug Reports & Feedback: Why are my comments being marked as spam?  Please help me!
    >>> [2017-03-30T15:54:39] Bug Reports & Feedback: Spam redirects In the Disqus
    >>> [2017-03-30T15:43:08] Bug Reports & Feedback: Duplicated sections to comment after Disqus installation
    >>> [2017-03-30T15:21:03] Admin: How do I comment as my site?
    >>> [2017-03-30T15:01:54] Admin: Forgot login
    >>> [2017-03-30T13:08:37] Admin: Transferring a community?
    >>> [2017-03-30T10:45:47] Embed: Comments disappeared in my site but present in the Community and on site Disqus
    >>> [2017-03-30T10:04:32] Installation: Import old comment is not working on Blogger
    >>> [2017-03-30T06:23:04] Bug Reports & Feedback: disqus not loading on new posts wordpress


## Development

Generate the corresponding PyPI-readable reStructuredText, `README.rst`:

    pandoc README.md -o README.rst

Publish to PyPI:

    python setup.py sdist bdist_wheel upload


## License

Copyright © 2017 Christopher Brown. [MIT Licensed](https://chbrown.github.io/licenses/MIT/#2017).
