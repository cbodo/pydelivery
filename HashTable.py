class HashTable:
    # Initializes a HashTable class object with optional parameter size that
    # defaults to 10.
    #
    # Time Complexity: O(n)
    # Space Complexity: O(n^2)
    def __init__(self, size=10):
        # Initializes an empty list (O(1)).
        self.table = []
        # Adds "size"-number of empty lists to table to store key/value pairs (O(n)).
        for i in range(size):
            self.table.append([])

    # Gets the hash for the current item.
    #
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def _get_hash(self, key):
        # Returns hashed key % number of elements in the table as the key (O(1)).
        return hash(key) % len(self.table)

    # Inserts new item into table.
    #
    # Time Complexity: O(n)
    # Space Complexity: O(1)
    def insert(self, key, item):
        # Gets list associated with passed key (O(1)).
        list = self.table[self._get_hash(key)]
        # Checks if key already exists in list, and adds item if so (O(n)).
        for i in list:
            if(i[0] == key):
                i[1] = item
                return True
        # Creates a new key/value pair in list if key is not found (O(1)).
        key_value = [key, item]
        list.append(key_value)
        return True

    # Lookup Function.
    # Gets value associated with key in hash table.
    #
    # Time Complexity: O(n)
    # Space Complexity: O(1)
    def search(self, key):
        # Gets list associated with passed key (O(1)).
        list = self.table[self._get_hash(key)]
        # Checks list for key and returns associated value (O(n)).
        for i in list:
            if(i[0] == key):
                return i[1]
        # Returns None if key is not found in list (O(1)).
        return None

    # Removes an item from hash table with specified key.
    #
    # Time Complexity: O(n)
    # Space Complexity: O(1)
    def remove(self, key):
        # Gets list associated with key (O(1)).
        list = self.table[self._get_hash(key)]

        # Removes key/value pair if found in list (O(n)).
        for i in list:
            if(i[0] == key):
                list.remove([i[0], i[1]])
