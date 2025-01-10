from geracao import MIPSGenerator
import scanner
import semantica

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

    "PARAMS": [["TIPO", "id", "TIPO_ID_LIST"]],
    "TIPO_ID_LIST": [[",","TIPO", "id", "TIPO_ID_LIST"], ["ε"]],


    "TIPO": [["int","INT_OPTION"], ["boolean"], ["id"]],
    "INT_OPTION": [["[", "]"], ["ε"]],

    "CMD_LIST": [["CMD", "CMD_LIST"], ["ε"]],
    "CMD": [["MATCHED_CMD"],
            ["UNMATCHED_CMD"]],

    "MATCHED_CMD": [["{", "CMD_LIST'", "}"],
                    ["if", "(", "EXP", ")", "MATCHED_CMD", "else", "MATCHED_CMD"],
                    ["while", "(", "EXP", ")", "CMD"],
                    ["System.out.println", "(", "EXP", ")", ";"],
                    ["id", "CMD'"]],

    "UNMATCHED_CMD": [["if", "(", "EXP", ")", "CMD"],
                    ["if", "(", "EXP", ")", "MATCHED_CMD", "else", "UNMATCHED_CMD"]],
                    
    "CMD'": [["[", "EXP", "]", "=", "EXP", ";"], ["=", "EXP", ";"]],

    "EXP": [["REXP", "EXP'"]],
    "EXP'": [["&&", "REXP", "EXP'"], ["ε"]],

    "REXP": [["AEXP", "REXP'"]],
    "REXP'": [["<", "AEXP", "REXP'"], ["==", "AEXP", "REXP'"], ["!=", "AEXP", "REXP'"], ["ε"]],

    "AEXP": [["MEXP", "AEXP'"]],
    "AEXP'": [["+", "MEXP", "AEXP'"], ["-", "MEXP", "AEXP'"], ["ε"]],

    "MEXP": [["SEXP", "MEXP'"]],
    "MEXP'": [["*", "SEXP", "MEXP'"], ["ε"]],

    "SEXP": [["!", "SEXP"],  ["-", "SEXP"], ["true"], ["false"], ["num"], ["null"],["new","new_options"],["PEXP", "PEXP_OPTIONS"]],
    "PEXP_OPTIONS": [[".", "length"], ["[", "EXP", "]"], ["ε"]],

    "new_options":[["new_int_array"],["id_possible"]],
    "new_int_array": [["int", "[", "EXP", "]"]],

    "PEXP": [["id_possible"], ["this", "PEXP'"], ["(", "EXP", ")", "PEXP'"]],
    "id_possible": [["id", "id_options"]],
    "id_options": [["(", ")", "PEXP'"], ["PEXP'"]],

    "PEXP'": [[".", "id", "PEXP''"], ["ε"]],
    "PEXP''": [["(", "EXPS_OPTIONAL", ")", "PEXP'"], ["ε"]],

    "EXPS_OPTIONAL": [["EXPS"], ["ε"]],

    "EXPS": [["EXP", "EXPS_LIST"],],
    "EXPS_LIST": [["," , "EXP", "EXPS_LIST"], ["ε"]]
}

test_grammar ={
    "K": [["R","X"]],
    "R": [["int"],["class"]],
    "Z":[["void"],["public"]],
    "X":[["Z", "W"], ["ε"]],
    "W":[["id"]],

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
                if producao == "Ellipsis":
                    print()
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

def follow(firsts, gramatica):
    # Inicializa os conjuntos FOLLOW como listas vazias
    follow = {regra: [] for regra in gramatica}
    
    # Adiciona '$' ao conjunto FOLLOW do símbolo inicial
    follow[list(gramatica.keys())[0]].append("$")
    
    changes = True
    while changes:
        changes = False
        
        # Itera através da gramática
        for regra in gramatica:
            for producao in gramatica[regra]:
                # Itera através de cada símbolo na produção
                for i in range(len(producao)):
                    if producao[i] in gramatica:  # Se o símbolo é um não-terminal
                        # Caso em que estamos no final da produção (A -> αB)
                        if i == len(producao) - 1:
                            for terminal in follow[regra]:
                                if terminal not in follow[producao[i]]:
                                    follow[producao[i]].append(terminal)
                                    changes = True
                        else:
                            # Olha para o próximo símbolo na produção
                            next_symbol = producao[i + 1]
                            if next_symbol not in gramatica:  # É um terminal
                                if next_symbol not in follow[producao[i]]:
                                    follow[producao[i]].append(next_symbol)
                                    changes = True
                            else:  # É um não-terminal
                                # Adiciona FIRST(next_symbol) (exceto epsilon) ao FOLLOW do não-terminal atual
                                for terminal in firsts[next_symbol]:
                                    if terminal != "ε" and terminal not in follow[producao[i]]:
                                        follow[producao[i]].append(terminal)
                                        changes = True
                                # Se FIRST(next_symbol) contém epsilon, propaga FOLLOW(A) para FOLLOW(B)
                                if "ε" in firsts[next_symbol]:
                                    for terminal in follow[regra]:
                                        if terminal not in follow[producao[i]]:
                                            follow[producao[i]].append(terminal)
                                            changes = True
    
    return follow
             

def tabela_ll1(gramatica):
    firsts = firstFunc(gramatica)
    follows = follow(firsts,gramatica)
    tabela = {}
    
    for regra in gramatica:
        tabela[regra] = {}
    for regra in gramatica:
        tabela[regra] = {}
        for producao in gramatica[regra]:
            if producao[0] == "ε":
                tabela[regra]["$"] = ["ε"]
            else:
                if producao[0] not in gramatica:
                    if producao[0] not in tabela[regra]:
                        tabela[regra][producao[0]] = producao
                else:
                    for terminal in firsts[producao[0]]:
                        if terminal != "ε" and terminal not in tabela[regra]:
                            tabela[regra][terminal] = producao
                if "ε" in firsts[regra]:
                    for terminal in follows[regra]:
                        if terminal not in tabela[regra]:
                            tabela[regra][terminal] = ["ε"]
            
    return tabela

def print_tabela(tabela):
    for simbolo in tabela:
        print(simbolo)
        for terminal in tabela[simbolo]:
            print("\t", terminal, ":", tabela[simbolo][terminal])

# print_tabela(tabela_ll1(test_grammar))
class arvore(object):
    def __init__(self, parent = None, id = None, child =None, data = None, type = any, nivel=0):
        self.parent = parent
        self.child = child
        self.id = id
        self.type = type
        self.data = data
        self.nivel = nivel
    
    def add_child(self,name, data, id):
        if self.child == None:
            self.child = []
        new_child = arvore(data=data, id=name,type = any, parent=self)
        self.child.append(new_child)
        return new_child

    def append_child(self, child):
        if self.child == None:
            self.child = []
        self.child.append(child)

    def simplify(self):
        
        if self.type != any:
            return self
        elif self.child == None:
            return
        elif len(self.child) > 1:
            child_list = []
            for child in self.child:
                temp = child.simplify()
                if temp is not None:
                    child_list.append(temp)
            self.child = child_list
        if len(self.child) == 1:
            if self.child[0] is not None:
                self.child = [self.child[0].simplify()]
                if len(self.child) == 1:
                    if self.child[0] is not None:
                        return self.child[0]
        return self


    def print_tree(self, level=0, is_last=True, indent="  "):

        if self.data is None:
            print("Empty tree")
            return
        qmark = "\u25A1"  # Unicode right angle quotation mark for better visual representation

        # Print the current node with proper indentation
        print(indent * level + ("|- " if level > 0 else "") +
              (qmark if is_last else "|") + str(self.data) +" "+ (("tipo:"+str(self.type)) if self.type != any else "")) 

        # Recursively print child nodes with adjusted indentation
        if self.child:
            i = 0
            while(len(self.child) > i):
                is_last_child = (i == len(self.child) - 1)
                if self.child[i] is not None:
                    self.child[i].print_tree(level + 1, is_last_child, indent)
                i += 1

def parser(tabela,gramatica,entrada):

    semantic_table = semantica.semantic_table("IDS table")
    pendente = []

    producao_inicial= list(gramatica.keys())[0]
    pilha = ["$", producao_inicial]
    entrada.append("$")

    syntatic_tree_pointer : arvore
    child_list = []
    nivel = 0
    entradaPointer = 0
    while True:
        print("\n------------------------------------")
        # tree.print_tree()
        print("Pilha: ",pilha," entrada: ", entrada[entradaPointer])
        topoPilha = pilha[-1]


        #se o topo da pilha for o simbolo de fim da pilha e o simbolo de entrada for o mesmo aceita
        if topoPilha == entrada[entradaPointer][0] == "$":
            for pend in pendente:
                if not semantic_table.search_variable(pend):
                    print("Variável não declarada: ", pend)
                    return
            print("Aceito")
            return syntatic_tree_pointer
        if topoPilha == "#":
            #removendo o marcador "#"
            pilha.pop()

            #removendo o pai da child_list
            childrens_father = pilha.pop()

            novo_no = arvore(id=childrens_father, data=childrens_father,nivel=(nivel-1))
            index = 0
            while(index < len(child_list)):
                child = child_list[index]
                if child.nivel == nivel:
                    novo_no.append_child(child)
                    child_list.pop(index)
                
                else:
                    index += 1
            child_list.append(novo_no)
            syntatic_tree_pointer = novo_no
            nivel -=1
            continue
        #se o topo da pilha for uma produção possivel
        elif topoPilha in gramatica:

            #se houver transicao na tabela utilizando o topo da pilha e o simbolo de entrada então substitui o topo da pilha pela nova produção
            if entrada[entradaPointer][1] in tabela[topoPilha]:
                producao = tabela[topoPilha][entrada[entradaPointer][1]]
                print("Produção: ", producao)
                pilha.append("#")
                nivel += 1

                if producao[0] != "ε":

                    for simbolo in reversed(producao):
                        pilha.append(simbolo)
            
                else:
                    print("Adicao de ε")
            else:
                print("Erro. Não existe regra para", topoPilha, entrada[entradaPointer][1])
                break
        
        #em caso de match
        elif topoPilha == entrada[entradaPointer][1]:
            print('match', ":", entrada[entradaPointer][0])
            nova_child = arvore(id=entrada[entradaPointer][0], data=entrada[entradaPointer][0], type=entrada[entradaPointer][1], nivel=nivel)
            if entrada[entradaPointer][0] == "ComputeFac":
                print(entrada[entradaPointer][1])
            
            #if de analise semantica: checagem da existencia da variavel
            if entrada[entradaPointer][0] == "{":
                semantic_table.novo_escopo()
            elif entrada[entradaPointer][0] == "}":
                semantic_table.fim_escopo()
            elif entrada[entradaPointer][1] == 'id':
                idlist ={'boolean', 'class' , 'String', 'int',}
                search = semantic_table.search_variable(entrada[entradaPointer][0])
                type_position = 0
                if entrada[entradaPointer - 1][0] in idlist:
                    type_position = 1
                if entrada[entradaPointer - 3][0] in idlist:
                    type_position = 3
                if type_position != 0:
                    if entrada[entradaPointer -2][0] == "public":      

                        semantic_table.add_variable(entrada[entradaPointer][0], None, entrada[entradaPointer - type_position][0], True)
                    else:
                        semantic_table.add_variable(entrada[entradaPointer][0], None, entrada[entradaPointer - type_position][0])

                    if(entrada[entradaPointer + 1][0] == "=" and entrada[entradaPointer + 2][1] == "num"):
                        semantic_table.search_variable(entrada[entradaPointer][0],entrada[entradaPointer + 2][0],"num")
                   
                elif (search is not None):
                    if search["valor"] is not None:
                        nova_child.type = search["tipo"]
                        nova_child.data = search["valor"]
                        nova_child.id = search["data"]
                else:
                    pendente.append(entrada[entradaPointer][0])
                    print("Variável ainda não declarada")
                    
            #fim do if de analise semantica
            entradaPointer += 1
            child_list.append(nova_child)
            pilha.pop()
        else:
            print("Erro. ")
            break

Input = scanner.scanner(list("""
class Factorial{
    public static void main(String[] a){

    System.out.println(new Fac().ComputeFac( 10 + 10 ));
}
}
class Fac {
    public int ComputeFac(int num){
        int num_aux; 
        if (num != 1)
        num_aux = 4;
        else
        num_aux = num * (this.ComputeFac(num-2 ));
        return num_aux ;
    }
} $
"""))
# Input = scanner.scanner(list("""  int public alberto $"""))
avr = parser(tabela_ll1(gramatica_minijava),gramatica_minijava,Input)
simple = avr.simplify()
simple
final_tree = semantica.check_constants_operators(simple).print_tree()

# print(tabela_ll1(test_grammar))
# print(follow(firstFunc(gramatica_minijava),gramatica_minijava))
# print(firstFunc(gramatica_minijava))

# Input = scanner.scanner(list("""int public $"""))
# parser(tabela_ll1(test_grammar),test_grammar,Input)


# generator = MIPSGenerator()
# generator.generate_code(final_tree)  # Assuming `root` is the parsed AST root
# print(generator.get_code())
