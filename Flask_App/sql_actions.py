def add_data_dashboard(db, data):
    cursor = db.cursor()
    for row in data.values():
        cursor.execute("INSERT INTO "
                       "Dashboard(user_id, file_name, start_date, end_date,file_type) "
                       "VALUES(%s,%s,%s,%s,%s)", row)
    db.commit()
    cursor.close()


def add_data_users(db, data):
    cursor = db.cursor()
    qry1 = "INSERT INTO Users (uid) VALUES (%s)"
    cursor.execute(qry1, (data,))
    db.commit()
    cursor.close()


def retrieve_data_table_chart(db, some_id):
    cursor = db.cursor()
    qry1 = "SELECT D.uid, D.file_name, DIFF(D.start_date,D.end_date) FROM Dashboard D WHERE user_id={} Group by D.uid,D.file_name".format(some_id)
    cursor.execute(qry1)
    records = cursor.fetchall()
    return records


def retrieve_data_pie_chart(db, some_id):
    cursor = db.cursor()
    qry1 = "SELECT D.uid,D.file_type,D.Count(D.file_type) FROM Dashboard D WHERE D.uid={} Group by D.file_type".format(some_id)
    cursor.execute(qry1)
    records = cursor.fetchall()
    return records
