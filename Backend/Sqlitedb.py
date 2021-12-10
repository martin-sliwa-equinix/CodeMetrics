import sqlite3

from sqlite3 import Error
from pathlib import Path

class DBHandler:
    def __init__(self):
        self.filepath = Path("./data.db")

        self.sql_create_branch_table= """ CREATE TABLE IF NOT EXISTS branches (
                id integer PRIMARY KEY,
                repo_name text NOT NULL,
                branch_name text NOT NULL
                ); """

        self.sql_create_commit_table= """ CREATE TABLE IF NOT EXISTS commits (
                id integer PRIMARY KEY,
                commit_sha text NOT NULL UNIQUE,
                last_modified text,
                stats_added int,
                stats_deleted int,
                committer text,
                branch_name,
                FOREIGN KEY (branch_name) REFERENCES branches(branch_name)
                ); """

        #Connect to the db
        self.conn = self.create_connection(self.filepath)

        #Ensure tables are created on init
        if self.conn is not None:
            self.create_table(self.sql_create_branch_table)
            self.create_table(self.sql_create_commit_table)

    def create_connection(self, filepath):
        conn = None
        try:
            conn = sqlite3.connect(filepath)
        except Error as e:
            print(e)
        
        return conn

    def create_table(self, sql_command):
        try:
            c = self.conn.cursor()
            c.execute(sql_command)
        except Error as e:
            print(e)

    def insert_branch(self, branch):
        sql = """ INSERT INTO branches(repo_name, branch_name)
        VALUES(?,?)
        """
        conn = self.conn

        cur = conn.cursor()
        cur.execute(sql, branch)
        conn.commit()

    def insert_commit(self, commit):
        sql = """ INSERT INTO commits(commit_sha, last_modified, stats_added, stats_deleted, committer, branch_name)
        VALUES(?,?,?,?,?,?)
        """
        conn = self.conn

        cur = conn.cursor()
        cur.execute(sql, commit)
        conn.commit()

    def get_graphdata_codedensity(self):
        #Return rows with following format:
        # Reponame | Date of commit | commits added + subtracted

        sql = """
        SELECT branches.repo_name, commits.last_modified, commits.stats_added + commits.stats_deleted
        FROM commits, branches
        WHERE commits.branch_name = branches.branch_name
        """
        conn = self.conn

        cur = conn.cursor()
        cur.execute(sql)

        rows = cur.fetchall()
        return rows