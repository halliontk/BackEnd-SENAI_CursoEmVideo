from dic import especialidades
from nav_padrao import limpar_tela, delay, converter_data, converter_data_banco
from tabulate import tabulate
from IPython.core.display_functions import display


def cadastrar_medico(conexao, cursor):
    print("-=-= CADASTRO DE MÉDICOS =-=-")

    crm = input("CRM: ")

    sql = "SELECT ID FROM MEDICO WHERE CRM = %s"
    cursor.execute(sql, (crm,))
    resultado = cursor.fetchall()

    if len(resultado) != 0:
        print("CRM já cadastrado em outro médico!")
        delay()

    else:
        rg = input("RG: ")

        sql = "SELECT ID FROM MEDICO WHERE RG = %s"
        cursor.execute(sql, (rg,))
        resultado = cursor.fetchall()

        if len(resultado) != 0:
            print("RG já cadastrado em outro médico!")
            delay()

        else:

            cpf = input("CPF: ")

            sql = "SELECT ID FROM MEDICO WHERE CPF = %s"
            cursor.execute(sql, (cpf,))
            resultado = cursor.fetchall()

            if len(resultado) != 0:
                print("CPF já cadastrado em outro médico!")
                delay()

            else:

                nome = input("Nome: ")
                email = input("E-mail: ")
                endereco = input("Endereço: ")
                cep = input("CEP: ")

                while True:
                    print("\nEspecialidade Médica: ")
                    for chave, valor in especialidades.items():
                        print(f"{chave} - {valor}")

                    chave_esp_medica = int(input("\nEscolha uma opção: "))

                    if chave_esp_medica not in especialidades:
                        print("Opção Inválida!")
                        delay()
                        limpar_tela()

                    else:
                        break

                dt_nasc = converter_data_banco(input("Data de nascimento (DD/MM/YYYYY): "))
                dt_admissao = converter_data_banco(input("Data de admissão (DD/MM/YYYYY): "))
                dt_desligamento = None

                sql = '''INSERT INTO medico (CRM, NOME, RG, CPF, EMAIL, ENDERECO, CEP, ESP_MEDICA, DT_NASC, DT_ADMISSAO)   
                                                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                valores = (crm, nome, rg, cpf, email, endereco, cep, chave_esp_medica, dt_nasc, dt_admissao)

                try:
                    cursor.execute(sql, valores)
                    conexao.commit()  # Confirmar a transação no SGBD
                    print(f"Médico {nome} cadastrado com sucesso!")

                except Exception as e:
                    print(f"Erro: {e}")


def excluir_medico(conexao, cursor):
    print("-=-= EXCLUSÃO DE MÉDICO =-=-\n")
    cpf = input("CRM: ")

    try:
        sql = "SELECT ID, NOME FROM MEDICO WHERE CRM = %s"
        cursor.execute(sql, (cpf,))
        resultado = cursor.fetchall()  # retorna para resultado; todas as linhas retornadas pela execução da query

        if len(resultado) == 0:
            print("Médico não encontrado.")
            delay()

        else:
            id_medico = resultado[0][0]
            nome_medico = resultado[0][1]

            op_exclusao = int(
                input(f"\nDeseja excluir o médico {nome_medico}?\n1. Sim\n2. Não\n\nEscolha uma opção: "))

            if op_exclusao == 1:
                sql = "DELETE FROM MEDICO WHERE ID = %s"
                cursor.execute(sql, (id_medico,))
                conexao.commit()
                input(f"\nPaciente {nome_medico} excluído\nPressione enter para continuar.")

            elif op_exclusao == 2:
                print("Retornando ao menu principal")
                delay()

            else:
                print("Opção inválida.")
                delay()
    except Exception as e:
        print("Erro ", e)


def consultar_todos_medicos(cursor):
    try:
        sql = '''SELECT CRM, NOME, RG, CPF, EMAIL, ENDERECO, CEP, ESP_MEDICA, DT_NASC, DT_ADMISSAO, DT_DESLIGAMENTO, STATUS_MEDICO 
        FROM MEDICO
        ORDER BY NOME ASC'''
        cursor.execute(sql)
        resultado = cursor.fetchall()

        if len(resultado) == 0:
            print("Não há médicos cadastrados no Sistema!")
            delay()

        else:
            resultados = []

            for item in resultado:
                item = list(item)

                item[8] = converter_data(item[8])
                item[9] = converter_data(item[9])
                item[10] = converter_data(item[10])

                chave_esp = item[7]
                item[7] = especialidades.get(chave_esp)   #GET -> Pega os valores do dic (dicionário)

                resultados.append(item)

            colunas = ['CRM', 'NOME', 'RG', 'CPF', 'E-MAIL', 'ENDEREÇO', 'CEP', 'ESPECIALIDADE', 'DATA NASCIMENTO','DATA ADMISSÃO','DATA DESLIGAMENTO', 'STATUS MÉDICO']
            tabela = tabulate(resultados, headers=colunas, tablefmt='grid')
            display(tabela)
            input("\nPressione Enter para continuar...")

    except Exception as e:
        print("Erro: ", e)


def consultar_por_crm(cursor):
    crm_procurado = input("CRM: ")
    try:
        sql = '''SELECT CRM, NOME, RG, CPF, EMAIL, ENDERECO, CEP, ESP_MEDICA, DT_NASC, DT_ADMISSAO, DT_DESLIGAMENTO, STATUS_MEDICO 
                        FROM MEDICO
                    WHERE CRM = %s'''
        cursor.execute(sql,(crm_procurado,))
        resultado = cursor.fetchall()

        if len(resultado) == 0:
            print("Médico não encontrado!")
            delay()

        else:
            resultados = []

            for item in resultado:
                item = list(item)

                item[8] = converter_data(item[8])
                item[9] = converter_data(item[9])
                item[10] = converter_data(item[10])

                chave_esp = item[7]
                item[7] = especialidades.get(chave_esp)

                resultados.append(item)


            colunas = ['CRM', 'NOME', 'RG', 'CPF', 'E-MAIL', 'ENDEREÇO', 'CEP', 'ESPECIALIDADE', 'DATA NASCIMENTO','DATA ADMISSÃO','DATA DESLIGAMENTO', 'STATUS MÉDICO']
            tabela = tabulate(resultados, headers=colunas, tablefmt='grid')
            display(tabela)
            input("\nPressione Enter para continuar...")

    except Exception as e:
        print("Erro: ", e)


def inativar_medico(conexao, cursor):
    print(" -=-=INATIVAR MÉDICO=-=- \n") #certeza que era

    crm = input("CRM: ")

    try:
        sql = "SELECT ID, NOME FROM MEDICO WHERE CRM = %s"
        cursor.execute(sql, (crm,))
        resultado = cursor.fetchall()  # vai gravar nos resultado todas as linhas retornadas pela execução da query
        if len(resultado) == 0:
            print("Médico não encontrado!")
            delay()

        else:
            id_medico = resultado[0][0]
            nome_medico = resultado[0][1]
            sql = "SELECT STATUS_MEDICO FROM MEDICO WHERE ID = %s;"
            cursor.execute(sql, (id_medico,))
            resultado = cursor.fetchall()
            status_medico = resultado[0][0]

            if status_medico == 'Inativo':
                limpar_tela()
                input("Médico já está Inativo no Sistema.\n\n Pressione entrer para continuar...")

            else:
                op_desligamento = int(
                    input(f"Deseja desligar o Médico {nome_medico}?\n1.Sim 2.Não\n\n Escolha uma opção: "))

                if op_desligamento == 1:
                    data_desligamento = converter_data_banco(input("Data Desligamento (DD/MM/AAAA): "))
                    sql = "SELECT DT_CONSULTA FROM CONSULTA WHERE ID_MEDICO = %s AND DT_CONSULTA >=%s;"
                    cursor.execute(sql, (id_medico, data_desligamento))
                    resultado = cursor.fetchall()

                    if len(resultado) != 0:
                        print("Médico não poderá ser desligado, pois possui consultas vinculadas ao seu cadastro "
                              "com data igual ou maior à data inserida para o desligamento.\n\n"
                              "Pressione enter para retornar...")

                    else:
                        sql = "UPDATE MEDICO SET DT_DESLIGAMENTO = %s WHERE ID = %s;"
                        cursor.execute(sql, (data_desligamento, id_medico))
                        conexao.commit()
                        limpar_tela()
                        print(f"O médico{nome_medico} foi inativo!")
                        delay()

                elif op_desligamento == 2:
                    limpar_tela()
                    print("Retornando...")
                    delay()

                else:
                    limpar_tela()
                    print("Opção inválida!")
                    delay()

    except Exception as e:
        print("Erro:", e)


def ativar_medico(conexao, cursor):
    print(" -=-=ATIVAR MÉDICO=-=- \n")

    crm = input("CRM: ")

    try:
        sql = "SELECT ID, NOME, STATUS_MEDICO FROM MEDICO WHERE CRM = %s"
        cursor.execute(sql, (crm,))
        resultado = cursor.fetchall()  # vai gravar nos resultado todas as linhas retornadas pela execução da query
        if len(resultado) == 0:
            print("Médico não encontrado!")
            delay()

        else:
            id_medico = resultado[0][0]
            nome_medico = resultado[0][1]
            status_medico = resultado[0][2]

            if status_medico == 'Ativo':
                limpar_tela()
                input("Médico já está Ativo no Sistema.\n\n Pressione enter para continuar...")

            else:
                op_ativacao = int(
                    input(f"Deseja ativar o Médico {nome_medico}?\n1.Sim 2.Não\n\n Escolha uma opção: "))

                if op_ativacao == 1:
                    sql = "UPDATE MEDICO SET DT_DESLIGAMENTO = NULL WHERE ID = %s"
                    cursor.execute(sql,(id_medico,))
                    conexao.commit()

                    limpar_tela()
                    print(f"O médico {nome_medico} foi reativado.")

                elif op_ativacao == 2:
                    print(f"O médico {nome_medico} não foi reativado")
                    delay()

                else:
                    limpar_tela()
                    print("Opção inválida!")
                    delay()

    except Exception as e:
        print("Erro:", e)


def editar_medico(conexao, cursor):
    print(" -=-=EDIÇÃO DE MÉDICO=-=-\n ")
    crm = input("CRM: ")

    try:
        sql = "SELECT ID, CPF, RG, NOME FROM MEDICO WHERE CRM = %s"
        cursor.execute(sql, (crm,))
        resultado = cursor.fetchall()
        limpar_tela()
        if len(resultado) == 0:
            print("Médico não  encontrado!")
            delay()

        else:
            id_medico = resultado[0][0]
            cpf_atual = resultado[0][1]
            rg_atual = resultado[0][2]
            nome_atual = resultado[0][3]

            novo_crm = input("Novo CRM: ")
            cursor.execute(sql, (novo_crm,))
            resultado = cursor.fetchall()

            if len(resultado) != 0 and novo_crm != crm:
                limpar_tela()
                print("CRM já esta cadastrado para outro médico!")
                delay()

            else:
                novo_cpf = input("Novo CPF: ")

                sql = "SELECT ID FROM MEDICO WHERE CPF = %s"
                cursor.execute(sql, (id_medico,))
                resultado = cursor.fetchall() # ->>>>>>>>>>>>>fetchall: pega todos os registros e reune

                #Se o resultado da query for diferente de zero e o ID diferente do ID atual do médico, impedir.
                if len(resultado) != 0 and (id_medico,) not in resultado:
                    limpar_tela()
                    print("CPF já cadastrado para outro médico!")
                    delay()

                else:
                    novo_rg = input("Novo RG: ")

                    sql = "SELECT ID FROM MEDICO WHERE RG = %s "
                    cursor.execute(sql, (novo_rg,))
                    resultado = cursor.fetchall()

                    if len(resultado) !=0 and id_medico not in resultado:
                        limpar_tela()
                        print("RG já cadastrado para outro médico")
                        delay()

                    else:
                        nome = input("Nome: ")
                        email = input("E-mail: ")
                        endereco = input("Endereço: ")
                        cep = input("CEP: ")

                        while True:
                            print("\nEspecialidade Médica: ")
                            for chave, valor in especialidades.items():
                                print(f"{chave} - {valor}")

                            chave_esp_medica = int(input("\nEscolha uma opção: "))

                            if chave_esp_medica not in especialidades:
                                print("Opção Inválida!")
                                delay()
                                limpar_tela()

                            else:
                                break

                        dt_nasc = converter_data_banco(input("Data de nascimento (DD/MM/YYYYY): "))
                        dt_admissao = converter_data_banco(input("Data de admissão (DD/MM/YYYYY): "))
                        dt_desligamento = None

                        #verificar no meu banco se o nome é ESPECIALIDADE MEDICA OU ESP_MEDICA
                        sql = '''UPDATE MEDICO
                                    SET CRM = %s, NOME, RG, CPF, EMAIL, ENDERECO, CEP ESPECIALIDADE_MEDICA, DT_NASC, DT_ADMISSAO  
                                WHERE
                                    ID = %s'''

                        valores = (novo_crm, nome, novo_rg, novo_cpf, email, endereco, cep, chave_esp_medica, dt_nasc, dt_admissao, id_medico)

                        cursor.execute(sql, valores)
                        conexao.commit()
                        limpar_tela()
                        print(f"Médico {nome} alterado com Sucesso!")
                        delay()

    except Exception as e:
        print(f"Erro: {e}")


def relatorio_especialidades(cursor):
    for chave, valor in especialidades.items():
        print(f"{chave} - {valor}")

    especialidade_procurada = input("Especialidade: ")

    try:
        sql = '''SELECT CRM, 
                        NOME, 
                        ESP_MEDICA 
                        FROM MEDICO
                        WHERE ESP_MEDICA = %s
                        ORDER BY NOME ASC'''

        cursor.execute(sql, (especialidade_procurada,))
        resultado = cursor.fetchall()
        limpar_tela()

        if len(resultado) == 0:
            print("Não há especialidades cadastradas!")
            delay()
            limpar_tela()

        else:
            resultados = []

            for item in resultado:
                item = list(item)

                chave_especialidade = item[2]
                item[2] = especialidades.get(chave_especialidade)

                resultados.append(item)

            colunas = ['CRM', 'NOME', 'ESPECIALIDADE']
            tabela = tabulate(resultados, headers=colunas, tablefmt='grid')
            display(tabela)
            input("\nPressione Enter para continuar...")

    except Exception as e:
        print("Erro: ", e)


def relatorio_status(cursor):
    status_procurado = int(input("Digite o Status\n1. Ativo\n2. Inativo\n\nSelecione uma opção:"))

    try:
        if status_procurado == 1 or status_procurado == 2:

            if status_procurado ==1:
                status_procurado = 'Ativo'

            elif status_procurado ==2:
                status_procurado = 'Inativo'

            sql = '''SELECT CRM, 
                            NOME, 
                            ESP_MEDICA,
                            STATUS_MEDICO
                            FROM MEDICO
                            WHERE STATUS_MEDICO = %s
                            ORDER BY MEDICO.NOME ASC'''

            cursor.execute(sql, (status_procurado,))
            resultado = cursor.fetchall()
            limpar_tela()

            if len(resultado) == 0:
                print("Não há medicos no status escolhido")
                delay()
                limpar_tela()

            else:
                resultados = []

                for item in resultado:
                    item = list(item)

                    chave_esp = item[2]
                    item[2] = especialidades.get(chave_esp)

                    resultados.append(item)

                colunas = ['CRM', 'NOME', 'ESPECIALIDADE','STATUS']
                tabela = tabulate(resultados, headers=colunas, tablefmt='grid')
                display(tabela)
                input("\nPressione Enter para continuar...")
        else:
            print("Código inválido!")
    except Exception as e:
        print("Erro: ", e)




'''relatório de médicos para pedir todos os médicos por especialidade médica
mostrar a tabela de especialdiades para o usuario escolher
exibir: CRM, Nome do Médico, Especialidade (Order by ordenar por nome)'''

'''Relatório por status:
solicita médicos ativos e inativos
exibir: CRM, Nome do médico, especialidade e status(Order by ordenar por nome)'''
