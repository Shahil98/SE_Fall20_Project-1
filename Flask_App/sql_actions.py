def add_data_dashboard(db, data):
    cursor = db.cursor()
    for row in data:
        cursor.execute("INSERT INTO "
                       "Dashboard(user_id, file_name, start_date, end_date) "
                       "VALUES(%s,%s,%s,%s)", row)
    db.commit()
    cursor.close()


def add_data_users(db, data):
    cursor = db.cursor()
    cursor.execute("INSERT INTO Users(uid) VALUES(%s)", data)
    db.commit()
    cursor.close()


def retrieve_data(db, some_id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Dashboard WHERE user_id = %s", (some_id,))
    # user_id, file_name, start_date, end_date
    records = cursor.fetchall()
    for row in records:
        print("User ID: ", row[0])
        print("File Name: ", row[1])
        print("Start Date and Time: ", row[2]")
        print("End Date and Time: ", row[3], "\n")
    return records