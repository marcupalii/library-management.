from app import celery, logger, db
from app.models import NextBook, BookSeries, Book, EntryWishlist, Wishlist, Notifications
from app.Stable_matching_algorithm.algorithm import Stable_matching
from datetime import datetime, timedelta
import pytz


def update_state():
    from app.models import User, NextBook, Book, Wishlist
    wishlists = Wishlist.query.all()

    users_with_wishlist = {}
    trust_coeffs = {}
    book_count = {}

    for wishlist in wishlists:
        next_book = NextBook.query.filter_by(id_user=wishlist.id_user).first()

        if next_book.status == "None":
            entry_wishlist = wishlist.entry_wishlists
            if len(entry_wishlist) != 0:
                if wishlist.id_user not in users_with_wishlist.keys():
                    users_with_wishlist.update({wishlist.id_user: []})

                if wishlist.id_user not in trust_coeffs.keys():
                    user = User.query.filter_by(id=wishlist.id_user).first()
                    trust_coeffs.update({wishlist.id_user: user.trust_coeff})

                for entry in entry_wishlist:
                    book = Book.query.filter_by(id=entry.id_book).first()

                    users_with_wishlist[wishlist.id_user].append({
                        'book_id': book.id,
                        'nr_of_days': entry.period,
                        'rank': entry.rank
                    })

                    if book.id not in book_count.keys():
                        book_count.update({book.id: book.count_free_books})

    return users_with_wishlist, trust_coeffs, book_count


def update_ranks(rank, id_wishlist):
    _entryes_wishlist = EntryWishlist.query.filter_by(id_wishlist=id_wishlist)

    for entry in _entryes_wishlist:
        if entry.rank > rank:
            entry.rank -= 1
            db.session.commit()


def generate_notification(match,user_id):
    notification = Notifications(
        id_user=user_id,
        content="You received the {} book, you have 3hrs to accept or deny!".format(
            Book.query.filter_by(id=match['book_id']).first().name),
        status="unread"
    )
    db.session.add(notification)
    db.session.commit()


def write_result_of_matching(matched):
    for user_id in matched.keys():

        # check if user still wanted the book
        wishList = Wishlist.query.filter_by(id_user=user_id).first()
        _entry_wishlit = EntryWishlist.query.filter_by(
            id_wishlist=wishList.id,
            id_book=matched[user_id]['book_id'],
            period=matched[user_id]['nr_of_days']
        ).first()

        _next_book = NextBook.query.filter_by(id_user=user_id).first()

        if _entry_wishlit:
            rank = _entry_wishlit.rank

            db.session.delete(_entry_wishlit)

            _book_series = BookSeries.query.filter_by(
                book_id=matched[user_id]['book_id'],
                status="available"
            ).first()

            _book_series.status = "taken"

            _book = Book.query.filter_by(id=matched[user_id]['book_id']).first()
            _book.count_free_books -= 1

            _next_book.id_book = matched[user_id]['book_id']
            _next_book.id_series_book = _book_series.id
            _next_book.period =matched[user_id]['nr_of_days']
            _next_book.status = "Pending"

            db.session.commit()

            print("_next_book", _next_book.id_book, _next_book.period, _next_book.status, _next_book.id_series_book)

            update_ranks(rank, wishList.id)
            generate_notification(matched[user_id],user_id)


def clean_unaccepted_books():
    _next_book = NextBook.query.filter_by(status="Pending").all()

    for entry in _next_book:
        time_now = datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('Europe/Bucharest'))
        time_entry = entry.updated_at.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('Europe/Bucharest'))
        if (time_entry + timedelta(seconds=50)) - time_now >= timedelta(seconds=0):
            _book = Book.query.filter_by(id=entry.id_book).first()
            _book.count_free_books += 1
            _book_series = BookSeries.query.filter_by(id=entry.id_series_book).first()
            _book_series.status = "available"

            entry.updated_at = time_now
            entry.id_book = None
            entry.id_series_book = None
            entry.period = None
            entry.status = "None"

            notification = Notifications(
                id_user=entry.id_user,
                content="You lost the {} book, because u did not accept within 3hrs ".format(_book.name),
                status="unread"
            )
            db.session.add(notification)

            db.session.commit()


@celery.task()
def stable_matching_routine():
    clean_unaccepted_books()

    users_with_wishlist, trust_coeffs, book_count = update_state()

    stable_matching = Stable_matching(users_with_wishlist, trust_coeffs, book_count)
    stable_matching.run()
    matched = stable_matching.get_match()
    del stable_matching

    write_result_of_matching(matched)
    logger.info("stable matching algorithm done")
