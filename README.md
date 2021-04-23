The following is the link to mrjohnsonalexander Harvards Extensions School CSCI E-33a Spring 2021 - Final Project public repo:
https://github.com/mrjohnsonalexander/vibes

# Introduction
A vibe is a feeling inpsired by a shared personal experience, members post vibes offered to our community, and transparently share reviews of vibes experienced.
The canary launch of this platform is targeted for USA WA State adults over 18 years, and ~75% of the 7.5 million WA Residence are over 18.

# Background
This is a Django, Javascript, HTML, and CSS only application.
I created a vibesite project, and vibe app.
Created users: admin, firstadopter, secondadopter.
Submitted proposal for review.
Authored Status report.

# Auth Flow
Register
- Username
- Email
- Password
Login
Logout

# Create Vibe
Optional form values
- title
- description
- location
- url

# Next things todo:
- Enable creating/viewing profiles.
- Enable users to toggle cheers to vibes.
- Enable sending/replying/archiving direct messages
- Enable users to comment on vibes.
- Enable searching vibes that are sorted by date.
- Enable users to post frequency reviews of vibes (more detail than a comment)
- Enable toggling being a fan of a profile.
- Enable profiles to list all: vibes/reviews posted, and profiles that are a fan of.
- Enable autoscolling of Vibes on main page
- Enable Basic capabilities limiting: Limited to 1 Vibe per use, limit 1 uploaded and 1 url images, can initiate by sending 1 message per day, reply to any message, post upto 10 comments per month.
- Enable Premium capabilities: Upto 5 vibes posted at a time, unlimited comments and messages, additional profile images.

# Future Development
Payments, Push notifications, Emails, Calander, Map, Facebook/Google Auth, Mobile App.

# Assumptions:
- MVP will be built using Django in two weeks.
- Vibe members have used platforms like Hinge and/or AirBnB Experiences to share an experience with a like minded adult.

# Rough Vibes model
1. Description of what the vibe is.
2. Location where its planned to occur
3. Date Time estimated for the vibe to last
4. Member who offers this vibe, and link to profile.
5. Media applicable to invisioning members vibe.
6. Comments from members about the offered vibe.
7. Estimated expense of the vibe, that is in the form '$', like: $ <= $100, $$ <=$200, $$$ <= $300, etc.
 
