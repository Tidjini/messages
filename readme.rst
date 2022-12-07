# Messages
######################
For message testing application, using: python socketio with gevent library 


Each user can create a discusion room
Each discussion room contain many owners / many visitors
Each discusion contain messages with sender / reciever

1/ clean users AUTH

TODO:
create user A:
create user B:
create user C

A create discussion with B
A send message to B
B got notfied with message content
B reply to A with message
A got notifeyd with B message Content

A resend Quit message and restart same process
 

// todo
//- auth functions/ create, and authentication, username/pass
//- cache token, in key value android
//- get list of discussions -> from here you can go to list users (contacts)
//- create a discussion
//- discussion -> activity



installing
-- dj-database-url for working with Db ULRS (For Remotes with ENV Vaiables)

-- vercel.json
-- build.sh for building commands 
-- dj-database-url with env var DATABASE_URL
-- python-decouple to get local env vars