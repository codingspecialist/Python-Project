import openpyxl
import pymysql

#데이터베이스연결
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='bitc5600', db='cos', charset='utf8')
#커서생성
cursor = db.cursor()

# 엑셀파일 열기
wb = openpyxl.load_workbook('static/data/coordinate.xlsx')
 
# 현재 Active Sheet 얻기
ws = wb.active

# table 삭제
sql = "drop table coordinate"
cursor.execute(sql)

# table 생성
sql = """
        CREATE TABLE coordinate(
            num int auto_increment primary key,
            addr1 varchar(100),
            addr2 varchar(100),
            addr3 varchar(100),
            x varchar(100),
            y varchar(100)
        )engine=InnoDB DEFAULT CHARSET=utf8;
      """
cursor.execute(sql)

# CCTV정보 읽기
seq = 1
for r in ws.rows:
    if seq != 1:
        col_0 = r[0].value #주소1
        col_1 = r[1].value #주소2
        col_2 = r[2].value #주소3
        col_3 = r[3].value #x좌표
        col_4 = r[4].value #y좌표
        
        sql = f"INSERT INTO coordinate(addr1,addr2,addr3,x,y) VALUES('{col_0}','{col_1}','{col_2}','{col_3}','{col_4}')"
        print(str(seq)+'/3773')
        cursor.execute(sql)
    seq=seq+1
   
#모든 것이 정상적으로 끝나면 commit
db.commit()
