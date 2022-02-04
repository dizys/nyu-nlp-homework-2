import re
import sys

def extract_dollar_amounts(text):
    result = re.findall(r'\$\d+(?:\.\d\d)?', text)
    return result


def main() -> None:
    if len(sys.argv) != 2:
        print('Usage: python3 dollar_program.py <file>')
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        text = f.read()
        amountList = extract_dollar_amounts(text)
        print('\n'.join(amountList))


if __name__ == '__main__':
    main()