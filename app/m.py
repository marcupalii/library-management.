# print('importing models... %s' % __name__)
from app import db
import hashlib
import datetime
db.metadata.clear()


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    address = db.Column(db.String(150),nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)
    type = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    trust_coeff = db.Column(db.Integer, nullable=False)

    next_book = db.relationship('NextBook', uselist=False, backref='user')
    wishlist = db.relationship('Wishlist', backref='user', uselist=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '(Id {} First_name {},Last_Name {} Email {}, Type {}, Pass {} )'.format(self.id, self.first_name,self.last_name,self.email, self.type, self.password)


class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.String(30), nullable=False)
    count_total = db.Column(db.Integer, nullable=False)
    count_free_books = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    book_series = db.relationship('BookSeries', backref='book', uselist=True)
    def __repr__(self):
        return '( Book {}, Type {}, Count {} {} )  '.format(self.name,self.type,self.count_total,self.count_free_books)

class BookSeries(db.Model):
    __tablename__ = 'bookseries'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    series = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.String(20),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)



class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    entry_wishlists = db.relationship('EntryWishlist', uselist=True, backref='wishlist')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "( id {},id_user {})  ".format(self.id,self.id_user)


class EntryWishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_wishlist = db.Column(db.Integer, db.ForeignKey('wishlist.id'), nullable=False)
    id_book = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    period = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "( id {}, id_wishlist {}, id_book {}, rank {}, period {})  ".format(self.id,self.id_wishlist,self.id_book,self.rank,self.period)


class NextBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    period = db.Column(db.Integer,nullable=True)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Log(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    entryes_log = db.relationship('EntryLog', uselist=True, backref='log')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "(id {}, id_user {}, id_entrylog {})  ".format(self.id,self.id_user,self.id_entryLog)

class EntryLog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    id_log = db.Column(db.Integer, db.ForeignKey('log.id'), nullable=False)

    id_book_series = db.Column(db.Integer, db.ForeignKey('bookseries.id'), nullable=False)

    status = db.Column(db.String(30), nullable=False)
    period_start = db.Column(db.DateTime, nullable=False)
    period_end = db.Column(db.DateTime, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "(id {}, id_log {}, id_book_series {}, status {}, period {} {})  ".format(self.id, self.id_log, self.id_book_series, self.status, self.period_start,self.period_end)

class ReservedBookEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    id_book_series = db.Column(db.Integer, db.ForeignKey('bookseries.id'), nullable=False)

    id_reserved_book = db.Column(db.Integer, db.ForeignKey('reservedbook.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class ReservedBook(db.Model):
    __tablename__ = "reservedbook"
    id = db.Column(db.Integer,primary_key=True)

    id_user = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    reserved_book_entryes = db.relationship('ReservedBookEntry', uselist=True, backref='reserved_book')

    count = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)




if __name__ == "__main__":
    # db.drop_all()
    db.create_all()


    # admin = User(first_name='Jhon', last_name='Doe', address="Main str nr 26", email='admin@gmail.com', type='admin',
    #              password=hashlib.sha512("admin".encode()).hexdigest(), trust_coeff=0)
    #
    # db.session.add(admin)
    # db.session.commit()
    # wishlist = Wishlist(user=admin)
    # db.session.add(admin)
    # db.session.commit()
    #
    #
    # #  ----------------------       ONE TO MANY model   ------------------------------------
    # book1 = Book(name="book1", type="type1", count_total=2, count_free_books=2)
    # book2 = Book(name="book2", type="type3", count_total=2, count_free_books=2)
    #
    # db.session.add(book1)
    # db.session.add(book2)
    # db.session.commit()
    #
    # book_series1 = BookSeries(book=book1, series="310SL1", status="available")
    # book_series2 = BookSeries(book=book1, series="310SL2", status="available")
    #
    # book_series3 = BookSeries(book=book2, series="311SL1", status="available")
    # book_series4 = BookSeries(book=book2, series="311SL2", status="available")
    #
    # db.session.add(book_series1)
    # db.session.add(book_series2)
    # db.session.add(book_series3)
    # db.session.add(book_series4)
    # db.session.commit()
    # #  ---------------------- ------------- ------------------------------------

    # user = User(first_name='first name', last_name='last name', address="Main str nr 26", email='user@gmail.com', type='user',
    #              password=hashlib.sha512("user".encode()).hexdigest(), trust_coeff=0)
    #
    # db.session.add(user)
    # db.session.commit()
    # wishlist = Wishlist(user=user)
    # db.session.add(user)
    # db.session.commit()




    print(User.query.all())
    print(Book.query.all())
    print(BookSeries.query.all())
    print(Wishlist.query.all())
    print(EntryWishlist.query.all())

    # DROP SCHEMA public CASCADE;
    # CREATE SCHEMA public;