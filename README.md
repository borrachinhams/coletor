# Coletor de Processos Tomcat

Aplicação para buscar em seus servidores tomcat os processos que estão rodando e mostra-lo em apenas uma tela tudo o que esta sendo processado.

# Requerimentos

Funciona nas seguintes versões do Apache Tomcat

Servidor|Versão
-------|-------
Apache-tomcat|6
Apache-tomcat|7
Apache-tomcat|8
Apache-tomcat|9

É necessário que o servidor possua a aplicação **manager**. Esta aplicação vem por padrão no tomcat.

# Modo de Uso

Entre no arquivo *coletor/config.ini* e adicione todos os seus servidores seguindo o seguinte exemplo:

```bash
[servidores]
 10.10.10.10  8080
 10.10.10.11  8080
```

O primeiro será o IP do servidor tomcat e o segundo a porta.

Com os servidores configurados já podemos criar o container.

```bash
docker build -t coletor .
```

Agora basta iniciar o container passando as credêciais para acesso, tanto to *tomcat* quanto para acesso aplicação do *coletor*.

```bash
docker run --rm -d -p 8080:8080 -e LOGIN_USER=admin -e LOGIN_PASS=admin -e TOMCAT_USER=tomcat -e TOMCAT_PASS=tomcat coletor
```

Caso necessário poderá acionar o help

```bash 
docker run --rm -ti coletor --help
```