import streamlit as st
import streamlit_authenticator as stauth
from dependencies import consulta_nome, consulta_geral, add_registro, cria_tabela
from time import sleep

COOKIE_EXPIRY_DAYS = 30

def main():
    try:
        consulta_geral()
    except:
        cria_tabela()

    db_query = consulta_geral()

    registros = {'usernames': {}}
    for data in db_query:
        registros['usernames'][data[1]] = {'name': data[0], 'password': data[2]}


    authenticator = stauth.Authenticate(
        registros,
        'random_cookie_name',
        'random_signature_key',

        COOKIE_EXPIRY_DAYS,
    )

    if 'clicou_registrar' not in st.session_state:
        st.session_state['clicou_registrar'] = False

    if st.session_state['clicou_registrar'] == False:
        login_form(authenticator=authenticator)
    
    else:
        usuario_form()

def login_form(authenticator):
    name, authentication_status, username = authenticator.login()
    if authentication_status:
        authenticator.logout('Logout', 'main')
        # ---- DEFINIR O PROGRAMA A SER PROTEGIDO A PARTIR DESSE PONTO
        st.title('Area do Dashboard')
        st.write(f'*{name} está logado(a)!')
    elif authentication_status == False:
        st.error('Usuario/senha incorretos.')
    elif authentication_status == None:
        st.warning('Por favor informe um usuário e senha')
        cliclou_em_registrar = st.button('Registrar')
        if cliclou_em_registrar:
            st.session_state['clicou_registrar'] = True
            st.rerun()

def confirm_msg():
    hashed_password = stauth.Hasher([st.session_state.pswrd]).generate()
    if st.session_state.pswrd != st.session_state.confirm_pswrd:
        st.warning('Senhas não conferem')
        sleep(3)
    elif consulta_nome(st.session_state.user):
        st.warning('Nome de usuario ja existe.')
        sleep(3)
    else:
        add_registro(st.session_state.nome, st.session_state.user, hashed_password[0])
        st.success('Registro efetuado')
        sleep(3)

def usuario_form():
    with st.form(key='formulario', clear_on_submit=True):
        nome = st.text_input('Nome', key='nome')
        username = st.text_input('Usuario', key='user')
        password = st.text_input('Senha', key='pswrd', type='password')
        confirm_password = st.text_input('Confirme senha', key='confirm_pswrd', type='password')
        submit = st.form_submit_button(
            'Salvar', on_click=confirm_msg,
        )
    clicou_em_fazer_login = st.button('Fazer Login')
    if clicou_em_fazer_login:
        st.session_state['clicou_registrar'] = False
        st.rerun()

if __name__ == '__main__':
    main()