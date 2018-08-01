import sys
from termcolor import colored, cprint # pip3 install termcolor

text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])
cprint(text)
cprint('Hello, World!', 'green', 'on_red')

print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')
print_red_on_cyan('Hello, World!')
print_red_on_cyan('Hello, Universe!')

for i in range(10):
    cprint(i, 'magenta', end=' ')

cprint("Attention!", 'red', attrs=['bold'], file=sys.stderr)

print()
nustem_text = colored("NU", 'red')
nustem_text += colored("STEM", 'white')
cprint(nustem_text)
