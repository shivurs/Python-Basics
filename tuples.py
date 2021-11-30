tup = (1, 2, 3)
print(type(tup))
tup == [1, 2, 3]
print(tup[1])
print(tup + tup)

# tup[0] = 0    tuples do not support item assignment

tup = ()
print(len(tup))

tup = (1,)
print((1,) == 1)    #commas make the tuple a tuple
print((1,) == (1))
print(1 == (1))

# tokens in a sentence      -> use list of strings
# latitude/longitude pair   -> tuple of two floats
# Bible verse (Genesis 1:7) -> tuple of string, int, int