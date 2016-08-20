Curling Results Analysis
========================

Analyzing the outcomes of World Curling Federation tournaments available from
their `Results and Statistics website <results.worldcurling.org>`__. Requires
`requests <http://docs.python-requests.org/en/master/>`__ and
`beautifulsoup4 <https://www.crummy.com/software/BeautifulSoup/>`__.

I would like to determine if the outcomes of the bracket play in curling events
can be determined by the results of the preliminary round-robin play *without*
using player, team, or country modifiers (so predicting Canada to win every
time doesn't count). This analysis focuses on "macro"-strategy, so the final
results of each end, instead of shot selection, accuracy, and ice condition
considerations, for its model features.

Primary analysis is forthcoming.


Official API
------------

Official access to the WCF's results database must be obtained prior to using
the official API to access the information. Access follows standard REST
conventions. I am implementing this access method in ``wcfapi.py``, which only
requires the user to obtain a username and password from the WCF to proceed.

Once you have access, create a ``credentials.json`` file in the same directory
you are working in as follows::

    {
        "Username": "user.me",
        "Password": "something+else"
    }

Basic usage is as follows::

    from wcfapi import WCF
    t = WCF()
    t.load_user().connect()

So, after exploring the official API, the only additional functionality I get
is accessing the accuracy of the teams within the individual games...which I
can pull from my homebrewed API in a similar fashion. The official API access
also *cannot* give individual end information, so it is inherently *worse* for
what I need it to do.


API
---

I've written a basic API to pull the box score data from the WCF: ``wcf.py``.
Right now, it's a basic loading and converting API for just the box scores, so
I lose or don't pull information about the specific players on the team, the
location or venue, the dates it was played, or even the gender of the athletes.
I will have to pull that stuff eventually (into ``wcf.Tournament``), but for
now raw numbers seem OK. The others may require another round of exploration.

Usage is simple::

    import wcf
    t = wcf.Tournament(tournamentID)
    t.load_all_games()

    final = t.games[-1]
    print(final.teams[final.winner])

From this starting point, a lot of the "business logic" that I put into the
previous two notebooks/scripts is within this module. The aggregate data part
is still another layer on top of the access, but this should help for batch
processing.

Testing is also simple::

    nosetests tests [--with-coverage --cover-package=wcf]
