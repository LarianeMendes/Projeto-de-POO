from interfaceUsuario import Usuario
from gerenciadorusuario import GerenciadorUsuarios
import os
from cliente import Cliente

class Administrador(Usuario):
    def __init__(self, gerenciador: GerenciadorUsuarios, nome: str = None, sobrenome: str = None, email: str = None, senha: str = None, cpf: str = None, nivel_acesso: str = 'admin') -> None:
        self._gerenciador = gerenciador
        super().__init__(nome, sobrenome, email, senha, cpf)
        self.nivel_acesso = nivel_acesso
        self.tipo = "admin"
    
    def to_dict(self) -> dict:
        return {
            'nome': self.get_nome(),
            'sobrenome': self.get_sobrenome(),
            'email': self.get_email(),
            'senha': self.get_senha(),
            'cpf': self.get_cpf(),
            'tipo': 'admin'
        }
    
    def cadastrar(self) -> None:
        print(f"Administrador {self.get_nome()} {self.get_sobrenome()} cadastrado com email {self.get_email()} e nível de acesso {self.nivel_acesso}.")
        
    def aprovar_cartoes(self) -> None:
        pedidos = [cliente for cliente in self._gerenciador.usuarios if isinstance(cliente, Cliente) and cliente.status_cartao == 'pendente']
        if not pedidos:
            print("\nNão há solicitações de cartão pendentes.")
            return
        for i, cliente in enumerate(pedidos, start=1):
            print(f"{i}. {cliente.get_nome()} (Email: {cliente.get_email()})")

        escolha = input("\nEscolha um cliente para aprovar o cartão ou '0' para cancelar: ")
        if escolha.isdigit() and int(escolha) > 0 and int(escolha) <= len(pedidos):
            cliente_selecionado = pedidos[int(escolha) - 1]
            limite_inicial = float(input(f"Digite o limite inicial para o cartão de {cliente_selecionado.get_nome()}: "))
            cliente_selecionado.status_cartao = 'aprovado'
            cliente_selecionado.limite_cartao = limite_inicial
            self._gerenciador.salvar_usuarios()
            print(f"Cartão de crédito aprovado para {cliente_selecionado.get_nome()} com limite de R${limite_inicial:.2f}.")
        else:
            print("Operação cancelada ou entrada inválida.")
           
    def visualizar_informacoes_cliente(self) -> None:
        clientes = [cliente for cliente in self._gerenciador.usuarios if isinstance(cliente, Cliente)]
    
        if not clientes:
            print("Não há clientes cadastrados.")
            return
        
        print("\nLista de clientes:")
        for idx, cliente in enumerate(clientes, start=1):
            print(f"{idx}. Nome: {cliente.get_nome()}, Email: {cliente.get_email()}, Cartão: {cliente.status_cartao}, "
                  f"R${cliente.limite_cartao:.2f}, Aumento de Limite: R${cliente.limite_requerido:.2f}, "
                  f"Encerramento: {'Sim' if cliente.solicitar_encerramento else 'Não'}")
        
        escolha = input("\nEscolha um cliente para visualizar as informações detalhadas ou '0' para cancelar: ").strip()
        
        if escolha.isdigit() and int(escolha) > 0 and int(escolha) <= len(clientes):
            cliente_selecionado = clientes[int(escolha) - 1]
            print(f"\nNome: {cliente_selecionado.get_nome()}")
            print(f"Sobrenome: {cliente_selecionado.get_sobrenome()}")
            print(f"Email: {cliente_selecionado.get_email()}")
            print(f"CPF: {cliente_selecionado.get_cpf()}")
            print(f"Saldo Atual: R${cliente_selecionado.get_saldo():.2f}")
            print(f"Limite Cartão: R${cliente_selecionado.limite_cartao:.2f}")
            print(f"Status Cartão: {cliente_selecionado.status_cartao}")
            print(f"Dívida Cartão: R${cliente_selecionado.divida_cartao:.2f}")
            print(f"Requerimento de Aumento de Limite: R${cliente_selecionado.limite_requerido:.2f}")
            print(f"Solicitação de Encerramento de Conta: {'Sim' if cliente_selecionado.solicitar_encerramento else 'Não'}")
        else:
            print("Operação cancelada ou entrada inválida.")
            
    def encerrar_conta_cliente(self) -> None:
        solicitacoes = [cliente for cliente in self._gerenciador.usuarios if isinstance(cliente, Cliente) and cliente.solicitar_encerramento]
        
        if not solicitacoes:
            print("Não há solicitações de encerramento pendentes.")
            return
        
        print("\nSolicitações de encerramento pendentes:")
        for idx, cliente in enumerate(solicitacoes, start=1):
            print(f"{idx}. {cliente.get_nome()} - Email: {cliente.get_email()}")

        escolha = input("Escolha uma conta para encerrar ou '0' para cancelar: ").strip()
        if escolha.isdigit() and int(escolha) > 0 and int(escolha) <= len(solicitacoes):
            cliente_selecionado = solicitacoes[int(escolha) - 1]
            if cliente_selecionado.get_saldo() == 0 and cliente_selecionado.divida_cartao == 0:
                self._gerenciador.usuarios.remove(cliente_selecionado)
                arquivo_fatura = f"fatura_{cliente_selecionado.get_email().replace('@', '_').replace('.', '_')}.txt"
                try:
                    os.remove(arquivo_fatura)
                except FileNotFoundError:
                    pass
                self._gerenciador.salvar_usuarios()
                print(f"Conta de {cliente_selecionado.get_nome()} encerrada com sucesso.")
            else:
                print("A conta não pode ser encerrada. Verifique se há saldo ou dívidas pendentes.")
        else:
            print("Operação cancelada ou entrada inválida.")
    
    def aprovar_aumento_limite(self) -> None:
        solicitacoes = [cliente for cliente in self._gerenciador.usuarios if isinstance(cliente, Cliente) and cliente.limite_requerido > 0]
        
        if not solicitacoes:
            print("\nNão há solicitações de aumento de limite pendentes.")
            return

        print("\nSolicitações de aumento de limite pendentes:")
        for idx, cliente in enumerate(solicitacoes, start=1):
            print(f"{idx}. {cliente.get_nome()} - Email: {cliente.get_email()}, Solicitação: R${cliente.limite_requerido:.2f}")
        
        escolha = input("Escolha uma solicitação para aprovar ou digite 0 para cancelar: ")
        if escolha.isdigit() and int(escolha) > 0 and int(escolha) <= len(solicitacoes):
            cliente_selecionado = solicitacoes[int(escolha) - 1]
            cliente_selecionado.limite_cartao = cliente_selecionado.limite_requerido
            cliente_selecionado.limite_requerido = 0
            self._gerenciador.salvar_usuarios()
            print(f"Limite de crédito de {cliente_selecionado.get_nome()} aumentado para R${cliente_selecionado.limite_cartao:.2f}.")
            print("Solicitação de aumento de limite aprovada e processada com sucesso.")
        elif escolha == 0:
            print("Operação cancelada.")
        else:
            print("Entrada inválida.")
