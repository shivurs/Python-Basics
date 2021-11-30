numbers = [1, 2, 3]
numbers2 = [1, 2, 3]
print(numbers == numbers2)
print(numbers is numbers2)

numbers.append([4, 5])
print(numbers[-1])
numbers[0] = 0
print(numbers)

letters = 'abc'
letters = letters + 'de'
print(letters[-1])
letters = letters.replace('a', 'A')
print(letters)

# tokens in a sentence      -> use list of strings
# latitude/longitude pair   -> tuple of two floats
# Bible verse (Genesis 1:7) -> tuple of string, int, int

s = 'Hello, World'
print(s[9:7])