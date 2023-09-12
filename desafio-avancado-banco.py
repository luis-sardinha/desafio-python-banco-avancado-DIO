from abc import ABC, ABCMeta, abstractclassmethod, abstractproperty
from datetime import datetime


class Cliente:

    def __init__(self, endereco):
        self.endereco = endereco
        self.lista_contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.lista_contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._numero_de_saques = 0
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
        
    @property
    def numero_de_saques(self):
        return self._numero_de_saques
           
    def funcao_saque(self, valor):
        saldo = self.saldo
        
        if valor > saldo:
            print("Saldo insuficiente")
        elif valor == 0 or valor < 0:
            print("Saque nao realizado, valor digitado foi 0 ou insuficiente")
        else:
            self._saldo -= valor
            retornar_menu = input("Saque realizado com sucesso!! Pressione qualque tecla para voltar ao menu")
        return saldo, Historico   

    def funcao_deposito(self, valor):
        if valor == 0:
            print("O Valor do deposito nao pode ser menor que zero")
        else:      
            self._saldo += valor
            print("Deposito realizado com sucesso!!")
            return self.saldo, Historico
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite_saque=500, limite_diario=3):
        super().__init__(numero, cliente)
        self.limite_saque = limite_saque
        self.limite_diario = limite_diario

    def funcao_saque(self, valor):
        numero_de_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        excedeu_numero_saques = numero_de_saques >= self.limite_diario
        excedeu_limite_conta = valor > self.limite_saque
        
        if excedeu_numero_saques:
            print("\nNão foi possivel realizar a operação, limite de numero de saques atingido")
        
        elif excedeu_limite_conta:
            print(f"\nNão foi possivel sacar, valor maximo de saque é de: R$ {float(self.limite_saque)} por saque")
        
        else:
            return super().funcao_saque(valor)
        
        return False
    def __str__(self):
        return f"""\
            Agência: \t{self.agencia}
            C/C:\t {self.numero}
            Titular:\t {self.cliente.nome}"""

class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.funcao_saque(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
        
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.funcao_deposito(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def criar_cliente(lista_clientes):
    cpf = input("Informe o CPF: ")
    cliente = buscar_cliente(cpf, lista_clientes)
    
    if cliente:
        print("Ja existe um cliente com este CPF")
        return
    
    nome = input("Informe o nome completo do cliente: ")
    data_nascimento = input("Informe a data de nascimento: ")
    endereco = input("Informe o endereco:")
    
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    lista_clientes.append(cliente)
    
    print("cliente adicionado com sucesso")

def criar_conta(numero_conta, lista_contas, lista_clientes):
    
    cpf = input("Digite o CPF: ")
    cliente = buscar_cliente(cpf, lista_clientes)
    
    if not cliente:
        print("\nCliente não encontrado")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    lista_contas.append(conta)
    cliente.lista_contas.append(conta)
    
    print("Conta criada com sucesso!")
    
def buscar_cliente(cpf, lista_clientes):
    for cliente in lista_clientes:
        if cliente.cpf == cpf:
            return cliente
        return None
    #cliente_encontrado = [cliente for cliente in lista_clientes if cliente.cpf == cpf]
    #return cliente_encontrado[0] if cliente_encontrado else None

def buscar_conta(lista_clientes):
    if not lista_clientes.lista_contas:
        print("Cliente  nao possui conta")
        return
    return lista_clientes.lista_contas[0]

def funcao_depositar(lista_clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = buscar_cliente(cpf, lista_clientes)
    
    if not cliente:
        print(" Cliente não encontrado")
        return
    
    valor = float(input("Digite o valor do depósito: "))
    transacao = Deposito(valor)
    conta = buscar_conta(cliente)
        
    if not conta:
        print("Conta nao encontrada")
        return
    
    cliente.realizar_transacao(conta, transacao)
        
def funcao_sacar(lista_clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = buscar_cliente(cpf, lista_clientes)
    
    if cliente:
        valor = float(input("Digite o valor do saque: "))
        transacao = Saque(valor)
        conta = buscar_conta(cliente)
        cliente.realizar_transacao(conta, transacao)
    else:
        print("Cliente não encontrado")
    
def funcao_extrato(lista_clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = buscar_cliente(cpf, lista_clientes)
    
    if not cliente:
        print("Cliente não encontrado!!")
        return
    conta = buscar_conta(cliente)
    if not conta:
        return
    
    print("""
        ---------- Extrato ----------""")
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = "Nenhuma transacão foi encontrada"
    else:
        for transacao in transacoes:
            extrato += f"{transacao['tipo']}:R${transacao['valor']:.2f}"
            
    print(extrato)
    print(f"O Saldo da conta é: {conta.saldo:.2f}")
    
    retornar_menu = input("\nTecle enter para retornar ao menu inicial")
    return


    
    cpf = input("Digite o CPF: ")
    for usuario in lista_usuario:
        if usuario['CPF'] == cpf:
            print("\nJa existe um usuario com esse cpf")
            return
    
    nome = input("Digite o nome completo: ")    
    data_nascimento = input("Digite a data de nascimento (DD/MM/AAAA): ")
    logradouro = input("Digite o logradouro: ")
    bairro = input("Digite o bairro: " )
    cidade = input("Digite a: cidade: ")
    estado = input("Digite a sigla do: estado): ")
    endereco_formatado = logradouro + " - " + bairro + " - " + cidade + "/"+ estado
    
    usuario = {
        'nome': nome,
        'Data Nascimento': data_nascimento,
        'CPF': cpf,
        'Endereço': [endereco_formatado] 
        }
    lista_usuario.append(usuario)
    return usuario
    retornar_menu = input("\nCadastro realizado com sucesso! Tecle enter para retornar ao menu inicial")

def listar_contas(lista_contas):
    for conta in lista_contas:
        print((str(conta)))
    
   
def main():
    lista_contas = [] # agencia, numero da conta e usuário. numero sequencial iniciando com 1
    lista_clientes = [] # nome, data de nascimento, cpf e end(str no formato: logradouro - bairro - ceidade/sigla estado) sem duplicidade.

    while True:

        def menu_principal():

            menu = """ 
                Digite a Opção desejada
            ---------------------------------
            [cc] Criar conta
            [c] Criar usuario
            [l] Listar usuarios
            [lc] Listar contas
            [d] Depositar
            [s] Sacar
            [e] Extrato
            [q] Sair
            ---------------------------------
            """
            print(menu)
        menu_principal()
        opcao = input()
        
        if opcao == "cc":
            numero_conta = len(lista_contas) + 1
            criar_conta(numero_conta, lista_contas, lista_clientes)
            
        elif opcao == "c":
           criar_cliente(lista_clientes)
           
        elif opcao == "l":
            
            print("""======= Usuários Cadastrados =======""")
            for novo_usuario in lista_clientes:
                print(f"{novo_usuario}\n")
            
            retornar_menu = input("\nTecle enter para retornar ao menu inicial")

        elif opcao == "lc":
           listar_contas(lista_contas)

        elif opcao == "d":
            funcao_depositar(lista_clientes)
            """ cliente_buscado = buscar_cliente(cpf, lista_clientes)
            if cliente_buscado:
                valor = input(float("\nDigite o valor do depósito: "))
                transacao = Deposito(valor)
            else:
                print("\nCliente não encontrado!")
                return """
                
        elif opcao == "s":

            funcao_sacar(lista_clientes)
            #saldo, saques_realizados = funcao_saque(saldo=saldo, saque=saque, lista_saques=saques_realizados, limite=limite_saque, numero_de_saques=numero_de_saques, limite_diario=LIMITE_SAQUE)
            #numero_de_saques += 1
            
        elif opcao == "e":
            funcao_extrato(lista_clientes)
                  
        elif opcao == "q":

            print("Obrigado por utilizar nossos serviços!\n")
            break 

        else:
            print("Operação incorreta, digite a opcao desejada: ") 
main()