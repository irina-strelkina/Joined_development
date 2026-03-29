import argparse
import cowsay

parser = argparse.ArgumentParser()

parser.add_argument("message")
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
    print(
        cowsay.cowsay(
            message=args.message,
            cow=args.cow,
            eyes=args.eyes,
            tongue=args.tongue,
            width=args.width,
            wrap_text=not args.no_wrap,
        )
    )