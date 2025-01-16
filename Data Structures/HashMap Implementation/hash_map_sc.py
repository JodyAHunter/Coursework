# Name: Jody Hunter
# OSU Email: huntejod@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap (Portfolio Assignment)
# Due Date: 06/09/2023
# Description: HashMap implementation with collision handling by chaining

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        # Resize the hash map by doubling its capacity if table load > 1.0
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity*2)

        # obtain hash value by calling hash function on the given key
        hash = self._hash_function(key)

        # obtain index for given key/value pair
        index = hash % self._capacity

        # If given key does not exist in the linked list at given index
        if self._buckets[index].contains(key) is None:
            # Insert the new key/ value pair and increment the hash map size
            self._buckets[index].insert(key, value)
            self._size += 1

        # Key exists in linked list, remove the node, then insert the new node
        # Size stays the same due to key already existing
        else:
            self._buckets[index].remove(key)
            self._buckets[index].insert(key, value)

    def empty_buckets(self) -> int:
        """
        Method that returns how many of the buckets in the hash map are empty.
        """
        # Initialize a counter to 0
        counter = 0

        # Loop through the range of the hash map's capacity
        for i in range(self._capacity):

            # Check length of linked list; if it is 0, bucket is empty
            if self._buckets[i].length() == 0:

                # Increment counter
                counter += 1

        return counter

    def table_load(self) -> float:
        """
        Method that returns the hash table's load factor
        """
        # divide hash map's size by capacity and return the result
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Method that erases the contents of the hash map; capacity unchanged
        """
        # Initialize a new empty dynamic array
        new_dyn_arr = DynamicArray()

        # Assign the hash map's buckets to the new array
        self._buckets = new_dyn_arr

        # Assign the hash map's size to 0
        self._size = 0

        # Add a linked list to each index in the new empty underlying array
        for i in range(self._capacity):
            self._buckets.append(LinkedList())


    def resize_table(self, new_capacity: int) -> None:
        """
        Method that updates the capacity of the hash map and rehashes all
        existing content in the hash map.
        """
        # If new capacity given is less than 1, nothing happens
        if new_capacity < 1:
            return

        # New capacity must be a prime number
        # Call is_prime method, if not True, set new_capacity to next prime num
        if self._is_prime(new_capacity) is not True:
            new_capacity = self._next_prime(new_capacity)

        # Create a new hash map object with the new capacity
        new_hash_map = HashMap(new_capacity, self._hash_function)

        # Handles case where new capacity is 2, keeps hash map initialization
        # from changing new_capacity from 2 to 3
        if new_capacity == 2:
            new_hash_map._capacity = 2

        # Iterate over the range of the hash map's capacity
        for i in range(self._capacity):

            # If length of linked list at current index is not 0
            if self._buckets[i].length() != 0:

                # Iterate over each node in the linked list
                for node in self._buckets[i]:

                    # Call put method to add current node's key/value pair
                    # to the newly created hash map
                    new_hash_map.put(node.key, node.value)

        # Re-assign the original hash map's capacity, size, and buckets
        # to the new hash map's capacity, size, and buckets
        self._capacity = new_hash_map._capacity
        self._size = new_hash_map._size
        self._buckets = new_hash_map._buckets



    def get(self, key: str):
        """
        Method that takes a given key and returns its value, or None
        if the key does not exist in the hash map.
        """
        # obtain hash value by calling hash function on the given key
        hash = self._hash_function(key)

        # obtain index for given key
        index = hash % self._capacity

        # If given key does not exist in the linked list at given index
        if self._buckets[index].contains(key) is None:
            # Return None
            return None

        # Key exists in linked list, return the value of the given key
        else:
            return self._buckets[index].contains(key).value

    def contains_key(self, key: str) -> bool:
        """
        Method that takes a given key and returns True if the key exists in
        the hash map, or False if it does not exist.
        """
        # obtain hash value by calling hash function on the given key
        hash = self._hash_function(key)

        # obtain index for given key
        index = hash % self._capacity

        # If given key exists in the linked list at given index
        if self._buckets[index].contains(key) is not None:
            # Return True
            return True

        # Otherwise, return False
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Method that takes a given key and removes the key/pair value.
        """
        # obtain hash value by calling hash function on the given key
        hash = self._hash_function(key)

        # obtain index for given key
        index = hash % self._capacity

        # If given key exists in the linked list at given index
        if self._buckets[index].contains(key) is not None:
            # Remove node with given key from linked list
            self._buckets[index].remove(key)
            # Decrement hash map size by 1
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method that creates and returns a dynamic array where each index is a
        tuple containing a key/value pair from the hash map.
        """
        # Initialize a dynamic array that will store the key/value pairs
        keys_and_values_arr = DynamicArray()

        # Loop over the range of the hash map's capacity
        for i in range(self._capacity):
            # If length of linked list at current node is not 0
            if self._buckets[i].length() != 0:
                # Iterate over each node in the linked list
                for node in self._buckets[i]:
                    # Initialize a tuple variable with the key and value
                    key_and_value_tuple = node.key, node.value
                    # append the tuple to the dynamic array created
                    keys_and_values_arr.append(key_and_value_tuple)

        # Return the key/value pair array
        return keys_and_values_arr


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Function that takes a dynamic array and returns a tuple with the first
    value being a dynamic array containing the highest occurring value/values
    and the second value being an integer representing how many times the
    highest occurring values occurred.
    """
    # Initialize a hash map object
    map = HashMap()

    # Initialize a dynamic array
    mode_dyn_array = DynamicArray()

    # Initialize a counter variable
    counter = 0

    # Iterate over the range of the length of the given dynamic array
    for i in range(da.length()):

        # If-else block that checks if the key at the current index exists in
        # the hash map object. If the key does not exist, it will be placed in
        # the map with the put method with the key and a value of 1. If the key
        # already exists in the map, it will be updated by incrementing its
        # value by 1
        if map.contains_key(da[i]):
            map.put(da[i], map.get(da[i]) + 1)
        else:
            map.put(da[i], 1)

    # Call the get_keys_and_values method to create an array of key/value pairs
    keys_and_values_arr = map.get_keys_and_values()

    # Iterate over the range of the length of the keys and values array
    for i in range(keys_and_values_arr.length()):
        # If the value of the current index is greater than the counter
        if keys_and_values_arr[i][1] >= counter:
            # Update counter with that value
            counter = keys_and_values_arr[i][1]

    # Iterate over the range of the length of the keys and values array
    for i in range(keys_and_values_arr.length()):
        # If the value of the current index is equal to counter
        if keys_and_values_arr[i][1] == counter:
            # Append the key of that index to the mode dynamic array
            mode_dyn_array.append(keys_and_values_arr[i][0])

    # Return a tuple with the mode dynamic array and the counter number
    return mode_dyn_array, counter


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

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
