def clean_pan(pan):
    """
    Removes spaces from a PAN and upper-cases it.
    Safely handles None, non-string, or empty input.
    """
    if not isinstance(pan, str) or not pan.strip():
        return "Invalid input"
    return pan.strip().replace(' ', '').upper()


def parse_amount(text):
    """
    Converts an amount such as 'Rs 12,50,000' into an int.
    Safely handles non-string or malformed numeric inputs.
    """
    if not isinstance(text, str):
        return "Invalid input"
    cleaned = text.replace('Rs', '').replace(',', '').strip()
    if not cleaned.isdigit():
        return "Invalid input"
    try:
        return int(cleaned)
    except ValueError:
        return "Invalid input"


def parse_tax_slab(line):
    """
    Parses 'LOW-HIGH:RATE' into a (low, high, rate) tuple.
    Safely handles malformed input formats.
    """
    if not isinstance(line, str) or ':' not in line:
        return "Invalid input"
    try:
        limits, rate = line.split(':')
        if '-' not in limits:
            return "Invalid input"
        low, high = limits.split('-')
        return int(low), int(high), int(rate)
    except (ValueError, AttributeError):
        return "Invalid input"


def main():
    print("==== Running clean_pan ====")
    value = input("Enter a PAN (e.g. abcde 1234f): ")
    print("Cleaned PAN:", clean_pan(value))

    print("\n==== Running parse_amount ====")
    value = input("Enter an amount (e.g. Rs 12,50,000): ")
    print("Amount in rupees:", parse_amount(value))

    print("\n==== Running parse_tax_slab ====")
    value = input("Enter a tax slab as LOW-HIGH:RATE (e.g. 250000-500000:5): ")
    print("Tax slab (low, high, rate):", parse_tax_slab(value))


if __name__ == "__main__":
    main()
