from ldap3 import SUBTREE, Server, Connection, SIMPLE, SYNC, ALL
from decouple import config

LDAP_SERVER = config('LDAP_SERVER')
LDAP_SEARCH_BASE = config('LDAP_SEARCH_BASE')  # Base de pesquisa LDAP exemplo 'dc=dominio,dc=com,dc=br'

user_ad = config('USER_AD') # Pega informações de usuário de serviço
user_password = config('USER_AD_PASSWORD') # Pega a senha do usuário de serviço

# Configure o servidor LDAP
server = Server(LDAP_SERVER, get_info=ALL)



def search_email(email):    
    try:
        print(f'Email passado: {email}')
        # Cria conexão com LDAP
        conn = Connection(server, user=user_ad, password=user_password, auto_bind=True, authentication=SIMPLE, client_strategy=SYNC, read_only=True)
        # Filtro de pesquisa baseado no atributo "UserPrincipalName" que representa o e-mail
        search_filter = f'(&(objectClass=person)(UserPrincipalName={email}))'
        conn.search(LDAP_SEARCH_BASE, search_filter, attributes=['sn', 'UserPrincipalName', 'samAccountName'])
        if conn.entries:
            print(f'\nConexão bem-sucedida!')
            samAccountName = conn.entries[0].samAccountName
            conn.unbind()
            return samAccountName
        else:
            conn.unbind()
            return ''
    except ValueError as error:
        print(error)
        return ''

def authenticate_ldap(username, password):
    try:
        user = search_email(username)
        print(f'\n\nUsuário recebido do filtro: {user}')
        if user != '':
            # Cria conexão com LDAP
            conn = Connection(server, user=f'aviva\\{user}', password=password, authentication=SIMPLE, client_strategy=SYNC, read_only=True)
            if conn.bind():
                # Autenticação bem-sucedida
                print("\n\nAutenticação bem-sucedida")
                conn.unbind()
                return True
            else:
                # Autenticação falhou
                print("\n\nFalha na autenticação")
                return False
        else:
            print('Usuário inválido')
    except ValueError as error:
        print(error)