
# Importar modulo de identacao
from src.cliente import Cliente, PessoaFisica, Conta, ContaCorrente, Historico, Transacao, Saque, Deposito
from models.dominio import DbBanco
from src.validarcpf import filtrarcpf

db = DbBanco()

def filtrar_cliente(cpf):
    cpf = (cpf,)
    clientes_filtrados = db.listarClientes(indice=cpf)
    return clientes_filtrados if clientes_filtrados else None


def recuperar_conta_cliente(id):
    id = (id,)
    contas_filtradas = db.listarContas(indice=id)
    return contas_filtradas if contas_filtradas else None


def depositar(clientes, contas):
    cpf = filtrarcpf(input("Informe o CPF do cliente: "))

    if cpf != clientes[2]:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    saldo(clientes[0], valor)
    transacao.registrar(contas[4])

def sacar(clientes, contas):
    cpf = filtrarcpf(input("Informe o CPF do cliente: "))

    if cpf != clientes[2]:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    saldo(clientes[0], valor)
    transacao.registrar(contas[4])


def exibir_extrato(clientes, contas):

    saldo_db = db.listarSaldo(contas[0])

    if not clientes:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    if not contas:
        return

    print("\n================ EXTRATO ================")
    transacoes = Historico().transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {saldo_db:.2f}")
    print("==========================================")


def criar_cliente(clientes: list):
    cpf = input("Informe o CPF (somente número): ")
    cpf = filtrarcpf(cpf)

    if cpf == False:
        print("Cpf invalido !")
        return

    cliente = filtrar_cliente(cpf)
    if cliente[2] == cpf:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (aaaa-mm-dd): ").strip()
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ").strip()

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    dados_cliente = (nome, cpf, data_nascimento, endereco)
    resultado_db = db.inserirCliente(dados_cliente) # Metodo do db para inserir registros
    
    if resultado_db == False:
        print("Erro ao cadastrar cliente !")
        return

    cliente = filtrar_cliente(cpf)
    clientes.extend([cliente[0], cliente[1], cliente[2], cliente[3], cliente[4]])

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cpf = filtrarcpf(cpf)

    if cpf == False:
        print("Cpf invalido !")
        return
    
    cliente = filtrar_cliente(cpf)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cpf, numero=numero_conta)

    agencia = int(1) # Obter o numero da agencia
    dados = (cliente[0], cliente[2], agencia, numero_conta) # Cliente[0] armazena o id do cliente
    resultado_db = db.inserirConta(dados) # Metodo do db para inserir registros

    if resultado_db == False:
        print("Erro ao cadastrar conta !")
        return
    else:
        saldo(cliente[0])

    contas.extend([cliente[0], agencia, numero_conta, conta])

    print("\n=== Conta criada com sucesso! ===")

def saldo(indice, valor):
    adicionar_saldo = db.inserirSaldo(indice, valor)
    return adicionar_saldo

def login(clientes: list, contas: list):
    cpf = input("Digite seu cpf: ")
    cpf = filtrarcpf(cpf)

    if cpf == False:
        print("Cpf invalido !")
        return

    cliente = filtrar_cliente(cpf)

    if cliente == None:
        print("\n@@@Cliente não possui conta!")
        return

    conta = recuperar_conta_cliente(cliente[0])

    if (conta):
        contas.extend([conta[0], conta[1], conta[2], conta[3]])

    clientes.extend([cliente[0], cliente[1], cliente[2], cliente[3], cliente[4]])
    conta = Conta(conta[3], clientes)
    contas.append([conta])

    print(f"Bem-vindo de volta, {clientes[1]}.")


def excluir_registro(clientes):
    clientes = list(clientes)
    cliente = filtrar_cliente(clientes[0])

    if not clientes:
        print("Cliente não encontrado !")
        return 

    while True:
        opcao = input("Deseja excluir todos os seus dados ? S ou N (S para sim N para nao)").strip()

        if opcao == "S":
            indice = cliente[0]
            db.excluirRegistro(indice)
            if excluir_registro == False:
                print("Erro ao excluir dados !")
                return
            else:
                print("Seus dados foram excluidos com sucesso!")
                return 
            
        elif opcao == "N":
            return

        else:
            print("Opção invalida ")
            continue
        