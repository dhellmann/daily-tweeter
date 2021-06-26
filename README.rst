===============
 daily-tweeter
===============

Schedule a series of tweets to be posted on a given day

Use the ``schedule`` command to convert a list of post messages into a
data file scheduling the posts to be published on given dates.

Use the ``publish`` command to read a schedule file and post the
update scheduled for the current date.

Posts File
==========

The input posts file should be a YAML file containing a list of
strings with the full text of the messages to be published.

::

    - "trace — Follow Program Flow https://pymotw.com/3/trace/"
    - "urllib.robotparser — Internet Spider Access Control https://pymotw.com/3/urllib.robotparser/"
    - "compileall — Byte-compile Source Files https://pymotw.com/3/compileall/"

Schedule File
=============

The generated schedule file contains a ``posts`` entry with a list of
the messages and the date on which they should be published.

::

  posts:
  - date: '2021-06-28'
    message: trace — Follow Program Flow https://pymotw.com/3/trace/
  - date: '2021-07-05'
    message: urllib.robotparser — Internet Spider Access Control https://pymotw.com/3/urllib.robotparser/
  - date: '2021-07-12'
    message: compileall — Byte-compile Source Files https://pymotw.com/3/compileall/
