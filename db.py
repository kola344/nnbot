import sqlite3
import os

def get_bases():
    return [i.replace('.db', '') for i in os.listdir('databases')]

class users_db:
    def __init__(self):
        self.db = sqlite3.connect('users.db')
        self.cursor = self.db.cursor()

    def add_user(self, user_id, first_name, last_name, username, city, district, education, public_place, street):
        self.cursor.execute('''INSERT INTO users (user_id, first_name, last_name, username, city, district, education, public_place, street) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (user_id, first_name, last_name, username, city, district, education, public_place, street))
        self.db.commit()

    def check_user(self, user_id):
        self.cursor.execute('''SELECT user_id FROM users WHERE user_id = ?''', (user_id, ))
        return False if self.cursor.fetchone() is None else True

    def get_userdata(self, user_id):
        self.cursor.execute('''SELECT * FROM users WHERE user_id = ?''', (user_id, ))
        data = self.cursor.fetchone()
        return {"id": data[0], "first_name": data[1], "last_name": data[2], "username": data[3], "city": data[4], "district": data[5], "education": data[6], "public_place": data[7], "street": data[8]}


    def get_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return self.cursor.fetchall()

class places:
    def __init__(self):
        self.db = sqlite3.connect('places.db')
        self.cursor = self.db.cursor()

    def add_education(self, name, district):
        self.cursor.execute("INSERT INTO educations (name, district) VALUES (?, ?)", (name, district))
        self.db.commit()

    def add_public_place(self, place, district):
        self.cursor.execute("INSERT INTO public_places (place, district) VALUES (?, ?)", (place, district))
        self.db.commit()

    def add_street(self, street, district):
        self.cursor.execute('''INSERT INTO streets (street, district) VALUES (?, ?)''' , (street, district))
        self.db.commit()

    def delete_education(self, name, district):
        self.cursor.execute('''DELETE FROM educations WHERE name = ? and district = ?''', (name, district))
        self.db.commit()

    def delete_public_place(self, place, district):
        self.cursor.execute('''DELETE FROM public_places WHERE place = ? and district = ?''', (place, district))
        self.db.commit()

    def delete_street(self, street, district):
        self.cursor.execute('''DELETE FROM streets WHERE street = ? and district = ?''', (street, district))
        self.db.commit()

    def get_educations(self, district):
        self.cursor.execute('''SELECT * FROM educations WHERE district = ?''', (district, ))
        return [i[0] for i in self.cursor.fetchall()]

    def get_public_places(self, district):
        self.cursor.execute('''SELECT * FROM public_places WHERE district = ?''', (district, ))
        return [i[0] for i in self.cursor.fetchall()]

    def get_street(self, district):
        self.cursor.execute('''SELECT * FROM streets WHERE district = ?''', (district, ))
        return [i[0] for i in self.cursor.fetchall()]


if __name__ == '__main__':
    user = users_db()
    print(user.get_userdata(1659397548))