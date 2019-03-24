from app import db
from app.m import User, Wishlist, EntryWishlist, Book, NextBook

def _add_entry_into_nextbook(user_id):
    _next_book = NextBook.query.filter_by(id_user=user_id)
    if not _next_book:
        _next_book = NextBook.query.filter_by(id_user=user_id, status="None")
        db.session.add(_next_book)
        db.session.commit()


def getNextBook(user_id):
    _next_book = NextBook.query.filter_by(id_user=user_id).first()

    if _next_book:
        if _next_book.status != "None":
            _wishlists = Wishlist.query.filter_by(id_user=user_id)
            for _wishlist in _wishlists:
                if _wishlist:
                    _entrywishlist = _wishlist.entrywishlist
                    if _entrywishlist.id_book == _next_book.id_book and _entrywishlist.period == _next_book.period:
                        _next_book.status = "Pending"
                        db.session.commit()
                        return _next_book
                    else:
                        _next_book.status = "None"
                        db.session.commit()
                        return None
    return None
