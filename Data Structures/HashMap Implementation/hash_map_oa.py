# Name: Jody Hunter
# OSU Email: huntejod@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap (Portfolio Assignment)
# Due Date: 06/09/2023
# Description: HashMap implementation with collision handling by open addressing

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Method that adds a new key/value pair in the hash map, or if the
        key already exists, its current value is overwritten.
        """
        # Resize the hash map by doubling its capacity if table load > 0.5
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity*2)

        # obtain hash value by calling hash function on the given key
        hash = self._hash_function(key)

        # obtain index for given key/value pair
        index = hash % self._capacity

        # If the index is empty, place a hash entry with the key/value pair
        # at the given index using the dynamic array set_at_index method
        if self._buckets[index] is None:
            self._buckets.set_at_index(index, HashEntry(key, value))
            # Increment hash map size by 1
            self._size += 1

        # If the index is not empty, use quadratic probing to find empty index
        else:
            # Initialize a 'j' variable starting at 1
            j = 1
            # Initialize a quadratic probing variable equal to index
            quad_probe = index

            # Loop until the quadratic probe finds an empty index
            while self._buckets[quad_probe] is not None:

                # If key at current index matches the key given in this method
                if self._buckets[quad_probe].key == key:

                    # If the hash entry at current index is not a tombstone
                    if not self._buckets[quad_probe].is_tombstone:

                        # Place given Hash entry at index, overwriting value
                        self._buckets[quad_probe] = HashEntry(key, value)
                        return

                    # If the hash entry at current index is a tombstone
                    elif self._buckets[quad_probe].is_tombstone:

                        # Place given Hash entry at index, increment size
                        self._buckets[quad_probe] = HashEntry(key, value)
                        self._size += 1
                        return

                # update index using quadratic probe formula
                quad_probe = (index + j ** 2) % self._capacity
                j += 1

            # When empty index is found, place Hash entry, increment size
            self._buckets.set_at_index(quad_probe, HashEntry(key, value))
            self._size += 1


    def table_load(self) -> float:
        """
        Method that returns the hash table's load factor
        """
        # Divide hash map's size by capacity and return the result
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Method that returns how many of the buckets in the hash map are empty.
        """
        # Subtract hash map size from hash map capacity and return the result
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Method that updates the capacity of the hash map and rehashes all
        existing content in the hash map.
        """
        # If new capacity given is less than hash map size, do nothing
        if new_capacity < self._size:
            return

        # New capacity must be a prime number
        # Call is_prime method, if not True, set new_capacity to next prime num
        if self._is_prime(new_capacity) is None:
            new_capacity = self._next_prime(new_capacity)

        # Create a new hash map object with the new capacity
        new_hash_map = HashMap(new_capacity, self._hash_function)

        # Handles case where new capacity is 2, keeps hash map initialization
        # from changing new_capacity from 2 to 3
        if new_capacity == 2:
            new_hash_map._capacity = 2

        # Iterate over the range of the capacity of the hash map
        for i in range(self._capacity):

            # If the current index of the underlying array is not empty
            if self._buckets[i] is not None:

                # If the current index's hash entry is not a tombstone
                if not self._buckets[i].is_tombstone:

                    # Call put method for new hash map, with the key and value
                    # from the current index of the original hash map
                    new_hash_map.put(self._buckets[i].key, self._buckets[i].value)

        # Re-assign the original hash map's capacity, size, and buckets
        # to the new hash map's capacity, size, and buckets
        self._capacity = new_hash_map._capacity
        self._size = new_hash_map._size
        self._buckets = new_hash_map._buckets

    def get(self, key: str) -> object:
        """
        Method that takes a given key and returns its value, or None
        if the key does not exist in the hash map.
        """
        # obtain hash value by calling hash function on the given key
        hash = self._hash_function(key)

        # obtain index for given key
        index = hash % self._capacity

        # Initialize a variable with the hash entry at the index of the hash map
        index_entry = self._buckets[index]

        # If the index is empty, do nothing
        if index_entry is None:
            return

        # If the entry's key matches given key and is not a tombstone
        if index_entry.key == key and index_entry.is_tombstone is False:
            # return the value of the entry
            return index_entry.value

        # Otherwise, implement quadratic probing
        else:
            # Initialize a 'j' variable starting at 1
            j = 1
            # Initialize a quadratic probing variable equal to index
            quad_probe = index

            # Loop until the entry at the index is empty
            while self._buckets[quad_probe] is not None:
                # If key at index matches given key
                if self._buckets[quad_probe].key == key:
                    # If entry is not a tombstone, return the value
                    if not self._buckets[quad_probe].is_tombstone:
                        return self._buckets[quad_probe].value

                # update index using quadratic probe formula
                quad_probe = (index + j ** 2) % self._capacity
                j += 1

            # Return None if key is not found in the hash map
            return None

    def contains_key(self, key: str) -> bool:
        """
        Method that takes a given key and returns True if the key exists in
        the hash map, or False if it does not exist.
        """
        # obtain hash value by calling hash function on the given key
        hash = self._hash_function(key)

        # obtain index for given key
        index = hash % self._capacity

        # Initialize a variable with the hash entry at the index of the hash map
        index_entry = self._buckets[index]

        # If index is empty, return False
        if index_entry is None:
            return False

        # If key of entry matches key given and entry is not a tombstone
        if index_entry.key == key and index_entry.is_tombstone is False:
            # Return True
            return True

        # Otherwise, implement quadratic probing
        else:
            # Initialize a 'j' variable starting at 1
            j = 1
            # Initialize a quadratic probing variable equal to index
            quad_probe = index

            # Loop until the entry at the index is empty
            while self._buckets[quad_probe] is not None:
                # If the key of the entry at the index matches given key
                if self._buckets[quad_probe].key == key:
                    # If entry at index is not a tombstone, return True
                    if not self._buckets[quad_probe].is_tombstone:
                        return True

                # update index using quadratic probe formula
                quad_probe = (index + j ** 2) % self._capacity
                j += 1

            # Return False if key is not found in the hash map
            return False


    def remove(self, key: str) -> None:
        """
        Method that takes a given key and removes the key/pair value.
        """
        # obtain hash value by calling hash function on the given key
        hash = self._hash_function(key)

        # obtain index for given key
        index = hash % self._capacity

        # Initialize a variable for the entry at the index to be removed
        remove = self._buckets[index]

        # If the index is empty, do nothing
        if remove is None:
            return

        # If the key of the entry matches the given key and is not a tombstone
        if remove.key == key and remove.is_tombstone is False:
            # Change the entry's is_tombstone value to True
            remove.is_tombstone = True
            # Decrement the hash map size by 1
            self._size -= 1

        # Otherwise, implement quadratic probing
        else:
            # Initialize a 'j' variable starting at 1
            j = 1
            # Initialize a quadratic probing variable equal to index
            quad_probe = index

            # Loop until the entry at the index is empty
            while self._buckets[quad_probe] is not None:
                # If the key of the entry at the index matches given key
                if self._buckets[quad_probe].key == key:
                    # If entry at index is not a tombstone
                    if not self._buckets[quad_probe].is_tombstone:
                        # Change entry's is_tombstone value to True
                        self._buckets[quad_probe].is_tombstone = True
                        # Decrement the hash map size by 1
                        self._size -= 1

                # update index using quadratic probe formula
                quad_probe = (index + j ** 2) % self._capacity
                j += 1

    def clear(self) -> None:
        """
        Method that erases the contents of the hash map; capacity unchanged
        """
        # Initialize a new empty dynamic array
        new_dyn_arr = DynamicArray()

        # Assign the hash map's buckets to the new array
        self._buckets = new_dyn_arr

        # Loop over the range of the hash map's capacity
        for i in range(self._capacity):
            # Append the value None to each bucket in the hash map
            self._buckets.append(None)

        # Assign the hash map's size to 0
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method that creates and returns a dynamic array where each index is a
        tuple containing a key/value pair from the hash map.
        """
        # Initialize a dynamic array that will store the key/value pairs
        keys_and_values_arr = DynamicArray()

        # Loop over the range of the hash map's capacity
        for i in range(self._capacity):
            # If the given index is not empty
            if self._buckets[i] is not None:
                # If the entry at the given index is not a tombstone
                if not self._buckets[i].is_tombstone:
                    # Create a tuple with the entry's key/value pair
                    key_and_value_tuple = \
                        self._buckets[i].key, self._buckets[i].value
                    # Append the key/value tuple to the created dynamic array
                    keys_and_values_arr.append(key_and_value_tuple)

        # Return the keys and values dynamic array
        return keys_and_values_arr

    def __iter__(self):
        """
        Method that allows the hash map to iterate across itself.
        """
        # Initialize an index variable for the hash map to the value of 0
        self._index = 0

        return self

    def __next__(self):
        """
        Method that returns the next value in the hash map depending on the
        iterator's current value.
        """
        try:
            # Initialize a value variable to the entry of the current index
            value = self._buckets[self._index]
            # Loop until the index is not empty or until the entry is not a TS
            while value is None or value.is_tombstone is True:
                # Increment the index value and update the value variable
                self._index = self._index + 1
                value = self._buckets[self._index]

            # Raise StopIteration if DynamicArrayException occurs
        except DynamicArrayException:
            raise StopIteration

        # Increment index variable and return value
        self._index = self._index + 1
        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
