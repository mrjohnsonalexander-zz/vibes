# Introduction
Vibe is an online community platform for listing and reviewing shared experiences; the canary launch of this platform is targeted for USA WA State adults over 18 years, and ~75% of the 7.5 million WA Residence are over 18. A vibe is a feeling inspired by a shared personal experience, members post vibes offered to our community, and transparently share reviews of vibes experienced. 

# Background
This is a Python, Javascript, HTML, and CSS only application; created as a course final project using Django. Djangon vibesite project has as a single vibe app.

For testing I created the following users:
admin, firstadopter, secondadopter, thirdadopter, forthadopter, and fifthadopter.

The following capabilities are enabled:
- Can register with username being default profile preferred name.
- Can create/edit a vibe but can not edit vibe's user didn't create.
- Can view all community created vibes sorted by date on index page.
- Can click any vibe creator's username to view their profile
- Can click any vibe image to view detail view.
- Can toggle cheers to vibes.
- Profile shows Fan/Follow Counts, and "Become a Fan" or "Stop Being a fan" button when viewing profiles that are not the current user.

# Next things todo:
- Enable users to comment on vibes.
- Enable users toggling being a fan of a profile.
- Enable autoscolling of Vibes on main page
- Enable sending/replying/archiving direct messages
- Enable searching vibes that are sorted by date.
- Enable users to post reviews of vibes (more detail than a comment)
- Enable profiles to list all: vibes/reviews posted, and profiles that are a fan of.


# Future Development
Research Payments, Push notifications, Emails, Calander, Map, Facebook/Google Auth, Mobile App; flush out account types like: 
- Enable Basic capabilities limiting: Limited to 1 Vibe per user, limit 1 uploaded and 1 url images, can comment upto 3 times per day, can reply to any message, but can not initiate any direct message.
- Enable Premium capabilities: Upto 5 vibes posted at a time, unlimited comments and messages, additional profile images.

# Assumptions:
- MVP will be built using Django in two weeks.
- Vibe members have used platforms like Hinge and/or AirBnB Experiences to share an experience with a like minded adult.

# Things to fix:
- Location and URL should be optional; currently errors when placeholders not replaced with values.
- JS error: "AddEventListener of null" due because profile Fan toggle element missing when viewing vibes.
- JS error: "replceWith of null" occurs when viewing profiles dur to Form element missing.
