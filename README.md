# mathdrill

my university course so far hasnt taught me the maths i would like to get proficient in so i made this. its a terminal quiz that drills you on the stuff that most courses tend to overlook. modular arithmetic, gcd/lcm, bitwise ops, base conversions, primes, combinatorics. you can choose difficulty and itll throw questions at you, it will track your score and speed. it also keeps a daily streak so you have a reason to comeback.

## setup

clone the repo and install it:

```
git clone https://github.com/emanntahirr/my-course-doesnt-teach-me-maths-nooooo.git
cd my-course-doesnt-teach-me-maths-nooooo
pip install .
```

## usage

run it:

```
mathdrill
```

or:

```
python -m mathdrill
```

by default you get 5 questions at difficulty 1 across all categories.

## flags

`-n NUM` set the number of questions (default is 5)

`-d {1,2,3}` set the difficulty level, 1 is easy, 3 is hard

`-c CATEGORY` focus on one category instead of all of them

`--adaptive` auto-scales difficulty based on how you're doing. get 3 right in a row and it bumps up, get 3 wrong in a row and it drops down

`--weakspot` focuses on the categories you're worst at based on your history. 70% of questions come from your weak spots, 30% random

`--stats` view your practice history, streak, and accuracy

## categories

`modular` `gcd` `bitwise` `base` `primes` `combinatorics`

## examples

10 questions at difficulty 2:

```
mathdrill -n 10 -d 2
```

only bitwise questions:

```
mathdrill -c bitwise
```

hard primes drill, 20 questions:

```
mathdrill -c primes -d 3 -n 20
```

adaptive mode:

```
mathdrill --adaptive
```

drill your weak spots:

```
mathdrill --weakspot
```

check your stats:

```
mathdrill --stats
```

## what to expect

it shows you a question, you type your answer, it tells you if you got it right or wrong and how long you took. at the end you get a summary with your score, average time, and a breakdown by category. it also tracks your daily streak so if you practice every day it counts up, miss a day and it resets.
