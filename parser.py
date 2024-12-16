gramatica = {
    "PROG": [["MAIN", "{", "CLASSE", "}"]],

    "MAIN": [["class", "id", "{", "public", "static", "void", "main", "(", "String", "[", "]", "id", ")", "{", "CMD", "}", "}"]],

    "CLASSE": [["class", "id", "CLASSE'"],["extends", "id", "{", "VAR_LIST", "METODO_LIST", "}"], ["{", "VAR_LIST", "METODO_LIST", "}"]],

    "VAR_LIST": [["VAR", "VAR_LIST"], ["ε"]],
    "VAR": [["TIPO", "id", ";"]],

    "METODO_LIST": [["METODO", "METODO_LIST"], ["ε"]],
    "METODO": [["public", "TIPO", "id", "(", "PARAMS", ")", "{", "VAR_LIST", "CMD_LIST", "return", "EXP", ";", "}"]],

    "PARAMS": [["TIPO", "id", "PARAMS'"], ["ε"]],
    "PARAMS'": [[",", "TIPO", "id", "PARAMS'"], ["ε"]],

    "TIPO": [["int", "[", "]"], ["boolean"], ["int"], ["id"]],

    "CMD_LIST": [["CMD", "CMD_LIST"], ["ε"]],
    "CMD": [["{", "CMD'", "}"],
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
    "PEXP''": [["(", "EXPS", ")", "PEXP'"], ["ε"]],

    "EXPS": [["EXP", "EXPS'"], ["ε"]],
    "EXPS'": [[",", "EXP", "EXPS'"], ["ε"]]
}

def first(gramatica):
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

def follow(firsts):
    follow = {}
    for simbolo in gramatica:
        follow[simbolo] = []
    follow["PROG"].append("$")
    changes = True
    while changes:
        changes = False
        for simbolo in gramatica:
            for producao in gramatica[simbolo]:
                for i in range(len(producao)):
                    if producao[i] in gramatica:
                        if i == len(producao) - 1:
                            for innerFollow in follow[simbolo]:
                                if innerFollow not in follow[producao[i]]:
                                    follow[producao[i]].append(innerFollow)
                                    changes = True
                        else:
                            if producao[i+1] not in gramatica:
                                if producao[i+1] not in follow[producao[i]]:
                                    follow[producao[i]].append(producao[i+1])
                                    changes = True
                            for innerFirst in firsts[producao[i+1]]:
                                if innerFirst not in follow[producao[i]]:
                                    follow[producao[i]].append(innerFirst)
                                    changes = True
                            if "ε" in firsts[producao[i+1]]:
                                for innerFollow in follow[simbolo]:
                                    if innerFollow not in follow[producao[i]]:
                                        follow[producao[i]].append(innerFollow)
                                        changes = True
    return follow

print(follow(first(gramatica)))