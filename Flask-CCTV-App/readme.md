###lon 경도(가로)X, loc 위도(세로)Y
CREATE TABLE cctv(
    num int auto_increment primary key,
    addr1 varchar(100),
    addr2 varchar(100),
    loc varchar(100),
    lon varchar(100)
)engine=InnoDB DEFAULT CHARSET=utf8;