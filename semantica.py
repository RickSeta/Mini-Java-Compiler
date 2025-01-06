
class semantic_table:
    def __init__(self, name):
        self.name = name
        self.tables_list = [{}]
    
    def add_variable(self, data, valor, tipo):
        found = self.search_variable(data, valor)
        if not found:
            self.tables_list[-1][data] = {"data" : data, "valor" : valor, "tipo" : tipo}
    
    def search_variable(self, data, valor = None, tipo = None):
        for table in self.tables_list:
            if data in table:
                # print("data: ", data, " achado em: ", table, " valor: ", table[data]["valor"])
                if valor:
                    table[data]["valor"] = valor
                if tipo:
                    table[data]["tipo"] = tipo
                return table[data]
            
        print("data: ", data, " não encontrado")
        return None
    
    def novo_escopo(self):
        self.tables_list.append({})
    
    def fim_escopo(self):
        self.tables_list.pop()
    
    def semantic_check(token, next_token, dnext_token):
        print()
    
def check_constants_operators(arvore):
    
    pai = arvore
    if not pai.child:
        return arvore
    
    filho_index = 0
    resultado = 0
    while filho_index < len(pai.child):
        filho = pai.child[filho_index]
        if filho.type == "num" and filho_index == 0:
            temp = pai.child[filho_index + 1]
            if temp.child[0]:
                if temp.child[0].data in {"+", "-", "*"}:
                    if temp.child[0].data == "+":
                        resultado = int(filho.data) + int(temp.child[1].data)
                    elif temp.child[0].data == "-":
                        resultado = int(filho.data) - (temp.child[1].data)
                    elif temp.child[0].data == "*":
                        resultado = int(filho.data) * (temp.child[1].data)
                    pai.child = []
                    pai.type = "num"
                    pai.data = resultado
        if pai.child:
            pai.child[filho_index] = check_constants_operators(filho) # type: ignore
        filho_index += 1
    return pai


# tabela = semantic_table("Tabela de Teste")

# # Adiciona variáveis no escopo global
# tabela.add_variable("x", 10, "int")
# tabela.add_variable("y", 20, "int")

# # Busca variáveis no escopo global
# tabela.search_variable("x") # Saída: 10
# tabela.search_variable("y")  # Saída: 20
# tabela.search_variable("z")  # Saída: None

# # Cria um novo escopo
# tabela.novo_escopo()

# # Adiciona variáveis no novo escopo
# tabela.add_variable("x", 30, "int")
# tabela.add_variable("z", 40, "int")

# # Busca variáveis no novo escopo
# print(tabela.search_variable("x"))  # Saída: 30
# print(tabela.search_variable("z"))  # Saída: 40

# # Retorna ao escopo anterior
# tabela.fim_escopo()

# # Busca variáveis no escopo global novamente
# print(tabela.search_variable("x"))  # Saída: 10
# print(tabela.search_variable("z"))  # Saída: None