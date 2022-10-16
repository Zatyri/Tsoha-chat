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
  creator integer references users(id) ON DELETE CASCADE,
  isPrivate boolean NOT NUll DEFAULT false  
);
CREATE TABLE IF NOT EXISTS usersInRoom
(
  room integer references rooms(id) ON DELETE CASCADE,
  userID integer references users(id) ON DELETE SET NULL
);

INSERT INTO rooms (title) SELECT 'Julkinen' 
WHERE NOT EXISTS (SELECT * FROM rooms WHERE rooms.id = 1);

CREATE TABLE IF NOT EXISTS messages
(
  id SERIAL NOT NULL PRIMARY KEY,
  author integer references users(id) ON DELETE SET NULL,  
  content character varying,
  likes integer DEFAULT 0,
  postedTime timestamp 
);
CREATE TABLE IF NOT EXISTS messagesInRoom
(
  room integer references rooms(id) ON DELETE CASCADE,
  messageID integer references messages(id) 
);
CREATE TABLE IF NOT EXISTS repliedMessages
(
  parentMessage integer references messages(id),
  childMessage integer references messages(id)
);

CREATE TABLE IF NOT EXISTS likedMessages
(
  messageID integer references messages(id),
  userID integer references users(id) ON DELETE SET NULL
);