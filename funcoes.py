import subprocess
import win32com.client
import time
import json

config_file = 'config.json'

def carregar_json():
    try:
        with open(config_file, 'r') as file:
            conteudo = file.read().strip()
            if not conteudo:  # Se o arquivo estiver vazio
                raise FileNotFoundError
            return json.loads(conteudo)  # Carrega o JSON do conteúdo
    except (FileNotFoundError, json.JSONDecodeError):
        print('Arquivo JSON não encontrado ou inválido.')
        return {}

def funcao_sap():
    # Abrir o exe do SAP
    subprocess.Popen(r'C:\Program Files (x86)\SAP\NWBC65\NWBC')
    print('\nAbrindo o exe do SAP...\n')

    # Esperar até o SAP GUI estar carregado
    time.sleep(1)

    tentativas = 0
    config = carregar_json()  # Carrega o config ANTES das tentativas

    while tentativas <= 25:
        try:
            SapGuiAuto = win32com.client.GetObject("SAPGUISERVER")
            if not SapGuiAuto:
                tentativas += 1
                print("\nSAP GUI não está disponível...\n")
                time.sleep(2)  # Delay entre tentativas
                continue

            application = SapGuiAuto.GetScriptingEngine
            connection = application.Children(0)
            session = connection.Children(0)

            print('\nSAP GUI carregado com sucesso... Vamos realizar o login.\n')

            # Realizar login
            session.findById("wnd[0]").resizeWorkingPane(235, 50, False)  # Tela cheia
            session.findById("wnd[0]/usr/txtRSYST-MANDT").text = "100"  # Cliente
            session.findById("wnd[0]/usr/txtRSYST-BNAME").text = config.get("login", "")  # Usuário
            session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = config.get("senha", "")  # Senha
            session.findById("wnd[0]/usr/txtRSYST-LANGU").text = "PT"  # Idioma
            session.findById("wnd[0]/usr/txtRSYST-LANGU").setFocus()
            session.findById("wnd[0]/usr/txtRSYST-LANGU").caretPosition = 2
            session.findById("wnd[0]").sendVKey(0)

            try:
                session.findById("wnd[1]/tbar[0]/btn[0]").press()
                print("Elemento opcional encontrado e interagido com sucesso.")
            except:
                print("Elemento opcional não encontrado. Continuando a execução.")

            time.sleep(1)

            # Verificar se o login foi bem-sucedido
            try:
                session.findById("wnd[0]/tbar[1]/btn[34]").setfocus()
                print('Login realizado com sucesso')
                return False, "Login realizado com sucesso."  # Erro=False, mensagem de sucesso
            except:
                print('Falha ao logar. Login e Senha podem estar errados.')
                session.findById("wnd[0]").close()
                return True, """\nFalha ao Logar. 
                Login ou Senha podem estar errados.
                Aperte no ícone de engrenagem para alterar as credenciais.
                Depois aperte o botão novamente."""

        except Exception as e:
            print(f'Erro: {e}\nAguardando o SAP GUI carregar...\n')
            tentativas += 1
            time.sleep(2)  # Delay entre tentativas

    # Caso o loop exceda o limite de tentativas
    return True, "Não foi possível estabelecer conexão com o SAP GUI. Verifique o SAP e tente novamente."



def teste():
    vezes = 0
    while vezes <= 5:
        print(f'opa {vezes}')
        vezes += 1
        time.sleep(1)