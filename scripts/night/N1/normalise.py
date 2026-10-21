"""Address normaliser for the DoneStat pipeline (N1).

One function, `norm(addr)`, used for every address join: 311 PROBADDRESS,
MSD PROP_ADD, LRA Address, forestry-maintenance PROPERTYADDRESS, Cityworks
WoAddress. It follows the T-COMMON rule (uppercase; part before the first
comma; strip "ST LOUIS..." suffixes; remove punctuation; AVENUE/AVE->AV,
STREET->ST, BOULEVARD->BLVD, DRIVE->DR, PLACE->PL, ROAD->RD, COURT->CT,
TERRACE->TER, LANE->LN, PARKWAY->PKWY; collapse spaces) with two deliberate
changes, both tested below:

1. The city suffix is stripped only at the END of the string, so the street
   called St. Louis Avenue survives ("1234 ST LOUIS AV ST LOUIS MO 63115" ->
   "1234 ST LOUIS AV"; T-COMMON's regex turned it into "1234").
2. "&" is kept as a token so intersections stay distinguishable from
   addresses.

`block(addr_norm)` returns the public, block-level form: the house number is
rounded down to the hundred ("1234 LEMP AV" -> "1200 block of LEMP AV").
Intersections of two house numbers ("1234 & 1238 EXAMPLE AV") are rounded the
same way, and any further run of house numbers is dropped from the label,
including the short form of a range ("1234-36 EXAMPLE AV": the "36" would give
the exact house number back, so it is dropped; N10 privacy scan, 14 Oct).
All test addresses below are made up (real or EXAMPLE street names, invented numbers); N10 checked on 14 Oct that
none is a real address in MSD's address file or the 311 file.
Run `python3 -I normalise.py` to execute the tests.
"""
import re

ABBR = {'AVENUE': 'AV', 'AVE': 'AV', 'STREET': 'ST', 'BOULEVARD': 'BLVD', 'DRIVE': 'DR',
        'PLACE': 'PL', 'ROAD': 'RD', 'COURT': 'CT', 'TERRACE': 'TER', 'LANE': 'LN',
        'PARKWAY': 'PKWY'}
_PUNCT = re.compile(r"[^A-Z0-9& ]")
_UNIT = re.compile(r"\s(APT|UNIT|STE|SUITE|#)\s.*$")


def norm(a):
    if a is None:
        return ''
    a = str(a).upper().replace('#', ' # ').strip()
    a = a.split(',')[0]
    a = _UNIT.sub('', ' ' + a + ' ').strip()
    a = _PUNCT.sub(' ', a)
    t = a.split()
    # trailing ZIP, state, city -- only at the end, and never eat the street itself
    if len(t) > 2 and re.fullmatch(r'6\d{4}(\d{4})?', t[-1]):
        t = t[:-1]
    if len(t) > 2 and t[-1] == 'MO':
        t = t[:-1]
    for city in (['ST', 'LOUIS'], ['SAINT', 'LOUIS'], ['STLOUIS']):
        k = len(city)
        if len(t) > k + 1 and t[-k:] == city:
            rest = t[:-k]
            # keep "1234 ST LOUIS" (the avenue written without its type)
            if len(rest) >= 2:
                t = rest
            break
    t = [ABBR.get(x, x) for x in t]
    # "1234 ST LOUIS" is St. Louis Avenue written without its type
    if len(t) == 3 and t[0].isdigit() and t[1:] == ['ST', 'LOUIS']:
        t.append('AV')
    return ' '.join(t)


def parts(n):
    """(house_number:int|None, street:str) from a normalised address."""
    t = n.split()
    if not t or '&' in t:
        return None, n
    if t[0].isdigit():
        return int(t[0]), ' '.join(t[1:])
    m = re.fullmatch(r'(\d+)[A-Z]?', t[0])
    if m:
        return int(m.group(1)), ' '.join(t[1:])
    return None, n


def _is_house_number(t):
    # three or more digits: house numbers; leaves 'I 64', 'HWY 40' and ordinals ('16TH') alone
    return t.isdigit() and len(t) >= 3


def _drop_leading_numbers(street):
    # a street name never starts with a bare number ('16TH' has letters); a leading bare number is the rest of a
    # house-number range, which would put the exact house number back into a block label
    t = street.split()
    while t and t[0].isdigit():
        t = t[1:]
    return ' '.join(t)


def block(n):
    """Public block-level label for a normalised address. Never returns a house number."""
    if not n:
        return ''
    toks = n.split()
    if '&' in toks:
        if not any(_is_house_number(t) for t in toks):
            return n  # a street intersection is already coarser than a parcel
        # "1234 & 1238 LEMP AV": round the first number, keep the street
        nums = [int(t) for t in toks if _is_house_number(t)]
        street = _drop_leading_numbers(' '.join(t for t in toks if t != '&' and not _is_house_number(t)))
        return f"{(nums[0] // 100) * 100} block of {street}" if street else ''
    num, street = parts(n)
    # drop any further house numbers ("1234 1238 LEMP AV" from "1234-1238 LEMP AV")
    street = ' '.join(t for t in street.split() if not _is_house_number(t))
    if num is not None:
        street = _drop_leading_numbers(street)  # "1234 36 EXAMPLE AV" from "1234-36 EXAMPLE AV"
    if num is None:
        return street
    return f"{(num // 100) * 100} block of {street}" if street else ''


def _tests():
    cases = {
        '1234 LEMP AV ST LOUIS MO 63118': '1234 LEMP AV',
        '1234 Lemp Avenue': '1234 LEMP AV',
        '1234 ROBERT AVE, 63111': '1234 ROBERT AV',
        '1234 ST LOUIS AV ST LOUIS MO 63115': '1234 ST LOUIS AV',
        '1234 ST LOUIS AVENUE': '1234 ST LOUIS AV',
        '1234 ST LOUIS': '1234 ST LOUIS AV',
        '1234 MC REE AV ST LOUIS 63110': '1234 MC REE AV',
        '1234 DELOR ST 63116': '1234 DELOR ST',
        '1234 LAFAYETTE AV ST LOUIS': '1234 LAFAYETTE AV',
        '1234   GRATTAN ST ': '1234 GRATTAN ST',
        'N 9TH ST & CASS AVE': 'N 9TH ST & CASS AV',
        '1234 N EXAMPLE ST ST LOUIS MO 63147': '1234 N EXAMPLE ST',
        '1234 MAGNOLIA AVE.': '1234 MAGNOLIA AV',
        '1234 N 99TH ST APT 2': '1234 N 99TH ST',
        '': '',
        None: '',
    }
    for raw, want in cases.items():
        got = norm(raw)
        assert got == want, (raw, got, want)
    blocks = {
        '1234 LEMP AV': '1200 block of LEMP AV',
        '42 EXAMPLE BLVD': '0 block of EXAMPLE BLVD',
        'N 9TH ST & CASS AV': 'N 9TH ST & CASS AV',
        'I 64 & GRAND BLVD': 'I 64 & GRAND BLVD',
        'LEMP AV': 'LEMP AV',
        '1234 & 1238 LEMP AV': '1200 block of LEMP AV',
        '1234 1238 LEMP AV': '1200 block of LEMP AV',
        norm('1234-1238 Lemp Ave'): '1200 block of LEMP AV',
        '1234 N 99TH ST': '1200 block of N 99TH ST',
        norm('1234-36 Lemp Ave'): '1200 block of LEMP AV',
        '1234 36 N 99TH ST': '1200 block of N 99TH ST',
        '1234 & 36 LEMP AV': '1200 block of LEMP AV',
    }
    for a, want in blocks.items():
        assert block(a) == want, (a, block(a), want)
    assert parts('1234 R FOREST AV') == (1234, 'R FOREST AV')
    n_tests = len(cases) + len(blocks) + 1
    print(f'normalise.py: {n_tests} tests passed')


if __name__ == '__main__':
    _tests()
