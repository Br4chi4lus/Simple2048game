import game

size = -1
stack_size = -1
while 4 > size or size > 8:
    try:
        size = int(input("Enter board size (4-8)\n"))
        if 4 > size or size > 8:
            print("Invalid size, enter a value between 4 and 8")
    except ValueError:
        print("Invalid input, enter a valid integer")

while 2 > stack_size or stack_size > 5:
    try:
        stack_size = int(input("Enter number of remembered moves(2-5)\n"))
        if 2 > stack_size or stack_size > 5:
            print("Invalid size, enter a value between 2 and 5")
    except ValueError:
        print("Invalid input, enter a valid integer")

game = game.Game(size, stack_size)
game.game()



