import numpy as np

def is_space(char):
    return char in {' ', '\n', '\t', '\r', '\f'}

Input = list("aaaabba aa + a<=")

T = {
    1: {'letra': 2, 'digito': 3, }, 
}

T = {
    1: {'a': 2, 'b': 3}, 
    2: {'a': 2, 'b': 3}, 
    3: {'a': 1, 'b': 3},  
}

Accept = {1: False, 2: True, 3: False}

def check_special_char(char):
    is_special = char in {'+', '-', '*', '/', '(', ')', '{', '}', '[', ']', ';', ',', '.', '=', '!', '<', '>', '&'}
    # print("Caractere passado: ", char)
    if is_special:
        # print("Caractere especial truado: ", char)
        return True
 
    return False
def double_special_char(char, input):
    next = input[0]
    if char + next == '==':
        return "=="
    elif char + next == '!=':
        return "!="
    elif char + next == '<=':
        return "<="
    elif char + next == '>=':
        return ">="
    elif char + next == '&&':
        return "and"
    elif char + next == '/*':
        return "/*"
    elif char + next == '*/':
        return "*/"
    elif char + next == '//':
        return "//"
    return False

def checa_aceito(state, accept, token, token_sequence):
    if (token == ''):
        return
    if (accept[state]):
        print("\nAceito")
        print("Token: ", token,"\n")
        token_sequence.append((token,state))
        print(token_sequence, "\n")
    else:
        print("Rejeitado\n")

def scanner(input, accept, transitionTable): 
    
    input_current = 0
    final_index= len(input)
    token_sequence = []
    while(input_current < final_index):
        token = ""
        state = 1
        while(input_current < final_index):

            ch = input.pop(0)
            special = check_special_char(ch)
            if(special != False):
                token_class = double_special_char(ch, input)
                if ch in {'=', '!', '<', '>', '&'} and token_class:
                    checa_aceito(state, accept, token, token_sequence)
                    token = ch + input.pop(0)
                    token_sequence.append((token, token_class))
                    input_current += 2
                    print("Caractere especial duplo aceito: ", token)
                    token = ""

                else:
                    if ch in {'+', '-', '*', '/', '(', ')', '{', '}', '[', ']', ';', ',', '.', '=', '!', '<', '>'}:
                        
                        checa_aceito(state, accept, token, token_sequence)
                        token_sequence.append((ch, ch))
                        print("Caractere especial aceito: ", ch)
                        token = ""
                        input_current += 1
                    

                break
            if (is_space(ch)):
                print("\nFim do token por espaço")
                input_current += 1
                break
            if(ch not in transitionTable[state]):
                print("Erro")
                input_current += 1
                break
            if (transitionTable[state][ch]):
                
                token += ch
                input_current += 1
                print("Estado: ", state, "Caracter: ", ch)
            else:
                print("Erro")
                break

            state = T[state][ch]
            print("Novo estado: ", state)
        checa_aceito(state, accept, token, token_sequence)
    return token_sequence

scanner(Input, Accept, T)