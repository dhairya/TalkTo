drop table if exists entries;
create table talkto (
  id integer primary key autoincrement,
  name string not null,
  office string not null,
  what string not null
);