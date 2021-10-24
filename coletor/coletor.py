from flask import Flask, render_template, request, Response
from collections import OrderedDict, namedtuple
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup as bs
from functools import wraps
from requests import get
from os import getenv
import argparse

"""
Script para fazer buscas de aplicativos rodando nos 
servidores que possuem apache-tomcat

"""

app = Flask(__name__)

def coletor():
    def requisicao(ip, porta):
        try:
            url = 'http://{}:{}/manager/status'.format(ip, porta)
            req = get(url, auth=HTTPBasicAuth(opcoes.tomcat_user, opcoes.tomcat_pass), timeout=5)
            
            return req.text
        
        except:
            xpto = 'Erro ' + ip
            return xpto


    def coletor(html):
        dados = []
        pag = bs(html, 'html.parser')

        for n in range(7,len(pag.findAll('tr'))):
            dados_bruto = pag.findAll('tr')[n]
            xpto = dados_bruto.findAll('td')

            if len(xpto) > 0:
                dados.append(xpto)

        for i in dados:
            if 'ms' in i[1].text:
                yield i


    read = open(opcoes.config, 'r')
    content = read.readlines()

    # interando no conf para os servidores
    servidores = OrderedDict()
    for i in content[1:]:
        temp = i.split()
        servidores[temp[0]] = temp[1]

    estrutura = namedtuple('Servidor', 'ip, stage, time, sent, recv, client, vhost, request')
    dados = []

    for servidor in servidores:
        # Buscando informacoes no servidor
        html = requisicao(servidor, servidores.get(servidor))

        #Coletado dados com o bs4
        dados_apl = list(coletor(html))

        #Organizando informacoes
        for i in range(len(dados_apl)):
            dados_srv = estrutura(ip=servidor,
                            stage=dados_apl[i][0].text,
                            time=dados_apl[i][1].text,
                            sent=dados_apl[i][2].text,
                            recv=dados_apl[i][3].text,
                            client=dados_apl[i][4].text,
                            vhost=dados_apl[i][5].text,
                            request=dados_apl[i][-1].text)
            dados.append(dados_srv)

    return dados

@app.route('/')
def web():
    #Inciando esquema de autenticacao no pagina
    def check_auth(username, password):
        """Modulo para verificar usuario e senha"""
        return username == opcoes.login_user and password == opcoes.login_pass

    def authenticate():
        """Sends a 401 response that enables basic auth"""
        return Response(
        'Desculpe, nao pude verificar suas credenciais.\n'
        'Favor entrar com as credenciais corretas!', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password):
                return authenticate()
            return f(*args, **kwargs)
        return decorated


    @requires_auth
    def home():
        ips = []
        
        read = open(opcoes.config, 'r')
        content = read.readlines()
        for i in content[1:]:
            ips.append(i.split()[0])


        return render_template("index.html", dados=coletor(), ips=ips)
    
    return home()


parser = argparse.ArgumentParser(description='Coletor de Processos Tomcat')
parser.add_argument('--config', type=str, help='Localização de conf dos servidores', default='config.ini')
parser.add_argument('--login_user', type=str, help='Usuario para logar na aplicação', default=getenv("LOGIN_USER"))
parser.add_argument('--login_pass', type=str, help='Senha para logar na aplicação', default=getenv("LOGIN_PASS"))
parser.add_argument('--tomcat_user', type=str, help='Usuario para logar no manager do tomcat', default=getenv("TOMCAT_USER"))
parser.add_argument('--tomcat_pass', type=str, help='Senha para logar no manager do tomcat', default=getenv("TOMCAT_PASS"))
opcoes = parser.parse_args()

app.run(host='0.0.0.0',port=8080,debug=True)
