# print('importing schedule... %s' % __name__)
import time
import schedule
posible_match = []
users_without_books = []
users_cannot_be_matched = []


def write_result_of_matching():
    global posible_match, users_cannot_be_matched
    from app.models import NextBook
    from app import db

    for match in posible_match:
        _next_book = NextBook.query.filter_by(id_user=int(match[0]))

        _next_book.id_book = int(match[1][0])
        _next_book.period = match[1][1]
        _next_book.status = "Checking"
        print("_next_book", _next_book.id_book,_next_book.period,_next_book.status)
        db.session.commit()

    posible_match = []

    for unmatch in users_cannot_be_matched:
        _next_book = NextBook.query.filter_by(id_user=int(unmatch[0]))
        _next_book.id_book = int(unmatch[1][0])
        _next_book.period = unmatch[1][1]
        _next_book.status = "None"
        db.session.commit()

    users_cannot_be_matched = []


def begin_matching(user, user_with_wishList, book_return_coefficient, quantity_per_book):
    global users_without_books
    # print("DEALING WITH %s " %(user))

    for wish in user_with_wishList:

        taken_match = []
        taken_match = list(filter(lambda pair: str(pair[1][0]).strip() == str(wish[0]).strip(), posible_match))

        # print("wish", wish)
        # print("posible_match:", posible_match)
        # print("taken_match:", taken_match)
        if (len(taken_match) == 0):
            posible_match.append([user, wish])

            users_without_books.remove(user)
            # print('%s is no longer without a  book and is now matched with %s' % (user, wish))
            return

        elif len(taken_match) > 0:

            if len(taken_match) < quantity_per_book.get(wish[0]):
                posible_match.append([user, wish])
                users_without_books.remove(user)
                return
            else:
                # print('all book of type {} is taken already..'.format(wish))

                current_user_coeff = wish[1]-(book_return_coefficient.get(user)/100 * wish[1])

                #     search for user that reserved that book and their coeff is less than current_user_coeff

                for taken in taken_match:
                    # print("taken:",taken)
                    user_taken_coeff = taken[1][1]-(book_return_coefficient.get(taken[0])/100 * taken[1][1])

                    if user_taken_coeff > current_user_coeff:
                        posible_match.remove(taken)
                        posible_match.append([user, wish])
                        users_without_books.remove(user)
                        users_without_books.append(taken[0])
                        return

    users_without_books.remove(user)
    users_cannot_be_matched.append([user,wish])


def stable_matching(users_with_wishlist,trust_coeffs,book_count):

    global users_without_books
    # print("users_with_wishlist", users_with_wishlist)
    users_without_books = [key for key in users_with_wishlist.keys()]
    for key in users_with_wishlist.keys():
        temp = users_with_wishlist[key]
        users_with_wishlist[key] = []
        users_with_wishlist[key] += [el for el in sorted(temp, key=lambda el: el[2])]

    print("users_with_wishlist",users_with_wishlist)
    print("trust_coeffs",trust_coeffs)
    print("book_count",book_count)

    # print(users_with_wishlist)
    while len(users_without_books) > 0:
        for user in users_with_wishlist:
            begin_matching(user,users_with_wishlist[user],trust_coeffs,book_count)


def update_state():
    from app.models import User, Wishlist, Book, NextBook

    users_with_wishlist = {}
    trust_coeffs = {}
    book_count = {}

    _wishlists = Wishlist.query.all()

    for _wishlist in _wishlists:
        _next_book = NextBook.query.filter_by(id_user=_wishlist.id_user).first()

        if _next_book.status == "None":
            if _wishlist.id_user not in users_with_wishlist.keys():
                users_with_wishlist.update({str(_wishlist.id_user): []})

            if _wishlist.id_user not in trust_coeffs.keys():
                _user = User.query.filter_by(id=_wishlist.id_user).first()
                trust_coeffs.update({str(_wishlist.id_user):_user.trust_coeff})

            _entrywishlist = _wishlist.entrywishlist
            _book = Book.query.filter_by(id=_entrywishlist.id_book).first()

            users_with_wishlist[str(_wishlist.id_user)].append(
                (str(_book.id),_entrywishlist.period,_entrywishlist.rank)
            )

            if _book.id not in book_count.keys():
                book_count.update({str(_book.id):_book.count})

    return (users_with_wishlist,trust_coeffs,book_count)


T = time.time()


def routine():
    print(time.time()-T)
    users_with_wishlist,trust_coeffs,book_count = update_state()
    stable_matching(users_with_wishlist,trust_coeffs,book_count)
    write_result_of_matching()


def schedule_stable_match():
    schedule.every(1).seconds.do(routine)
    time.sleep(5)
    while True:
        schedule.run_pending()
        time.sleep(1)



