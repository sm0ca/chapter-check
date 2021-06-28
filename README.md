# Chapter Check

(Note that although this project was created for my computer science course, it can be used by anyone who finds it helpful! - sxnch)

This software allows you to maintain a personal manga list, in which you can
add all of the ongoing manga that you'd like to keep up-to-date with. With a
Chapter Check manga list, you have the option to search for new chapter
releases (Chapter Check's primary function), modify your list (add/remove
manga), and view the list to check your last-read chapters!

### Dependencies
requests: (can be installed with "pip install requests")

### Demo Account Information:

- Both username and password: demo

- The demo account comes pre-configured with 8 mangas

- "Dr. Stone", "Jujutsu Kaisen", "Noragami", "Tomadachi Game", "Blue Period",
  "Ao no Futsumashi", and "Yuan Zun" are all purposely set to be behind the
  latest chapter, in order to showcase what the program does when a new chapter
  is released. Also, such a large quantity of manga was chosen so that the
  scrollbar could be shown in action (since it only appears on the manga list
  and new releases screens if there are 6 or more items that need to be
  displayed).

- "Berserk" is set to the latest chapter (as of 06/06/21), to showcase how the
  program handles the presence of up-to-date manga among those that have new
  releases (such as the entries outlined in the point above)

- "Yuan Zun" is included because although it may not be the most popular
  series, a couple of chapters are released every week (with typically a one
  to three day wait time in between releases), allowing for live testing of
  the program without having to wait for a week or month for new chapters (as
  can be the case for various other manga)


Some other popular manga you may want to try adding include:

- "Boku no Hero Academia" ("BNHA" will also work!)
- "One Punch Man" ("OPM" will also work!)
- "Fire Force" (or "Enen no Shouboutai")
- "Black Clover"
- "Dragon Ball"
- "Bleach"

#### Additional Note (strictly for testing purposes, not intended for consumer use):

When manually tampering with the values for last-read chapters within a user's
manga list (to test the "search new releases" function), ensure that extra
blank lines are not added to the end of the file (as this can cause unintended
errors in the program when attempting to parse from the file).


#### Disclaimer:

Chapter Check does not own or imply ownership of any of the images used in the
application. All images belong to their respective owners. Chapter Check users
and its programmers are not liable for any of the content displayed in this
application.
