from app import db
from app.models import User, Wishlist, EntryWishlist, Book, NextBook

def _add_entry_into_nextbook(user_id):
    _next_book = NextBook.query.filter_by(id_user=user_id)
    if not _next_book:
        _next_book = NextBook.query.filter_by(id_user=user_id, status="None")
        db.session.add(_next_book)
        db.session.commit()



