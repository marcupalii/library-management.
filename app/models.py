from app import db
import hashlib
from flask_login import UserMixin
from datetime import datetime
import pytz

db.metadata.clear()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(150), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)
    type = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    trust_coeff = db.Column(db.Integer, nullable=False)

    next_book = db.relationship('NextBook', uselist=False, backref='user')
    wishlist = db.relationship('Wishlist', backref='user', uselist=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))

    def __repr__(self):
        return '(Id {} First_name {},Last_Name {} Email {}, Type {}, Pass {} )'.format(self.id, self.first_name,
                                                                                       self.last_name, self.email,
                                                                                       self.type, self.password)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.String(30), nullable=False)
    count_total = db.Column(db.Integer, nullable=False)
    count_free_books = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))
    book_series = db.relationship('BookSeries', backref='book', uselist=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    lazy = "dynamic"

    def __repr__(self):
        return '( Book {}, Type {}, Count {} {} )  '.format(self.name, self.type, self.count_total,
                                                            self.count_free_books)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    books = db.relationship('Book', backref='author', uselist=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))
    lazy = "dynamic"

    def __repr__(self):
        return '( id {}, name {}, books {} creted_at {})  '.format(self.id, self.name, self.books, self.created_at)


class BookSeries(db.Model):
    __tablename__ = 'bookseries'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    series = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))

    def __repr__(self):
        return '( id {}, book_id {}, series {}, status {} )'.format(self.id, self.book_id, self.series, self.status)


class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    entry_wishlists = db.relationship('EntryWishlist', uselist=True, backref='wishlist')
    created_at = db.Column(db.DateTime, default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))

    def __repr__(self):
        return "( id {},id_user {})  ".format(self.id, self.id_user)


class EntryWishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_wishlist = db.Column(db.Integer, db.ForeignKey('wishlist.id'), nullable=False)
    id_book = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    period = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))

    def __repr__(self):
        return "( id {}, id_wishlist {}, id_book {}, rank {}, period {})  ".format(self.id, self.id_wishlist,
                                                                                   self.id_book, self.rank, self.period)


class NextBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_book = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=True)
    id_series_book = db.Column(db.Integer, db.ForeignKey('bookseries.id'), nullable=True)
    period = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))

    def __repr__(self):
        return "(id {}, id_user {}, id_book {}, id_series_book {}, period {}, status {}".format(self.id, self.id_user,
                                                                                                self.id_book,
                                                                                                self.id_series_book,
                                                                                                self.period,
                                                                                                self.status)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    entryes_log = db.relationship('EntryLog', uselist=True, backref='log')
    created_at = db.Column(db.DateTime, default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))

    def __repr__(self):
        return "(id {}, id_user {}, id_entrylog {})  ".format(self.id, self.id_user, self.id_entryLog)


class EntryLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_log = db.Column(db.Integer, db.ForeignKey('log.id'), nullable=False)

    id_book_series = db.Column(db.Integer, db.ForeignKey('bookseries.id'), nullable=False)

    status = db.Column(db.String(30), nullable=False)
    period_start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))
    period_end = db.Column(db.DateTime, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))

    def __repr__(self):
        return "(id {}, id_log {}, id_book_series {}, status {}, period {} {})  ".format(self.id, self.id_log,
                                                                                         self.id_book_series,
                                                                                         self.status, self.period_start,
                                                                                         self.period_end)
#
#
# class ReservedBookEntry(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#
#     id_book_series = db.Column(db.Integer, db.ForeignKey('bookseries.id'), nullable=False)
#
#     id_reserved_book = db.Column(db.Integer, db.ForeignKey('reservedbook.id'), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
#         pytz.timezone('Europe/Bucharest')))
#
#
# class ReservedBook(db.Model):
#     __tablename__ = "reservedbook"
#     id = db.Column(db.Integer, primary_key=True)
#
#     id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#
#     reserved_book_entryes = db.relationship('ReservedBookEntry', uselist=True, backref='reserved_book')
#
#     count = db.Column(db.Integer, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
#         pytz.timezone('Europe/Bucharest')))
#

class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))


import random

if __name__ == "__main__":
    db.create_all()

    # ----------------------       ONE TO MANY model   ------------------------------------
    author1 = Author(name="author1")
    author2 = Author(name="author2")
    author3 = Author(name="author3")
    author4 = Author(name="author4")
    author5 = Author(name="author5")
    db.session.add(author1)
    db.session.add(author2)
    db.session.add(author3)
    db.session.add(author4)
    db.session.add(author5)
    db.session.commit()
    authors = [author1, author2, author3, author4, author5]

    for i in range(1, 50):
        total = random.choice([2, 3, 4])
        free = random.choice([0, 1, 2])
        book = Book(
            name="book{}".format(i),
            author=random.choice(authors),
            type="type{}".format(random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])),
            count_total=total+2,
            count_free_books=free+2
        )
        db.session.add(book)
        for j in range(1, 4):
            book_series = BookSeries(book=book, series="{}SL{}".format(i,j), status="available")
            db.session.add(book_series)
        db.session.commit()

    #  ---------------------- ------------- ------------------------------------

    admin = User(first_name='Jhon', last_name='Doe', address="Main str nr 26", email='admin@gmail.com', type='admin',
                 password=hashlib.sha512("admin".encode()).hexdigest(), trust_coeff=0)

    db.session.add(admin)
    db.session.commit()
    wishlist = Wishlist(user=admin)
    db.session.add(wishlist)
    db.session.commit()

    next_book2 = NextBook(user=admin, period=0, status="None")
    db.session.add(next_book2)
    db.session.commit()

    for i in range(1, 20):
        user = User(
            first_name='first{}'.format(i),
            last_name='last{}'.format(i),
            address="Main str nr 26",
            email='user{}@gmail.com'.format(i), type='user',
            password=hashlib.sha512("user{}".format(i).encode()).hexdigest(), trust_coeff=0
        )

        db.session.add(user)
        db.session.commit()
        wishlist = Wishlist(user=user)
        db.session.add(wishlist)
        db.session.commit()

        next_book = NextBook(user=user, period=0, status="None")
        db.session.add(next_book)
        db.session.commit()

    print(User.query.all())
    print(Book.query.all())
    print(BookSeries.query.all())
    print(Wishlist.query.all())
    print(EntryWishlist.query.all())

    print(NextBook.query.all())
    # print("\n\n\n")
    # entryes = Book.query.filter(Book.name.like('%%'))
    # form_bool = "book2"
    # form_bool = False
    # name = form_bool if form_bool else '%%'
    # print("name=",name)
    # entryes = Book.query.filter(Book.name.like(name))
    # for entry in entryes:
    #     print(entry)
    # print(NextBook.query.filter_by(id=1,id_user=1).first())

    # print("\n join: \n")
    # results = Author.query.join(Book., Author.id == Book.author_id).filter_by(type="type1")
    # results = Book.query.filter_by(type="type1").join(Author, Author.id== Book.author_id).add_columns(Author.id,Author.name,Author.created_at)
    # for result in results:
    #     print(result[0])

    # print(Book.query.all())
    # print(Book.query.filter_by(count_total=2).order_by(Book.created_at.desc()).all())

    # DROP SCHEMA public CASCADE;
    # CREATE SCHEMA public;
