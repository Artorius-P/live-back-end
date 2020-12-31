drop table if exists participants;
drop table if exists rooms;
drop table if exists users;





create table users (
  id integer primary key autoincrement,
  username string not null,
  password string not null,
  identity integer not null,
  mail string not null
);

create table rooms (
  id integer primary key autoincrement,
  tid integer not null,
  name string not null,
  profile string not null default '无',
  foreign key (tid) references users(id) 
);

create table participants (
  uid integer not null,
  rid integer not null,
  foreign key (uid) references users(id) ,
  foreign key (rid) references rooms(id) ,
  primary key (uid, rid)
);


