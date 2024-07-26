import streamlit as st
import pandas as pd
import os

# Função para verificar se o usuário já existe
def verificar_usuario(username):
    if not os.path.exists("usuarios.csv"):
        return False
    usuarios = pd.read_csv("usuarios.csv")
    return username in usuarios['username'].values

# Função para cadastrar novo usuário
def cadastrar_usuario(username, password):
    if not os.path.exists("usuarios.csv"):
        # Criar o arquivo CSV com cabeçalho se não existir
        with open("usuarios.csv", "w") as f:
            f.write("username,password\n")
    # Adicionar novo usuário ao arquivo CSV
    with open("usuarios.csv", "a") as f:
        f.write(f"{username},{password}\n")

# Função para verificar login
def verificar_login(username, password):
    if not os.path.exists("usuarios.csv"):
        return False
    usuarios = pd.read_csv("usuarios.csv")
    for _, row in usuarios.iterrows():
        if row['username'] == username and row['password'] == password:
            return True
    return False

# Função para a página de cadastro
def pagina_cadastro():
    st.title("Cadastro de Usuário")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    cadastro = st.button("Cadastrar")

    if cadastro:
        if verificar_usuario(username):
            st.error("Usuário já existe")
        else:
            cadastrar_usuario(username, password)
            st.success("Usuário cadastrado com sucesso")

# Função para a página de login
def pagina_login():
    st.title("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    login = st.button("Entrar")

    if login:
        if verificar_login(username, password):
            st.session_state['login'] = True
            st.session_state['usuario'] = username
            st.session_state['pagina'] = "Principal"  # Redireciona para a página principal após login
        else:
            st.error("Usuário ou senha incorretos")

# Função para a página após o login
def pagina_principal():
    st.title(f"Bem-vindo, {st.session_state['usuario']}")
    st.write("Esta é a página principal após o login.")
    st.text("Parabéns, você entrou com sucesso!")
    st.image("nj.jpg")
    if st.button("Sair"):
        st.session_state['login'] = False
        st.session_state['usuario'] = None
        st.session_state['pagina'] = "Login"  # Redireciona para a página de login

# Função principal para controlar a navegação entre as páginas
def main():
    # Inicializa o estado da sessão se não estiver definido
    if 'login' not in st.session_state:
        st.session_state['login'] = False
    if 'pagina' not in st.session_state:
        st.session_state['pagina'] = "Login"  # Página inicial

    # Controle de navegação baseado na página atual
    if st.session_state['login']:
        st.sidebar.title("Navegação")
        pagina = st.sidebar.selectbox("Selecione a Página", ["Principal", "Logout"])
        if pagina == "Logout":
            st.session_state['login'] = False
            st.session_state['usuario'] = None
            st.session_state['pagina'] = "Login"
    else:
        pagina = st.sidebar.selectbox("Selecione a Página", ["Cadastro", "Login"])

    if pagina == "Cadastro":
        pagina_cadastro()
    elif pagina == "Login":
        pagina_login()
    elif pagina == "Principal":
        if st.session_state['login']:
            pagina_principal()
        else:
            st.warning("Por favor, faça o login primeiro.")

if __name__ == "__main__":
    if 'login' not in st.session_state:
        st.session_state['login'] = False
    main()
