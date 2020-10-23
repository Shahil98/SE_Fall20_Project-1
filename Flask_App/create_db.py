import mysql.connector


def _drop_tables(db):
    cursor = db.cursor()
    try:
        cursor.execute('DROP TABLE Dashboard')
    except mysql.connector.Error:
        pass
    try:
        cursor.execute('DROP TABLE Users')
    except mysql.connector.Error:
        pass
    db.commit()
    cursor.close()


def _create_tables(db):
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE Users(
    uid VARCHAR(200),
    PRIMARY KEY(uid)
);""")
    db.commit()
    cursor.execute("""CREATE TABLE Dashboard(
    uid VARCHAR(200),
    file_name VARCHAR(200) NOT NULL,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    PRIMARY KEY(uid),
    FOREIGN KEY (uid) REFERENCES Users(uid) ON DELETE CASCADE
);""")
    db.commit()
    cursor.close()


def load_demo_data(db):
    _drop_tables(db)
    _create_tables(db)
    print("Loading Demo Data")


if __name__ == '__main__':
    db = mysql.connector.connect(host='localhost',
                                 database='code_time',
                                 user='root',
                                 password='codetime')

    load_demo_data(db)
