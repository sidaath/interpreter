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
    

    if file_contents:
        #validity of current '=' token while tokenizing
        eq_operator_valid : bool    = True

        #validity of current '/' token while tokenizing
        slash_operator_valid : bool = True

        #track line number in loop
        line : int = 1

        iterator = enumerate(file_contents)
        for index,character in iterator:
            if character == '\n':
                line += 1
            elif character == '\t' or character == ' ':
                continue
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
                if eq_operator_valid:
                    if index+1 < len(file_contents) and file_contents[index+1] == '=':
                        print('EQUAL_EQUAL == null')
                        eq_operator_valid = False
                    else:
                        print('EQUAL = null')
                else:
                    eq_operator_valid = True
            elif character == '!':
                if index+1 < len(file_contents) and file_contents[index+1] == '=':
                    print('BANG_EQUAL != null')
                    eq_operator_valid = False
                else:
                    print('BANG ! null')
            elif character == '<':
                if index+1 < len(file_contents) and file_contents[index+1] == '=':
                    print('LESS_EQUAL <= null')
                    eq_operator_valid = False
                else:
                    print('LESS < null')
            elif character == '>':
                if index+1 < len(file_contents) and file_contents[index+1] == '=':
                    print('GREATER_EQUAL >= null')
                    eq_operator_valid = False
                else:
                    print('GREATER > null')
            elif character == '/':
                if slash_operator_valid:
                    if index+1 < len(file_contents) and file_contents[index+1] =='/':
                        slash_operator_valid = False
                    else:
                        print('SLASH / null')
                else:
                    #second '/', rest of line is a comment, stop reading line (skip line when scanning multi lines)
                    while character != '\n':
                        item: tuple[int, str] = next(iterator)
                        character = item[1]
                    line += 1
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
