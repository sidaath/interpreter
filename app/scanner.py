import sys

class Tokenizer:
    """Class to handle tokenization"""
    tokens : list[str] = []

    def tokenize(self, filename : str) -> bool:
        with open(filename) as file:
            file_contents = file.read()
        
        errors : bool = False
        
        if file_contents:
            #track line number in loop
            line : int = 1

            #validity of current '/' token while tokenizing
            slash_operator_valid : bool = True

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
                        identifier : str = self.handle_identifier(index, iterator, character, file_contents)
                        if self.is_reserved(identifier):
                            self.tokens.append(f"{identifier.upper()} {identifier} null")
                        else:
                            self.tokens.append(f"IDENTIFIER {identifier} null")
                    elif character == '\n':
                        line += 1
                    elif character == '\t' or character == ' ':
                        continue
                    elif self.is_simple_literal(character):
                        self.tokens.append(f"{self.get_token_type(character)} {character} null")
                    elif character == '=':
                        self.tokens.append(self.handle_eq_literal(index, iterator, file_contents))
                    elif character == '!':
                        self.tokens.append(self.handle_bang_literal(index, iterator, file_contents))
                    elif character == '<':
                        self.tokens.append(self.handle_ineq(index, iterator, character, file_contents))
                    elif character == '>':
                        self.tokens.append(self.handle_ineq(index, iterator, character, file_contents))
                    elif character == '/':
                        if slash_operator_valid:
                            if index+1 < len(file_contents) and file_contents[index+1] =='/':
                                slash_operator_valid = False
                            else:
                                self.tokens.append('SLASH / null')
                        else:
                            #second '/', rest of line is a comment, stop reading line (skip line when scanning multi lines)
                            while character != '\n':
                                item: tuple[int, str] = next(iterator,(0,'\n'))
                                character = item[1]
                            line += 1
                    elif character == '"':
                        string_ret : tuple[str,int,int] = self.handle_string(index, iterator, character, file_contents)
                        line :int                       = line + string_ret[2]
                        
                        if string_ret[1] == 0:
                            self.tokens.append(string_ret[0])
                        else:
                            print(f'[line {line}] Error: Unterminated string.', file=sys.stderr)
                            errors = True            
                    elif character.isdigit():
                        self.tokens.append(self.handle_num(index, iterator, character, file_contents))
                    else:
                        errors = True
                        print(f"[line {line}] Error: Unexpected character: {character}", file=sys.stderr)
            self.tokens.append("EOF  null")
        else:
            self.tokens.append("EOF  null")
        return errors


    #check if next character exists
    def is_next(self, current_index : int, stream : str)->bool:
        if current_index + 1 < len(stream):
            return True
        else:
            return False


    #handle '=' sign and '==' sign
    def handle_eq_literal(self, index : int, iterator:enumerate[str], stream : str) -> str:
        
        if not self.is_next(index, stream):
            return "EQUAL = null"
        else:
            #is_next() guarantees there is a next character
            if stream[index+1] == '=':
                next(iterator)
                return "EQUAL_EQUAL == null"
            else:
                return "EQUAL = null"
            
    #handle '!'
    def handle_bang_literal(self, index : int, iterator:enumerate[str], stream : str) -> str:
        if not self.is_next(index, stream):
            return "BANG ! null"
        else:
            #is_next() guarantees there is a next character
            if stream[index+1] == '=':
                next(iterator)
                return "BANG_EQUAL != null"
            else:
                return "BANG ! null"

    #handle inequality operators
    def handle_ineq(self, index : int, iterator : enumerate[str], character:str, stream : str)->str:
        if not (character == '>' or character == '<'):
            return ""
        if not self.is_next(index, stream):
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
    def handle_num(self, index : int, iterator : enumerate[str], character : str, stream : str)->str:
        decimal : bool = False
        num_arr : list[str]= []
        in_number : bool = True
        next_char : str = ''

        if not character.isdigit():
            return ""
        else:
            while in_number:
                num_arr.append(character)
                if self.is_next(index, stream):
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
                number_lexeme : str = ''.join(num_arr)

                n : int = len(num_arr) - 1
                
                while n > 0:
                    if num_arr[n] == '0':
                        num_arr.pop()
                        n = n-1
                    elif num_arr[n] == '.':
                        num_arr.append('0')
                        n = 0
                    else:
                        n = 0

                
                number_literal : str = ''.join(num_arr)
                return "NUMBER "+number_lexeme+" "+number_literal
            else:
                number : str = ''.join(num_arr)
                return "NUMBER "+number+" "+number+".0"

    #handle strings
    def handle_string(self, index : int, iterator : enumerate[str], character : str, stream : str)->tuple[str,int, int]:
        in_string : bool        = True
        string_arr : list[str]  = []
        error : bool            = False
        line : int              = 0
        
        if not character == '"':
            return (f"FUNCTION handle_string() CALLED WITH INVALID ARGUMENT : {character}", 1, 0)
        else:
            if not self.is_next(index, stream):
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
        

    #handle identifiers - _123az, abc, space seperated
    def handle_identifier(self, index : int, iterator : enumerate[str], character : str, stream : str):
        in_identifier : bool        = True
        identifier_arr: list[str]   = []

        if not (character == '_' or character.isalpha()):
            return f"FUNCTION handle_identifier() called with invalid argument {character}"

        if not self.is_next(index, stream):
            return f"IDENTIFIER {character} null"
        else:
            identifier_arr.append(character)
            while in_identifier:
                if self.is_next(index, stream):
                    next_char : str = stream[index + 1]
                    if not (next_char == '_' or next_char.isalnum()):
                        in_identifier = False
                    else:
                        _next = next(iterator, (len(stream),''))
                        character = _next[1]
                        index     = _next[0]
                        identifier_arr.append(character)
                else:
                    in_identifier = False

        string: str = ''.join(identifier_arr)
        return string



    #check if reserved word
    def is_reserved(self, word : str)->bool:
        match word:
            case "and":
                return True
            case "class":
                return True
            case "else":
                return True
            case "false":
                return True
            case "for":
                return True
            case "fun":
                return True
            case "if":
                return True
            case "nil":
                return True
            case "or":
                return True
            case "print":
                return True
            case "return":
                return True
            case "super":
                return True
            case "this":
                return True
            case "true":
                return True
            case "var":
                return True
            case "while":
                return True
            case _:
                return False


    def is_literal(self, character : str) -> bool:
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

    def is_simple_literal(self, character : str)->bool:
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

    def get_token_type(self, character : str)->str:
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



    def is_complex_literal(self, character : str)->bool:
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
