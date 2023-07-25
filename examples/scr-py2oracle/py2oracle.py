import oracledb

connection = oracledb.connect(user="xyz", password="xyz", dsn="<server>:<port>/<path>")

cursor = connection.cursor()

# Insert a row
cursor.execute("insert into mas_sqlstmt (correlation_id, x) values ('pytest', 0)")
connection.commit()

# Query for inserted row
for row in cursor.execute("select correlation_id from mas_sqlstmt where x=0"):
    print(row)

# Delete the row
cursor.execute("delete from mas_sqlstmt where x=0")
connection.commit()
