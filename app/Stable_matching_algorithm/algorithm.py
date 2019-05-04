
class Stable_matching:

    def __init__(self,users_with_wishlist, trust_coeffs, book_count):
        self.__users_with_wishlist = users_with_wishlist
        self.__trust_coeffs = trust_coeffs
        self.__book_count = book_count
        self.__posible_match = {}
        self.__users_without_books = []
        self.__users_cannot_be_matched = []

    def get_match(self):
        return self.__posible_match

    def __sort_state_data(self):
        self.__users_without_books = [key for key in self.__users_with_wishlist.keys()]
        for user_id in self.__users_with_wishlist.keys():
            wishlist = self.__users_with_wishlist[user_id]
            self.__users_with_wishlist[user_id] = [wish for wish in sorted(wishlist, key=lambda wish: wish['rank'])]

    def __match_user(self,user):

        for wish in self.__users_with_wishlist[user]:
            taken_match = {
                u_id: self.__posible_match[u_id] for u_id in filter(
                    lambda user_id:
                        str(self.__posible_match[user_id]['book_id']).strip() ==
                        str(wish['book_id']).strip(), self.__posible_match.keys()
                    )
            }

            if len(taken_match) == 0:
                self.__posible_match.update({user: wish})
                self.__users_without_books.remove(user)
                return

            elif len(taken_match) > 0:

                if len(taken_match) < self.__book_count.get(wish['book_id']):
                    self.__posible_match.update({user: wish})
                    self.__users_without_books.remove(user)
                    return
                else:
                    current_user_coeff = wish['nr_of_days'] - (self.__trust_coeffs.get(user) / 100 * wish['nr_of_days'])
                    for user_id in taken_match.keys():
                        user_taken_coeff = taken_match[user_id]['nr_of_days'] - (self.__trust_coeffs.get(user_id) / 100 * taken_match[user_id]['nr_of_days'])
                        if user_taken_coeff > current_user_coeff:
                            self.__posible_match.pop(taken_match[user_id],"None")
                            self.__posible_match.update({user: wish})
                            self.__users_without_books.remove(user)
                            self.__users_without_books.append(taken_match[user_id])
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



