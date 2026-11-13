import database.database as db
try:
    conn=db.get_conn()
    if conn.is_connected():
        print("Welcome to Insyra an bussiness power automation tool")
        conn.close()
except Exception as e:
    print("Connection Error:", e)    