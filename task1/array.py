# Дан массив чисел, состоящий из некоторого количества подряд идущих единиц, за которыми следует какое-то количество
# подряд идущих нулей: 111111111111111111111111100000000.
# Найти индекс первого нуля (то есть найти такое место, где заканчиваются единицы, и начинаются нули)

from time import time

array = "11111111111111111111111110000000011111111111111"
# array = ('11111111111111111111111111111' * 1111111) + '0000000000111111111111111111111111111111111'


# декоратор подсета времени выполнения функции
def time_of_function(function):
    def wrapped(*args):
        start_time = time()
        res = function(*args)
        end_time = time()
        print(end_time - start_time)
        return res
    return wrapped


# example_1  сложность O(n)
@time_of_function
def task_1(array):
    for i, element in enumerate(array):
        if element == '0':
            return i


print(f'example_1 : {task_1(array)}')


# example_2 сложность O(n)
@time_of_function
def task_2(array):
    try:
        return ([i for i, element in enumerate(array) if element == '0'])[0]
    except IndexError:
        return None


print(f'example_2 : {task_2(array)}')


# example_3 сложность O(1)
@time_of_function
def task_3(array):
    try:
        return array.index('0')
    except ValueError:
        return None


print(f'example_3 : {task_3(array)}')