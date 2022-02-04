import re
import sys
from regex_utils import reg_or, reg_opt, reg_seq

def get_extract_dollar_regex():
    eng_quantities_exp = reg_or('thousand', 'million', 'billion', 'trillion', 'gazillion')

    exp = reg_or(
        r'\$\d+(?:\.\d\d)?',
        reg_seq(r'\$\d+(?:\.\d+)?(?:\s+)?', eng_quantities_exp),
    )
    return exp


def main() -> None:
    if len(sys.argv) != 2:
        print('Usage: python3 dollar_program.py <file>')
        sys.exit(1)
    
    exp = get_extract_dollar_regex()

    with open(sys.argv[1], 'r') as f:
        text = f.read()
        amount_list = re.findall(exp, text)
        print('\n'.join(amount_list))

if __name__ == '__main__':
    main()