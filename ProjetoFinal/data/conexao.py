import xml.etree.ElementTree as ET
import mysql.connector as mycon

database = 'db_bancoTeste'
pathXml = 'data/xml/'


def conectarMSQL():
    try:
        conexao = mycon.connect(
            host="localhost",
            port=3306,
            user="root",
            passwd="root"
        )
    except mycon.Error as erro:
        print(f"\nERRO: {erro}")
    return conexao


def criarBanco():
    conexao = conectarMSQL()
    cursor = conexao.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    conexao.close()
    print("Banco criado com sucesso.")


def verificarBD():
    conexao = conectarMSQL()
    cursor = conexao.cursor()
    sqlShow = (f"SHOW DATABASES LIKE '{database}'")
    cursor.execute(sqlShow)
    basedados = cursor.fetchall()
    conexao.close()
    if basedados == []:
        criarBanco()
    return True


def conectarBD():
    if verificarBD():
        try:
            banco = mycon.connect(
                host="localhost",
                port=3306,
                user="root",
                passwd="root",
                database=database
            )
        except mycon.Error as erro:
            print(f"\nERRO: {erro}")
        return banco


def criarTabelas():
    banco = conectarBD()
    cursor = banco.cursor()
    comandoCreate = """
CREATE TABLE IF NOT EXISTS utilizador (
        id INT NOT NULL AUTO_INCREMENT,
        nome VARCHAR(20) NOT NULL,
        senha VARCHAR(256) NOT NULL,
        cargo VARCHAR(20) NOT NULL,
        PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS banco (
        id INT NOT NULL AUTO_INCREMENT,
        codigo VARCHAR(4) NOT NULL,
        nome VARCHAR(20) NOT NULL,
        PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS agencia (
        id INT NOT NULL AUTO_INCREMENT,
        numero VARCHAR(4) NOT NULL,
        cod_banco VARCHAR(4) NOT NULL,
        morada VARCHAR(20) NOT NULL,
        PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS cliente (
        id INT NOT NULL AUTO_INCREMENT,
        nif VARCHAR(9) NOT NULL,
        nome VARCHAR(150) NOT NULL,
        morada VARCHAR(300) NOT NULL,
        contato VARCHAR(15) NOT NULL,
        categoria VARCHAR(10) NOT NULL,
        PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS conta (
        id INT NOT NULL AUTO_INCREMENT,
        numero VARCHAR(11) NOT NULL,
        tipo VARCHAR(20) NOT NULL,
        nif VARCHAR(9) NOT NULL,
        cod_banco VARCHAR(4) NOT NULL,
        num_agencia VARCHAR(4) NOT NULL,
        nib VARCHAR(21) NOT NULL,
        iban VARCHAR(25) NOT NULL,
        saldo FLOAT NOT NULL,
        data_abertura DATE NOT NULL,
        PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS tipoConta (
        id INT NOT NULL AUTO_INCREMENT,
        tipo VARCHAR(20) NOT NULL,
        PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS transacao (
        id INT NOT NULL AUTO_INCREMENT,
        num_conta VARCHAR(11) NOT NULL,
        descricao VARCHAR(20) NOT NULL,
        valor FLOAT NOT NULL,
        data DATE NOT NULL,
        PRIMARY KEY (id)
);
    """
    cursor.execute(comandoCreate)
    banco.close()


def verificarTabela(tabela):
    banco = conectarBD()
    cursor = banco.cursor()
    sqlShow = (f"SHOW TABLES LIKE '{tabela}'")
    cursor.execute(sqlShow)
    tabelas = cursor.fetchall()
    banco.close()
    if tabelas == []:
        criarTabelas()
    return True


def inserirDadosXmlTabela(tabela, campos):
    banco = conectarBD()
    cursor = banco.cursor()
    treeXml = ET.parse(f'{pathXml}{tabela}s.xml')
    xml = treeXml.findall(f'{tabela}')
    tcampos = '('
    tvalores = '('
    for i, v in enumerate(xml, start=1):
        for campo in campos:
            valor = v.find(f'{campo}').text
            tcampos += f'{campo}, '
            tvalores += f'"{valor}", '
        tcIndice = tcampos.rfind(',')
        tcampos = f'{tcampos[:tcIndice]})'
        tvIndice = tvalores.rfind(',')
        tvalores = f'{tvalores[:tvIndice]})'
        sql = f'INSERT INTO {tabela}{tcampos} VALUES {tvalores}'
        cursor.execute(sql)
        banco.commit()
        tcampos = '('
        tvalores = '('
        print(f"{i}º {tabela} inserido(a) com sucesso.")


def inserirCampoXmlTabela(tabela, campo):
    banco = conectarBD()
    cursor = banco.cursor()
    treeXml = ET.parse(f'{pathXml}{tabela}s.xml')
    xml = treeXml.findall(f'{tabela}')
    for i, v in enumerate(xml, start=1):
        valor = v.find(f'{campo}').text
        sql = f'INSERT INTO {tabela}({campo}) VALUES ("{valor}")'
        cursor.execute(sql)
        banco.commit()
        print(f"{tabela} inserido(a) com sucesso.")


def verificarDadosTabela(tabela):
    if verificarTabela(tabela):
        banco = conectarBD()
        cursor = banco.cursor()
        sqlSelect = (f"SELECT * FROM {tabela}")
        cursor.execute(sqlSelect)
        dados = cursor.fetchall()
        banco.close()
        if dados == []:
            if tabela == 'utilizador':
                campos = ['nome', 'senha', 'cargo']
                inserirDadosXmlTabela(tabela, campos)
            elif tabela == 'banco':
                campos = ['codigo', 'nome']
                inserirDadosXmlTabela(tabela, campos)
            elif tabela == 'agencia':
                campos = ['numero', 'cod_banco', 'morada']
                inserirDadosXmlTabela(tabela, campos)
            elif tabela == 'cliente':
                campos = ['nif', 'nome', 'morada', 'contato', 'categoria']
                inserirDadosXmlTabela(tabela, campos)
            elif tabela == 'tipoConta':
                inserirCampoXmlTabela(tabela, 'tipo')
            else:
                return False
        return True


def verificarId(tabela, id, numero):
    if verificarDadosTabela(tabela):
        banco = conectarBD()
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM {tabela} WHERE {id}='{numero}'")
        dados = cursor.fetchall()
        banco.close()
        if dados == []:
            return False
        else:
            return True
    return False


def adicionarDadosTabela(tabela, campos, valores, id, numero):
    banco = conectarBD()
    cursor = banco.cursor()
    tcampos = '('
    tvalores = '('
    for campo, valor in zip(campos, valores):
        tcampos += f'{campo}, '
        tvalores += f'"{valor}", '
    tcIndice = tcampos.rfind(',')
    tcampos = f'{tcampos[:tcIndice]})'
    tvIndice = tvalores.rfind(',')
    tvalores = f'{tvalores[:tvIndice]})'
    comandoInsert = f'INSERT INTO {tabela}{tcampos} VALUES {tvalores}'
    cursor.execute(comandoInsert)
    banco.commit()
    tcampos = '('
    tvalores = '('
    print(f"{tabela} inserido(a) com sucesso.")


def inserirDadosTabela(tabela, campos, valores, id, numero):
    if not verificarId(tabela, id, numero):
        banco = conectarBD()
        cursor = banco.cursor()
        tcampos = '('
        tvalores = '('
        for campo, valor in zip(campos, valores):
            tcampos += f'{campo}, '
            tvalores += f'"{valor}", '
        tcIndice = tcampos.rfind(',')
        tcampos = f'{tcampos[:tcIndice]})'
        tvIndice = tvalores.rfind(',')
        tvalores = f'{tvalores[:tvIndice]})'
        comandoInsert = f'INSERT INTO {tabela}{tcampos} VALUES {tvalores}'
        cursor.execute(comandoInsert)
        banco.commit()
        tcampos = '('
        tvalores = '('
        print(f"{tabela} inserido(a) com sucesso.")
    else:
        return False


def inserirCampoTabela(tabela, campo, valor):
    if not verificarId(tabela, campo, valor):
        banco = conectarBD()
        cursor = banco.cursor()
        comandoInsert = f"INSERT INTO {tabela}({campo}) VALUES ('{valor}')"
        cursor.execute(comandoInsert)
        banco.commit()
        banco.close()
        print(f"{campo} inserido(a) com sucesso.")
    else:
        return False


def selecionarDadosTabela(tabela, id=None, numero=None, exceto=None):
    if verificarDadosTabela(tabela):
        lista = []
        banco = conectarBD()
        cursor = banco.cursor()
        if numero != None:
            sqlSelect = (f"SELECT * FROM {tabela} WHERE {id} = '{numero}'")
        elif exceto != None:
            sqlSelect = (f"SELECT * FROM {tabela} WHERE {id} != '{exceto}'")
        else:
            sqlSelect = (f"SELECT * FROM {tabela}")
        cursor.execute(sqlSelect)
        dados = cursor.fetchall()
        for dado in dados:
            lista.append(dado)
        return lista
        banco.close()
    else:
        print(f"\033[91mTabela {tabela} está vazia.\033[m")
        return False


def selecionarCampoTabela(tabela, campo=None, id=None, numero=None, exceto=None):
    if verificarDadosTabela(tabela):
        lista = []
        banco = conectarBD()
        cursor = banco.cursor()
        if numero != None:
            sqlSelect = (
                f"SELECT {campo} FROM {tabela} WHERE {id} = '{numero}'")
        elif exceto != None:
            sqlSelect = (
                f"SELECT {campo} FROM {tabela} WHERE {id} != '{exceto}'")
        else:
            sqlSelect = (f"SELECT {campo} FROM {tabela}")
        cursor.execute(sqlSelect)
        dados = cursor.fetchall()
        banco.close()
        for dado in dados:
            lista.append(dado)
        return lista
    else:
        print(f"\033[91mTabela {tabela} está vazia.\033[m")
        return False


def atualizarDadosTabela(tabela, id, numero, campos, valores):
    valida = False
    dados = selecionarDadosTabela(tabela, id, numero)
    for campo, valor in zip(campos, valores):
        if dados:
            op = atualizarCampoTabela(tabela, campo, valor, id, numero)
            if op:
                valida = True
            else:
                valida = False
        else:
            print(f"\033[91mTabela {tabela} não possui {id} {numero}.\033[m")
            return False
    return valida


def atualizarCampoTabela(tabela, campo, valor, id, numero):
    dados = selecionarCampoTabela(tabela, campo, id, numero)
    if dados:
        banco = conectarBD()
        cursor = banco.cursor()
        comandoUpdate = f"UPDATE {tabela} SET {campo}='{valor}' WHERE {id}='{numero}'"
        cursor.execute(comandoUpdate)
        banco.commit()
        banco.close()
        return True
    else:
        print(f"\033[91mTabela {tabela} não possui {id} {numero}.\033[m")
        return False


def excluirDadosTabela(tabela, id=None, numero=None):
    dados = selecionarDadosTabela(tabela, id, numero)
    if dados != []:
        banco = conectarBD()
        cursor = banco.cursor()
        if numero != None:
            sqlDelete = (f"DELETE FROM {tabela} WHERE {id}='{numero}'")
        else:
            sqlDelete = (f"DELETE FROM {tabela}")
        cursor.execute(sqlDelete)
        banco.commit()
        print(f"\033[93mDados apagados com sucesso.\033[m")
        banco.close()
        return True
    else:
        print(f"\033[91mTabela {tabela} não possui {id} {numero}.\033[m")
        return False
