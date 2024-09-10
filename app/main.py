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
            else:
                character : str = token[1]
                index : int       = token[0]
                
                if character == '_' or character.isalpha():
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
                elif character == '=':
                    print(handle_eq_literal(index, iterator, file_contents))
                elif character == '!':
                    print(handle_bang_literal(index, iterator, file_contents))
                elif character == '<':
                    print(handle_ineq(index, iterator, character, file_contents))
                elif character == '>':
                    print(handle_ineq(index, iterator, character, file_contents))
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
                    string_ret : tuple[str,int,int] = handle_string(index, iterator, character, file_contents)
                    line :int                       = line + string_ret[2]
                    
                    if string_ret[1] == 0:
                        print(string_ret[0])
                    else:
                        print(f'[line {line}] Error: Unterminated string.', file=sys.stderr)
                        errors = True            
                elif character.isdigit():
                    print(handle_num(index, iterator, character, file_contents))
                else:
                    errors = True
                    print(f"[line {line}] Error: Unexpected character: {character}", file=sys.stderr)

    print("EOF  null")

    if errors:
        exit(65)
    else:
        exit(0)


#check if next character exists
def is_next(current_index : int, stream : str)->bool:
    if current_index + 1 < len(stream):
        return True
    else:
        return False


#handle '=' sign and '==' sign
def handle_eq_literal(index : int, iterator:enumerate[str], stream : str) -> str:
    
    if not is_next(index, stream):
        return "EQUAL = null"
    else:
        #is_next() guarantees there is a next character
        if stream[index+1] == '=':
            next(iterator)
            return "EQUAL_EQUAL == null"
        else:
            return "EQUAL = null"
        
#handle '!'
def handle_bang_literal(index : int, iterator:enumerate[str], stream : str) -> str:
    if not is_next(index, stream):
        return "BANG ! null"
    else:
        #is_next() guarantees there is a next character
        if stream[index+1] == '=':
            next(iterator)
            return "BANG_EQUAL != null"
        else:
            return "BANG ! null"

#handle inequality operators
def handle_ineq(index : int, iterator : enumerate[str], character:str, stream : str)->str:
    if not (character == '>' or character == '<'):
        return ""
    if not is_next(index, stream):
        if character == '<':
            return "LESS < null"
        else:
            return "GREATER > null"
    else:
        #is_next() has guranteed next character exists
        if not stream[index+1] == '=':
            if character == '<':
                return "LESS < null"
            else:
                return "GREATER > null"
        else:
            if character == '<':
                next(iterator)
                return "LESS_EQUAL <= null"
            else:
                next(iterator)
                return "GREATER_EQUAL >= null"
            
#handle numbers - RETURN : [ string, error_code(0,1), (count \n) ]
def handle_num(index : int, iterator : enumerate[str], character : str, stream : str)->str:
    decimal : bool = False
    num_arr : list[str]= []
    in_number : bool = True
    next_char : str = ''

    if not character.isdigit():
        return ""
    else:
        while in_number:
            num_arr.append(character)
            if is_next(index, stream):
                next_char = stream[index + 1]
                if next_char == '.' and decimal:
                    in_number = False
                elif next_char == '.' and not decimal:
                    if stream[index + 2].isdigit():
                        _next = next(iterator,(len(stream),'')) 
                        character = _next[1]
                        index = _next[0]
                        decimal = True
                    else:
                        in_number = False
                elif next_char.isdigit():
                    _next = next(iterator,(len(stream),'')) 
                    character  = _next[1]
                    index = _next[0]
                else:
                    in_number = False
            else:
                in_number = False

        if decimal:
            number : str = ''.join(num_arr)
            return "NUMBER "+number+" "+number
        else:
            number : str = ''.join(num_arr)
            return "NUMBER "+number+" "+number+".0"

#handle strings
def handle_string(index : int, iterator : enumerate[str], character : str, stream : str)->tuple[str,int, int]:
    in_string : bool        = True
    string_arr : list[str]  = []
    error : bool            = False
    line : int              = 0
    
    if not character == '"':
        return (f"FUNCTION handle_string() CALLED WITH INVALID ARGUMENT : {character}", 1, 0)
    else:
        if not is_next(index, stream):
            # line -> "[EOF]
            return ("",1, 0)
        else:
            while in_string:
                _next : tuple[int,str]  = next(iterator, (len(stream),""))
                
                character         = _next[1]
                index             = _next[0]

                if index == len(stream):
                    #end of file without terminating string
                    in_string = False
                    error = True
                else:
                    if character == '"':
                        in_string = False
                    else:
                        string_arr.append(character)
                        if character == '\n':
                            line += 1

    if error:
        return ("",1,0)
    else:
        string : str = ''.join(string_arr)
        return (f"STRING \"{string}\" {string}", 0, line)


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
        case '.':
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
