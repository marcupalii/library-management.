from app import db
db.metadata.clear()
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    type = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    trust_coeff = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '(User {}, Email {}, Type {}, Pass {} )'.format(self.username, self.email, self.type, self.password)

# class Book(db.Model):
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True, nullable=False)
#     type = db.Column(db.String(30), nullable=False)
#     count = db.Column(db.Integer,nullable=False)
#
#     def __repr__(self):
#         return '<Book %r>' % self.name


#
# class Log(db.Model):
#
#     id = db.Column(db.Integer, primary_key=True)
#     id_user = db.Column(db.Integer, nullable=False)
#     id_entryLog = db.Column(db.Integer, nullable=False)
#     entry_log = db.relationship('EntryLog',backref='partOf',lazy=True)
#
#
# class EntryLog(db.Model):
#
#     id = db.Column(db.Integer, primary_key=True)
#     id_log = db.Column(db.Integer, nullable=False)
#     id_book = db.Column(db.Integer, nullable=False)
#     status = db.Column(db.String(30), nullable=False)
#     period = db.Column(db.Date, nullable=False)
#
#
# class Wishlist(db.Model):
#
#     id = db.Column(db.Integer, primary_key=True)
#     id_user = db.Column(db.Integer, nullable=False)
#     id_entry_wishlist = db.Column(db.Integer, nullable=False)
#     entry_wishlist = db.relationship('EntryWishlist', backref='partOf', lazy=True)
#
#
# class EntryWishlist(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     id_wishlist = db.Column(db.Integer, db.ForeignKey('wishlist.id'), nullable=False)
#     id_book = db.Column(db.Integer, nullable=False)
#     rank = db.Column(db.Integer, nullable=False)
#     period = db.Column(db.Integer, nullable=False)
#
import hashlib
if __name__ == "__main__":
    # db.drop_all()
    # db.create_all()
    # admin = User(username='admin', email='admin@example.com',type='admin',password=hashlib.sha512("admin".encode()).hexdigest(),trust_coeff=0)
    # user = User(username='user', email='guest@example.com',type="user",password=hashlib.sha512("user".encode()).hexdigest(),trust_coeff=0)
    # db.session.add(admin)
    # db.session.add(user)
    # db.session.commit()
    print(User.query.all())


