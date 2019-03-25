
import time
import schedule
posible_match = []
users_without_books = []
users_cannot_be_matched = []


def write_result_of_matching():
    global posible_match, users_cannot_be_matched
    from app.models import NextBook, BookSeries, Book
    from app import db

    for match in posible_match:

        _next_book = NextBook.query.filter_by(id_user=match[0]).first()
        print("==",match[1][0],"==",type(match[1][0]))
        print("BookSeries.query.all()",BookSeries.query.all())
        _book_series = BookSeries.query.filter_by(book_id=match[1][0], status="available").first()
        _book_series.status = "taken"
        db.session.commit()

        _book = Book.query.filter_by(id=match[1][0]).first()
        _book.count_free_books -= 1
        db.session.commit()

        _next_book.id_book = match[1][0]
        _next_book.id_book_series = _book_series.id
        _next_book.period = match[1][1]
        _next_book.status = "Checking"
        print("_next_book", _next_book.id_book,_next_book.period,_next_book.status)
        db.session.commit()

    posible_match.clear()
    print("users_cannot_be_matched",users_cannot_be_matched)


def begin_matching(user, user_with_wishList, book_return_coefficient, quantity_per_book):
    global users_without_books

    for wish in user_with_wishList:

        taken_match = []
        taken_match = list(filter(lambda pair: str(pair[1][0]).strip() == str(wish[0]).strip(), posible_match))

        if len(taken_match) == 0:
            posible_match.append([user, wish])
            users_without_books.remove(user)
            return

        elif len(taken_match) > 0:

            if len(taken_match) < quantity_per_book.get(wish[0]):
                posible_match.append([user, wish])
                users_without_books.remove(user)
                return
            else:
                current_user_coeff = wish[1]-(book_return_coefficient.get(user)/100 * wish[1])
                for taken in taken_match:
                    user_taken_coeff = taken[1][1]-(book_return_coefficient.get(taken[0])/100 * taken[1][1])
                    if user_taken_coeff > current_user_coeff:
                        posible_match.remove(taken)
                        posible_match.append([user, wish])
                        users_without_books.remove(user)
                        users_without_books.append(taken[0])
                        return

    users_without_books.remove(user)
    users_cannot_be_matched.append([user,wish])


def stable_matching(users_with_wishlist, trust_coeffs, book_count):

    global users_without_books

    users_without_books = [key for key in users_with_wishlist.keys()]
    for key in users_with_wishlist.keys():
        temp = users_with_wishlist[key]
        users_with_wishlist[key] = []
        users_with_wishlist[key] += [el for el in sorted(temp, key=lambda el: el[2])]

    while len(users_without_books) > 0:
        for user in users_with_wishlist:
            begin_matching(user, users_with_wishlist[user], trust_coeffs, book_count)


def update_state():
    from app.models import User, Wishlist, Book, NextBook

    users_with_wishlist = {}
    trust_coeffs = {}
    book_count = {}

    _wishlists = Wishlist.query.all()


    for _wishlist in _wishlists:
        _next_book = NextBook.query.filter_by(id_user=_wishlist.id_user).first()

        if _next_book.status == "None":
            _entry_wishlist = _wishlist.entry_wishlists
            if len(_entry_wishlist) != 0:
                if _wishlist.id_user not in users_with_wishlist.keys():
                    users_with_wishlist.update({_wishlist.id_user: []})

                if _wishlist.id_user not in trust_coeffs.keys():
                    _user = User.query.filter_by(id=_wishlist.id_user).first()
                    trust_coeffs.update({_wishlist.id_user:_user.trust_coeff})

                for _entry in _entry_wishlist:
                    _book = Book.query.filter_by(id=_entry.id_book).first()

                    users_with_wishlist[_wishlist.id_user].append(
                        (_book.id, _entry.period, _entry.rank)
                    )

                    if _book.id not in book_count.keys():
                        book_count.update({_book.id: _book.count_free_books})

    return users_with_wishlist, trust_coeffs, book_count


T = time.time()


def routine():
    print(time.time()-T)
    users_with_wishlist, trust_coeffs, book_count = update_state()
    stable_matching(users_with_wishlist,trust_coeffs,book_count)
    write_result_of_matching()


def schedule_routine():
    time.sleep(5)
    schedule.every(20).seconds.do(routine)
    while True:
        schedule.run_pending()
        time.sleep(1)


