
import time
import schedule

T = time.time()

class Stable_matching:

    def __init__(self):
        self.__users_with_wishlist = {}
        self.__trust_coeffs = {}
        self.__book_count = {}
        self.__posible_match = []
        self.__users_without_books = []
        self.__users_cannot_be_matched = []

    def __update_state(self):
        from app.models import User, Wishlist, Book, NextBook
        _wishlists = Wishlist.query.all()

        for _wishlist in _wishlists:
            _next_book = NextBook.query.filter_by(id_user=_wishlist.id_user).first()

            if _next_book.status == "None":
                _entry_wishlist = _wishlist.entry_wishlists
                if len(_entry_wishlist) != 0:
                    if _wishlist.id_user not in self.__users_with_wishlist.keys():
                        self.__users_with_wishlist.update({_wishlist.id_user: []})

                    if _wishlist.id_user not in self.__trust_coeffs.keys():
                        _user = User.query.filter_by(id=_wishlist.id_user).first()
                        self.__trust_coeffs.update({_wishlist.id_user: _user.trust_coeff})

                    for _entry in _entry_wishlist:
                        _book = Book.query.filter_by(id=_entry.id_book).first()

                        self.__users_with_wishlist[_wishlist.id_user].append(
                            (_book.id, _entry.period, _entry.rank)
                        )

                        if _book.id not in self.__book_count.keys():
                            self.__book_count.update({_book.id: _book.count_free_books})

    def __sort_state_data(self):
        self.__users_without_books = [key for key in self.__users_with_wishlist.keys()]
        for key in self.__users_with_wishlist.keys():
            temp = self.__users_with_wishlist[key]
            self.__users_with_wishlist[key] = []
            self.__users_with_wishlist[key] += [el for el in sorted(temp, key=lambda el: el[2])]

    def __match_user(self,user):

        for wish in self.__users_with_wishlist[user]:
            taken_match = list(filter(lambda pair: str(pair[1][0]).strip() == str(wish[0]).strip(), self.__posible_match))

            if len(taken_match) == 0:
                self.__posible_match.append([user, wish])
                self.__users_without_books.remove(user)
                return

            elif len(taken_match) > 0:

                if len(taken_match) < self.__book_count.get(wish[0]):
                    self.__posible_match.append([user, wish])
                    self.__users_without_books.remove(user)
                    return
                else:
                    current_user_coeff = wish[1] - (self.__trust_coeffs.get(user) / 100 * wish[1])
                    for taken in taken_match:
                        user_taken_coeff = taken[1][1] - (self.__trust_coeffs.get(taken[0]) / 100 * taken[1][1])
                        if user_taken_coeff > current_user_coeff:
                            self.__posible_match.remove(taken)
                            self.__posible_match.append([user, wish])
                            self.__users_without_books.remove(user)
                            self.__users_without_books.append(taken[0])
                            return

        self.__users_without_books.remove(user)
        self.__users_cannot_be_matched.append([user, self.__users_with_wishlist[user]])

    def __begin_matching(self):

        while len(self.__users_without_books) > 0:
            for user in self.__users_with_wishlist:
                self.__match_user(user)

        self.__users_with_wishlist.clear()
        self.__trust_coeffs.clear()
        self.__book_count.clear()

    def __write_result_of_matching(self):
        from app.models import NextBook, BookSeries, Book
        from app import db

        for match in self.__posible_match:
            _next_book = NextBook.query.filter_by(id_user=match[0]).first()
            print("==", match[1][0], "==", type(match[1][0]))
            print("BookSeries.query.all()", BookSeries.query.all())
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
            print("_next_book", _next_book.id_book, _next_book.period, _next_book.status)
            db.session.commit()

        print("users_cannot_be_matched", self.__users_cannot_be_matched)
        self.__posible_match.clear()
        self.__users_cannot_be_matched.clear()

    def run(self):
        print(time.time() - T)
        self.__update_state()
        self.__sort_state_data()
        self.__begin_matching()
        self.__write_result_of_matching()


def schedule_routine():
    time.sleep(5)
    stable_matching = Stable_matching()
    schedule.every(20).seconds.do(stable_matching.run)
    while True:
        schedule.run_pending()
        time.sleep(1)


