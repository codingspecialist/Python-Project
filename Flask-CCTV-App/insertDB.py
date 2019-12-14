import openpyxl
import pymysql

#데이터베이스연결
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='bitc5600', db='cos', charset='utf8')
#커서생성
cursor = db.cursor()

# 엑셀파일 열기
wb = openpyxl.load_workbook('static/data/cctv_busan.xlsx')
 
# 현재 Active Sheet 얻기
ws = wb.active
 
# CCTV정보 읽기
seq = 1
for r in ws.rows:
    col_1 = r[1].value   #주소
    col_6 = r[6].value   #카메라방향
    col_10 = r[10].value #위도(세로)
    col_11 = r[11].value #경도(가로)

    sql = f"INSERT INTO cctv(addr1,addr2,loc,lon) VALUES('{col_1}','{col_6}','{col_10}','{col_11}')"
    print(str(seq)+'/8491')
    cursor.execute(sql)
    seq=seq+1
   
#모든 것이 정상적으로 끝나면 commit
db.commit()
