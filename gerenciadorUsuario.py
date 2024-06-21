import os
import pandas as pd

class GerenciadorUsuarios:
    def __init__(self, nome_arquivo="usuarios_BliBank.csv"):
        '''
        Inicializa o GerenciadorUsuarios carregando os usuários do arquivo CSV especificado.

        Parâmetros
        ----------
        nome_arquivo : str, opcional
            Nome do arquivo CSV contendo os dados dos usuários.
        '''
        from cliente import Cliente
        from administrador import Administrador
        
        self.Cliente = Cliente
        self.Administrador = Administrador
        self.nome_arquivo = nome_arquivo
        self.usuarios = []
        self.sessao_atual = None
        self.carregar_usuarios()

    def carregar_usuarios(self):
        '''
        Carrega os usuários a partir de um arquivo CSV e os adiciona à lista de usuários.
        '''
        from cliente import Cliente
        from administrador import Administrador
        if os.path.exists(self.nome_arquivo):
            try:
                usuarios_df = pd.read_csv(self.nome_arquivo, dtype={'senha': str}).fillna('')

                for _, row in usuarios_df.iterrows():
                    try:
                        nome = str(row['nome']).strip()
                        sobrenome = str(row['sobrenome']).strip()
                        email = str(row['email']).strip().lower()
                        senha = str(row['senha']).strip()
                        cpf = str(row['cpf']).strip()
                        tipo = str(row['tipo']).strip().lower()

                        if tipo == 'cliente':
                            cliente = Cliente(
                                self, nome=nome, sobrenome=sobrenome, email=email, senha=senha, cpf=cpf,
                                saldo=float(row['saldo']), status_cartao=row['status_cartao'],
                                limite_cartao=float(row['limite_cartao']), divida_cartao=float(row['divida_cartao']),
                                limite_requerido=float(row.get('limite_requerido', 0.0)), solicitar_encerramento=row.get('solicitar_encerramento', False)
                            )
                            self.usuarios.append(cliente)
                        elif tipo == 'admin':
                            admin = Administrador(
                                self, nome=nome, sobrenome=sobrenome, email=email, senha=senha, cpf=cpf
                            )
                            self.usuarios.append(admin)
                        else:
                            print(f"Tipo de usuário desconhecido ou faltando: {tipo}")  
                    except KeyError as e:
                        print(f"Erro ao carregar usuário: coluna {e} faltando")
                    except Exception as e:
                        print(f"Erro ao carregar usuário: {e}")
            except Exception as e:
                print(f"Erro ao ler o arquivo CSV: {e}")

    def salvar_usuarios(self):
        '''
        Salva a lista de usuários no arquivo CSV especificado.
        '''
        dados_usuarios = []
        for usuario in self.usuarios:
            dados_usuarios.append(usuario.to_dict())
        usuarios_df = pd.DataFrame(dados_usuarios)
        usuarios_df.to_csv(self.nome_arquivo, index=False)

    def verificar_cpf_existente(self, cpf):
        '''
        Verifica se um CPF já está cadastrado no sistema.

        Parâmetros
        ----------
        cpf : str
            CPF a ser verificado.

        Retorna
        -------
        bool
            True se o CPF já existir, False caso contrário.
        '''
        for usuario in self.usuarios:
            if usuario.get_cpf() == cpf:
                return True
        return False

    def verificar_email_existente(self, email):
        '''
        Verifica se um email já está cadastrado no sistema.

        Parâmetros
        ----------
        email : str
            Email a ser verificado.

        Retorna
        -------
        bool
            True se o email já existir, False caso contrário.
        '''
        for usuario in self.usuarios:
            if usuario.get_email() == email:
                return True
        return False

    def login(self, email, senha):
        '''
        Realiza o login de um usuário no sistema.

        Parâmetros
        ----------
        email : str
            Email do usuário.
        senha : str
            Senha do usuário.

        Retorna
        -------
        Cliente ou Administrador
            O usuário logado, ou None se o login falhar.
        '''
        for usuario in self.usuarios:
            if usuario.get_email() == email:
                if usuario.get_senha() == senha:
                    self.sessao_atual = usuario
                    return usuario
                else:
                    print("Senha incorreta.")
        print("Usuário não encontrado ou senha incorreta.")
        return None

    def logout(self):
        '''
        Realiza o logout do usuário atual.
        '''
        self.sessao_atual = None

    def cadastrar_usuario(self, nome, sobrenome, email, senha, cpf, tipo):
        '''
        Cadastra um novo usuário no sistema.

        Parâmetros
        ----------
        nome : str
            Nome do usuário.
        sobrenome : str
            Sobrenome do usuário.
        email : str
            Email do usuário.
        senha : str
            Senha do usuário.
        cpf : str
            CPF do usuário.
        tipo : str
            Tipo do usuário ('cliente' ou 'administrador').

        Retorna
        -------
        None
        '''
        from cliente import Cliente
        from administrador import Administrador
        tipo = tipo.lower()  
        if tipo == 'cliente':
            novo_usuario = Cliente(self, nome=nome, sobrenome=sobrenome, email=email, senha=senha, cpf=cpf)
        elif tipo == 'administrador':
            novo_usuario = Administrador(self, nome=nome, sobrenome=sobrenome, email=email, senha=senha, cpf=cpf)
        else:
            raise ValueError("Tipo de usuário inválido")
        
        self.usuarios.append(novo_usuario)
        self.salvar_usuarios()
