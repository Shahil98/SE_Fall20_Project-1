def add_data_dashboard(db, data):
    cursor = db.cursor()
    for row in data:
        uid = row['uid']
        file_name = row['file_name']
        start_date = row['start_date']
        end_date = row['end_date']
        file_type = row['file_type']
        cursor.execute("INSERT INTO "
                       "Dashboard(uid, file_name, start_date, end_date,file_type) "
                       "VALUES(%s,%s,%s,%s,%s)", (uid, file_name, start_date, end_date, file_type,))
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
    qry1 = "SELECT D.uid, D.file_name, SUM(TIMESTAMPDIFF(MINUTE,D.start_date,D.end_date)) AS DIF FROM Dashboard D WHERE uid='{}' Group by D.uid,D.file_name".format(some_id)
    cursor.execute(qry1)
    records = cursor.fetchall()
    return records
    # [(uid1,file_name1,Diff1),(uid1,file_name2,Diff2)]


def retrieve_data_pie_chart(db, some_id):
    cursor = db.cursor()
    qry1 = "SELECT D.uid,D.file_type,Count(D.file_type) FROM Dashboard D WHERE D.uid='{}' Group by D.file_type".format(some_id)
    cursor.execute(qry1)
    records = cursor.fetchall()
    return records
    # [(uid1,file_type1,Count1),(uid1,file_type2,Count2)]


def retrieve_data_graph_chart(db, some_id):
    cursor = db.cursor()
    qry1 = "SELECT D.uid,D.file_type,SUM(TIMESTAMPDIFF(MINUTE,D.start_date,D.end_date)) AS DIF FROM Dashboard D WHERE D.uid='{}' Group by D.file_type".format(some_id)
    cursor.execute(qry1)
    records = cursor.fetchall()
    return records
    # [(uid1,file_type1,time_diff1),(uid1,file_type2,time_diff2)]


def check_user(db, some_id):
    cursor = db.cursor()
    qry1 = "SELECT * FROM Users U WHERE U.uid='{}'".format(some_id)
    cursor.execute(qry1)
    records = cursor.fetchone()
    if not records:
        return -1
    return records
