
from app import celery, logger, db
from app.models import NextBook, BookSeries, Book, EntryWishlist, Wishlist
from app.Stable_matching_algorithm.algorithm import Stable_matching



def update_state():
    from app.models import User, NextBook, Book, Wishlist
    _wishlists = Wishlist.query.all()

    users_with_wishlist = {}
    trust_coeffs = {}
    book_count = {}

    for _wishlist in _wishlists:
        _next_book = NextBook.query.filter_by(id_user=_wishlist.id_user).first()

        if _next_book.status == "None":
            _entry_wishlist = _wishlist.entry_wishlists
            if len(_entry_wishlist) != 0:
                if _wishlist.id_user not in users_with_wishlist.keys():
                    users_with_wishlist.update({_wishlist.id_user: []})

                if _wishlist.id_user not in trust_coeffs.keys():
                    _user = User.query.filter_by(id=_wishlist.id_user).first()
                    trust_coeffs.update({_wishlist.id_user: _user.trust_coeff})

                for _entry in _entry_wishlist:
                    _book = Book.query.filter_by(id=_entry.id_book).first()

                    users_with_wishlist[_wishlist.id_user].append(
                        (_book.id, _entry.period, _entry.rank)
                    )

                    if _book.id not in book_count.keys():
                        book_count.update({_book.id: _book.count_free_books})

    return users_with_wishlist, trust_coeffs, book_count

def update_ranks(rank,id_wishlist):
    _entryes_wishlist = EntryWishlist.query.filter_by(id_wishlist=id_wishlist)

    for entry in _entryes_wishlist:
        if entry.rank > rank:
            entry.rank -= 1
            db.session.commit()

def write_result_of_matching(matched):

    for match in matched:

        # check if user still wanted the book
        wishList = Wishlist.query.filter_by(id_user=match[0]).first()
        _entry_wishlit = EntryWishlist.query.filter_by(
            id_wishlist=wishList.id,
            id_book=match[1][0],
            period=match[1][1]
        ).first()

        _next_book = NextBook.query.filter_by(id_user=match[0]).first()

        if _entry_wishlit:
            rank = _entry_wishlit.rank

            db.session.delete(_entry_wishlit)

            _book_series = BookSeries.query.filter_by(book_id=match[1][0], status="available").first()
            _book_series.status = "taken"

            _book = Book.query.filter_by(id=match[1][0]).first()
            _book.count_free_books -= 1

            _next_book.id_book = match[1][0]
            _next_book.id_book_series = _book_series.id
            _next_book.period = match[1][1]
            _next_book.status = "Pending"

            db.session.commit()

            print("_next_book", _next_book.id_book, _next_book.period, _next_book.status)

            update_ranks(rank, wishList.id)


@celery.task()
def stable_matching_routine():
    users_with_wishlist, trust_coeffs, book_count = update_state()
    stable_matching = Stable_matching(users_with_wishlist, trust_coeffs, book_count)

    stable_matching.run()
    matched = stable_matching.get_match()
    del stable_matching

    write_result_of_matching(matched)
    logger.info("stable matching algorithm done")