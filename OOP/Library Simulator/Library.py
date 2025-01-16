# Author: Jody Hunter
# GitHub username: JodyAHunter
# Date: 01/13/2023
# Description: This program is a Library Simulator that utilizes three classes - LibraryItem, Patron, and Library.
# There are also three subclasses that inherit from the LibraryItem class - Book, Album, and Movie.
# This program uses these classes to keep track of the current status of a library's available items and its
# patrons along with their current items and possible overdue fees.

class LibraryItem:
    """Represents a Library item that can be checked out from the Library by a patron.
    Six data members include a library item id number, title of item, location of item,
    whether the item is currently checked out or not, if the item is currently requested
    by a patron, and the date that the item was last checked out."""
    def __init__(self, library_item_id, title):
        self._library_item_id = library_item_id
        self._title = title
        self._location = "ON_SHELF"
        self._checked_out_by = None
        self._requested_by = None
        self._date_checked_out = 0

    def get_library_item_id(self):
        """Get method that returns a LibraryItem object's id number."""
        return self._library_item_id

    def get_title(self):
        """Get method that returns the title of a LibraryItem object."""
        return self._title

    def get_location(self):
        """Get method for a libraryItem object's current location."""
        return self._location

    def set_location(self, new_location):
        """Set method for the location of a LibraryItem object."""
        self._location = new_location

    def get_checked_out_by(self):
        """Get method that returns the Patron who currently has checked out the item."""
        return self._checked_out_by

    def set_checked_out_by(self, patron_id):
        """Set method for the checked_out_by status of a LibraryItem by a Patron."""
        self._checked_out_by = patron_id

    def get_requested_by(self):
        """Get method that returns the Patron who currently has requested the item."""
        return self._requested_by

    def set_requested_by(self, patron_id):
        """Set method for the set_requested_by status of a LibraryItem by a Patron."""
        self._requested_by = patron_id

    def get_date_checked_out(self):
        """Get method that returns the day that the item was checked out."""
        return self._date_checked_out

    def set_date_checked_out(self, date):
        """Set method for the date_checked_out status of a LibraryItem."""
        self._date_checked_out = date


class Book(LibraryItem):
    """Represents a Book subclass that inherits from the LibraryItem Class."""
    def __init__(self, library_item_id, title, author):
        super().__init__(library_item_id, title)
        self._author = author

    def get_author(self):
        """Get method that returns the author's name of a Book object"""
        return self._author

    def get_check_out_length(self):
        """Get method that returns the number of days that a book may be checked out."""
        return 21


class Album(LibraryItem):
    """Represents an Album subclass that inherits from the LibraryItem Class."""
    def __init__(self, library_item_id, title, artist):
        super().__init__(library_item_id, title)
        self._artist = artist

    def get_artist(self):
        """Get method that returns the artist's name of an Album object."""
        return self._artist

    def get_check_out_length(self):
        """Get method that returns the number of days that an album may be checked out."""
        return 14


class Movie(LibraryItem):
    """Represents a Movie subclass that inherits from the LibraryItem Class."""
    def __init__(self, library_item_id, title, director):
        super().__init__(library_item_id, title)
        self._director = director

    def get_director(self):
        """Get method that returns the director's name of a Movie object."""
        return self._director

    def get_check_out_length(self):
        """Get method that returns the number of days that a movie may be checked out."""
        return 7


class Patron:
    """Represents a patron of the library. Four data members include a patron_id, name,
    a collection of checked_out_items, and a fine_amount for late fees."""
    def __init__(self, patron_id, name):
        self._patron_id = patron_id
        self._name = name
        self._checked_out_items = []
        self._fine_amount = 0

    def get_patron_id(self):
        """Get method that returns a Patron's patron_id."""
        return self._patron_id

    def get_name(self):
        """Get method that returns a Patron's name."""
        return self._name

    def get_checked_out_items(self):
        """Get method that returns a Patron's list of checked_out_items."""
        return self._checked_out_items

    def get_fine_amount(self):
        """Get method that returns a Patron's fine_amount."""
        return round(self._fine_amount, 2)

    def add_library_item(self, library_item):
        """Method that takes a library_item and adds it to the collection of checked_out_items."""
        self._checked_out_items.append(library_item)

    def remove_library_item(self, library_item):
        """Method that takes a library_item and removes it from the collection of checked_out_items."""
        self._checked_out_items.remove(library_item)

    def amend_fine(self, amount):
        """Method that changes the Patron's current fine_amount."""
        self._fine_amount += amount


class Library:
    """Represents a Library that has an inventory of LibraryItems and is used by numerous Patrons."""
    def __init__(self):
        self._holdings = []
        self._members = []
        self._current_date = 0

    def get_holdings(self):
        """Get method that returns a list of the Library's LibraryItem objects."""
        return self._holdings

    def get_members(self):
        """Get method that returns a list of the Library's Patrons."""
        return self._members

    def get_current_day(self):
        """Get method that returns the current date of a Library."""
        return self._current_date

    def add_library_item(self, library_item):
        """Method that adds a LibraryItem object to the holding's collection."""
        self._holdings.append(library_item)

    def add_patron(self, patron):
        """Method that adds a Patron object to the members collections."""
        self._members.append(patron)

    def lookup_library_item_from_id(self, library_item_id):
        """Method that takes a library_item_id number, iterates through the Library's holdings list,
        and returns the object associated with the given id or None if item does not exist in the
        holding's collection."""
        for library_item in self._holdings:
            if library_item.get_library_item_id() == library_item_id:
                return library_item
        return None

    def lookup_patron_from_id(self, patron_id):
        """Method that takes a patron_id number, and iterates through the Library's members list,
         and returns the patron associated with the given id or None if patron does not exist in
         the member's collection."""
        for patron in self._members:
            if patron.get_patron_id() == patron_id:
                return patron
        return None

    def check_out_library_item(self, patron_id, library_item_id):
        """Method that takes a given patron_id and library_item_id. The previously established
        lookup_library_item_from_id and lookup_patron_from_id methods are used to establish a
        patron and library_item variable that holds the value of the patron object and library_item
        object associated with the given id respectively. If the patron object returned from the
        lookup method is None, then a message is returned informing the user that a patron by that
        id does not exist. Likewise, if the library_item object returned is None, then a message is
        returned informing the user that a library_item by that id does not exist. The LibraryItem's
        get_location method is called and returns a message that the item is already checked out if
        its current location is CHECKED_OUT. If the get_location and get_requested_by methods show
        that the item is currently on hold and requested by a different patron, it will return a
        message informing the user that the item is currently on hold by someone else. If none of
        these conditions are met, then we iterate through each item in the Library's holdings,
        comparing the library_item variable with each item until a match is found. Once a match is
        found, the item's checked_out_by_status is set to the patron object, date_checked_out is set
        to the library's current date, the item's location is set to CHECKED_OUT, if the item was
        currently requested by the patron given, the item's requested_by status is set to None, and
        the item is added to the patron's list of checked out items. A message is also returned stating
        that the check-out was successful."""
        patron = self.lookup_patron_from_id(patron_id)
        library_item = self.lookup_library_item_from_id(library_item_id)
        if patron is None:
            return "patron not found"
        elif library_item is None:
            return "item not found"
        elif library_item.get_location() == "CHECKED_OUT":
            return "item already checked out"
        elif (library_item.get_location() == "ON_HOLD_SHELF") and (library_item.get_requested_by() != patron):
            return "item on hold by other patron"
        else:
            for item in self._holdings:
                if item == library_item:
                    item.set_checked_out_by(patron_id)
                    item.set_date_checked_out(self._current_date)
                    item.set_location("CHECKED_OUT")
                    if item.get_requested_by() == patron:
                        item.set_requested_by(None)
                    patron.add_library_item(item)
                    return "check out successful"

    def return_library_item(self, library_item_id):
        """Method that takes a given library_item_id and uses the lookup_library_item_from_id method
        to initialize the library item to a library_item variable. If the value of the library item
        returned from the lookup method is None, a message is returned stating that the library item
        does not exist. The get location method is then used to check if the library item is not checked
        out already. If the item is not currently checked out, a message is returned stating that the
        item is already in the library. If the library item exists, and it is checked out, the
        get_checked_out_by method is used to find the id of the patron who currently has the item being
        returned. This value is initialized to a patron_id variable. This patron_id variable is then used
        along with the lookup_patron_from_id method to get the patron object and initialize the value to a
        patron variable. The library item is removed from the patron's list of checked_out_items using the
        remove_library_item method. If the library item is currently requested, the item's new location
        is set to ON_HOLD_SHELF. If the item is not currently requested, the new location is set to ON_SHELF.
        Finally, the item's checked_out_by status is set to None, and a message is returned stating that
        the return was successful."""
        library_item = self.lookup_library_item_from_id(library_item_id)
        if library_item is None:
            return "item not found"
        elif library_item.get_location() != "CHECKED_OUT":
            return "item already in library"
        else:
            patron_id = library_item.get_checked_out_by()
            patron = self.lookup_patron_from_id(patron_id)
            patron.remove_library_item(library_item)
            if library_item.get_requested_by() is not None:
                library_item.set_location("ON_HOLD_SHELF")
            else:
                library_item.set_location("ON_SHELF")
            library_item.set_checked_out_by(None)
            return "return successful"

    def request_library_item(self, patron_id, library_item_id):
        """Method that takes a given patron_id and library_item_id. The previously established
        lookup_library_item_from_id and lookup_patron_from_id methods are used to establish a
        patron and library_item variable that holds the value of the patron object and library_item
        object associated with the given id respectively. If the patron object returned from the
        lookup method is None, then a message is returned informing the user that a patron by that
        id does not exist. Likewise, if the library_item object returned is None, then a message is
        returned informing the user that a library_item by that id does not exist. If the library
        item's requested_by_status is not None, then a message is returned stating that the item is
        already on hold. If the item is not already on hold, then the item's new requested_by status
        is set to the patron object returned from the used lookup method. If the item's current location
        is ON_SHELF, then its location is set to ON_HOLD_SHELF. A message is returned stating that the
        request was successful."""
        patron = self.lookup_patron_from_id(patron_id)
        library_item = self.lookup_library_item_from_id(library_item_id)
        if patron is None:
            return "patron not found"
        elif library_item is None:
            return "item not found"
        elif library_item.get_requested_by() is not None:
            return "item already on hold"
        else:
            library_item.set_requested_by(patron)
            if library_item.get_location() == "ON_SHELF":
                library_item.set_location("ON_HOLD_SHELF")
            return "request successful"

    def pay_fine(self, patron_id, dollar_amount):
        """Method that takes a patron_id and a dollar_amount to pay a patron's fine from overdue items.
        The lookup_from_patron_id method is used to initialize a patron variable with the value of the
        patron object associated with the given id. If the patron's value is None, a message is returned
        stating that the patron does not exist. The amend_fine method is used with a negative sign to subtract
        the dollar_amount being paid from the patron's current fine_amount. A message is returned stating
        that the payment was successful."""
        patron = self.lookup_patron_from_id(patron_id)
        if patron is None:
            return "patron not found"
        else:
            patron.amend_fine(-dollar_amount)
            return "payment successful"

    def increment_current_date(self):
        """Method that is used to increment the current day of a library while also tracking overdue
        library items and adjusting patron's fines as needed. This method uses nested for loops to
        iterate through each item held by each patron in the library's list of members.
        in the library's list of members. For each item in each patron's list of checked_out_items,
        a days_checked_out variable is initialized with the result of the current_date of the library
        minus the date that each item was checked out. This days_checked_out value is then compared to
        the check_out_length of each item. If the days_checked_out value is greater than the item's
        check_out_length, the patron's fine is increased by $0.10 (10 cents)."""
        self._current_date += 1
        for patron in self._members:
            for item in patron.get_checked_out_items():
                days_checked_out = self._current_date - item.get_date_checked_out()
                if days_checked_out > item.get_check_out_length():
                    patron.amend_fine(0.10)
