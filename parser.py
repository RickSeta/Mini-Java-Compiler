gramatica_minijava = {
    "PROG": [["MAIN", "CLASSE_LIST"]],
    "CLASSE_LIST": [["CLASSE", "CLASSE_LIST"], ["ε"]],

    "MAIN": [["class", "id", "{", "public", "static", "void", "main", "(", "String", "[", "]", "id", ")", "{", "CMD", "}", "}"]],

    "CLASSE": [["class", "id", "EXTENDS_ID_OPTIONAL", "{", "VAR_LIST", "METODO_LIST", "}"]],
    "EXTENDS_ID_OPTIONAL": [["extends", "id"], ["ε"]],

    "VAR_LIST": [["VAR", "VAR_LIST"], ["ε"]],
    "VAR": [["TIPO", "id", ";"]],

    "METODO_LIST": [["METODO", "METODO_LIST"], ["ε"]],
    "METODO": [["public", "TIPO", "id", "(", "PARAMS_OPTIONAL", ")", "{", "VAR_LIST", "CMD_LIST", "return", "EXP", ";", "}"]],
    "PARAMS_OPTIONAL": [["PARAMS"], ["ε"]],

    "PARAMS": [["TIPO", "id", "PARAMS", "TIPO_ID_LIST"]],
    "TIPO_ID_LIST": [[",","TIPO", "id", "TIPO_ID_LIST"], ["ε"]],


    "TIPO": [["int", "[", "]"], ["boolean"], ["int"], ["id"]],

    "CMD_LIST": [["CMD", "CMD_LIST"], ["ε"]],
    "CMD": [["{", "CMD_LIST'", "}"],
            ["if", "(", "EXP", ")", "CMD", "else", "CMD"],
            ["if", "(", "EXP", ")", "CMD"],
            ["while", "(", "EXP", ")", "CMD"],
            ["System.out.println", "(", "EXP", ")", ";"],
            ["id", "CMD'"]],

    "CMD'": [["[", "EXP", "]", "=", "EXP", ";"], ["=", "EXP", ";"]],

    "EXP": [["REXP", "EXP'"]],
    "EXP'": [["&&", "REXP", "EXP'"], ["ε"]],

    "REXP": [["AEXP", "REXP'"]],
    "REXP'": [["<", "AEXP", "REXP'"], ["==", "AEXP", "REXP'"], ["!=", "AEXP", "REXP'"], ["ε"]],

    "AEXP": [["MEXP", "AEXP'"]],
    "AEXP'": [["+", "MEXP", "AEXP'"], ["-", "MEXP", "AEXP'"], ["ε"]],

    "MEXP": [["SEXP", "MEXP'"]],
    "MEXP'": [["*", "SEXP", "MEXP'"], ["ε"]],

    "SEXP": [["!", "SEXP"], ["-", "SEXP"], ["true"], ["false"], ["num"], ["null"],
             ["new", "int", "[", "EXP", "]"], ["PEXP", ".", "length"], ["PEXP", "[", "EXP", "]"]],

    "PEXP": [["id", "PEXP'"], ["this", "PEXP'"], ["new", "id", "(", ")", "PEXP'"], ["(", "EXP", ")", "PEXP'"]],
    "PEXP'": [[".", "id", "PEXP''"], ["ε"]],
    "PEXP''": [["(", "EXPS_OPTIONAL", ")", "PEXP'"], ["ε"]],
    "EXPS_OPTIONAL": [["EXPS"], ["ε"]],

    "EXPS": [["EXP", "EXPS_LIST'"],],
    "EXPS_LIST": [["," , "EXP", "EXPS_LIST"], ["ε"]]
}

test_grammar ={
    "S": [["(", "S",")","S"], ["ε"]],
}
def firstFunc(gramatica):
    firsts = {}
    for simbolo in gramatica:
        firsts[simbolo] = []
    changes = True
    while changes:
        changes = False
        for simbolo in gramatica:
            for producao in gramatica[simbolo]:
                if producao[0] == "ε":
                    if "ε" not in firsts[simbolo]:
                        firsts[simbolo].append("ε")
                        changes = True
                elif producao[0] not in gramatica:
                    if producao[0] not in firsts[simbolo]:
                        firsts[simbolo].append(producao[0])
                        changes = True
                else:
                    for innerFirst in firsts[producao[0]]:
                        if innerFirst not in firsts[simbolo]:
                            firsts[simbolo].append(innerFirst)
                            changes = True
                    
    return firsts

def follow(firsts,gramatica):
    follow = {}
    for simbolo in gramatica:
        follow[simbolo] = []
    follow[list(gramatica.keys())[0]].append("$")
    changes = True
    while changes:
        changes = False
        for simbolo in gramatica:
            for producao in gramatica[simbolo]:
                for i in range(len(producao)):
                    if producao[i] in gramatica:
                        #se for ultimo simbolo na producao
                        if i == len(producao) - 1:
                            for innerFollow in follow[simbolo]:
                                if innerFollow not in follow[producao[i]]:
                                    follow[producao[i]].append(innerFollow)
                                    changes = True
                        else:
                            #se for terminal
                            if producao[i+1] not in gramatica:
                                print(producao[i+1])
                                if producao[i+1] not in follow[producao[i]]:
                                    if follow[producao[i]] !=  "ε":
                                        follow[producao[i]].append(producao[i+1])
                                        changes = True
                            else:
                                #se for não terminal
                                for innerFirst in firsts[producao[i+1]]:
                                    if innerFirst not in follow[producao[i]]:
                                        if innerFirst !=  "ε":
                                            follow[producao[i]].append(innerFirst)
                                            changes = True
                                #se o first do proximo simbolo da producao contem "ε"
                                if "ε" in firsts[producao[i+1]]:
                                    for innerFollow in follow[simbolo]:
                                        if innerFollow not in follow[producao[i]]:
                                            follow[producao[i]].append(innerFollow)
                                            changes = True
        return follow


def tabela_ll1(gramatica):
    firsts = firstFunc(gramatica)
    follows = follow(firsts,gramatica)
    tabela = {}
    for simbolo in gramatica:

        tabela[simbolo] = {}
        for producao in gramatica[simbolo]:
            #se producao[0] não for for terminal
            if(producao[0] in gramatica):
                for terminal in firsts[producao[0]]:
                    if terminal != "ε":
                        tabela[simbolo][terminal] = producao
                if "ε" in firsts[producao[0]]:
                    for terminal in follows[simbolo]:
                        tabela[simbolo][terminal] = producao
            else:
                #se for terminal e não epsilon
                if producao[0] != "ε":
                    tabela[simbolo][producao[0]] = producao
                else:
                    #se for ε
                    for terminal in follows[simbolo]:
                        tabela[simbolo][terminal] = producao
    return tabela

def print_tabela(tabela):
    for simbolo in tabela:
        print(simbolo)
        for terminal in tabela[simbolo]:
            print("\t", terminal, ":", tabela[simbolo][terminal])

print_tabela(tabela_ll1(test_grammar))