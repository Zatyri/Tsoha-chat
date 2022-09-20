CREATE TABLE IF NOT EXISTS users
(
    id SERIAL NOT NULL PRIMARY KEY,
    username character varying NOT NULL,
    password character varying NOT NULL,
    uuid character varying NOT NULL UNIQUE,
    role integer NOT NULL DEFAULT 1    
);
CREATE TABLE IF NOT EXISTS rooms
(
  id SERIAL NOT NULL PRIMARY KEY,
  title character varying NOT NULL,
  creator integer references users(id),
  isPrivate boolean NOT NUll DEFAULT false  
);
CREATE TABLE IF NOT EXISTS usersInRoom
(
  room integer references rooms(id),
  userID integer references users(id)
);

INSERT INTO rooms (title) SELECT 'Public' 
WHERE NOT EXISTS (SELECT * FROM rooms WHERE rooms.id = 1);

CREATE TABLE IF NOT EXISTS messages
(
  id SERIAL NOT NULL PRIMARY KEY,
  author integer references users(id),  
  content character varying,
  likes integer DEFAULT 0,
  postedTime timestamp 
);
CREATE TABLE IF NOT EXISTS messagesInRoom
(
  room integer references rooms(id),
  messageID integer references messages(id)
);
CREATE TABLE IF NOT EXISTS repliedMessages
(
  parentMessage integer references messages(id),
  childMessage integer references messages(id)
);