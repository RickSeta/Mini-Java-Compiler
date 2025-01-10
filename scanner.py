

def is_space(char):
    return char in {' ', '\n', '\t', '\r', '\f'}

def check_special_char(char,token):
    is_special = char in {'+', '-', '*', '(', ')', '{', '}', '[', ']', ';', ',', '.', '=', '!', '<', '>', '&'}
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
        # print(token, state)
        if reservada(token):
            # print("\nPalavra reservada: ", token)
            token_sequence.append((token, token))
            return

        # print("\nAceito")
        # print("Token: ", token,"\n")

        if state == 2:
            classe = 'id'
        elif state == 4:
            classe = 'num'
        elif state == 5:
            if token != 'System.out.println':
                print("Erro")
                return

        token_sequence.append((token,classe))
    else:
        print("Rejeitado\n")


def check_char(char):
    if char.isalpha():
        return 'letra'
    if char.isdigit():
        return 'numero'
    if char == "_":
        return 'underline'
    if char == ".": 
        return '.'
    if char == "/":
        return '/'
    if char == "*":
        return '*'
    if char == "\n":
        return '\n'
    return 'outro'

def scanner(input): 
    input.append(' ')
    transitionTable = {
    1: {'letra': 2, 'numero': 4, 'underline': 3, 'outro': 3, '.' : 3, '/': 6, '*': 3, '\n': 2 }, # Estado inicial
    2: {'letra': 2, 'numero': 2, 'underline': 2, 'outro': 3, '.' : 5, '/': 6, '*': 3, '\n': 2 }, # Estado de aceitação identificador
    3: {'letra': 3, 'numero': 3, 'underline': 3, 'outro': 3, '.' : 3, '/': 6, '*': 3, '\n': 3 }, # Estado de erro
    4: {'letra': 3, 'numero': 4, 'underline': 3, 'outro': 3, '.' : 3, '/': 6, '*': 3, '\n': 3 }, # Estado para numeros
    5: {'letra': 5, 'numero': 3, 'underline': 3, 'outro': 3, '.' : 5, '/': 6, '*': 3, '\n': 5 }, # Estado para o System.out.println

    6: {'letra': 3, 'numero': 3, 'underline': 3, 'outro': 3, '.' : 3, '/': 7, '*': 9, '\n': 3 }, # Estado para o segundo char do indicador de comentario
    7: {'letra': 7, 'numero': 7, 'underline': 7, 'outro': 7, '.' : 7, '/': 7, '*': 7, '\n': 1 }, # Estado para comentario inline

    9: {'letra': 9, 'numero': 9, 'underline': 9, 'outro': 9, '.' : 9, '/': 9, '*': 10,'\n': 9 }, # Estado para primeiro asterisco do block comment
    10: {'letra': 9,'numero': 9, 'underline': 9, 'outro': 9, '.' : 9, '/': 1, '*': 10,'\n': 9 }, # Estado para asterisco dentro do block comment aguardadndo pela barra
    }
    accept = {1: False, 2: True, 3: False, 4: True, 5: True, 6: False, 7: True, 8: True, 9: False, 10: False}
    
    token_sequence = []
    not_comment = True

    while(len(input) > 0):
        token = ""
        state = 1
        while(len(input) > 0):
            ch = input.pop(0)

            if not_comment: #ignore comments
                if (is_space(ch)): #ends token if sees a space

                    # print("\nFim do token por espaço")
                    break

                special = check_special_char(ch, token) #check if char is special

                if(special != False):
                    if ch in {'=', '!', '<', '>', '&'}: #check if char is a special char that can be double
                        
                        token_class = double_special_char(ch, input)
                        if token_class:
                            checa_aceito(state, accept, token, token_sequence)
                            token = ch + input.pop(0)
                            token_sequence.append((token, token_class))
                            # print("Caractere especial duplo aceito: ", token)
                            token = ""
                            break
                    #se for char unico
                    checa_aceito(state, accept, token, token_sequence)
                    token_sequence.append((ch, ch))
                    # print("Caractere especial aceito: ", ch)
                    token = ""
                    break

            if (transitionTable[state][check_char(ch)] != 3): #if not in error state then 
                
                state = transitionTable[state][check_char(ch)]
                if state not in {6, 7, 9, 10}: #if not in comment state then add to token
                    not_comment = True
                    token += ch
                else:
                    not_comment = False
                    # print("Caractere no estado de comentario: ", ch, " estado:", transitionTable[state][check_char(ch)])
                # print("Estado: ", state, "Caracter: ", ch)
                
            else:
                if ch == "$":
                    token_sequence.append((ch, ch))
                else:
                    print("Erro", ch)
                    break

        checa_aceito(state, accept, token, token_sequence)
        
    return token_sequence

Input = list("""class Factorial{
 public static void main(String[] a){
 System.out.println(new Fac().ComputeFac(10));
 }
}
""")