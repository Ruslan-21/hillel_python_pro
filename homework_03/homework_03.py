
# 1. STRINGS

def len_str(text):
    return len(text)

def join_str(a, b):
    return a + b


print(len_str("Hello"))
print(join_str("Hello", " World"))
print("")


# 2. NUMBERS

def square(x):
    return x ** 2

def sum_numbers(a, b):
    return a + b

def div_int(a, b):
    return a // b, a % b


print(square(5))
print(sum_numbers(2, 3))
print(div_int(10, 3))
print("")


# 3. LISTS

def avg(nums):
    return sum(nums) / len(nums)

def common(a, b):
    return list(set(a) & set(b))


print(avg([1, 2, 3, 4, 5]))
print(common([1, 2, 3], [2, 3, 4]))
print("")


# 4. DICT

def dicts(d):
    for k in d:
        print(k)

def merge(d1, d2):
    r = d1.copy()
    r.update(d2)
    return r


dicts({'name': 'Alex', 'age': 25})
print(merge({'a': 1}, {'b': 2}))
print("")


# 5. SETS

def union(a, b):
    return a | b

def sub(a, b):
    return a.issubset(b)


print(union({1, 2}, {2, 3}))
print(sub({1, 2}, {1, 2, 3}))
print("")




def even(n):
    if n % 2 == 0:
        return "Парне"
    else:
        return "Непарне"

def evens(nums):
    r = []
    for n in nums:
        if n % 2 == 0:
            r.append(n)
    return r



print(even(7))
print(evens([1, 2, 3, 4, 5, 6]))
print("")


# 7. LAMBDA

lamb = lambda x: "парне" if x % 2 == 0 else "не парне"


print(lamb(10))
print(lamb(7))