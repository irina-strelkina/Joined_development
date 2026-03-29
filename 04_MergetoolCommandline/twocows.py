import argparse
import shlex
import cowsay


def parse_kv_tokens(tokens):
    params = {}
    for token in tokens:
        if "=" not in token:
            raise ValueError(f"Expected parameter=value, got: {token}")
        key, value = token.split("=", 1)
        params[key] = value
    return params


def parse_shlex_command(line):
    tokens = shlex.split(line)
    if not tokens:
        return None

    message = tokens[0]
    cow = "default"

    if len(tokens) >= 2 and "=" not in tokens[1]:
        cow = tokens[1]
        extra_tokens = tokens[2:]
    else:
        extra_tokens = tokens[1:]

    extra = parse_kv_tokens(extra_tokens) if extra_tokens else {}

    return {
        "message": message,
        "cow": cow,
        "extra": extra,
    }


parser = argparse.ArgumentParser()

parser.add_argument("message1", nargs="?")
parser.add_argument("message2", nargs="?")

parser.add_argument("-f", dest="cow", default="default")
parser.add_argument("-e", dest="eyes", default="oo")
parser.add_argument("-T", dest="tongue", default="  ")
parser.add_argument("-W", dest="width", type=int, default=40)
parser.add_argument("-n", dest="no_wrap", action="store_true")
parser.add_argument("-l", dest="list_cows", action="store_true")

parser.add_argument("-F", dest="cow2", default="default")
parser.add_argument("-E", dest="eyes2", default="oo")
parser.add_argument("-N", dest="no_wrap2", action="store_true")

args = parser.parse_args()

if args.list_cows:
    print("\n".join(cowsay.list_cows()))
else:
    first = cowsay.cowsay(
        message=args.message1,
        cow=args.cow,
        eyes=args.eyes,
        tongue=args.tongue,
        width=args.width,
        wrap_text=not args.no_wrap,
    ).splitlines()

    second = cowsay.cowsay(
        message=args.message2,
        cow=args.cow2,
        eyes=args.eyes2,
        width=args.width,
        wrap_text=not args.no_wrap2,
    ).splitlines()

    first_width = max(len(line) for line in first)
    second_width = max(len(line) for line in second)
    height = max(len(first), len(second))

    first = [" " * first_width] * (height - len(first)) + [line.ljust(first_width) for line in first]
    second = [" " * second_width] * (height - len(second)) + [line.ljust(second_width) for line in second]

    for left, right in zip(first, second):
        print(left + "  " + right)