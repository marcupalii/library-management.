from app import db
import hashlib
from flask_login import UserMixin
from datetime import datetime, timedelta
import pytz

db.metadata.clear()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    library_card_id = db.Column(db.String(10), unique=True)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    address = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)
    type = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    trust_coeff = db.Column(db.Integer, nullable=False)

    next_book = db.relationship('NextBook', uselist=False, backref='user')
    settings = db.relationship('User_settings', uselist=False, backref='user')
    wishlist = db.relationship('Wishlist', backref='user', uselist=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return '(Id {} First_name {},Last_Name {} Email {}, Type {}, Pass {} )'.format(
            self.id,
            self.first_name,
            self.last_name,
            self.email,
            self.type,
            self.password
        )


class BookTypes(db.Model):
    __tablename__ = 'booktypes'
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(30), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    count_total = db.Column(db.Integer, nullable=False)
    count_free_books = db.Column(db.Integer, nullable=False)
    book_series = db.relationship('BookSeries', backref='book', uselist=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    lazy = "dynamic"
    type_id = db.Column(db.Integer, db.ForeignKey('booktypes.id'), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return '( Book {}, Type {}, Count {} {} )  '.format(
            self.name,
            BookTypes.query.filter_by(id=self.type_id).first(),
            self.count_total,
            self.count_free_books
        )


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=True, nullable=False)
    last_name = db.Column(db.String(80), unique=True, nullable=False)
    books = db.relationship('Book', backref='author', uselist=True)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    lazy = "dynamic"

    def __repr__(self):
        return '( id {}, name {}, books {} creted_at {})  '.format(
            self.id,
            self.name,
            self.books,
            self.created_at
        )


class BookSeries(db.Model):
    __tablename__ = 'bookseries'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    series = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return '( id {}, book_id {}, series {}, status {} )'.format(
            self.id,
            self.book_id,
            self.series,
            self.status
        )


class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    entry_wishlists = db.relationship('EntryWishlist', uselist=True, backref='wishlist')
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return "( id {},id_user {})  ".format(self.id, self.id_user)


class EntryWishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_wishlist = db.Column(db.Integer, db.ForeignKey('wishlist.id'), nullable=False)
    id_book = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    period = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return "( id {}, id_wishlist {}, id_book {}, rank {}, period {})  ".format(
            self.id,
            self.id_wishlist,
            self.id_book,
            self.rank,
            self.period
        )


class NextBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_book = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=True)
    id_series_book = db.Column(db.Integer, db.ForeignKey('bookseries.id'), nullable=True)
    rank = db.Column(db.Integer, default=0)
    period = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return "(id {}, id_user {}, id_book {}, id_series_book {}, period {}, status {}".format(
            self.id,
            self.id_user,
            self.id_book,
            self.id_series_book,
            self.period,
            self.status
        )


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    entryes_log = db.relationship('EntryLog', uselist=True, backref='log')
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return "(id {}, id_user {}, id_entrylog {})  ".format(
            self.id,
            self.id_user,
            self.id_entryLog
        )


class EntryLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_log = db.Column(db.Integer, db.ForeignKey('log.id'), nullable=False)

    id_book_series = db.Column(db.Integer, db.ForeignKey('bookseries.id'), nullable=False)

    status = db.Column(db.String(30), nullable=False)
    period_start = db.Column(db.DateTime(timezone=True), default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))
    period_end = db.Column(db.DateTime(timezone=True), nullable=False)
    period_diff = db.Column(db.String(30), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return "(id {}, id_log {}, id_book_series {}, status {}, period {} {})  ".format(
            self.id,
            self.id_log,
            self.id_book_series,
            self.status,
            self.period_start,
            self.period_end
        )


class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)


class User_settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    wishlist_option = db.Column(db.Integer, default=1)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest')))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)


import random

if __name__ == "__main__":
    db.create_all()

    # ----------------------       ONE TO MANY model   ------------------------------------
    author1 = Author(
        first_name="author1 first name",
        last_name="author1 last name",
        created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
            pytz.timezone('Europe/Bucharest'))
    )
    author2 = Author(
        first_name="author2 first name",
        last_name="author2 last name",
        created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
            pytz.timezone('Europe/Bucharest'))
    )
    author3 = Author(
        first_name="author3 first name",
        last_name="author3 last name",
        created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
            pytz.timezone('Europe/Bucharest'))
    )
    author4 = Author(
        first_name="author4 first name",
        last_name="author4 last name",
        created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
            pytz.timezone('Europe/Bucharest'))
    )
    author5 = Author(
        first_name="author5 first name",
        last_name="author5 last name",
        created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
            pytz.timezone('Europe/Bucharest'))
    )
    db.session.add(author1)
    db.session.add(author2)
    db.session.add(author3)
    db.session.add(author4)
    db.session.add(author5)
    db.session.commit()
    authors = [author1, author2, author3, author4, author5]

    type1 = BookTypes(
        type_name="type1",
        created_at= datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('Europe/Bucharest'))
    )

    type2 = BookTypes(
        type_name="type2",
        created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
            pytz.timezone('Europe/Bucharest'))
    )

    type3 = BookTypes(
        type_name="type3",
        created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
            pytz.timezone('Europe/Bucharest'))
    )

    type4 = BookTypes(
        type_name="type4",
        created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
            pytz.timezone('Europe/Bucharest'))
    )

    type5 = BookTypes(
        type_name="type5",
        created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
            pytz.timezone('Europe/Bucharest'))
    )

    db.session.add(type1)
    db.session.add(type2)
    db.session.add(type3)
    db.session.add(type4)
    db.session.add(type5)

    db.session.commit()

    types_ids = [t.id for t in BookTypes.query.all()]

    for i in range(1, 50):
        book = Book(
            name="book{}".format(i),
            author=random.choice(authors),
            type_id=random.choice(types_ids),
            count_total=4,
            count_free_books=4,
            created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                pytz.timezone('Europe/Bucharest'))
        )
        db.session.add(book)
        for j in range(1, 5):
            book_series = BookSeries(
                book=book,
                series="{}SL{}".format(i, j),
                status="available",
                created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                    pytz.timezone('Europe/Bucharest'))
            )
            db.session.add(book_series)
        db.session.commit()

    #  ---------------------- ------------- ------------------------------------

    admin = User(
        first_name='Jhon',
        last_name='Doe',
        address="Bld Mihail Kogalniceanu, nr. 8 Bl 1, Sc 1, Ap 09",
        email='admin@gmail.com',
        type='admin',
        created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
            pytz.timezone('Europe/Bucharest')),
        password=hashlib.sha512("admin".encode()).hexdigest(),
        trust_coeff=0,
        library_card_id="100AAA0000",
        zip_code="932010",
        country="Romania",
        city="Iasi"
    )

    db.session.add(admin)
    db.session.commit()
    wishlist = Wishlist(
        user=admin,
        created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
            pytz.timezone('Europe/Bucharest'))
    )
    db.session.add(wishlist)
    db.session.commit()

    next_book2 = NextBook(
        user=admin,
        period=0,
        status="None",
        created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
            pytz.timezone('Europe/Bucharest')
        )
    )
    db.session.add(next_book2)
    db.session.commit()

    settings = User_settings(
        user=admin,
        created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
            pytz.timezone('Europe/Bucharest')
        )
    )
    db.session.add(settings)
    db.session.commit()
    for i in range(1, 20):
        library_card_id = ""
        if i < 10:
            library_card_id = "000AAA000{}".format(i)
        else:
            library_card_id = "000AAA00{}".format(i)
        user = User(
            first_name='first{}'.format(i),
            last_name='last{}'.format(i),
            address="Bld Mihail Kogalniceanu, nr. 8 Bl 1, Sc 1, Ap 09",
            email='user{}@gmail.com'.format(i),
            type='user',
            password=hashlib.sha512("user{}".format(i).encode()).hexdigest(),
            trust_coeff=random.choice([-20, -10, 10, 0, 20, 40]),
            created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                pytz.timezone('Europe/Bucharest')),
            library_card_id=library_card_id,
            city="Iasi",
            country="Romania",
            zip_code="970632"
        )

        db.session.add(user)
        db.session.commit()
        wishlist = Wishlist(
            user=user,
            created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                pytz.timezone('Europe/Bucharest'))
        )
        db.session.add(wishlist)
        db.session.commit()

        next_book = NextBook(
            user=user,
            period=0,
            status="None",
            created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                pytz.timezone('Europe/Bucharest'))
        )
        db.session.add(next_book)
        db.session.commit()

        settings = User_settings(
            user=user,
            created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                pytz.timezone('Europe/Bucharest')
            )
        )
        db.session.add(settings)
        db.session.commit()


    print(User.query.all())
    print(Book.query.all())
    print(BookSeries.query.all())
    print(Wishlist.query.all())
    print(EntryWishlist.query.all())
    print(NextBook.query.all())
    #
    # now = datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
    #             pytz.timezone('Europe/Bucharest'))
    # after = now +timedelta(weeks=33,days=1,hours=1,minutes=2,seconds=21)
    #
    # print(now)
    # print(after)
    # diff = now - after
    # print(diff)
    # import re
    #
    # days = re.search("\s*(\d+)\s*days",str(diff)).groups(0)[0]
    # hours, minutes, seconds = re.search("(\d+):(\d+):(\d+)",str(diff)).groups()
    # print(days, hours, minutes, seconds)
    # user = User.query.filter_by(first_name="first3").first()
    # log = Log.query.filter_by(id_user=user.id).first()
    # print(log.id)
    # for i in range(0, 100):
    #     log_id = i
    #     entry_logs = db.session().query(EntryLog).filter(
    #         (EntryLog.id_log == log_id)
    #         & ~(EntryLog.status.in_(["Reserved","Reserved"]))
    #     ).all()
    #     if entry_logs:
    #         print(i)
    #         print(entry_logs)
    #         break
# DROP SCHEMA public CASCADE;
# CREATE SCHEMA public;
