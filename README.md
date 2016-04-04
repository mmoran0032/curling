Canadian Curling Association Analysis
=====================================

**Idea:** predict the outcome of the tournament games based on the outcomes and
statistics from the round-robin games of that tournament.


Details
-------

Since the Canadian Curling Association has horrible PDFs of the results
(available at
[Archive](http://www.curling.ca/championships/archived-statistics/)), here's
how I've gotten around that limitation, using a few websites.

1.  Download the PDF from the website.

1.  Convert to plain text while maintaining layout:
    ```
    pdftotext -layout FILENAME.pdf NEWFILE.txt
    ```

1.  Do a visual check that everything turns out right (should be fine)


Data
----

From the individual games, I want to track (for each team involved) the
following items:

- if the team won (`won`)

- team's final score (`score`)

- final score differential (`score_diff`)

- total ends played (`num_ends`)

- number of scoring ends for the team (`scoring_ends`)

- number of scoring ends while team had hammer (`scoring_hammer`)

- number of blank ends (`blank_ends`)

- number of blank ends while team had hammer (`blank_hammer`)
