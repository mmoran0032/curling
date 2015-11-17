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