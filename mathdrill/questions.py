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

    g = math.gcd(a, b)
    if random.random() < 0.5:
        return {
            "category": "GCD / LCM",
            "question_type": "gcd",
            "question": f"What is gcd({a}, {b})?",
            "answer": g,
        }
    else:
        return {
            "category": "GCD / LCM",
            "question_type": "lcm",
            "question": f"What is lcm({a}, {b})?",
            "answer": (a * b) // g,
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


# ── bayes ───────────────────────────────────────────────────────────

def _bayes_counts(pop, prevalence_den, accuracy):
    # true positives and false positives out of a population of pop
    have = pop // prevalence_den
    healthy = pop - have
    true_pos = have * accuracy // 100
    false_pos = healthy * (100 - accuracy) // 100
    return true_pos, false_pos


def bayes(difficulty=1):
    if difficulty == 1:
        prevalence_den, accuracy, pop = 100, 90, 10_000
    elif difficulty == 2:
        prevalence_den, accuracy, pop = 1_000, 95, 100_000
    else:
        prevalence_den, accuracy, pop = 10_000, 99, 1_000_000

    condition = random.choice(["a rare disease", "a genetic marker", "a manufacturing defect"])
    setup = f"1 in {prevalence_den:,} have {condition}. A test is {accuracy}% accurate in both directions."
    true_pos, false_pos = _bayes_counts(pop, prevalence_den, accuracy)
    total_pos = true_pos + false_pos

    if random.random() < 0.5:
        return {
            "category": "Bayes",
            "question_type": "bayes_count",
            "question": f"{setup} Of {pop:,} tested, how many test positive in total?",
            "answer": total_pos,
        }

    return {
        "category": "Bayes",
        "question_type": "bayes_percent",
        "question": f"{setup} You test positive. What is P(you have it)? Answer as a percentage to 1 decimal place.",
        "answer": round(100 * true_pos / total_pos, 1),
        "float_answer": True,
        "tolerance": 0.15,
    }


# ── conditioning ────────────────────────────────────────────────────

def conditioning(difficulty=1):
    # "at least one" and "this specific one" give different answers, that's the whole point
    if difficulty == 1:
        if random.random() < 0.5:
            return {
                "category": "Conditioning",
                "question_type": "cond_at_least_two",
                "question": "A family has 2 children. At least one is a girl. What is P(both are girls)? (fraction)",
                "answer": "1/3",
                "string_answer": True,
            }
        return {
            "category": "Conditioning",
            "question_type": "cond_specific_two",
            "question": "A family has 2 children. The elder is a girl. What is P(both are girls)? (fraction)",
            "answer": "1/2",
            "string_answer": True,
        }

    if difficulty == 2:
        sides = random.choice([4, 6, 8])
        k = _rand(1, sides)
        if random.random() < 0.5:
            return {
                "category": "Conditioning",
                "question_type": "cond_at_least_dice",
                "question": f"Two fair {sides}-sided dice. At least one shows a {k}. What is P(both show {k})? (fraction)",
                "answer": f"1/{2 * sides - 1}",
                "string_answer": True,
            }
        return {
            "category": "Conditioning",
            "question_type": "cond_specific_dice",
            "question": f"Two fair {sides}-sided dice. The first shows a {k}. What is P(both show {k})? (fraction)",
            "answer": f"1/{sides}",
            "string_answer": True,
        }

    if random.random() < 0.5:
        n = _rand(3, 4)
        # (1/2^n) / (1 - 1/2^n) simplifies to 1/(2^n - 1)
        return {
            "category": "Conditioning",
            "question_type": "cond_at_least_n",
            "question": f"A family has {n} children. At least one is a girl. What is P(all {n} are girls)? (fraction)",
            "answer": f"1/{2 ** n - 1}",
            "string_answer": True,
        }

    doors = _rand(3, 8)
    return {
        "category": "Conditioning",
        "question_type": "cond_monty",
        "question": f"{doors} doors, one prize. You pick one. The host knows where the prize is and opens {doors - 2} empty doors. You switch. What is P(you win)? (fraction)",
        "answer": f"{doors - 1}/{doors}",
        "string_answer": True,
    }


# ── expected value ──────────────────────────────────────────────────

def _optimal_stopping_ev(sides, rolls):
    # work backwards from the last roll, keep a face only if it beats what a reroll is worth
    ev = (sides + 1) / 2
    for _ in range(rolls - 1):
        keep = [v for v in range(1, sides + 1) if v > ev]
        ev = (sum(keep) + (sides - len(keep)) * ev) / sides
    return ev


def expected_value(difficulty=1):
    if difficulty == 1:
        win = _rand(2, 10) * 10
        lose = _rand(1, 5) * 10
        favourable = _rand(1, 5)
        total = favourable + _rand(1, 5)
        ev = (favourable * win - (total - favourable) * lose) / total
        return {
            "category": "Expected Value",
            "question_type": "ev_game",
            "question": f"A game pays {win} with probability {favourable}/{total} and costs you {lose} otherwise. Expected value to 2 decimal places?",
            "answer": round(ev, 2),
            "float_answer": True,
            "tolerance": 0.02,
        }

    sides = 6 if difficulty == 2 else random.choice([4, 6, 8, 10])
    rolls = 2 if difficulty == 2 else _rand(2, 4)
    return {
        "category": "Expected Value",
        "question_type": "ev_reroll",
        "question": f"Roll a fair {sides}-sided die, take the value or reroll. At most {rolls} rolls, you must take the last. Playing optimally, expected value to 2 decimal places?",
        "answer": round(_optimal_stopping_ev(sides, rolls), 2),
        "float_answer": True,
        "tolerance": 0.02,
    }


# ── percentages and ratios ──────────────────────────────────────────

def percentages(difficulty=1):
    if difficulty == 1:
        variants = ["pct_of", "pct_change"]
    elif difficulty == 2:
        variants = ["pct_change", "pct_reverse", "ratio_split"]
    else:
        variants = ["pct_reverse", "pct_compound", "ratio_split"]
    variant = random.choice(variants)

    if variant == "pct_of":
        pct = random.choice([5, 10, 15, 20, 25, 40, 60, 75])
        n = _rand(2, 40) * 20
        return {
            "category": "Percentages",
            "question_type": "pct_of",
            "question": f"What is {pct}% of {n:,}?",
            "answer": round(n * pct / 100, 2),
            "float_answer": True,
            "tolerance": 0.01,
        }

    if variant == "pct_change":
        before = _rand(2, 50) * 20
        after = _rand(2, 50) * 20
        while after == before:
            after = _rand(2, 50) * 20
        return {
            "category": "Percentages",
            "question_type": "pct_change",
            "question": f"Revenue moved from {before:,} to {after:,}. Percentage change to 1 decimal place, negative for a fall?",
            "answer": round(100 * (after - before) / before, 1),
            "float_answer": True,
            "tolerance": 0.1,
        }

    if variant == "pct_reverse":
        pct = random.choice([8, 10, 12, 15, 20, 25])
        before = _rand(5, 60) * 20
        direction = random.choice(["rise", "fall"])
        after = before * (1 + pct / 100) if direction == "rise" else before * (1 - pct / 100)
        return {
            "category": "Percentages",
            "question_type": "pct_reverse",
            "question": f"After a {pct}% {direction} a figure stands at {after:,.2f}. What was it before? 2 decimal places.",
            "answer": round(before, 2),
            "float_answer": True,
            "tolerance": 0.05,
        }

    if variant == "pct_compound":
        up = random.choice([10, 20, 25, 30, 50])
        down = random.choice([10, 20, 25, 30, 50])
        net = 100 * ((1 + up / 100) * (1 - down / 100) - 1)
        return {
            "category": "Percentages",
            "question_type": "pct_compound",
            "question": f"A value rises {up}% then falls {down}%. Net percentage change to 1 decimal place, negative for a fall?",
            "answer": round(net, 1),
            "float_answer": True,
            "tolerance": 0.1,
        }

    a, b = _rand(1, 9), _rand(1, 9)
    total = (a + b) * _rand(3, 40)
    return {
        "category": "Percentages",
        "question_type": "ratio_split",
        "question": f"Split {total:,} in the ratio {a}:{b}. What is the larger share?",
        "answer": total * max(a, b) // (a + b),
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
    "bayes": bayes,
    "conditioning": conditioning,
    "expected": expected_value,
    "percentages": percentages,
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
    "Bayes": "bayes",
    "Conditioning": "conditioning",
    "Expected Value": "expected",
    "Percentages": "percentages",
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
    "bayes_count": "bayes", "bayes_percent": "bayes",
    "cond_at_least_two": "conditioning", "cond_specific_two": "conditioning",
    "cond_at_least_dice": "conditioning", "cond_specific_dice": "conditioning",
    "cond_at_least_n": "conditioning", "cond_monty": "conditioning",
    "ev_game": "expected", "ev_reroll": "expected",
    "pct_of": "percentages", "pct_change": "percentages", "pct_reverse": "percentages",
    "pct_compound": "percentages", "ratio_split": "percentages",
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
