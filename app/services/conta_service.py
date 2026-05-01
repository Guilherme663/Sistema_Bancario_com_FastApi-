from app.repositories.conta_repo import criar_conta, buscar_conta, atualizar_saldo
from app.repositories.transacoes_repo import registrar_transacao
#aqui ele cria uma conta automaticamente para o cliente, verificando se já existe uma conta para ele, caso exista ele lança uma exceção, caso contrário ele cria a conta normalmente
async def criar_conta_service(cliente_id:int):
    conta = await buscar_conta(cliente_id)
    
    if conta:
        raise Exception("Conta já existe para este cliente.")
    
    await criar_conta(cliente_id)

#aqui ele busca a conta do cliente, para verificar o saldo e aplicar um novo deposito no saldo, caso o valor seja negativo ou zero ele lança uma exceção, caso contrário ele atualiza o saldo normalmente
async def depositar(cliente_id:int, valor:float):
    
    if valor <= 0:
        raise Exception("Valor de depósito deve ser positivo.")
    
    conta = await buscar_conta(cliente_id)
    
    if not conta:
        raise Exception("Conta não encontrada.")
    
    conta_id, _, saldo = conta
    novo_saldo = saldo + valor
    await atualizar_saldo(conta_id, novo_saldo)
    await registrar_transacao(conta_id, "deposito", valor)
    return novo_saldo

#aqui ele busca a conta do cliente, para verificar o saldo e aplicar um novo saque no saldo, caso o valor seja negativo ou zero ele lança uma exceção, caso contrário ele atualiza o saldo normalmente, caso o valor do saque seja maior que o saldo ele lança uma exceção de saldo insuficiente
async def sacar(cliente_id:int, valor:float):
    
    if valor <= 0:
        raise Exception("Valor de saque deve ser positivo.")
    
    conta = await buscar_conta(cliente_id)
    
    if not conta: 
        raise Exception("Conta não encontrada.")
    
    conta_id, _, saldo = conta
    if valor > saldo:
        raise Exception("Saldo insuficiente.")
    
    novo_saldo = saldo - valor
    await registrar_transacao(conta_id, "saque", valor)
    await atualizar_saldo(conta_id, novo_saldo)
    return novo_saldo