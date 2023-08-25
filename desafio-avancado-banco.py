from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Cliente:

    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

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
        #self._historico = Historico()
    
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
        #return self._historico
        pass
    
    def sacar(self, valor):
        pass
        

def funcao_deposito(saldo, valor, lista_depositos):
    if valor == 0:
        print("O Valor do deposito nao pode ser menor que zero")
    else:      
        saldo += valor
        lista_depositos += f"\nR$ {valor:.2f}"
        retornar_menu = input("Deposito realizado com sucesso!!, pressione qualquer tecla para voltar ao menu")
        return saldo, lista_depositos
    
def funcao_saque(*, saldo, saque, lista_saques, limite, numero_de_saques, limite_diario ):
    
    excedeu_numero_saques = numero_de_saques >= limite_diario
    
    if saque > saldo:
        print("Saldo insuficiente")
    elif saque == 0 or saque < 0:
        print("Saque nao realizado, valor digitado foi 0 ou insuficiente")
    elif excedeu_numero_saques:
        print("Não foi possivel realizar a operação, limite de numero de saques atingido")
    elif saque > limite:
        print(f"Não foi possivel sacar, valor maximo de saque é de: R$ {float(limite)} por saque")
    else:
        saldo -= saque
        lista_saques += f"\nR$ {saque:.2f}"
        numero_de_saques += 1
        retornar_menu = input("Saque realizado com sucesso!! Pressione qualque tecla para voltar ao menu")
    return saldo, lista_saques

def funcao_extrato(saldo, lista_depositos, lista_saques):
    print("""
        ---------- Extrato ----------""")
    print("Depositos realizados: ", (lista_depositos))
    print("Saques realizados: ", (lista_saques))
    print("O Saldo da conta é:", (saldo))
    
    retornar_menu = input("\nTecle enter para retornar ao menu inicial")
    return saldo, lista_depositos, lista_saques

def criar_usuario(lista_usuario):
    
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

def criar_conta(agencia, conta, lista_usuario):
    
    cpf = input("Digite o CPF: ")
    for usuario in lista_usuario:
        if usuario['CPF'] == cpf:
            print("\nA Conta foi criada com sucesso!")
            return {"agencia": agencia, "numero_conta": conta, "usuario": usuario}
        else:
            print("Usuário não encontrado")
   
def main():
    lista_contas = [] # agencia, numero da conta e usuário. numero sequencial iniciando com 1
    lista_usuario = [] # nome, data de nascimento, cpf e end(str no formato: logradouro - bairro - ceidade/sigla estado) sem duplicidade.
    AGENCIA = "0001"
    proxima_conta = 1
    conta = 0
    
    saldo = 0
    depositos_realizados = ""
    saques_realizados = ""
    numero_de_saques = 0
    limite_saque = 500
    LIMITE_SAQUE = 3

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
            conta += 1
            nova_conta = criar_conta(AGENCIA, conta, lista_usuario)
            lista_contas.append(nova_conta)
            
        elif opcao == "c":
           criar_usuario(lista_usuario)
           
        elif opcao == "l":
            
            print("""======= Usuários Cadastrados =======""")
            for novo_usuario in lista_usuario:
                print(f"{novo_usuario}\n")
            
            retornar_menu = input("\nTecle enter para retornar ao menu inicial")

        elif opcao == "lc":
            print("""======= Contas Cadastradas =======""")
            for nova_conta in lista_contas:
                print(f"{nova_conta}\n")
            
            retornar_menu = input("\nTecle enter para retornar ao menu inicial")

        elif opcao == "d":
            deposito = float(input("Opcao depósito selecionada, quanto deseja depositar na conta?: "))
            saldo, depositos_realizados = funcao_deposito(saldo, deposito, depositos_realizados)
        
        elif opcao == "s":

            saque = float(input("Digite quanto deseja sacar: ?\n"))
            saldo, saques_realizados = funcao_saque(saldo=saldo, saque=saque, lista_saques=saques_realizados, limite=limite_saque, numero_de_saques=numero_de_saques, limite_diario=LIMITE_SAQUE)
            numero_de_saques += 1
            
        elif opcao == "e":
            saldo, depositos_realizados, saques_realizados = funcao_extrato(saldo, lista_depositos=depositos_realizados, lista_saques=saques_realizados)
                  
        elif opcao == "q":

            print("Obrigado por utilizar nossos serviços!\n")
            break 

        else:
            print("Operação incorreta, digite a opcao desejada: ") 
main()