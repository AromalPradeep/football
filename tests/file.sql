create table users(
email_id varchar(50) primary key,
username varchar(50) unique not null,
password varchar(50) not null,
role varchar(50) not null
);

create table players(
player_id int primary key,
player_name varchar(50) unique not null,
age int not null,
height int not null,
weight int not null,
nationality varchar(50) not null,
goals_saved int,
goals_against int,
goals_scored int,
assist int,
yellow_card int,
red_card int
);

create table teams(
team_id int primary key,
team_name varchar(50) unique not null,
manager varchar(50) not null,
captain varchar(50) not null,
matches_played int,
win int,
draw int,
lose int,
goal_diff int,
foreign key (captain) references players(player_name)
);


create table games(
game_id int primary key,
team_1 varchar(50) not null,
team_2 varchar(50) not null,
team_1_goal int,
team_2_goal int,
team_1_possession int,
team_2_possession int,
team_1_shots int,
team_2_shots int,
team_1_shots_on_target int,
team_2_shots_on_target int,
team_1_pass int,
team_2_pass int,
team_1_yellow_cards int,
team_2_yellow_cards int,
team_1_red_cards int,
team_2_red_cards int,
team_1_fouls int,
team_2_fouls int,
team_1_offside int,
team_2_offside int,
team_1_corners int,
team_2_corners int,
team_1_penalty int,
team_2_penalty int,
foreign key (team_1) references teams(team_name),
foreign key (team_2) references teams(team_name)
);

create table Argentina(
player_id int,
player_name varchar(50),
jersy_no int unique,
appearances int,
position varchar(5),
foreign key (player_id) references players(player_id),
foreign key (player_name) references players(player_name)
);
create table Brazil(
player_id int,
player_name varchar(50),
jersy_no int unique,
appearances int,
position varchar(5),
foreign key (player_id) references players(player_id),
foreign key (player_name) references players(player_name)
);
create table Croatia(
player_id int,
player_name varchar(50),
jersy_no int unique,
appearances int,
position varchar(5),
foreign key (player_id) references players(player_id),
foreign key (player_name) references players(player_name)
);
create table England(
player_id int,
player_name varchar(50),
jersy_no int unique,
appearances int,
position varchar(5),
foreign key (player_id) references players(player_id),
foreign key (player_name) references players(player_name)
);
create table France(
player_id int,
player_name varchar(50),
jersy_no int unique,
appearances int,
position varchar(5),
foreign key (player_id) references players(player_id),
foreign key (player_name) references players(player_name)
);
create table Morocco(
player_id int,
player_name varchar(50),
jersy_no int unique,
appearances int,
position varchar(5),
foreign key (player_id) references players(player_id),
foreign key (player_name) references players(player_name)
);
create table Netherlands(
player_id int,
player_name varchar(50),
jersy_no int unique,
appearances int,
position varchar(5),
foreign key (player_id) references players(player_id),
foreign key (player_name) references players(player_name)
);
create table Portugal(
player_id int,
player_name varchar(50),
jersy_no int unique,
appearances int,
position varchar(5),
foreign key (player_id) references players(player_id),
foreign key (player_name) references players(player_name)
);