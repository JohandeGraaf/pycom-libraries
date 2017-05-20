#!/usr/bin/env python

from datetime import datetime
import mysql.connector as mysql
import db_config


class DbWriter():
    """
    Class for writing data to a MySQL database.
    User specific settings can be entered in db_config.py
    """

    def __init__(self):
        try:
            self.cnx = mysql.connect(user=db_config.DB_USER,
                                     password=db_config.DB_PASS,
                                     host=db_config.DB_HOST,
                                     database=db_config.DB_DB)
            self.cursor = self.cnx.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Wrong user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def insert_row(self, query):
        self.cursor.execute(query)
        self.cnx.commit()

    def close_conn(self):
        self.cursor.close()
        self.cnx.close()


if __name__ == "__main__":
    """
    This section is for testing.

    In this example I have created a simple table called lopy_data
        id: int(11) primary key, auto increment
        date_time: datetime
        payload: varchar(255)
    """
    queries = [
        """INSERT INTO lopy_data VALUES(null, '{}', '{}'); """.format(
            datetime.now(), "23.75"),
        """INSERT INTO lopy_data VALUES(null, '{}', '{}'); """.format(
            datetime.now(), "21.38")
    ]

    # create a database writer instance
    db = DbWriter()

    # test some queries (above)
    for q in queries:
        print q
        db.insert_row(q)

    # when we're done, close the connection
    db.close_conn()
