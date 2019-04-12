
class Stable_matching:

    def __init__(self,users_with_wishlist, trust_coeffs, book_count):
        self.__users_with_wishlist = users_with_wishlist
        self.__trust_coeffs = trust_coeffs
        self.__book_count = book_count
        self.__posible_match = []
        self.__users_without_books = []
        self.__users_cannot_be_matched = []

    def get_match(self):
        return self.__posible_match

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

    def run(self):
        self.__sort_state_data()
        self.__begin_matching()



