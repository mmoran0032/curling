Curling Results Analysis
========================

Looking at curling box scores available from the World Curling Federation's
`Results and Statistics <results.worldcurling.org>`__ website.

Currently, I am waiting to hear back about the RESTful access to the website,
so for now I am using ``requests`` and ``bs4`` (beautiful soup) to pull game
data. This is also my first real use of these two libraries, so there will be a
lot of learning going into it.

During my exploratory search (``exploratory.ipynb``), I noticed that I *could*
get the game information somewhat RESTfully without too much issue. So far, I
haven't gone too far into it, but that could easily turn into a bootstrapped
API for accessing the game data, including building up the "name to tourney
number" part.

For now, I'm going to keep working on extracting raw data rom the site to build
up a database of score information for an ML algorithm.
