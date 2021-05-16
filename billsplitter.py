from random import choice
# write your code here
print('Enter the number of friends joining (including you):')
a = int(input())
if a <= 0:
    print('No one is joining for the party')
else:
    print('Enter the name of every friend (including you)'
          'each on a new line:')
    friends = [input() for _ in range(a)]
    print('Enter the total bill value:')
    m = int(input())
    print('Do you want to use the "Who is lucky?" feature? Write Yes/No:')
    n = input()
    if n == 'Yes':
        lucky = choice(friends)
        print(f'{lucky} is the lucky one!')
        friend = dict.fromkeys(friends, round(m / (a-1), 2))
        friend[lucky] = 0
    else:
        print('No one is going to be lucky')
        friend = dict.fromkeys(friends, round(m/a, 2))
    print(friend)
