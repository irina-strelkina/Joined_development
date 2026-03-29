import random
from collections import Counter


def bullscows(guess: str, secret: str) -> tuple[int, int]:
    bulls = sum(g == s for g, s in zip(guess, secret))
    cows = sum((Counter(guess) & Counter(secret)).values()) - bulls
    return bulls, cows


def ask(prompt: str, valid: list[str] = None) -> str:
    while True:
        word = input(prompt)
        if valid is None or word in valid:
            return word


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = random.choice(words)
    attempts = 0

    while True:
        guess = ask("Введите слово: ", words)
        attempts += 1

        bulls, cows = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", bulls, cows)

        if guess == secret:
            return attempts