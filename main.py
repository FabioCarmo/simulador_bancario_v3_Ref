
from time import sleep

# importar modulos do projeto
from views.opcoes import depositar, sacar, exibir_extrato,  filtrar_cliente, criar_cliente, criar_conta, \
login, recuperar_conta_cliente, excluir_registro
from views.menu import menu

# Funcao principal do sistema
def main():
    clientes = []
    contas = []

    while True:
        opcao = menu(clientes, contas)

        if not clientes:
            if opcao == '1':
                criar_cliente(clientes)
                sleep(1)
            elif opcao == '2':
                login(clientes, contas)
                sleep(1)
            elif opcao == '0':
                print('Encerrando...')
                sleep(2)
                break
            else:
                print('Operação Invalida. Tente Novamente!')
                sleep(1)
                continue
        
        else:
            if opcao == '1':
                depositar(clientes, contas)
                sleep(1)
            elif opcao == '2':
                sacar(clientes, contas)
                sleep(1)
            elif opcao == '3':
                exibir_extrato(clientes, contas)
                sleep(1)
            elif opcao == '4':
                numero_conta = len(contas) + 1
                numero_conta = int(numero_conta)
                criar_conta(numero_conta, clientes, contas)
            elif opcao == '9':
                excluir_registro(clientes)
                sleep(3)
            elif opcao == '0':
                print('Encerrando...')
                sleep(2)
                break
            else:
                print('Operação Invalida. Tente nonvamente!')
                sleep(1)
                continue

# Iniciar funcao main
if __name__ ==  "__main__":
    main()