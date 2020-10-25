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
    qry1 = "SELECT D.uid, D.file_name, SUM(TIMESTAMPDIFF(MINUTE,D.start_date,D.end_date)) DIF FROM Dashboard D WHERE uid={} Group by D.uid,D.file_name".format(some_id)
    cursor.execute(qry1)
    records = cursor.fetchall()
    return records
    # [(uid1,file_name1,Diff1),(uid1,file_name2,Diff2)]


def retrieve_data_pie_chart(db, some_id):
    cursor = db.cursor()
    qry1 = "SELECT D.uid,D.file_type,Count(D.file_type) FROM Dashboard D WHERE D.uid={} Group by D.file_type".format(some_id)
    cursor.execute(qry1)
    records = cursor.fetchall()
    return records
    # [(uid1,file_type1,Count1),(uid1,file_type2,Count2)]