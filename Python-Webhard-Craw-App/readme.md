###공통 코드
create table common(
    gubun int primary key,
    sitename varchar(50)
)engine=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO common VALUES(1, 'fileis');
INSERT INTO common VALUES(2, 'yesfile');

###영화 제목
create table movie(
    num int auto_increment primary key,
    title varchar(200),
    gubun int
)engine=InnoDB DEFAULT CHARSET=utf8;