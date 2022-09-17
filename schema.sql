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
  creator character varying NOT NUll,
  isPrivate boolean NOT NUll DEFAULT true  
);
CREATE TABLE IF NOT EXISTS usersInRoom
(
  room integer references rooms(id),
  userID integer references users(id)
);
CREATE TABLE IF NOT EXISTS messages
(
  id SERIAL NOT NULL PRIMARY KEY,
  author character varying references users(uuid),
  room integer references rooms(id),
  content character varying,
  likes integer DEFAULT 0,
  postedTime timestamp 
);
CREATE TABLE IF NOT EXISTS repliedMessages
(
  parentMessage integer references messages(id),
  childMessage integer references messages(id)
);