import re
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 dollar_program.py <file>')
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        text = f.read()
        print(text)
