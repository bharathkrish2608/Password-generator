import secrets
import string
from pathlib import Path
from typing import List, Tuple

SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?/\\|"  # noqa: W605 backslash for pool


def _build_pool(use_upper: bool, use_lower: bool, use_digits: bool, use_symbols: bool) -> str:
    pool = ""
    if use_lower:
        pool += string.ascii_lowercase
    if use_upper:
        pool += string.ascii_uppercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += SYMBOLS
    return pool


def generate_password(
    length: int,
    use_symbols: bool = True,
    use_upper: bool = True,
    use_lower: bool = True,
    use_digits: bool = True,
) -> str:
    if length < 4:
        raise ValueError("Password length must be at least 4 characters.")

    if not any([use_upper, use_lower, use_digits, use_symbols]):
        raise ValueError("Enable at least one character set.")

    categories = []
    if use_upper:
        categories.append(string.ascii_uppercase)
    if use_lower:
        categories.append(string.ascii_lowercase)
    if use_digits:
        categories.append(string.digits)
    if use_symbols:
        categories.append(SYMBOLS)

    def _pick(pool: str) -> str:
        return pool[secrets.randbelow(len(pool))]

    def _shuffle(chars: List[str]) -> List[str]:
        # Fisher-Yates using secrets for unpredictability
        for i in range(len(chars) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            chars[i], chars[j] = chars[j], chars[i]
        return chars

    # Guarantee one from each selected category
    password_chars = [_pick(category) for category in categories]

    pool = _build_pool(use_upper, use_lower, use_digits, use_symbols)
    remaining = length - len(password_chars)
    password_chars.extend(_pick(pool) for _ in range(remaining))
    _shuffle(password_chars)
    return "".join(password_chars)


def assess_strength(
    password: str,
    symbols_allowed: bool,
    upper_allowed: bool = True,
    lower_allowed: bool = True,
    digits_allowed: bool = True,
) -> Tuple[str, List[str]]:
    tips: List[str] = []
    length = len(password)

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in SYMBOLS for c in password)

    length_score = 2 if length >= 12 else 1 if length >= 10 else 0
    variety_score = sum([has_upper, has_lower, has_digit, has_symbol])
    symbol_bonus = 1 if symbols_allowed and has_symbol else 0

    score = length_score + variety_score + symbol_bonus

    if score >= 6:
        label = "Strong"
    elif score >= 4:
        label = "Medium"
    else:
        label = "Weak"

    if label == "Weak":
        if length < 12:
            tips.append("Increase the length to at least 12 characters.")
        if upper_allowed and not has_upper:
            tips.append("Add uppercase letters.")
        if lower_allowed and not has_lower:
            tips.append("Add lowercase letters.")
        if digits_allowed and not has_digit:
            tips.append("Include numbers.")
        if symbols_allowed and not has_symbol:
            tips.append("Include symbols for better entropy.")

    return label, tips


def prompt_yes_no(message: str, default: bool = True) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        choice = input(f"{message} {suffix} ").strip().lower()
        if not choice:
            return default
        if choice in {"y", "yes"}:
            return True
        if choice in {"n", "no"}:
            return False
        print("Please enter y or n.")


def prompt_int(message: str, minimum: int) -> int:
    while True:
        raw = input(message).strip()
        if not raw.isdigit():
            print("Enter a positive integer.")
            continue
        value = int(raw)
        if value < minimum:
            print(f"Value must be at least {minimum}.")
            continue
        return value


def maybe_save(passwords: List[str]) -> None:
    if not prompt_yes_no("Save generated passwords to passwords.txt?", default=False):
        return
    path = Path("passwords.txt")
    with path.open("a", encoding="utf-8") as fh:
        for pwd in passwords:
            fh.write(pwd + "\n")
    print(f"Saved {len(passwords)} password(s) to {path}.")


def main() -> None:
    print("\n=== Password Generator ===")
    while True:
        length = prompt_int("Desired length (min 4): ", 4)
        use_symbols = prompt_yes_no("Include symbols?", default=True)
        count = prompt_int("How many passwords to generate? ", 1)

        generated: List[str] = []
        for _ in range(count):
            pwd = generate_password(length, use_symbols)
            strength, tips = assess_strength(pwd, use_symbols)
            generated.append(pwd)
            print(f"\nPassword: {pwd}")
            print(f"Strength: {strength}")
            if tips:
                print("Tips:")
                for tip in tips:
                    print(f" - {tip}")

        maybe_save(generated)

        if not prompt_yes_no("Generate again?", default=False):
            break
    print("Goodbye!")


if __name__ == "__main__":
    main()
