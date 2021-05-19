# the new design of the program
# available methods are:
# game_header(), whose_turn(), end_criteria(), legal(), end_check1(), end_check2()
# user_play(), comp_play(), moves(), comp_check(), user_check()
# snake_display(), user_pieces(), win_message()

# Write your code here

# imports
from itertools import combinations_with_replacement
from random import randint, shuffle
from itertools import chain

# General preface
d = list(combinations_with_replacement([0, 1, 2, 3, 4, 5, 6], 2))
shuffle(d)

stock = [list(x) for x in d[0:14]]
comp = list(map(list, d[14:21]))
pl = list(map(list, d[21:28]))

num1, status1, winner, issue, val = [None]*5

b = [[6, 6], [5, 5], [4, 4], [3, 3], [2, 2], [1, 1], [0, 0]]
for j in b:
    if j not in (comp+pl):
        continue
    elif j in comp:
        num1 = j
        status1 = 'player'
        comp.remove(j)
        break
    elif j in pl:
        num1 = j
        status1 = 'computer'
        pl.remove(j)
        break

snake = [num1]


def game_header():
    print('=' * 70)
    print('Stock size:', len(stock))
    print('Computer pieces:', len(comp))
    snake_display()
    user_pieces()


def whose_turn():
    global val, issue
    if end_criteria():
        win_message()
    elif status1 == 'computer':
        print('Status: Computer is about to make a move. Press Enter to continue...')
        input()
        comp_play()
    elif status1 == 'player':
        player_turn()


def player_turn():
    global val, issue
    if issue == 'ValueError':
        try:
            val = int(input())
        except ValueError:
            issue = 'ValueError'
            print('Invalid input. Please try again.')
            whose_turn()
    else:
        print("Status: It's your turn to make a move. Enter your command.")
        try:
            val = int(input())
            if val not in range(-len(pl), len(pl) + 1):
                print('Invalid input. Please try again.')
                whose_turn()
        except ValueError:
            issue = 'ValueError'
            print('Invalid input. Please try again.')
            whose_turn()
    issue = None
    user_play(val)


def end_check1():
    cr1, cr2 = [], []
    fl = list(chain.from_iterable(snake))
    if fl[0] == fl[-1]:
        fl1, fl2 = fl[1:], fl[:len(fl)-1]
        for (res1, res2) in list(zip(fl1[0::2], fl1[1::2])):
            cr1.append(res1 == res2)
        for x, y in list(zip(fl2[0::2], fl2[1::2])):
            cr2.append(x == y)
        return any([all(cr1), all(cr2)])
    else:
        return False


def end_check2():
    fl = list(chain.from_iterable(snake))
    for i in set(fl):
        if fl.count(i) >= 8:
            return True
    else:
        return False


def end_criteria():
    global winner, snake
    if len(pl) and len(comp):
        return False
    elif len(snake) > 6 and end_check2() and end_check1():
        winner = 'draw'
        return True
    else:
        if len(pl) == 0:
            winner = 'player'
        elif len(comp) == 0:
            winner = 'computer'
        return True


def user_play(pn):
    global status1
    if pn == 0:
        pv = None
    else:
        pv = pl[(abs(pn) - 1)]          # changed from pop
    legal(pn, pv, pl)
    status1 = 'computer'
    whose_turn()


def comp_play():
    global status1
    cn = randint(-len(comp), +len(comp))
    if cn != 0:
        cv = comp[(abs(cn) - 1)]          # changed from pop
    else:
        cv = None
    legal(cn, cv, comp)                     # change to legal(cn, cv, comp)
    status1 = 'player'
    whose_turn()


def legal(rhl, shl, itemsl):
    global snake, issue
    link1, link2 = snake[0][0], snake[-1][1]
    rhls, shls, itemsls = [rhl, shl, itemsl]
    if shl is None:
        moves(rhls, shls, itemsls)
        game_header()
    elif link1 in shl or link2 in shl:
        if shl[0] == link2:
            rhls = abs(rhl)
        elif shl[0] == link1:
            shls = shl[::-1]
        elif shl[1] == link1:
            rhls = -abs(rhl)
        elif shl[1] == link2:
            shls = shl[::-1]
        itemsl.remove(shl)
        moves(rhls, shls, itemsls)
        game_header()
    else:
        if status1 == 'computer':
            comp_play()
        elif status1 == 'player':
            print('Illegal move. Please try again.')
            issue = 'ValueError'
            player_turn()


def moves(rh, sh, items):
    global snake, winner
    if rh > 0:
        snake.append(sh)
    elif rh < 0:
        snake.insert(0, sh)
    elif sh is None:
        if len(stock) == 0:
            winner = 'draw'
            win_message()
        else:
            items.append(stock.pop())


def snake_display():
    global snake
    if len(snake) > 6:
        print(*snake[:3], sep='', end='...')
        print(*snake[-3:], sep='')
        print()
    else:
        print(*snake, sep='')
        print()


def user_pieces():
    print('Your pieces:')
    for n, it in list(enumerate(pl, start=1)):
        print(f'{n}:{it}')


def win_message():
    if winner == 'computer':
        print("Status: The game is over. The computer won!")
    elif winner == 'player':
        print("Status: The game is over. You won!")
    elif winner == 'draw':
        print("Status: The game is over. It's a draw!")
    exit()


def game():
    game_header()
    whose_turn()


if __name__ == '__main__':
    game()
