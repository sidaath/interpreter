import sys
import scanner

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    x = scanner.Tokenizer()
    errors: bool = x.tokenize(filename=filename)


    if errors:
        exit(65)
    else:
        exit(0)

    match character:
        case '.':
            return True
        case '=':
            return True
        case '<':
            return True
        case '>':
            return True
        case '/':
            return True
        case '!':
            return True
    return False

if __name__ == "__main__":
    main()
