print('importing models... %s' % __name__)
from app import db
import hashlib
db.metadata.clear()


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    type = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    trust_coeff = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '(Id {} User {}, Email {}, Type {}, Pass {} )'.format(self.id, self.username, self.email, self.type, self.password)


class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.String(30), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '( Book {}, Type {}, Count {})  '.format(self.name,self.type,self.count)


class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # id_user = db.Column(db.Integer, db.ForeignKey('user.id'),unique=True, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    entrywishlist = db.relationship('EntryWishlist', uselist=False, backref='wishlist')

    def __repr__(self):
        return "( id {},id_user {})  ".format(self.id,self.id_user)


class EntryWishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_wishlist = db.Column(db.Integer, db.ForeignKey('wishlist.id'), nullable=False)
    id_book = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    period = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "( id {}, id_wishlist {}, id_book {}, rank {}, period {})  ".format(self.id,self.id_wishlist,self.id_book,self.rank,self.period)


# class Log(db.Model):
#
#     id = db.Column(db.Integer, primary_key=True)
#     id_user = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
#     id_entryLog = db.Column(db.Integer, nullable=False)
#     # entry_log = db.relationship('EntryLog',backref='partOf',lazy=True)
#
#     def __repr__(self):
#         return "(id {}, id_user {}, id_entrylog {})  ".format(self.id,self.id_user,self.id_entryLog)
#
# class EntryLog(db.Model):
#
#     id = db.Column(db.Integer, primary_key=True)
#     id_log = db.Column(db.Integer, db.ForeignKey('log.id'), nullable=False)
#     id_book = db.Column(db.Integer,db.ForeignKey('book.id'), nullable=False)
#     status = db.Column(db.String(30), nullable=False)
#     period = db.Column(db.Date, nullable=False)
#
#     def __repr__(self):
#         return "(id {}, id_log {}, id_book {}, status {},period {})  ".format(self.id, self.id_log, self.id_book, self.status, self.period)


if __name__ == "__main__":
    # db.drop_all()
    # db.create_all()
    # admin = User(username='admin', email='admin@example.com',type='admin',password=hashlib.sha512("admin".encode()).hexdigest(),trust_coeff=0)
    user = User(username='user1', email='guest1@example.com',type="user",password=hashlib.sha512("user".encode()).hexdigest(),trust_coeff=0)
    book1 = Book(name="book4", type="type1", count=1)
    book2 = Book(name="book5", type="type2", count=1)
    book3 = Book(name="book6", type="type2", count=1)
    #
    #
    # wishlist1 = Wishlist(id_user=2)
    # wishlist2 = Wishlist(id_user=2)
    # entrylist1 = EntryWishlist(wishlist=wishlist1,id_book=1,rank=2,period=23 )
    # entrylist2 = EntryWishlist(wishlist=wishlist2, id_book=2, rank=1, period=2)
    #
    #
    #
    # db.session.add(admin)
    db.session.add(user)
    db.session.add(book1)
    db.session.add(book2)
    db.session.add(book3)
    #
    #
    # db.session.add(entrylist1)
    # db.session.add(wishlist1)
    # db.session.add(entrylist2)
    # db.session.add(wishlist2)
    #
    #
    db.session.commit()


    print(User.query.all())
    print(Book.query.all())
    print(Wishlist.query.all())
    print(EntryWishlist.query.all())


