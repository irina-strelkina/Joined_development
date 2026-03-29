from collections import Counter


def bullscows(guess: str, secret: str) -> tuple[int, int]:
    bulls = sum(g == s for g, s in zip(guess, secret))
    cows = sum((Counter(guess) & Counter(secret)).values()) - bulls
    return bulls, cows