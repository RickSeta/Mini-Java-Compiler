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
class arvore(object):
    def __init__(self, parent = None, id = None, child =None, data = None, type = any):
        self.parent = parent
        self.child = child
        self.id = id
        self.type = type
        self.data = data
    
    def add_child(self,name, data, id):
        if self.child == None:
            self.child = []
        new_child = arvore(data=data, id=name,type = any, parent=self)
        self.child.append(new_child)
        return new_child

    def print_tree(self, level=0, is_last=True, indent="  "):
        """
        Prints the tree structure in a clear and readable format.

        Args:
            level (int, optional): The current level of the node in the tree. Defaults to 0.
            is_last (bool, optional): Whether the current node is the last child of its parent. Defaults to True.
            indent (str, optional): The indentation string to use for each level. Defaults to "  ".
        """
        if self.data is None:
            return
        qmark = "\u25A1"  # Unicode right angle quotation mark for better visual representation

        # Print the current node with proper indentation
        print(indent * level + ("|- " if level > 0 else "") +
              (qmark if is_last else "|") + str(self.data))

        # Recursively print child nodes with adjusted indentation
        if self.child:
            i = 0
            while(len(self.child) > i):
                is_last_child = (i == len(self.child) - 1)
                # print(self.child[i].data)
                # print(self.child[i].child)
                self.child[i].print_tree(level + 1, is_last_child, indent)
                i += 1

def parser(tabela,gramatica,entrada):
    producao_inicial= list(gramatica.keys())[0]
    pilha = ["$", producao_inicial]
    entrada.append("$")


    tree = arvore(data = producao_inicial, id = 1)
    syntatic_tree_pointer = tree
    syntatic_child_pilha =[]
    scp_counter = 0
    nivel = 0
    
    
    entradaPointer = 0
    while True:
        print("\n------------------------------------")
        tree.print_tree()
        print("Pilha: ",pilha," entrada: ", entrada[entradaPointer])
        topoPilha = pilha[-1]

        #Eqnaunto houver demarcador de nivel remova e reduza o nivel da arvore que esta sendo trabalho
        while topoPilha == "#":
            nivel -=1
            print("Reducao ao nivel ",nivel)
            pilha.pop()
            topoPilha = pilha[-1]
            syntatic_tree_pointer = syntatic_tree_pointer.parent
            scp_counter = syntatic_child_pilha.pop()
            scp_counter += 1
            if scp_counter < len(syntatic_tree_pointer.child):
                print(scp_counter)
                print(len(syntatic_tree_pointer.child))
                syntatic_tree_pointer = syntatic_tree_pointer.child[scp_counter]

        #se o topo da pilha for o simbolo de fim da pilha e o simbolo de entrada for o mesmo aceita
        if topoPilha == entrada[entradaPointer][0] == "$":
            print("Aceito")
            break

        #se o topo da pilha for uma produção possivel
        elif topoPilha in gramatica:

            #se houver transicao na tabela utilizando o topo da pilha e o simbolo de entrada então substitui o topo da pilha pela nova produção
            if entrada[entradaPointer][0] in tabela[topoPilha]:
                producao = tabela[topoPilha][entrada[entradaPointer]]
                print("Produção: ", producao)
                pilha.pop()
                
                

                if producao[0] != "ε":
                    pilha.append('#')
                    nivel +=1
                    syntatic_child_pilha.append(scp_counter)
                    scp_counter = 0

                    print("Adicao ao nivel ",nivel)

                    idcounter = 0
                    for simbolo in reversed(producao):
                        if simbolo != "ε":
                            pilha.append(simbolo)

                            #colocando nao terminal na arvore
                    
                    for simbolo in producao:
                        
                        syntatic_tree_pointer.add_child(simbolo, simbolo,simbolo+str(idcounter))
                        idcounter += 1
                    syntatic_tree_pointer = syntatic_tree_pointer.child[0]
                else:
                    print("Adicao de ε")
                    syntatic_tree_pointer.add_child("ε", "ε",str(entradaPointer))
                    
                    if(pilha[-1] != "#"):
                        scp_counter += 1
                        syntatic_tree_pointer = syntatic_tree_pointer.parent.child[scp_counter]
            else:
                print("Erro. Não existe regra para", topoPilha, entrada[entradaPointer])
                break
        elif topoPilha == entrada[entradaPointer]:
            print('match', ":", entrada[entradaPointer])
            pilha.pop()
            #colocando terminal na arvore
            print(syntatic_tree_pointer.data)
            syntatic_tree_pointer.add_child(entrada[entradaPointer],entrada[entradaPointer],entradaPointer)
            scp_counter += 1
            syntatic_tree_pointer = syntatic_tree_pointer.parent.child[scp_counter]
            
            entradaPointer += 1

        else:
            print("Erro. ")
            break
# tree = arvore(data = "S", id = "1")
# tree.add_child("S", "2")
# tree.add_child("S", "3")

# tree.child[0].add_child("S", "4")
# tree.child[0].add_child("S", "5")
# tree.child[1].add_child("S", "6")
# tree.child[1].add_child("S", "7")
# tree.child[0].child[0].add_child("S", "8")
# tree.print_tree()
parser(tabela_ll1(test_grammar),test_grammar,['(',')','(',')','$'])
