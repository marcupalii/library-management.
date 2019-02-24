print('importing schedule... %s' % __name__)
import threading
import time


datalock = threading.Lock()

DONE = True



posible_match = []
users_without_books = []
users_cannot_be_matched = []


def begin_matching(user,user_with_wishList,book_return_coefficient,quantity_per_book):
    global users_without_books
    print("DEALING WITH %s " %(user))

    for wish in user_with_wishList:

        taken_match = []
        taken_match = list(filter(lambda pair: str(pair[1][0]).strip() == str(wish[0]).strip(), posible_match))

        print("wish", wish)
        print("posible_match:", posible_match)
        print("taken_match:", taken_match)
        if (len(taken_match) == 0):
            posible_match.append([user, wish])

            users_without_books.remove(user)
            print('%s is no longer without a  book and is now matched with %s' % (user, wish))
            return

        elif (len(taken_match) > 0):

            if len(taken_match) < quantity_per_book.get(wish[0]):
                posible_match.append([user, wish])
                users_without_books.remove(user)
                return
            else:
                print('all book of type {} is taken already..'.format(wish))

                current_user_coeff = wish[1]-(book_return_coefficient.get(user)/100 * wish[1])

                #     search for user that reserved that book and their coeff is less than current_user_coeff

                for taken in taken_match:
                    print("taken:",taken)
                    user_taken_coeff = taken[1][1]-(book_return_coefficient.get(taken[0])/100 *taken[1][1])

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

    users_without_books = [key for key in users_with_wishlist.keys()]
    for key in users_with_wishlist.keys():
        users_with_wishlist[key] = [sorted(users_with_wishlist[key],key=lambda el : el[2])]

    print(users_with_wishlist)
    print(trust_coeffs)
    print(book_count)

    print(users_with_wishlist)
    while len(users_without_books) > 0:
        for user in users_with_wishlist:
            begin_matching(user,users_with_wishlist[user],trust_coeffs,book_count)

    print(posible_match)
    print(users_without_books)
    print(users_cannot_be_matched)

def update_state():
    from app.models import User, Wishlist, EntryWishlist, Book
    global data, DONE
    users_with_wishlist = {}
    trust_coeffs = {}
    book_count = {}

    _wishlists = Wishlist.query.all()

    for _wishlist in _wishlists:

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

    stable_matching(users_with_wishlist,trust_coeffs,book_count)
    DONE = True

def schedule_stable_match(_time):
    print("schedule_stable_match")
    print(_time)
    global DONE
    time.sleep(5)
    while True:
        if (time.time() - _time) % 20 >= 18 and DONE:
            DONE = False
            worker = threading.Thread(target=update_state())
            worker.start()


if __name__ =="__main__":

    # user_with_wishList = {
    #     'user1': 	[('B3', 3,4), ('B4', 7,3), ('B5', 20,2), ('B1', 2,1)],
    #     'user3': 	[('B2', 3,3), ('B1', 1,2), ('B5', 20,1)],
    #     'user4': 	[('B3', 3), ('B5', 2), ('B4', 5)],
    #     'user10': 	[('B2', 30,1)],
    #     'user5':    [('B3', 100,1)],
    #     'user6':    [('B3', 50,2), ('B5', 2,1)]
    # }
    #
    #
    # book_return_coefficient = {
    #     'user1': -10,
    #     'user3': 10,
    #     'user4': 25,
    #     'user10': -30,
    #     'user2':  15,
    #     'user5':  9,
    #     'user6':  9,
    # }
    # quantity_per_book= {
    #     'B1': 1,
    #     'B2': 1,
    #     'B3': 2,
    #     'B4': 1,
    #     'B5': 1,
    #     'B6': 1
    # }
    # stable_matching(user_with_wishList,book_return_coefficient,quantity_per_book)
    update_state()