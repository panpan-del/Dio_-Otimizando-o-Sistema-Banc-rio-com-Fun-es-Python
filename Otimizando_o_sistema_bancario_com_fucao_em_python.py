import textwrap

def menu():
    menu = """
    [d]\tDepositar  
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tLista conta
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, extrato, valor, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("\nDepósito realizado com sucesso")
    else:
        print("Valor digitado é inválido")
    return saldo, extrato

def sacar(*, saldo, extrato, valor, limite, numero_saques, limite_saques):
    passou_saldo = valor > saldo
    passou_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if passou_saldo:
        print("Operação falhou, saldo insuficiente")
    elif passou_limite:
        print("Operação falhou, valor de saque excede o limite de saques")
    elif excedeu_saques:
        print("Operação falhou, número máximo de saques excedido")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!")
    else:
        print("Operação inválida, valor inválido")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print("\nExtrato")
    print("Sem movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")

def criar_usuarios(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        print("\nJá existe usuário com esse CPF")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("Usuário criado com sucesso")

def filtrar_usuarios(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        print("\nConta criada com sucesso")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\nUsuário não encontrado.")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Digite o valor do depósito: ")) 
            saldo, extrato = depositar(saldo, extrato, valor)

        elif opcao == "s":
            valor = float(input("Digite o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                extrato=extrato,
                valor=valor,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )
            
        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)
        
        elif opcao == "nu":
            criar_usuarios(usuarios)
        
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
                
        elif opcao == "lc":
            listar_contas(contas)
        
        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
main()
