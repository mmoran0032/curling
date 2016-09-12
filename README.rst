Curling Results Analysis
========================

Analyzing the outcomes of World Curling Federation tournaments available from
their `Results and Statistics website <results.worldcurling.org>`__. Requires
`requests <http://docs.python-requests.org/en/master/>`__ and
`beautifulsoup4 <https://www.crummy.com/software/BeautifulSoup/>`__.

I've written an access API for the official WCF API in python, available
`here <https://github.com/mmoran0032/wcf>`__. Since it accesses the database
through official means, you will need to get a username and password from the
WCF before you can use it.


About
-----

I would like to determine if the outcomes of the bracket play in curling events
can be determined by the results of the preliminary round-robin play *without*
using player, team, or country modifiers (so predicting Canada to win every
time doesn't count). This analysis focuses on "macro"-strategy, so the final
results of each end, instead of shot selection, accuracy, and ice condition
considerations, for its model features.

Primary analysis is forthcoming.
