from __future__ import print_function, division
import sqlite3

class Database:

    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        self.c.execute('''create table if not exists macro(id integer primary key autoincrement, 
                                                            name text not null, 
                                                            language text not null, 
                                                            age_group text not null,
                                                            gender varchar(1) not null,
                                                            description text,
                                                            events_string text not null,
                                                            keyboard_events_path text not null, 
                                                            model_path text not null)''')
    def insert(self, data):
        """
        Insert data of tuple (name, language, age_group, gender, description, events_string, keyboard_events_path, model_path) into table
        """
        self.c.execute('insert into macro(name, language, age_group, gender, description, events_string, keyboard_events_path, model_path) values (?, ?, ?, ?, ?, ?, ?, ?)', data)
        self.conn.commit()

    def get_all(self):
        """
        Get all data in the table
        """
        self.c.execute('select * from macro')
        return self.c.fetchall()

    def get_list_model_keyboard(self):
        """
        get list of model and keyboard events in the table
        """
        self.c.execute('select model_path, keyboard_events_path from macro')
        return self.c.fetchall()

    def get_macro(self, id):
        """
        Get record according to an id
        """
        self.c.execute('select * from macro where id=?', (id,))
        return self.c.fetchone()

    def delete_macro(self, id):
        """
        Delete record according to an id
        """
        self.c.execute('delete from macro where id=?', (id,))
        self.conn.commit()

    def delete_all(self):
        """
        Delete all data in the table
        """
        self.c.execute('delete from macro')
        self.conn.commit()

    def close(self):
        """
        Close connection
        """
        self.conn.commit()
        self.conn.close()