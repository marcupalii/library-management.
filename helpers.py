from app import db
from app.models import User, Wishlist, EntryWishlist, Book, NextBook
import time

def _decrement_rank(rank,user_id):
    _wishlists = Wishlist.query.filter_by(id_user=user_id)
    for _wishlist in _wishlists:
        _entrywishlist = _wishlist.entrywishlist

        if _entrywishlist.rank > rank:
            _entrywishlist.rank -= 1
            db.session.commit()

def _remove_entry_from_nextbook(user_id):
    NextBook.query.filter_by(id_user=user_id).delete()
    db.session.commit()

def _wishlist_delete_entry(entry_id,entry_wishlist,user_id):
    _entrywislist = EntryWishlist.query.filter_by(id=entry_wishlist.id).first()
    rank = _entrywislist.rank
    db.session.delete(_entrywislist)
    Wishlist.query.filter_by(id=entry_id).delete()
    db.session.commit()
    _decrement_rank(rank,user_id)
    _wishlists = Wishlist.query.filter_by(id_user=user_id)

    if not _wishlists:
        _remove_entry_from_nextbook(user_id)


def _incremet_rank(rank,curr_user):
    _user = User.query.filter_by(username=curr_user).first()
    _wishlists = Wishlist.query.filter_by(id_user=_user.id)
    for _wishlist in _wishlists:
        _entrywishlist = _wishlist.entrywishlist
        if _entrywishlist.rank >= int(rank):
            _entrywishlist.rank += 1
            db.session.commit()


def _add_entry_into_nextbook(user_id):
    _next_book = NextBook.query.filter_by(id_user=user_id)
    if not _next_book:
        _next_book = NextBook.query.filter_by(id_user=user_id, status="None")
        db.session.add(_next_book)
        db.session.commit()


def _add_book_to_wishlist(book,curr_user,period,rank):
    _user_curr = User.query.filter_by(username=curr_user).first()
    _new_wishlist = Wishlist(id_user=_user_curr.id)
    _new_entry = EntryWishlist(wishlist=_new_wishlist,id_book=book.id,rank=rank,period=period)
    _incremet_rank(rank,curr_user)
    db.session.add(_new_wishlist)
    db.session.add(_new_entry)
    db.session.commit()
    _add_entry_into_nextbook(_user_curr.id)


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
