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

    errors : bool = False
    eq_op_count : int = 0


    if file_contents:
        line : int = 1
        for index,character in enumerate(file_contents):
            if character == '\n':
                line += 1
            elif character == '(':
                print('LEFT_PAREN ( null')
            elif character == ')':
                print('RIGHT_PAREN ) null')
            elif character == '{':
                print('LEFT_BRACE { null')
            elif character == '}':
                print('RIGHT_BRACE } null')
            elif character == '*':
                print('STAR * null')
            elif character == '.':
                print('DOT . null')
            elif character == ',':
                print('COMMA , null')
            elif character == '+':
                print('PLUS + null')
            elif character == '-':
                print('MINUS - null')
            elif character == ';':
                print('SEMICOLON ; null')
            elif character == '=':
                if eq_op_count == 1:
                    print('EQUAL_EQUAL == null')
                    eq_op_count = 0
                    continue
                if index + 1 < len(file_contents) and file_contents[index + 1] == '=':
                    eq_op_count = 1
                else:
                    print('EQUAL = null')
            else:
                errors = True
                print(f"[line {line}] Error: Unexpected character: {character}", file=sys.stderr)
        print("EOF  null")
    else:
        print("EOF  null")

    if errors:
        exit(65)
    else:
        exit(0)



if __name__ == "__main__":
    main()
