import itertools
from typing import List

def generate_numbers(_country_code: str = "+92", _perm_code: str = "3", _vendor_codes: List[str] = ["1", "2", "3", "4"], _number_length: int = 8, _cont_number: str = None):
    if _cont_number:
        start_number = _cont_number[len(_country_code + _perm_code):]
        start_vendor_code = start_number[0]
        start_number = start_number[1:]
        start_number = start_number.lstrip(''.join(_vendor_codes))
        start_number = str(int(start_number) + 1).zfill(_number_length)
        start_tuple = tuple(start_number)
    else:
        start_vendor_code = _vendor_codes[0]
        start_tuple = tuple("0" * _number_length)
    
    for vendor_code in _vendor_codes:
        if vendor_code < start_vendor_code:
            continue
        for number in itertools.product("0123456789", repeat=_number_length):
            if vendor_code == start_vendor_code and number < start_tuple:
                continue
            yield f"{_country_code}{_perm_code}{vendor_code}{''.join(number)}"