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
