import sys


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

    with open(filename) as file:
        file_contents = file.read()


    if file_contents:
        for character in file_contents:
            if character == '(':
                print('LEFT_PAREN ( null')
            if character == ')':
                print('RIGHT_PAREN ) null')
            if character == '{':
                print('LEFT_BRACE { null')
            if character == '}':
                print('RIGHT_BRACE } null')
            if character == '*':
                print('STAR * null')
            if character == '.':
                print('DOT . null')
            if character == ',':
                print('COMMA , null')
            if character == '+':
                print('PLUS + null')
            if character == '-':
                print('MINUS - null')
            if character == ';':
                print('SEMICOLON ; null')

        print("EOF  null")
    else:
        print("EOF  null")



if __name__ == "__main__":
    main()
