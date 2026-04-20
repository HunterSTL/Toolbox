ROMAN_NUMERAL_VALUE_SYMBOL_PAIRS = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I")
]

ROMAN_NUMERAL_VALUES = {
    "M": 1000,
    "D": 500,
    "C": 100,
    "L": 50,
    "X": 10,
    "V": 5,
    "I": 1
}

def convert_integer_to_roman_numeral(integer: int) -> str:
    if not 0 < integer < 4000:
        return "invalid input"

    roman_numeral = ""

    for value, symbol in ROMAN_NUMERAL_VALUE_SYMBOL_PAIRS:
        while integer >= value:
            roman_numeral += symbol
            integer -= value

    return roman_numeral

def is_valid_roman_character(character: str) -> bool:
    return character in ROMAN_NUMERAL_VALUES.keys()

def convert_roman_numeral_to_integer(roman_numeral: str) -> int | None:
    numeral_values_sum = 0
    length = len(roman_numeral)

    for index, character in enumerate(roman_numeral):
        if not is_valid_roman_character(character):
            return None

        value = ROMAN_NUMERAL_VALUES.get(character)
        if index + 1 < length and ROMAN_NUMERAL_VALUES.get(roman_numeral[index + 1]) > value:
            numeral_values_sum -= value
        else:
            numeral_values_sum += value

    return numeral_values_sum

def main():
    for _i in range(4001):
        _roman_numeral = convert_integer_to_roman_numeral(_i)
        _integer = convert_roman_numeral_to_integer(_roman_numeral)
        print(f"{_i} → {_roman_numeral} → {_integer}")

if __name__ == "__main__":
    main()