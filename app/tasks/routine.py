from app import celery, logger, db
from app.models import NextBook, BookSeries, Book, EntryWishlist, Wishlist, Notifications, User_settings, User, \
    EntryLog, Log
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
                    coeff = 0
                    if user.count_books_returned != 0:
                        coeff = user.trust_coeff / user.count_books_returned
                    trust_coeffs.update({wishlist.id_user: coeff})

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
    entryes_wishlist = EntryWishlist.query.filter_by(id_wishlist=id_wishlist)

    for entry in entryes_wishlist:
        if entry.rank > rank:
            entry.rank -= 1
            db.session.commit()


def generate_notification(match, user_id):
    notification = Notifications(
        id_user=user_id,
        content="You received the {} book, you have 3hrs to accept or deny!".format(
            Book.query.filter_by(id=match['book_id']).first().name),
        status="unread",
        created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
            pytz.timezone('Europe/Bucharest'))
    )
    db.session.add(notification)
    db.session.commit()


def write_result_of_matching(matched):
    for user_id in matched.keys():

        # check if user still wanted the book
        wishList = Wishlist.query.filter_by(id_user=user_id).first()
        entry_wishlit = EntryWishlist.query.filter_by(
            id_wishlist=wishList.id,
            id_book=matched[user_id]['book_id'],
            period=matched[user_id]['nr_of_days'],
        ).first()

        next_book = NextBook.query.filter_by(id_user=user_id).first()

        if entry_wishlit:
            rank = entry_wishlit.rank

            db.session.delete(entry_wishlit)

            book_series = BookSeries.query.filter_by(
                book_id=matched[user_id]['book_id'],
                status="available"
            ).first()

            if not book_series:
                continue

            book_series.status = "taken"

            book = Book.query.filter_by(id=matched[user_id]['book_id']).first()
            book.count_free_books -= 1

            next_book.id_book = matched[user_id]['book_id']
            next_book.id_series_book = book_series.id
            next_book.period = matched[user_id]['nr_of_days']
            next_book.status = "Pending"
            next_book.rank = rank

            db.session.commit()

            print("_next_book", next_book.id_book, next_book.period, next_book.status, next_book.id_series_book)

            update_ranks(rank, wishList.id)
            generate_notification(matched[user_id], user_id)


def clean_unaccepted_books():
    next_book = NextBook.query.filter_by(status="Pending").all()

    for entry in next_book:
        time_now = datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('Europe/Bucharest'))
        time_entry = entry.updated_at
        # timedelta(hours=3)
        if (time_now - (time_entry + timedelta(seconds=100))) >= timedelta(seconds=0):

            book = Book.query.filter_by(id=entry.id_book).first()
            book.count_free_books += 1
            book_series = BookSeries.query.filter_by(id=entry.id_series_book).first()
            book_series.status = "available"

            rank = entry.rank
            id_user = entry.id_user
            period = entry.period
            id_book = entry.id_book

            entry.updated_at = time_now
            entry.id_book = None
            entry.id_series_book = None
            entry.period = None
            entry.status = "None"
            entry.rank = 0

            notification = Notifications(
                id_user=entry.id_user,
                content="You lost the {} book, because u did not accept within 3hrs ".format(book.name),
                status="unread",
                created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                    pytz.timezone('Europe/Bucharest'))
            )
            db.session.add(notification)
            db.session.commit()

            settings = User_settings.query.filter_by(id_user=id_user).first()

            if settings.wishlist_option == 1:
                id_wishlist = User.query.filter_by(id=id_user).first().wishlist.id
                entry_wishlist = EntryWishlist.query.filter_by(id_wishlist=id_wishlist).all()

                for entry in entry_wishlist:
                    if entry.rank >= rank:
                        entry.rank += 1
                        db.session.commit()

                entry_wishlist = EntryWishlist(
                    id_wishlist=id_wishlist,
                    id_book=id_book,
                    rank=rank,
                    period=period,
                    created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest'))
                )
                db.session.add(entry_wishlist)
                db.session.commit()
            elif settings.wishlist_option == 3:
                id_wishlist = User.query.filter_by(id=id_user).first().wishlist.id
                last_rank = EntryWishlist.query.filter_by(id_wishlist=id_wishlist).count()
                entry_wishlist = EntryWishlist(
                    id_wishlist=id_wishlist,
                    id_book=id_book,
                    rank=last_rank + 1,
                    period=period,
                    created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest'))
                )
                db.session.add(entry_wishlist)
                db.session.commit()


def update_remaining_book_time():
    entry_logs = db.session() \
        .query(EntryLog) \
        .filter(~(EntryLog.status.in_(["Returned", "Reserved expired"]))
                ).all()

    for entry in entry_logs:
        entry.period_diff = entry.period_end - datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
            pytz.timezone('Europe/Bucharest'))
        db.session.commit()
        # timedelta(hours=24)
        if entry.period_start + timedelta(seconds=100) < datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                pytz.timezone('Europe/Bucharest')) and entry.status == "Reserved":
            entry.status = "Reserved expired"
            db.session.commit()

            log = Log.query.filter_by(id=entry.id_log).first()
            book_series = BookSeries.query.filter_by(id=entry.id_book_series).first()
            book_series.status = "available"
            db.session.commit()
            book = Book.query.filter_by(id=book_series.book_id).first()
            book.count_free_books += 1
            db.session.commit()

            notification = Notifications(
                id_user=log.id_user,
                content="The 24 hours reservation on book {} expired !".format(book.name),
                status="unread",
                created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                    pytz.timezone('Europe/Bucharest'))
            )
            print(notification)
            db.session.add(notification)
            db.session.commit()


@celery.task()
def stable_matching_routine():
    clean_unaccepted_books()
    update_remaining_book_time()

    users_with_wishlist, trust_coeffs, book_count = update_state()
    stable_matching = Stable_matching(users_with_wishlist, trust_coeffs, book_count)
    stable_matching.run()
    matched = stable_matching.get_match()
    del stable_matching

    write_result_of_matching(matched)
    logger.info("Routine done")
