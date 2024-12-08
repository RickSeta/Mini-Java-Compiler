import numpy as np

def is_space(char):
    return char in {' ', '\n', '\t', '\r', '\f'}

Input = ["a","b","b","a","a"," ","e","b","a","a","b","a","a","a"]

T = {
    1: {'a': 2, 'b': 3}, 
    2: {'a': 2, 'b': 3}, 
    3: {'a': 1, 'b': 3},  
}
Accept = {1: False, 2: True, 3: False}

def scanner(input, accept, transitionTable): 
    
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
        if (accept[state]):
            print("\nAceito")
            print("Token: ", token,"\n")
            token_sequence.append((token,state))
            print(token_sequence, "\n")
        else:
            print("Rejeitado\n")
    return token_sequence

scanner(Input, Accept, T)