# Introduction
Vibe is an online community platform for listing and reviewing shared experiences; the canary launch of this platform is targeted for USA WA State adults over 18 years, and ~75% of the 7.5 million WA Residence are over 18. A vibe is a feeling inspired by a shared personal experience, members post vibes offered to our community, and transparently share reviews of vibes experienced. 

# Background
This is a Python, Javascript, HTML, and CSS only application; created as a course final project using Django, and vibesite project has as a single vibe app.

For testing I created the following users:
admin, firstadopter, secondadopter, thirdadopter, forthadopter, and fifthadopter.

The following capabilities are enabled:
- Can register with username being default profile preferred name.
- Can create/edit a vibe but can not edit vibe's user didn't create.
- Can view all community created vibes sorted by date on index page.
- Can click any vibe creator's username to view their profile
- Can click any vibe image to view detail view.
- Can view all vibe comments on detail view.
- Can Add Comments to vibe details.
- Can toggle cheers to vibes.
- Profile shows Fan/Follow Counts, and "Become a Fan" or "Stop Being a fan" button when viewing profiles that are not the current user.
- Can autoscolling of Vibes on main page
- Can toggle being a fan of a profile
- Can send direct messages to profile preferred_name
- Can click any message to display body of that message.
- Can click on message sender to return to their profile where you can send another direct message.
- Can click on message archive link to update message archive value.
- Can click on Archived nav to view archived messages.
- Can view metrics in honeycomb: https://ui.honeycomb.io/mrjohnsonalexander/datasets/vibes

# Next things todo:
- Get feedback on status.

# Future Development
Research Payments, Push notifications, Emails, Calander, Map, Facebook/Google Auth, Mobile App; flush out account types like: 
- Enable Basic capabilities limiting: Limited to 1 Vibe per user, limit 1 uploaded and 1 url images, can comment upto 3 times per day, can reply to any message, but can not initiate any direct message.
- Enable Premium capabilities: Upto 5 vibes posted at a time, unlimited comments and messages, additional profile images.

# Assumptions:
- MVP will be built using Django in two weeks.
- Vibe members have used platforms like Hinge and/or AirBnB Experiences to share an experience with a like minded adult.

# Things to fix:
- Location and URL should be optional; currently errors when placeholders not replaced with values.
- JS error: "'AddEventListener' of null" because compose-form for messages available when viewing any profile is missing when viewing vibes.
- Autoscroll will repeated;y append last 10 vibes to end of page when there are no more.
- JS error: "'replceWith' of null" occurs when viewing "Received" "Sent" or "Archived" messages because vibeForm is missing when viewing message box.
- JS error: "403 Forbidden" when clicking "become a fan" or "Stop being a fan" on a profile, screen doesn't auto refresh count of "Fans", but refreshing screen shows correct Fan count.
- JS error: "Cannot set property 'style'" happens when clicking New Message "Submit" button, but clicking "Sent" will show last sent message title. 
