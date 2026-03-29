import random
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen


def bullscows(guess: str, secret: str) -> tuple[int, int]:
    bulls = sum(g == s for g, s in zip(guess, secret))
    cows = sum((Counter(guess) & Counter(secret)).values()) - bulls
    return bulls, cows


def ask(prompt: str, valid: list[str] = None) -> str:
    while True:
        word = input(prompt)
        if not valid or word in valid:
            return word


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


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


def load_words(source: str) -> list[str]:
    parsed = urlparse(source)

    if parsed.scheme in ("http", "https"):
        with urlopen(source) as response:
            content = response.read().decode("utf-8")
    else:
        content = Path(source).read_text(encoding="utf-8")

    return [line.strip() for line in content.splitlines() if line.strip()]


def filter_words(words: list[str], length: int) -> list[str]:
    return [word for word in words if len(word) == length]


def main() -> None:
    if len(sys.argv) < 2:
        print("Использование: python -m bullscows <словарь|URL> [длина]")
        raise SystemExit(1)

    source = sys.argv[1]
    length = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    words = load_words(source)
    words = filter_words(words, length)


if __name__ == "__main__":
    main()