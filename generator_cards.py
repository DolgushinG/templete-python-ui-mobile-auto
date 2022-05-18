import random


def sum_num(number):
    return number // 10 + number % 10


def luna(card_number):
    even_numbers = card_number[::2]
    odd_numbers = list(card_number[1::2])
    sum_odd_numbers = 0
    for i in odd_numbers:
        sum_odd_numbers += int(i)
    k = 0
    summ = 0
    for i in even_numbers:
        k = int(i) * 2
        summ += sum_num(k)
    return (summ + sum_odd_numbers) % 10


def generate_card_number():
    result = '4'
    for i in range(2, 16):
        random.seed()
        result += str(random.randint(1, 9))
    for i in range(0, 9):
        if (luna((result + str(i)).replace(" ", '')) == 0):
            result += str(i)
            return result


