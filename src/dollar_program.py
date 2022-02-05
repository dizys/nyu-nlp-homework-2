import re
import sys
from regex_utils import reg_or, reg_opt, reg_seq, reg_opt_rep


def get_extract_dollar_regex():
    space_exp = r'[\s\t\n]{1,10}'
    eng_digit_exp = reg_or('a', 'half', 'quarter', 'zero', 'one', 'two', 'three',
                           'four', 'five', 'six', 'seven', 'eight', 'nine')
    eng_teen_exp = reg_or('ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
                          'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen')
    eng_tens_exp = reg_or('twenty', 'thirty', 'forty',
                          'fifty', 'sixty', 'seventy', 'eighty', 'ninety')
    eng_hundreds_exp = reg_or('hundred', 'thousand',
                              'million', 'billion', 'trillion', 'gazillion')
    eng_number_component_exp = reg_or(
        eng_digit_exp, eng_teen_exp, eng_tens_exp, eng_hundreds_exp)
    eng_number_exp = reg_seq(reg_opt_rep(
        reg_seq(eng_number_component_exp, space_exp)), eng_number_component_exp)

    digits_integer_exp = reg_or(
        r'\d{0,3}\,\d{3}(?:\,\d{3}){0,}',
        '\d+'
    )

    digits_decimal_exp = r'\.\d{1,}'

    digits_number_exp = reg_seq(
        digits_integer_exp, reg_opt(digits_decimal_exp))

    nationality_abbr_exp = reg_or('XCD', 'AUD', 'BSD', 'BBD', 'BZD', 'BMD', 'BND', 'CAD', 'KYD', 'USD',
                                  'FJD', 'GYD', 'HKD', 'JMD', 'KID', 'LRD', 'NAD', 'NZD', 'SGD', 'SBD', 'SRD', 'TWD', 'TTD', 'TVD',)

    nationality_exp = reg_or(
        'Eastern Caribbean', 'Caribbean',
        'Australian',
        'Bahamian',
        'Barbadian',
        'Belize',
        'Bermudian',
        'Brunei',
        'Canadian',
        'Cayman Islands', 'Cayman',
        'United States', 'American', 'US',
        'Fijian',
        'Guyanese',
        'Hong Kong',
        'Jamaican',
        'Kiribati',
        'Liberian',
        'Namibian',
        'New Zealand',
        'Singapore',
        'Solomon Islands',
        'Spanish',
        'Surinamese',
        'New Taiwan',
        'Trinidad and Tobago',
        'Tuvaluan',
    )

    exp = reg_or(
        reg_seq(
            reg_opt('US', reg_opt(space_exp)),
            r'\$',
            reg_opt(space_exp),
            digits_number_exp,
            reg_opt(reg_opt(space_exp), eng_hundreds_exp),
        ),
        reg_seq(
            reg_or(eng_number_exp, digits_number_exp),
            space_exp,
            reg_or('dollars', 'dollar'),
            space_exp,
            'and',
            reg_or(eng_number_exp, digits_number_exp),
            reg_opt(
                space_exp,
                reg_or('cents', 'cent'),
            ),
        ),
        reg_seq(
            reg_or(eng_number_exp, digits_number_exp),
            space_exp,
            reg_or(
                reg_seq(
                    reg_opt(nationality_exp, reg_opt(space_exp)),
                    reg_or('dollars', 'dollar', 'cents', 'cent')
                ),
                nationality_abbr_exp
            )
        ),
    )
    return exp


def main() -> None:
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print('Usage: python3 dollar_program.py [-regex] <file>')
        sys.exit(1)

    exp = get_extract_dollar_regex()

    if sys.argv[1] == '-regex':
        print(exp)
        sys.exit(0)

    with open(sys.argv[1], 'r') as f:
        text = f.read()
        amount_list = re.findall(exp, text, re.IGNORECASE)
        print('\n'.join(amount_list))


if __name__ == '__main__':
    main()
