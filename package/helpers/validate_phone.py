import re

def validate_phone(number: str):
    number_clean = number.replace(" ", "").replace("-", "")

    pattern_prefixed_international = r"^(?:\+56|0056)"

    if re.match(pattern_prefixed_international, number_clean):
        number_without_prefixed = re.sub(pattern_prefixed_international, "", number_clean)
    else:
        number_without_prefixed = number_clean

    pattern_movil = r"^9\d{8}$"
    pattern_fixed = r"^[2-8]\d{7}$"

    return re.match(pattern_movil, number_without_prefixed) or re.match(pattern_fixed, number_without_prefixed)
