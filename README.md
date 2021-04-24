# Introduction
Vibe is an online community platform for listing and reviewing shared experiences; the canary launch of this platform is targeted for USA WA State adults over 18 years, and ~75% of the 7.5 million WA Residence are over 18. A vibe is a feeling inspired by a shared personal experience, members post vibes offered to our community, and transparently share reviews of vibes experienced. 

# Background
This is a Python, Javascript, HTML, and CSS only application; created as a course final project using Django. Djangon vibesite project has as a single vibe app.

For testing I created the following users:
admin, firstadopter, secondadopter, thirdadopter, forthadopter, and fifthadopter.

The following capabilities are enabled:
- Can register as a vibe user with username being default profile preferred name.
- Can create/edit a vibe.
- Can view all community created vibes sorted by date on index page.
- Can click any username to view their profile
- Profile shows vibes created by that member, Fan/Follow Counts, and "Become a Fan" or "Stop Being a fan" button when viewing profiles that are not the current user.

# Next things todo:
- Enable users to toggle cheers to vibes.
- Enable users to comment on vibes.
- Enable searching vibes that are sorted by date.
- Enable users to post reviews of vibes (more detail than a comment)
- Enable users toggling being a fan of a profile.
- Enable profiles to list all: vibes/reviews posted, and profiles that are a fan of.
- Enable autoscolling of Vibes on main page
- Enable sending/replying/archiving direct messages


# Future Development
Research Payments, Push notifications, Emails, Calander, Map, Facebook/Google Auth, Mobile App; flush out account types like: 
- Enable Basic capabilities limiting: Limited to 1 Vibe per use, limit 1 uploaded and 1 url images, can initiate by sending 1 message per day, reply to any message, post upto 10 comments per month.
- Enable Premium capabilities: Upto 5 vibes posted at a time, unlimited comments and messages, additional profile images.

# Assumptions:
- MVP will be built using Django in two weeks.
- Vibe members have used platforms like Hinge and/or AirBnB Experiences to share an experience with a like minded adult.

# Things to fix:
- Location and URL should be optional; currently errors when placeholders not replaced with values.
- Should not be able to edit vibe's the user didn't create and can.