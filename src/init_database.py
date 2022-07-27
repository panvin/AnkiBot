import sqlite3
from settings import db_path


class dbInit():

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn

    def create_table(self, conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def main(self):
        sql_create_servers_table =      """ CREATE TABLE IF NOT EXISTS Servers (
                                            id integer PRIMARY KEY,
                                            server_name text NOT NULL,
                                            study_channel text
                                        ); """

        sql_create_decks_table =     """CREATE TABLE IF NOT EXISTS Decks (
                                        id integer PRIMARY KEY,
                                        server_id integer NOT NULL,
                                        deck_name text NOT NULL,
                                        is_updated integer NOT NULL,
                                        user_in_charge text,
                                        FOREIGN KEY (server_id) REFERENCES Servers (id)
                                    );"""
        
        sql_create_cards_table =     """CREATE TABLE IF NOT EXISTS Cards (
                                        id integer PRIMARY KEY,
                                        deck_id integer NOT NULL,
                                        card_name text NOT NULL,
                                        first_field text NOT NULL,
                                        second_field text NOT NULL,
                                        is_active integer NOT NULL,
                                        FOREIGN KEY (deck_id) REFERENCES Decks (id)
                                    );"""

        # create a database connection
        conn = self.create_connection(db_path)

        # create tables
        if conn is not None:
            # create servers table
            self.create_table(conn, sql_create_servers_table)

            # create decks table
            self.create_table(conn, sql_create_decks_table)

            # create cards table
            self.create_table(conn, sql_create_cards_table)
        else:
            print("Error! cannot create the database connection.")



if __name__ == '__main__':
    myInit = dbInit()
    myInit.main()