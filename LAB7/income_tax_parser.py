import re

_DIGITS = re.compile(r"[0-9]+")


def clean_pan(pan):
    """
    Removes all whitespace from a PAN and upper-cases it.
    Returns None if pan is not a string.
    """
    if not isinstance(pan, str):
        return None
    return "".join(pan.split()).upper()


def parse_amount(text):
    """
    Converts an amount such as 'Rs 12,50,000' into an int.
    Returns None if the input is not a string or is not a valid amount.
    """
    if not isinstance(text, str):
        return None
    cleaned = re.sub(r"(?i)rs\.?|₹", "", text)
    cleaned = cleaned.replace(",", "")
    cleaned = "".join(cleaned.split())
    if not _DIGITS.fullmatch(cleaned):
        return None
    try:
        return int(cleaned)
    except ValueError:  # e.g. absurdly long digit strings
        return None


def parse_tax_slab(line):
    """
    Parses 'LOW-HIGH:RATE' into a (low, high, rate) tuple.
    Returns None if the line is not a string or is not in that format.
    """
    if not isinstance(line, str):
        return None
    parts = line.split(":")
    if len(parts) != 2:
        return None
    limits = parts[0].split("-")
    if len(limits) != 2:
        return None

    values = []
    for p in (limits[0], limits[1], parts[1]):
        p = p.strip()
        if not _DIGITS.fullmatch(p):
            return None
        try:
            values.append(int(p))
        except ValueError:
            return None

    low, high, rate = values
    if low > high or rate > 100:
        return None
    return low, high, rate


def main():
    print("==== Running clean_pan ====")
    value = input("Enter a PAN (e.g. abcde 1234f): ")
    print("Cleaned PAN:", clean_pan(value))

    print("\n==== Running parse_amount ====")
    value = input("Enter an amount (e.g. Rs 12,50,000): ")
    result = parse_amount(value)
    print("Amount in rupees:", result if result is not None else "Invalid amount")

    print("\n==== Running parse_tax_slab ====")
    value = input("Enter a tax slab as LOW-HIGH:RATE (e.g. 250000-500000:5): ")
    result = parse_tax_slab(value)
    print("Tax slab (low, high, rate):", result if result is not None else "Invalid slab")


if __name__ == "__main__":
    main()