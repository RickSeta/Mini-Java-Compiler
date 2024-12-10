import numpy as np

def is_space(char):
    return char in {' ', '\n', '\t', '\r', '\f'}

Input = list("if (x == 1) { System.out.println(x); } else { System.out.println(y); }")




def check_special_char(char,token):
    is_special = char in {'+', '-', '*', '/', '(', ')', '{', '}', '[', ']', ';', ',', '.', '=', '!', '<', '>', '&'}
    # print("Caractere passado: ", char)
    if is_special:
        if char == '.' and (token == "System" or token == "System.out"):
            #print(" char Ponto da palavra reservada identificado")
            return False
        return True
 
    return False

def reservada(token):
    if token in {'boolean', 'class', 'extends', 'public', 'static', 'void', 'main', 'String', 'return', 'int', 'if', 'else', 'while', 'System.out.println', 'length', 'true', 'false', 'this', 'new', 'null'}:
        return True

def double_special_char(char, input):
    next = input[0]
    if char + next in {'==', '!=', '<=', '>=', '&&', '/*', '*/', '//'}:
        return char + next
    return False

def checa_aceito(state, accept, token, token_sequence):
    if (token == ''):
        return

    if (accept[state]):
        if reservada(token):
            print("\nPalavra reservada: ", token)
            token_sequence.append((token, token))
            return

        print("\nAceito")
        print("Token: ", token,"\n")

        if state == 2:
            classe = 'id'
        elif state == 4:
            classe = 'integer'
        elif state == 5:
            if token != 'System.out.println':
                print("Erro")
                return

        token_sequence.append((token,classe))
    else:
        print("Rejeitado\n")

def checa_comentario(token):
    if token == '/*':
        return 1
    elif token == '*/':
        return 0
    elif token == '//':
        return 2

def check_char(char):
    if char.isalpha():
        return 'letra'
    if char.isdigit():
        return 'numero'
    if char == "_":
        return 'underline'
    if char == ".": 
        return '.'
    return 'outro'

def scanner(input ): 

    transitionTable = {
    1: {'letra': 2, 'numero': 4, 'underline': 3, 'outro': 3, '.' : 3}, # Estado inicial
    2: {'letra': 2, 'numero': 2, 'underline': 2, 'outro': 3, '.' : 5}, # Estado de aceitação identificador
    3: {'letra': 3, 'numero': 3, 'underline': 3, 'outro': 3, '.' : 3}, # Estado de rejeição
    4: {'letra': 3, 'numero': 4, 'underline': 3, 'outro': 3, '.' : 3}, # Estado para numeros
    5: {'letra': 5, 'numero': 3, 'underline': 3, 'outro': 3, '.' : 5}, # Estado para o System.out.println
    }
    accept = {1: False, 2: True, 3: False, 4: True, 5: True}
    
    tipo_comentario = 0
    input_current = 0
    final_index= len(input)
    token_sequence = []

    while(input_current < final_index):
        token = ""
        state = 1
        while(input_current < final_index):

            ch = input.pop(0)
            if (is_space(ch)):
                print("\nFim do token por espaço")
                input_current += 1
                break

            special = check_special_char(ch, token)
            if(special != False):
                if ch in {'=', '!', '<', '>', '&'}:
                    
                    token_class = double_special_char(ch, input)
                    if token_class:
                        checa_aceito(state, accept, token, token_sequence)
                        token = ch + input.pop(0)
                        token_sequence.append((token, token_class))
                        input_current += 2
                        tipo_comentario = checa_comentario(token)
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

            if (transitionTable[state][check_char(ch)] != 3):
                
                token += ch
                input_current += 1
                # print("Estado: ", state, "Caracter: ", ch)
                
                state = transitionTable[state][check_char(ch)]
                # print("Novo estado: ", state)
            else:
                print("Erro")
                break

        checa_aceito(state, accept, token, token_sequence)
        
        print(token_sequence, "\n")
    return token_sequence

scanner(Input)