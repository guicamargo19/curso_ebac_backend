def func():
    print('Function part 1')

    x = yield
    print(x)
    print('Function part 2')

    a = yield
    print(a)
    print('Function part 3')


try:

    y = func()

    next(y)	  # Part 1 executed, to reach the first yield we used next

    y.send(6)  # Part 2 executed and value sent 6

    y.send(12)  # Part 2 executed, value sent 12 and StopIteration raised

except StopIteration:
    pass
