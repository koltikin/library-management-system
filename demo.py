import functools

my_list = [2, 4, 5, 6, 7, 8]

initoal_num = int(input("enter a number? "))

result = functools.reduce(lambda x, y: x + y, my_list, initoal_num)
print(result)
