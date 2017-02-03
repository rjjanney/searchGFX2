# searchGFX2
Searches a directory listing file and filters results

Our graphics computers have their main storage on somewhat fragile fibre-linked servers, running just on the edge of reliability. We weren't allowed to index the drives, so search was impossible. Originally we were using a 3rd party app that was incredibly slow.

I decided to cache a list of all files using a simple cron job, once a day at 3am. The I developed a python program to search that data. So far the info cached is filename only. In the future I'd like to capture date/time created and owner info.

The latest version uses tkinter for a gui. Various regex searching and cacheing methods to do double term AND OR and NOT searches, and filter via filetype (solely uses 3 letter extension).
