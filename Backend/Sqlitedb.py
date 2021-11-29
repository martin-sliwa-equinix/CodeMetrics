import sqlite3

from sqlite3 import Error
from pathlib import Path

class DBHandler:
    def __init__(self):
        self.filepath = Path("./data.db")

        self.sql_create_repo_table= """ CREATE TABLE IF NOT EXISTS repos (
                id integer PRIMARY KEY,
                reponame text NOT NULL,
                reposha text NOT NULL
                ); """

        self.sql_create_commit_table= """ CREATE TABLE IF NOT EXISTS commits (
                id integer PRIMARY KEY,
                commitsha text NOT NULL,
                branchsha text,
                branchname text,
                lastmodified text,
                statsadded int,
                statsdeleted int,
                committer text,
                FOREIGN KEY (reposha) REFERENCES repos (reposha)
                ); """

        #Connect to the db
        self.conn = self.create_connection(self.filepath)

        #Ensure tables are created on init
        if self.conn is not None:
            self.create_table(self.conn, self.sql_create_commit_table)
            self.create_table(self.conn, self.sql_create_commit_table)

    def create_connection(self, filepath):
        conn = None
        try:
            conn = sqlite3.connect(filepath)
        except Error as e:
            print(e)
        
        return conn

    def create_table(self, conn, sql_command):
        try:
            c = conn.cursor()
            c.execute(sql_command)
        except Error as e:
            print(e)

    def insert_repo(self, conn, repo):
        sql = """ INSERT INTO repos(reponame, reposha)
        VALUES(?,?)
        """
        
        cur = conn.cursor()
        cur.execute(sql, repo)
        conn.commit()

    def insert_commit(self, conn, repo):
        sql = """ INSERT INTO commits(commitsha, branchsha, branchname, lastmodified, statsadded. statsdeleted, committer, reposha)
        VALUES(?,?,?,?,?,?,?,?)
        """

        cur = conn.cursor()
        cur.execute(sql, repo)
        conn.commit()