General Notes
=============

Logistic regression
-------------------

-   Score diff can't be my only variable... Need to include hammer, ends
    remaining (probably need to estimate based on previous games), and
    if I include historical data, pre-game win probabilities.
-   Last variable above probably only makes sense for bracket portion of
    tournament, so for round robin games all pre-game win probabilities
    would be set to 0.5
    -   But, then the model wouldn't learn anything about it...This is
        probably a harder problem to determine than I am initially thinking


Data storage
------------

-   Finalize what you're actually going to be saving! I don't know how it
    should be broken up, but look at Kaggle's NCAA March Machine Learning
    Madness to see what they did.


Ratings
-------

-   To get pre-game win probabilities, rank teams competing in the event
-   Since teams can change from event to event, and to be fair, start all
    teams in an event with the same initial rating and update it as they
    win or lose games
    -   Roughly follow ELO or similar ratings/updating schemes, since they
        are mathematically backed and I don't have to think about devising
        my own system, which helps
-   Pre-win probabilities will then be 50-50 for any game where neither
    team has played a game yet, and change based on the relative ratings of
    the two teams


Game state prediction
---------------------

-   Logistic regression over multiple parameters: current stone diff, if team
    has hammer next end, number of ends played
-   Could use ELO as an additional parameter, giving base win probability (zero
    stone diff, zero ends played, LSFE) if included
-   ELO gives rough win probability (1500 vs 1000 -> 0.93,
    1050 vs 1000 -> 0.54, etc)
    -   Decent as a starting point, but due to short timescale of tournaments,
        may either have to do something different or adjust k_factor
    -   Will probably create models with slightly different ELO parameters to
        look at dependence and decide what's the best


Update 2017-09-13
=================

Here's the goal for this work:
-   Pull WCF data and set up database that contains game and end information
-   Build predictive engine for likelihood of winning an individual game based
    on the current game state (scores, hammer, previous ends, etc)
