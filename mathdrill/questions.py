import random
import math


def _rand(lo, hi):
    return random.randint(lo, hi)


# ── modular arithmetic ──────────────────────────────────────────────

def mod_arithmetic(difficulty=1):
    if difficulty == 1:
        a, b, m = _rand(2, 20), _rand(2, 20), _rand(2, 10)
        op = random.choice(["+", "*"])
    elif difficulty == 2:
        a, b, m = _rand(10, 100), _rand(10, 100), _rand(7, 50)
        op = random.choice(["+", "*", "-"])
    else:
        a, b, m = _rand(50, 500), _rand(50, 500), _rand(10, 100)
        op = random.choice(["+", "*", "-", "**"])

    if op == "+":
        answer = (a + b) % m
    elif op == "-":
        answer = (a - b) % m
    elif op == "*":
        answer = (a * b) % m
    else:
        exp = _rand(2, 5)
        answer = pow(a, exp, m)
        return {
            "category": "Modular Arithmetic",
            "question": f"What is pow({a}, {exp}, {m})?",
            "answer": answer,
        }

    return {
        "category": "Modular Arithmetic",
        "question": f"What is ({a} {op} {b}) % {m}?",
        "answer": answer,
    }


# ── gcd / lcm ───────────────────────────────────────────────────────

def gcd_lcm(difficulty=1):
    if difficulty == 1:
        a, b = _rand(4, 50), _rand(4, 50)
    elif difficulty == 2:
        a, b = _rand(20, 200), _rand(20, 200)
    else:
        a, b = _rand(100, 1000), _rand(100, 1000)

    if random.random() < 0.5:
        return {
            "category": "GCD / LCM",
            "question": f"What is gcd({a}, {b})?",
            "answer": math.gcd(a, b),
        }
    else:
        lcm = (a * b) // math.gcd(a, b)
        return {
            "category": "GCD / LCM",
            "question": f"What is lcm({a}, {b})?",
            "answer": lcm,
        }


# ── binary / bitwise ────────────────────────────────────────────────

def bitwise(difficulty=1):
    if difficulty == 1:
        a, b = _rand(1, 15), _rand(1, 15)
    elif difficulty == 2:
        a, b = _rand(8, 63), _rand(8, 63)
    else:
        a, b = _rand(32, 255), _rand(32, 255)

    variant = random.choice(["and", "or", "xor", "bin_count"])

    if variant == "and":
        return {
            "category": "Bitwise",
            "question": f"What is {a} & {b}?",
            "answer": a & b,
        }
    elif variant == "or":
        return {
            "category": "Bitwise",
            "question": f"What is {a} | {b}?",
            "answer": a | b,
        }
    elif variant == "xor":
        return {
            "category": "Bitwise",
            "question": f"What is {a} XOR {b}?",
            "answer": a ^ b,
        }
    else:
        n = _rand(1, 255)
        return {
            "category": "Bitwise",
            "question": f"How many 1-bits in the binary representation of {n}?",
            "answer": bin(n).count("1"),
        }


# ── base conversion ─────────────────────────────────────────────────

def base_conversion(difficulty=1):
    if difficulty == 1:
        n = _rand(1, 31)
    elif difficulty == 2:
        n = _rand(16, 127)
    else:
        n = _rand(64, 511)

    variant = random.choice(["to_bin", "from_bin", "to_hex"])

    if variant == "to_bin":
        return {
            "category": "Base Conversion",
            "question": f"Convert {n} to binary (no 0b prefix).",
            "answer": bin(n)[2:],
            "string_answer": True,
        }
    elif variant == "from_bin":
        b = bin(n)[2:]
        return {
            "category": "Base Conversion",
            "question": f"Convert binary {b} to decimal.",
            "answer": n,
        }
    else:
        return {
            "category": "Base Conversion",
            "question": f"Convert {n} to hexadecimal (lowercase, no 0x prefix).",
            "answer": hex(n)[2:],
            "string_answer": True,
        }


# ── primes ───────────────────────────────────────────────────────────

def _is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def _prime_factors(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def primes(difficulty=1):
    if difficulty == 1:
        n = _rand(2, 50)
    elif difficulty == 2:
        n = _rand(20, 200)
    else:
        n = _rand(50, 500)

    variant = random.choice(["is_prime", "smallest_factor", "num_factors"])

    if variant == "is_prime":
        return {
            "category": "Primes",
            "question": f"Is {n} prime? (yes/no)",
            "answer": "yes" if _is_prime(n) else "no",
            "string_answer": True,
        }
    elif variant == "smallest_factor":
        if _is_prime(n) or n < 4:
            n = _rand(4, 100)
            while _is_prime(n):
                n = _rand(4, 100)
        return {
            "category": "Primes",
            "question": f"What is the smallest prime factor of {n}?",
            "answer": _prime_factors(n)[0],
        }
    else:
        if n < 4:
            n = _rand(4, 80)
        pf = _prime_factors(n)
        return {
            "category": "Primes",
            "question": f"How many prime factors does {n} have (with multiplicity)?",
            "answer": len(pf),
        }


# ── combinatorics ────────────────────────────────────────────────────

def combinatorics(difficulty=1):
    if difficulty == 1:
        n = _rand(3, 8)
        r = _rand(1, n)
    elif difficulty == 2:
        n = _rand(5, 12)
        r = _rand(2, min(n, 6))
    else:
        n = _rand(8, 15)
        r = _rand(2, min(n, 7))

    if random.random() < 0.5:
        answer = math.comb(n, r)
        return {
            "category": "Combinatorics",
            "question": f"What is C({n}, {r})?",
            "answer": answer,
        }
    else:
        answer = math.perm(n, r)
        return {
            "category": "Combinatorics",
            "question": f"What is P({n}, {r})?",
            "answer": answer,
        }


# ── registry ─────────────────────────────────────────────────────────

CATEGORIES = {
    "modular": mod_arithmetic,
    "gcd": gcd_lcm,
    "bitwise": bitwise,
    "base": base_conversion,
    "primes": primes,
    "combinatorics": combinatorics,
}


CATEGORY_DISPLAY_TO_KEY = {
    "Modular Arithmetic": "modular",
    "GCD / LCM": "gcd",
    "Bitwise": "bitwise",
    "Base Conversion": "base",
    "Primes": "primes",
    "Combinatorics": "combinatorics",
}


def random_question(difficulty=1, category=None):
    if category and category in CATEGORIES:
        gen = CATEGORIES[category]
    else:
        gen = random.choice(list(CATEGORIES.values()))
    return gen(difficulty)


def weakspot_question(difficulty=1, weak_categories=None):
    if not weak_categories:
        return random_question(difficulty)

    # map display names back to keys
    weak_keys = []
    for cat in weak_categories:
        key = CATEGORY_DISPLAY_TO_KEY.get(cat, cat)
        if key in CATEGORIES:
            weak_keys.append(key)

    if not weak_keys:
        return random_question(difficulty)

    # 70% chance to pick from a weak category, 30% random
    if random.random() < 0.7:
        key = random.choice(weak_keys)
        return CATEGORIES[key](difficulty)
    return random_question(difficulty)
