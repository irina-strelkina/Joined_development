import cmd
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


def parse_cowsay_args(arg):
    tokens = shlex.split(arg)
    if "reply" not in tokens:
        raise ValueError('cowsay requires "reply"')

    pos = tokens.index("reply")
    left = tokens[:pos]
    right = tokens[pos + 1:]

    if not left or not right:
        raise ValueError("both messages are required")

    first = parse_shlex_command(shlex.join(left))
    second = parse_shlex_command(shlex.join(right))

    return first, second


def normalize_lines(text):
    return text.splitlines()


class TwoCowsShell(cmd.Cmd):
    prompt = "twocows> "
    intro = "Type help or ? to list commands."

    def do_list_cows(self, arg):
        """List all available cows"""
        args = shlex.split(arg)
        if args:
            print("list_cows takes no arguments")
            return
        print("\n".join(cowsay.list_cows()))

    def do_make_bubble(self, arg):
        """Create a bubble for message"""
        args = shlex.split(arg)
        if not args:
            print("make_bubble requires a message")
            return

        message = args[0]
        params = parse_kv_tokens(args[1:]) if len(args) > 1 else {}

        width = int(params.get("width", 40))
        wrap_text = params.get("wrap_text", "True").lower() not in {"false", "0", "no"}

        print(cowsay.make_bubble(message, width=width, wrap_text=wrap_text))

    def do_EOF(self, arg):
        return True


if __name__ == "__main__":
    TwoCowsShell().cmdloop()