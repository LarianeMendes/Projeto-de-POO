import os
import pandas as pd

class GerenciadorUsuarios:
    def __init__(self, nome_arquivo="usuarios_BliBank.csv"):
        from cliente import Cliente
        from administrador import Administrador
        
        self.Cliente = Cliente
        self.Administrador = Administrador
        self.nome_arquivo = nome_arquivo
        self.usuarios = []
        self.sessao_atual = None
        self.carregar_usuarios()

    def carregar_usuarios(self):
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
        dados_usuarios = []
        for usuario in self.usuarios:
            dados_usuarios.append(usuario.to_dict())
        usuarios_df = pd.DataFrame(dados_usuarios)
        usuarios_df.to_csv(self.nome_arquivo, index=False)

    def verificar_cpf_existente(self, cpf):
        for usuario in self.usuarios:
            if usuario.get_cpf() == cpf:
                return True
        return False

    def verificar_email_existente(self, email):
        for usuario in self.usuarios:
            if usuario.get_email() == email:
                return True
        return False

    def login(self, email, senha):
        for usuario in self.usuarios:
            if usuario.get_email() == email:
                if usuario.get_senha() == senha:
                    self.sessao_atual = usuario
                    return usuario
                else:
                    print("Senha incorreta.")  # Depuração
        print("Usuário não encontrado ou senha incorreta.")  # Depuração
        return None

    def logout(self):
        self.sessao_atual = None

    def cadastrar_usuario(self, nome, sobrenome, email, senha, cpf, tipo):
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
