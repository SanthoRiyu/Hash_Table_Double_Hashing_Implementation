class HashTable(object):
    """Hashtable class - The class takes care of creation of hashtable and hash function
    Supported Operations : Insert, Selection, remove, Cleanup, get_keys
    Hash function - Implemented with basic operations and Double hashing collision handling
    The Hash table doubles in size when the threshold load factor reaches 0.5
    input format - 2010CSE1000 / 3.4
    """
    hash_resize_flag = False

    def __init__(self, size):
        """ Constructor to initialize the variables size, Hash table - value_array, Total_entries, threshold"""
        self.size = int(size)
        self.value_array = []
        self.total_entries = 0
        if self.size > 0:
            self.value_array = [None] * self.size
        else:
            raise Exception("Please initialize hash table with size > 0")
        self.threshold = 0.5

    #     def hash1(self,key):
    #         hash_sum = 0
    #         for idx, c in enumerate(key):
    #             hash_sum += (idx + len(key)) ** ord(c)
    #             hash_sum = hash_sum % self.size
    #         return hash_sum
    def hash1(self, key):
        """ Hash function to sum up the unicode character values of the input key
        using inbuilt function ord() and modulus with size of hashtable """
        hash_sum = sum([ord(c) for c in key])
        hash_sum = hash_sum % self.size
        return hash_sum

    @staticmethod
    def hash2(key):
        """ Second Hash function to subtract and modulo with a  prime number """
        hash_val = 5 - (key % 5)
        return hash_val

    def __str__(self):
        """Function to display the hash table syntax - print(object of class HashTable)"""
        output_lines = []
        for item in self.value_array:
            if item is not None:
                output_lines.append("Key: " + str(item[0]) + " Value: " + str(item[1]))
        return "\n".join(output_lines)

    def resize_hashtable(self):
        """ Resize function to increase the size of the hash table based on the load factor of 0.5 """
        # print('Hash table exceeded load factor - Resize done!!')
        self.hash_resize_flag = True
        new_size = 2 * self.size
        new_value_array = [None] * (self.size * 2)
        temp_size = self.size
        self.size = new_size
        for i in range(temp_size):
            if (self.value_array[i] is not None) and (self.value_array[i] != -1):
                self.add_Entries(self.value_array[i][0], self.value_array[i][1], new_value_array, new_size, True)
        self.value_array = new_value_array

    def __setitem__(self, key, value):
        """ __setitem__ is a inbuilt dunder variable that replaces add operation.
        Here the keys - student id and the value - cgpa passed to this function is added to the Hash table
        using the Double hashing method"""
        self.add_Entries(key, value, self.value_array, self.size)

    def add_Entries(self, key, value, value_array, size, resize_flag=False):
        """ Function implementation of the double hashing collision handling for insert operation
        and resize the hashtable if the threshold exceeds the load factor 0.5"""
        hash_v1 = self.hash1(key)
        if value_array[hash_v1] is None or value_array[hash_v1] == -1:
            value_array[hash_v1] = key, value
            self.total_entries += 1
            return
        else:
            if isinstance(value_array[hash_v1], tuple):
                if value_array[hash_v1][0] == key:
                    value_array[hash_v1] = key, value
                    return
            # find the next slot with double hashing
            added = False
            attempt_count = 1
            while not added:
                new_hash = (hash_v1 + attempt_count * self.hash2(hash_v1)) % size
                # print(value_array[new_hash])
                if value_array[new_hash] is not None and isinstance(value_array[new_hash], tuple):
                    if value_array[new_hash][0] == key:
                        value_array[new_hash] = key, value
                        return
                if value_array[new_hash] is None or value_array[new_hash] == -1:
                    value_array[new_hash] = key, value
                    self.total_entries += 1
                    added = True
                else:
                    attempt_count += 1
        if not resize_flag:
            if self.total_entries / size > self.threshold:
                self.resize_hashtable()

    def remove(self, key):
        """ Function implementation of the double hashing collision handling for delete operation"""
        hash_val = self.hash1(key)
        got_value = self.value_array[hash_val]
        if got_value is None or got_value == -1:
            print('Student ID not found')
            return None
        retrieved_key, retrieved_value = got_value
        if retrieved_key == key:
            self.value_array[hash_val] = -1
            self.total_entries -= 1
            print('Student ID removed')
            return
        else:
            # find the next slot with double hashing
            removed = False
            attempt_count = 1
            while not removed:
                new_hash = (hash_val + attempt_count * self.hash2(hash_val)) % self.size
                value_at_hash = self.value_array[new_hash]
                # print('value_at_hash :', value_at_hash)
                if value_at_hash is not None and value_at_hash != -1:
                    retrieved_key, retrieved_value = value_at_hash
                    if retrieved_key == key:
                        # Marking the removed item position by -1
                        self.value_array[new_hash] = -1
                        self.total_entries -= 1
                        removed = True
                        print('Student ID removed')
                    attempt_count += 1
                else:
                    attempt_count += 1

    def getKeys(self):
        """ Function to retrieve all the keys present inside the Hash table"""
        keys = []
        n = 0
        while n < self.size:
            if self.value_array[n] is not None:
                keys.append(self.value_array[n][0])
            n = n + 1
        return keys

    def __getitem__(self, key):
        """ Function implementation using double hashing for read operation"""
        hash_val1 = self.hash1(key)
        retrieved_value = None
        got_value = self.value_array[hash_val1]
#         print('got_value', got_value)
        if (got_value is not None) and got_value != -1:
            if got_value[0] == key:
                return got_value[1]
            else:
                # find the next slot with double hashing
                found = False
                attempt_count = 1
                while not found:
                    new_hash = (hash_val1 + attempt_count * self.hash2(hash_val1)) % self.size
                    value_at_hash = self.value_array[new_hash]
                    if value_at_hash is not None:
                        if value_at_hash != -1:
                            retrieved_key, retrieved_value = value_at_hash
                            if retrieved_key == key:
                                found = True
                        attempt_count += 1
                    else:
                        retrieved_value = None
                        break
        if retrieved_value is None:
            print('Student id not found')
        else:
            return retrieved_value

    def cleanup(self):
        """ Function implementation for cleanup of the all the entries in hash table.
        For element wise selective cleanup - Use the delete method"""
        del self.value_array[:]
        return 'Hash table cleanup completed!!!'