from interfaceUsuario import Usuario
import datetime
import random
import os

class Cliente(Usuario):
    def __init__(self, gerenciador, nome, sobrenome, email, senha, cpf, saldo=0.0, status_cartao='nenhum', limite_cartao=0.0, divida_cartao=0.0, limite_requerido=0.0, solicitar_encerramento=False):
        '''
        Inicializa um objeto Cliente.

        Parâmetros
        ----------
        gerenciador : GerenciadorUsuarios
            Instância do gerenciador de usuários.
        nome : str
            Nome do cliente.
        sobrenome : str
            Sobrenome do cliente.
        email : str
            Email do cliente.
        senha : str
            Senha do cliente.
        cpf : str
            CPF do cliente.
        saldo : float, opcional
            Saldo inicial do cliente.
        status_cartao : str, opcional
            Status do cartão de crédito do cliente.
        limite_cartao : float, opcional
            Limite do cartão de crédito do cliente.
        divida_cartao : float, opcional
            Dívida atual do cartão de crédito do cliente.
        limite_requerido : float, opcional
            Limite de crédito requerido pelo cliente.
        solicitar_encerramento : bool, opcional
            Indica se o cliente solicitou o encerramento da conta.
        '''
        super().__init__(nome, sobrenome, email, senha, cpf)
        self.__gerenciador = gerenciador
        self.__saldo = saldo
        self.status_cartao = status_cartao
        self.limite_cartao = limite_cartao
        self.divida_cartao = divida_cartao
        self.limite_requerido = limite_requerido
        self.solicitar_encerramento = solicitar_encerramento
        self.cartao_credito = CartaoCredito(self)
        self.gestao_conta = GestaoConta(self)  
        self.investimentos = Investimentos(self)  

    def get_saldo(self) -> float:
        '''
        Retorna o saldo do cliente, arredondando para sempre manter a formatação monetária.

        Retorna
        -------
        float
            Saldo do cliente.
        '''
        return round(self.__saldo,2)

    def set_saldo(self, novo_saldo: float) -> None:
        '''
        Define o saldo do cliente.

        Parâmetros
        ----------
        novo_saldo : float
            Novo saldo do cliente.
        '''
        self.__saldo = novo_saldo

    def get_gerenciador(self):
        '''
        Retorna o gerenciador de usuários.

        Retorna
        -------
        GerenciadorUsuarios
            Instância do gerenciador de usuários.
        '''
        return self.__gerenciador

    def cadastrar(self) -> None:
        '''
        Registra o cliente no sistema.
        '''
        print(f"Cliente {self.get_nome()} {self.get_sobrenome()} cadastrado com email {self.get_email()}.")

    def to_dict(self) -> dict:
        '''
        Converte os dados do cliente para um dicionário.

        Retorna
        -------
        dict
            Dicionário contendo os dados do cliente.
        '''
        return {
            'nome': self.get_nome(),
            'sobrenome': self.get_sobrenome(),
            'email': self.get_email(),
            'senha': self.get_senha(),
            'cpf': self.get_cpf(),
            'tipo': 'cliente',  
            'saldo': f"{self.__saldo:.2f}",
            'status_cartao': self.status_cartao,
            'limite_cartao': f"{self.limite_cartao:.2f}",
            'divida_cartao': f"{self.divida_cartao:.2f}",
            'limite_requerido': f"{self.limite_requerido:.2f}",
            'solicitar_encerramento': self.solicitar_encerramento
        }

class GestaoConta:
    def __init__(self, cliente: Cliente) -> None:
        '''
        Inicializa um objeto GestaoConta.

        Parâmetros
        ----------
        cliente : Cliente
            Instância do cliente.
        '''
        self.cliente = cliente

    def depositar(self, valor: float) -> None:
        '''
        Realiza um depósito na conta do cliente.

        Parâmetros
        ----------
        valor : float
            Valor a ser depositado.
        '''
        if valor > 0:
            novo_saldo = self.cliente.get_saldo() + valor
            self.cliente.set_saldo(novo_saldo)
            print(f"\nDepósito de R${valor:.2f} realizado com sucesso.")
            self.cliente.get_gerenciador().salvar_usuarios() 
        else:
            print("Valor de depósito inválido.")

    def sacar(self, valor: float) -> None:
        '''
        Realiza um saque na conta do cliente.

        Parâmetros
        ----------
        valor : float
            Valor a ser sacado.
        '''
        if valor <= 0:
            print("O valor de saque não pode ser negativo ou zero.")
        elif self.cliente.get_saldo() < valor:
            print("\nSaldo insuficiente.")
        else:
            novo_saldo = self.cliente.get_saldo() - valor
            self.cliente.set_saldo(novo_saldo)
            print(f"Saque de R${valor:.2f} realizado com sucesso. \nSaldo atual: R${self.cliente.get_saldo():.2f}")
            self.cliente.get_gerenciador().salvar_usuarios()

    def transferir(self, valor: float, email_destinatario: str) -> None:
        '''
        Realiza uma transferência para outro cliente.

        Parâmetros
        ----------
        valor : float
            Valor a ser transferido.
        email_destinatario : str
            Email do destinatário da transferência.
        '''
        destinatario = next((usuario for usuario in self.cliente.get_gerenciador().usuarios if usuario.get_email() == email_destinatario), None)
        if isinstance(destinatario, Cliente) and valor > 0 and self.cliente.get_saldo() >= valor:
            novo_saldo_remetente = self.cliente.get_saldo() - valor
            self.cliente.set_saldo(novo_saldo_remetente)
    
            novo_saldo_destinatario = destinatario.get_saldo() + valor
            destinatario.set_saldo(novo_saldo_destinatario)
    
            print(f"Seu saldo atual: R${self.cliente.get_saldo():.2f}")
    
            self.cliente.get_gerenciador().salvar_usuarios()
            destinatario.get_gerenciador().salvar_usuarios()
        else:
            print("Destinatário não é um cliente BliBank.")

    def solicitar_encerramento_conta(self) -> None:
        '''
        Solicita o encerramento da conta do cliente.
        '''
        if self.cliente.solicitar_encerramento:
            print("Uma solicitação de encerramento de conta já foi feita anteriormente.")
            return

        if self.cliente.get_saldo() != 0:
            print("Não é possível encerrar a conta: o saldo deve ser zero.")
            return

        if self.cliente.divida_cartao != 0:
            print("\nNão é possível encerrar a conta: há dívidas pendentes no cartão de crédito.")
            return

        arquivo_fatura = f"fatura_{self.cliente.get_email().replace('@', '_').replace('.', '_')}.txt"
        try:
            with open(arquivo_fatura, 'r') as fatura:
                if fatura.read().strip():
                    print("\nNão é possível encerrar a conta: há faturas em aberto.")
                    return
        except FileNotFoundError:
            pass

        self.cliente.solicitar_encerramento = True
        self.cliente.get_gerenciador().salvar_usuarios()
        print("\nSua solicitação de encerramento de conta foi recebida e será processada em breve.")


class CartaoCredito:
    def __init__(self, cliente: Cliente) -> None:
        '''
        Inicializa um objeto CartaoCredito.

        Parâmetros
        ----------
        cliente : Cliente
            Instância do cliente.
        '''
        self.cliente = cliente

    def solicitar_cartao(self) -> bool:
        '''
        Solicita um cartão de crédito para o cliente.

        Retorna
        -------
        bool
            True se a solicitação foi enviada, False caso contrário.
        '''
        if self.cliente.status_cartao == 'nenhum':
            self.cliente.status_cartao = 'pendente'
            print("Solicitação de cartão de crédito enviada. Aguarde aprovação.")
            self.cliente.get_gerenciador().salvar_usuarios()
            return True
        elif self.cliente.status_cartao == 'pendente':
            print("Já há uma solicitação pendente.")
            return False
        else:
            print("Você já possui um cartão aprovado.")
            return False

    def ver_detalhes_cartao(self) -> None:
        '''
        Exibe os detalhes do cartão de crédito do cliente.
        '''
        if self.cliente.status_cartao == 'aprovado':
            print(f"\nLimite Total: R${self.cliente.limite_cartao:.2f}")
            saldo_disponivel = self.cliente.limite_cartao - self.cliente.divida_cartao
            print(f"Limite Disponível: R${saldo_disponivel:.2f}")
            print(f"Dívida Atual: R${self.cliente.divida_cartao:.2f}")
    
            pasta_faturas = "faturas"
            arquivo_fatura = os.path.join(pasta_faturas, f"fatura_{self.cliente.get_email().replace('@', '_').replace('.', '_')}.txt")
            try:
                with open(arquivo_fatura, 'r') as fatura:
                    compras = fatura.readlines()
                    print("\nItens na Fatura:")
                    for compra in compras:
                        print(compra.strip())
            except FileNotFoundError:
                print("Nenhuma fatura disponível.")
        else:
            print("Você ainda não possui um cartão de crédito aprovado.")

    def registrar_compra(self, valor: float, loja: str, descricao: str) -> None:
        '''
        Registra uma compra no cartão de crédito do cliente.

        Parâmetros
        ----------
        valor : float
            Valor da compra.
        loja : str
            Nome da loja onde a compra foi realizada.
        descricao : str
            Descrição da compra.
        '''
        if self.cliente.status_cartao != 'aprovado':
            print("Você não possui um cartão de crédito aprovado.")
            return

        if not isinstance(valor, (int, float)) or valor <= 0:
            print("Valor inválido. Por favor, insira um valor numérico positivo.")
            return

        if valor > (self.cliente.limite_cartao - self.cliente.divida_cartao):
            print("Limite de crédito insuficiente.")
            return

        self.cliente.divida_cartao += valor

        pasta_faturas = "faturas"
        if not os.path.exists(pasta_faturas):
            os.makedirs(pasta_faturas)

        arquivo_fatura = os.path.join(pasta_faturas, f"fatura_{self.cliente.get_email().replace('@', '_').replace('.', '_')}.txt")
        data_hora_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open(arquivo_fatura, 'a') as fatura:
                fatura.write(f"{data_hora_atual},{loja},{descricao},{valor:.2f}\n")
            print(f"Compra de R${valor:.2f} aprovada na loja {loja} para {descricao}. Data: {data_hora_atual}")
        except IOError as e:
            print(f"Erro ao registrar a compra no arquivo: {e}")

        self.cliente.get_gerenciador().salvar_usuarios()

    def pagar_fatura(self) -> None:
        '''
        Paga a fatura do cartão de crédito do cliente.
        '''
        if self.cliente.status_cartao != 'aprovado':
            print("Você não possui um cartão de crédito aprovado para pagar faturas.")
            return

        pasta_faturas = "faturas"
        arquivo_fatura = os.path.join(pasta_faturas, f"fatura_{self.cliente.get_email().replace('@', '_').replace('.', '_')}.txt")
        try:
            with open(arquivo_fatura, 'r') as fatura:
                compras = fatura.readlines()
            
            total_fatura = sum(float(compra.split(',')[3]) for compra in compras)
            
            if self.cliente.get_saldo() < total_fatura:
                print("Saldo insuficiente para pagar a fatura.")
                print(f"Saldo atual: R${self.cliente.get_saldo():.2f}, Total da fatura: R${total_fatura:.2f}")
                return
            
            print("\nDetalhes da Fatura a ser Paga:")
            for compra in compras:
                data, loja, descricao, valor = compra.split(',')
                print(f"{data} - {descricao} na loja {loja} - R$ {valor.strip()}")
            
            os.remove(arquivo_fatura)
            print(f"\nFatura paga com sucesso. Total pago: R${total_fatura:.2f}. Todos os registros de compra foram limpos.")
            
            novo_saldo = self.cliente.get_saldo() - total_fatura
            self.cliente.set_saldo(novo_saldo)
            self.cliente.divida_cartao = 0.0
            self.cliente.get_gerenciador().salvar_usuarios()

        except FileNotFoundError:
            print("Nenhuma fatura encontrada para ser paga.")
        except Exception as e:
            print(f"Erro ao pagar a fatura: {e}")

    def solicitar_aumento_limite(self, valor: float) -> None:
        '''
        Solicita um aumento de limite do cartão de crédito do cliente.

        Parâmetros
        ----------
        valor : float
            Valor do novo limite solicitado.
        '''
        if self.cliente.status_cartao != 'aprovado':
            print("Você não possui um cartão de crédito aprovado para solicitar um aumento de limite.")
            return

        if valor <= self.cliente.limite_cartao:
            print(f"Solicitação de aumento recusada. O valor solicitado R${valor:.2f} deve ser maior que o limite atual de R${self.cliente.limite_cartao:.2f}.")
            return

        self.cliente.limite_requerido = valor
        self.cliente.get_gerenciador().salvar_usuarios()
        print(f"Solicitação de aumento de limite para R${valor:.2f} enviada. Aguarde aprovação.")

class Investimentos:
    def __init__(self, cliente: Cliente) -> None:
        '''
        Inicializa um objeto Investimentos.

        Parâmetros
        ----------
        cliente : Cliente
            Instância do cliente.
        '''
        self.cliente = cliente

    def investir(self, valor: float, tipo_investimento: str):
        '''
        Realiza um investimento para o cliente.

        Parâmetros
        ----------
        valor : float
            Valor a ser investido.
        tipo_investimento : str
            Tipo de investimento a ser realizado.

        Retorna
        -------
        tuple
            Uma tupla contendo o percentual de rendimento, valor do rendimento e valor final do investimento.
        '''
        rendimentos = {
            'ações': (-30, 30),
            'fiis': (-10, 10),
            'etfs': (-20, 20),
            'cripto': (-100, 500),
            'renda fixa': (5, 10)
        }
        tipo_investimento = tipo_investimento.lower()  
        
        if valor > 0 and valor <= self.cliente.get_saldo():
            if tipo_investimento in rendimentos:
                min_rend, max_rend = rendimentos[tipo_investimento]
                rendimento_percentual = random.uniform(min_rend, max_rend)
                rendimento_valor = valor * (rendimento_percentual / 100)
                valor_final = valor + rendimento_valor

                novo_saldo = self.cliente.get_saldo() - valor + valor_final
                self.cliente.set_saldo(novo_saldo)

                self.cliente.get_gerenciador().salvar_usuarios()
                return rendimento_percentual, rendimento_valor, valor_final
            else:
                raise ValueError("Tipo de investimento inválido.")
        else:
            raise ValueError("Saldo insuficiente.")
