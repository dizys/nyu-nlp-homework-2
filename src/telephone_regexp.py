import re
import sys
from regex_utils import reg_neg_lookahead, reg_neg_lookbehind, reg_or, reg_opt, reg_seq, reg_opt_rep


def get_telephone_regex():
    space_exp = r'[\s\t\n]{1,10}'
    delimiter_exp = r'\-'

    country_code_exp = r'\+[0-9]{1,3}'
    country_code_part = reg_seq(
        country_code_exp, reg_or(space_exp, delimiter_exp))

    area_code_exp = r'[0-9]{3}'
    area_code_part = reg_seq(
        reg_or(area_code_exp, reg_seq(r'\(', area_code_exp, r'\)')),
        reg_opt(reg_or(space_exp, delimiter_exp))
    )

    exchange_code_exp = r'[0-9]{3}'

    line_number_exp = r'[0-9]{4}'

    exp = reg_seq(
        reg_neg_lookbehind(r'[\d\-\$]'),
        reg_opt(
            reg_opt(country_code_part),
            area_code_part,
        ),
        exchange_code_exp,
        reg_opt(reg_or(space_exp, delimiter_exp)),
        line_number_exp,
    )

    return exp


def main() -> None:
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print('Usage: python3 telephone_regexp.py [-regex] <file>')
        sys.exit(1)

    exp = get_telephone_regex()

    if sys.argv[1] == '-regex':
        print(exp)
        sys.exit(0)

    with open(sys.argv[1], 'r') as f:
        text = f.read()
        amount_list = re.findall(exp, text, re.IGNORECASE)
        print('\n'.join(amount_list))


if __name__ == '__main__':
    main()
