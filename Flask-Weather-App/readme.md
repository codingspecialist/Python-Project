###좌표
CREATE TABLE coordinate(
    num int auto_increment primary key,
    addr1 varchar(100),
    addr2 varchar(100),
    addr3 varchar(100),
    x varchar(100),
    y varchar(100)
)engine=InnoDB DEFAULT CHARSET=utf8;