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
            "question_type": "mod_pow",
            "question": f"What is pow({a}, {exp}, {m})?",
            "answer": answer,
        }

    op_tag = {"+": "add", "-": "sub", "*": "mul"}[op]
    return {
        "category": "Modular Arithmetic",
        "question_type": f"mod_{op_tag}",
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
            "question_type": "gcd",
            "question": f"What is gcd({a}, {b})?",
            "answer": math.gcd(a, b),
        }
    else:
        lcm = (a * b) // math.gcd(a, b)
        return {
            "category": "GCD / LCM",
            "question_type": "lcm",
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
            "question_type": "bit_and",
            "question": f"What is {a} & {b}?",
            "answer": a & b,
        }
    elif variant == "or":
        return {
            "category": "Bitwise",
            "question_type": "bit_or",
            "question": f"What is {a} | {b}?",
            "answer": a | b,
        }
    elif variant == "xor":
        return {
            "category": "Bitwise",
            "question_type": "bit_xor",
            "question": f"What is {a} XOR {b}?",
            "answer": a ^ b,
        }
    else:
        n = _rand(1, 255)
        return {
            "category": "Bitwise",
            "question_type": "bit_popcount",
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
            "question_type": "base_to_bin",
            "question": f"Convert {n} to binary (no 0b prefix).",
            "answer": bin(n)[2:],
            "string_answer": True,
        }
    elif variant == "from_bin":
        b = bin(n)[2:]
        return {
            "category": "Base Conversion",
            "question_type": "base_from_bin",
            "question": f"Convert binary {b} to decimal.",
            "answer": n,
        }
    else:
        return {
            "category": "Base Conversion",
            "question_type": "base_to_hex",
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
            "question_type": "is_prime",
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
            "question_type": "smallest_factor",
            "question": f"What is the smallest prime factor of {n}?",
            "answer": _prime_factors(n)[0],
        }
    else:
        if n < 4:
            n = _rand(4, 80)
        pf = _prime_factors(n)
        return {
            "category": "Primes",
            "question_type": "num_factors",
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
            "question_type": "combination",
            "question": f"What is C({n}, {r})?",
            "answer": answer,
        }
    else:
        answer = math.perm(n, r)
        return {
            "category": "Combinatorics",
            "question_type": "permutation",
            "question": f"What is P({n}, {r})?",
            "answer": answer,
        }


# ── logarithms ──────────────────────────────────────────────────────

def logarithms(difficulty=1):
    if difficulty == 1:
        # powers of 2 and 10 — clean answers
        variant = random.choice(["log2_exact", "log10_exact"])
        if variant == "log2_exact":
            exp = _rand(1, 8)
            n = 2 ** exp
            return {
                "category": "Logarithms",
                "question_type": "log2_exact",
                "question": f"What is log2({n})?",
                "answer": exp,
            }
        else:
            exp = _rand(1, 5)
            n = 10 ** exp
            return {
                "category": "Logarithms",
                "question_type": "log10_exact",
                "question": f"What is log10({n})?",
                "answer": exp,
            }
    elif difficulty == 2:
        variant = random.choice(["floor_log2", "floor_log10", "log_product"])
        if variant == "floor_log2":
            n = _rand(3, 500)
            return {
                "category": "Logarithms",
                "question_type": "floor_log2",
                "question": f"What is floor(log2({n}))?",
                "answer": int(math.log2(n)),
            }
        elif variant == "floor_log10":
            n = _rand(2, 50000)
            return {
                "category": "Logarithms",
                "question_type": "floor_log10",
                "question": f"What is floor(log10({n}))? (i.e. how many digits minus 1)",
                "answer": int(math.log10(n)),
            }
        else:
            # log(a*b) = log(a) + log(b)
            a_exp = _rand(1, 5)
            b_exp = _rand(1, 5)
            a = 2 ** a_exp
            b = 2 ** b_exp
            return {
                "category": "Logarithms",
                "question_type": "log_product",
                "question": f"What is log2({a} * {b})?",
                "answer": a_exp + b_exp,
            }
    else:
        variant = random.choice(["floor_log2_hard", "log_power", "num_digits"])
        if variant == "floor_log2_hard":
            n = _rand(100, 10000)
            return {
                "category": "Logarithms",
                "question_type": "floor_log2",
                "question": f"What is floor(log2({n}))?",
                "answer": int(math.log2(n)),
            }
        elif variant == "log_power":
            # log_b(b^k) = k
            base = random.choice([2, 3, 5, 10])
            exp = _rand(2, 6)
            n = base ** exp
            return {
                "category": "Logarithms",
                "question_type": "log_power",
                "question": f"What is log base {base} of {n}?",
                "answer": exp,
            }
        else:
            # how many digits does n have?
            n = _rand(1, 9) * (10 ** _rand(2, 8))
            digits = len(str(n))
            return {
                "category": "Logarithms",
                "question_type": "num_digits",
                "question": f"How many digits does {n} have?",
                "answer": digits,
            }


# ── probability ─────────────────────────────────────────────────────

def _simplify_fraction(num, den):
    g = math.gcd(num, den)
    return num // g, den // g


def probability(difficulty=1):
    if difficulty == 1:
        variant = random.choice(["coin", "dice", "simple_draw"])
        if variant == "coin":
            n = _rand(2, 4)
            # probability of all heads in n flips = 1/2^n
            den = 2 ** n
            return {
                "category": "Probability",
                "question_type": "prob_coin",
                "question": f"What is the probability of getting all heads in {n} fair coin flips? (answer as a fraction like 1/{den})",
                "answer": f"1/{den}",
                "string_answer": True,
            }
        elif variant == "dice":
            target = _rand(1, 6)
            return {
                "category": "Probability",
                "question_type": "prob_dice",
                "question": f"What is the probability of rolling a {target} on a fair 6-sided die? (answer as a fraction)",
                "answer": "1/6",
                "string_answer": True,
            }
        else:
            # drawing from a bag
            red = _rand(1, 5)
            blue = _rand(1, 5)
            total = red + blue
            num, den = _simplify_fraction(red, total)
            return {
                "category": "Probability",
                "question_type": "prob_draw",
                "question": f"A bag has {red} red and {blue} blue balls. What is the probability of drawing red? (fraction)",
                "answer": f"{num}/{den}",
                "string_answer": True,
            }
    elif difficulty == 2:
        variant = random.choice(["dice_sum", "at_least_one", "expected_dice"])
        if variant == "dice_sum":
            target = _rand(2, 7)
            # count ways to get target with 2 dice
            ways = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == target)
            num, den = _simplify_fraction(ways, 36)
            return {
                "category": "Probability",
                "question_type": "prob_dice_sum",
                "question": f"Rolling 2 fair dice, what is the probability the sum is {target}? (fraction)",
                "answer": f"{num}/{den}",
                "string_answer": True,
            }
        elif variant == "at_least_one":
            # P(at least one head in n flips) = 1 - 1/2^n
            n = _rand(2, 5)
            den = 2 ** n
            num_ans = den - 1
            num_s, den_s = _simplify_fraction(num_ans, den)
            return {
                "category": "Probability",
                "question_type": "prob_at_least",
                "question": f"What is P(at least one head in {n} fair coin flips)? (fraction)",
                "answer": f"{num_s}/{den_s}",
                "string_answer": True,
            }
        else:
            # expected value of a die roll
            sides = random.choice([4, 6, 8])
            # E[X] = (sides+1)/2
            num, den = _simplify_fraction(sides + 1, 2)
            ans = f"{num}/{den}" if den > 1 else str(num)
            return {
                "category": "Probability",
                "question_type": "prob_expected",
                "question": f"What is the expected value of rolling a fair {sides}-sided die (1 to {sides})? (fraction or integer)",
                "answer": ans,
                "string_answer": True,
            }
    else:
        variant = random.choice(["conditional", "combo_prob", "repeated"])
        if variant == "conditional":
            # two draws without replacement
            red = _rand(3, 8)
            blue = _rand(3, 8)
            total = red + blue
            # P(2nd red | 1st red) = (red-1)/(total-1)
            num, den = _simplify_fraction(red - 1, total - 1)
            return {
                "category": "Probability",
                "question_type": "prob_conditional",
                "question": (
                    f"A bag has {red} red and {blue} blue balls. You draw one red ball "
                    f"(without replacement). What is P(2nd draw is also red)? (fraction)"
                ),
                "answer": f"{num}/{den}",
                "string_answer": True,
            }
        elif variant == "combo_prob":
            # choosing a committee: P(all from one group)
            n = _rand(3, 6)
            k = _rand(2, min(n, 3))
            total_pool = n + _rand(3, 6)
            ways_good = math.comb(n, k)
            ways_total = math.comb(total_pool, k)
            num, den = _simplify_fraction(ways_good, ways_total)
            return {
                "category": "Probability",
                "question_type": "prob_combo",
                "question": (
                    f"From a group of {total_pool} people ({n} women, {total_pool - n} men), "
                    f"choosing {k} at random. P(all women)? (fraction)"
                ),
                "answer": f"{num}/{den}",
                "string_answer": True,
            }
        else:
            # P(specific outcome in n independent trials)
            n = _rand(3, 5)
            # P(all sixes in n dice rolls) = 1/6^n
            den = 6 ** n
            return {
                "category": "Probability",
                "question_type": "prob_repeated",
                "question": f"What is P(rolling a 6 on all {n} rolls of a fair die)? (fraction)",
                "answer": f"1/{den}",
                "string_answer": True,
            }


# ── registry ─────────────────────────────────────────────────────────

CATEGORIES = {
    "modular": mod_arithmetic,
    "gcd": gcd_lcm,
    "bitwise": bitwise,
    "base": base_conversion,
    "primes": primes,
    "combinatorics": combinatorics,
    "logarithms": logarithms,
    "probability": probability,
}


CATEGORY_DISPLAY_TO_KEY = {
    "Modular Arithmetic": "modular",
    "GCD / LCM": "gcd",
    "Bitwise": "bitwise",
    "Base Conversion": "base",
    "Primes": "primes",
    "Combinatorics": "combinatorics",
    "Logarithms": "logarithms",
    "Probability": "probability",
}


def random_question(difficulty=1, category=None):
    if category and category in CATEGORIES:
        gen = CATEGORIES[category]
    else:
        gen = random.choice(list(CATEGORIES.values()))
    return gen(difficulty)


QUESTION_TYPE_TO_GENERATOR = {
    "mod_add": "modular", "mod_sub": "modular", "mod_mul": "modular", "mod_pow": "modular",
    "gcd": "gcd", "lcm": "gcd",
    "bit_and": "bitwise", "bit_or": "bitwise", "bit_xor": "bitwise", "bit_popcount": "bitwise",
    "base_to_bin": "base", "base_from_bin": "base", "base_to_hex": "base",
    "is_prime": "primes", "smallest_factor": "primes", "num_factors": "primes",
    "combination": "combinatorics", "permutation": "combinatorics",
    "log2_exact": "logarithms", "log10_exact": "logarithms", "floor_log2": "logarithms",
    "floor_log10": "logarithms", "log_product": "logarithms", "log_power": "logarithms",
    "num_digits": "logarithms",
    "prob_coin": "probability", "prob_dice": "probability", "prob_draw": "probability",
    "prob_dice_sum": "probability", "prob_at_least": "probability", "prob_expected": "probability",
    "prob_conditional": "probability", "prob_combo": "probability", "prob_repeated": "probability",
}


def question_by_type(question_type, difficulty=1):
    """Generate a question of the specific type. Retries until the right variant comes up."""
    cat_key = QUESTION_TYPE_TO_GENERATOR.get(question_type)
    if not cat_key or cat_key not in CATEGORIES:
        return random_question(difficulty)
    gen = CATEGORIES[cat_key]
    for _ in range(50):
        q = gen(difficulty)
        if q.get("question_type") == question_type:
            return q
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
