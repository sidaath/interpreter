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

        #maintain state of whether inside quotes (true) or outside quotes (false)
        string_open : bool          = False

        #store characters of string
        string_array : list[str]    = []

        #maintain state of whether inside number literal (true) or not (false)
        number_open : bool          = False

        #maintain if decimal places included in number literal - false (no decimal in literal)
        number_decimal : bool       = False

        #store digits of number
        number_array : list[str]    = []

        #maintain state of whether identifier open(true) or not (false)
        identifier_open : bool      = False

        #store characters of identifier
        identifier_array : list[str]= []

        #track line number in loop
        line : int = 1

        iterator = enumerate(file_contents)

        tokenize : bool = True

        while tokenize:
            token : tuple[int, str] | bool = next(iterator, False)
            if type(token) == bool:
                tokenize = False
                print('EOF  null')
            else:
                character : str = token[1]
                index : int       = token[0]

                if string_open and character !='"':
                    string_array.append(character)
                elif character == '_' or character.isalpha():
                    identifier_array.append(character)
                    if index+1 < len(file_contents):
                        next_char:str = file_contents[index+1]
                        if not (next_char.isalpha() or next_char  == '_') or next_char==' ':
                            identifier : str = ''.join(identifier_array)
                            print(f"IDENTIFIER {identifier} null")
                            identifier_array.clear()
                    if index+1 >= len(file_contents):
                        identifier : str = ''.join(identifier_array)
                        print(f"IDENTIFIER {identifier} null")
                elif character == '\n':
                    line += 1
                elif not identifier_open and (character == '\t' or character == ' '):
                    continue
                elif is_simple_literal(character):
                    print(f"{get_token_type(character)} {character} null")
                elif character == '.' and not number_open:
                    print('DOT . null')
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
                            item: tuple[int, str] = next(iterator,(0,'\n'))
                            character = item[1]
                        line += 1
                elif character == '"':
                    if string_open:
                        string_open = False
                        string : str = "".join(string_array)
                        print(f"STRING \"{string}\" {string}")
                        string_array.clear()
                    else:
                        string_open = True
                elif character.isdigit() or character == '.':
                    #print('in number block, character = ',character)
                    #test:wq
                    if character == '.':
                        number_decimal = True
                    if number_open:
                        number_array.append(character)
                    else:
                        number_open = True
                        number_array.append(character)

                    if index+1 < len(file_contents) and file_contents[index+1].isdigit() == False:
                        next_character : str = file_contents[index+1]
                        if next_character == '.':
                            if number_decimal:
                                #number literal already has decimal points, therefore this is DOT -> 34.55 '.'(this dot)
                                # no need to handle else -> next iteration will add it (assuming number literal validity checked later)
                                number_open = False
                                string = ''.join(number_array)
                                print(f"NUMBER {string} {string}")
                                number_array.clear()
                        else:
                            number_open = False
                            string = ''.join(number_array)
                            print(f"NUMBER {string} {string}.0")
                            number_array.clear()
                    elif index+1 >= len(file_contents):
                        #end of file
                        string = ''.join(number_array)
                        if number_decimal:
                            print(f"NUMBER {string} {string}")
                        else:
                            print(f"NUMBER {string} {string}.0") 
                else:
                    errors = True
                    print(f"[line {line}] Error: Unexpected character: {character}", file=sys.stderr)

            if string_open:
                print(f'[line {line}] Error: Unterminated string.', file=sys.stderr)
                errors = True
                print("EOF  null")
    else:
        print("EOF  null")

    if errors:
        exit(65)
    else:
        exit(0)


def is_literal(character : str) -> bool:
    match character:    
        case '(':
            return True
        case ')':
            return True
        case '{':
            return True
        case '}':
            return True
        case '*':
            return True
        case '.':
            return True
        case ',':
            return True
        case '+':
            return True
        case '-':
            return True
        case ';':
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

def is_simple_literal(character : str)->bool:
    match character:    
        case '(':
            return True
        case ')':
            return True
        case '{':
            return True
        case '}':
            return True
        case '*':
            return True
        case ',':
            return True
        case '+':
            return True
        case '-':
            return True
        case ';':
            return True
    return False

def get_token_type(character : str)->str:
    match character:    
        case '(':
            return "LEFT_PAREN"
        case ')':
            return "RIGHT_PAREN"
        case '{':
            return "LEFT_BRACE"
        case '}':
            return "RIGHT_BRACE"
        case '*':
            return "STAR"
        case '.':
            return "DOT"
        case ',':
            return "COMMA"
        case '+':
            return "PLUS"
        case '-':
            return "MINUS"
        case ';':
            return "SEMICOLON"
        case '=':
            return "EQUAL"
        case '==':
            return "EQUAL_EQUAL"
        case '<':
            return "LESS"
        case '>':
            return "GREATER"
        case '/':
            return "SLASH"
        case '!':
            return "BANG"
        case '!=':
            return "BANG_EQUAL"
        case '<=':
            return "LESS EQUAL"
        case '>=':
            return "GREATER EQUAL"
    return "-1"



def is_complex_literal(character : str)->bool:
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
