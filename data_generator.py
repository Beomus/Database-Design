from faker import Faker
import numpy as np
from tqdm import tqdm
import os
import pandas as pd

fake = Faker(['ja_JP', 'en_US'])
us = fake['en_US']
jp = fake['ja_JP']
gender = ["MA", "FE", "OT"]

def generate_member(n):
    with open("generate_member.sql", "w") as f:
        f.write("DELETE FROM member;\n")
        for i in tqdm(range(1, n)):
            i = i if i >= 10 else '0' + str(i)
            memberid = f"M0000000{i:2}"
            nameFirst = us.first_name()
            nameLast = us.last_name()
            phone = us.phone_number()
            email = us.ascii_safe_email()
            age = np.random.randint(12, 70)
            sex = np.random.choice(gender)
            postalCode = jp.postcode()
            street = us.address()
            sql_command = f"INSERT INTO member (memberid, namefirst, namelast, age, sex, phone, postalcode, street, email) VALUES ('{memberid}', '{nameFirst}', '{nameLast}', '{age}', '{sex}', '{phone}', '{postalCode}', '{street}', '{email}');\n"
            f.write(sql_command)

def generate_author(n):
    with open("generate_author.sql", "w") as f:
        f.write("DELETE FROM author;\n")
        for i in tqdm(range(1, n)):
            i = i if i >= 10 else '0' + str(i)
            authorid = f"A0000000{i:2}"
            nameFirst = us.first_name()
            nameLast = us.last_name()
            sex = np.random.choice(gender)
            sql_command = f"INSERT INTO author (authorid, namefirst, namelast, sex) VALUES ('{authorid}', '{nameFirst}', '{nameLast}', '{sex}');\n"
            f.write(sql_command)

def generate_book(n):
    with open("generate_book.sql", "w") as f:
        f.write("DELETE FROM book;\n")
        for i in tqdm(range(1, n)):
            i = str(i)
            bookid = "B" + "0"*(9 - len(i)) + i
            title = us.sentence(nb_words=np.random.randint(1, 5), variable_nb_words=True)
            condition = np.random.choice(["A", "B", "C"])
            isbn = fake.isbn13()
            quantity = np.random.randint(0, 5)
            price = np.random.randint(1, 60) * 100
            sql_command = f"INSERT INTO book (bookid, title, condition, isbn, quantity, price) VALUES ('{bookid}', '{title}', '{condition}', '{isbn}', '{quantity}', '{price}');\n"
            f.write(sql_command)

def generate_genre():
    genres = {}
    with open("genres.txt", "r") as f:
        text = f.readlines()
        for line in tqdm(text):
            genres[line[:3]] = line
    with open("generate_genre.sql", "w") as f:
        f.write("DELETE FROM genre;\n")
        for k, v in genres.items():
            sql_command = f"INSERT INTO genre (genreid, genre) VALUES ('{k}', '{v[:-1]}');\n"
            f.write(sql_command)

def link_tables(g, a):
    author = pd.read_csv('author.csv')
    authorids = author.authorid
    book = pd.read_csv('book.csv')
    bookids = book.bookid
    genre = pd.read_csv('genre.csv')
    genreids = genre.genreid
    with open("generate_bookgenre.sql", "w") as f:
        f.write("DELETE FROM bookgenre;\n")
        for _ in tqdm(range(g)):
            sql_command = f"INSERT INTO bookgenre (genreid, bookid) VALUES ('{np.random.choice(genreids)}', '{np.random.choice(bookids)}');\n"
            f.write(sql_command)
    with open("generate_bookauthor.sql", "w") as f:
        f.write("DELETE FROM bookauthor;\n")
        for _ in tqdm(range(a)):
            sql_command = f"INSERT INTO bookauthor (bookid, authorid) VALUES ('{np.random.choice(bookids)}', '{np.random.choice(authorids)}');\n"
            f.write(sql_command)

def generate_orders(n):
    member = pd.read_csv("member.csv")
    memberids = list(member.memberid)
    with open("generate_orders.sql", "w") as f:
        f.write("DELETE FROM orders;\n")
        for i in tqdm(range(1, n)):
            i = str(i)
            orderid = "O" + "0"*(9 - len(i)) + i
            memberid = np.random.choice(memberids)
            date = us.date_this_year(before_today=True, after_today=False)
            types = np.random.choice(["PUR", "SEL"])
            details = us.sentence(nb_words=np.random.randint(1, 10), variable_nb_words=True)
            sql_command = f"INSERT INTO orders (orderid, memberid, dates, type, details) VALUES ('{orderid}', '{memberid}', '{date}', '{types}', '{details}');\n"
            f.write(sql_command)

def link_orderline(n):
    book = pd.read_csv("book.csv")
    bookids = list(book.bookid)
    prices = list(book.price)
    orders = pd.read_csv("orders.csv")
    orderids = list(orders.orderid)
    with open("generate_orderline.sql", "w") as f:
        f.write("DELETE FROM orderline;\n")
        for _ in tqdm(range(n)):
            orderid = np.random.choice(orderids)
            bookid = np.random.choice(bookids)
            price = prices[bookids.index(bookid)]
            quantity = np.random.randint(1, 3)
            sql_command = f"INSERT INTO orderline (orderid, bookid, quantity, price) VALUES ('{orderid}', '{bookid}', '{quantity}', '{price}');\n"
            f.write(sql_command)

if __name__ == "__main__":
    # generate_member(50)
    # generate_author(20)
    # generate_book(200)
    # generate_genre()
    # link_tables(g=100, a=50)
    # generate_orders(1000)
    link_orderline(1300)