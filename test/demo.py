import random

print(random.randint(1, 100))


def digit(number: int, plus=True):
    if plus:
        return random.randint(number, 100)

    else:
        return random.randint(1, number)


print(digit(50, True))

for i in range(1, 100):
    first = random.randint(1, 100)

    if random.choice([True, False]):
        second = digit(first, True)

        operator = '+'
        res = second

        second = second- first
    else:
        second = digit(first, False)
        operator = '-'
        res = first - second

    # print('%s %s %s = res' % first, operator, second)
    print('{0} {1} {2} = {3}'.format(first, operator, second, res))
