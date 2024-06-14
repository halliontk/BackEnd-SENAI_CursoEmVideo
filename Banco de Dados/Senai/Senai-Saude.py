import mysql.connector  # importando biblioteca
from dic import generos, especialidades
from nav_padrao import limpar_tela, delay

try:  # tratar excessões e erros do programa, traz exatamente os erros
    conexao = mysql.connector.connect(host='localhost', user='root', password='', database='senai_saude') #Conectar no banco
    cursor = conexao.cursor()

# if conexao.is_connected():
# print("Conexão Realizada")

# Assim como o If e Else, o Exception é o "Else", se algo der ruim no try, ele pula pro Exception.
except Exception as e:
    print("Erro: ", e)

print("-=-= SENAI SAÚDE =-=-")
op_menu = int(input("1. Área de Pacientes\n2. Área de Médicos\n3. Área de Consultas\n0. Encerrar\n\nEscolha uma opção: "))
limpar_tela()  # Limpa tela

if op_menu == 1:
    print("-=-= ÁREA DE PACIENTES =-=-")
    op_menu_sec = int(input(("1. Cadastrar\n2. Editar\n3. Consultar\n4. Excluir\n\nEscolha uma opção: ")))

    match op_menu_sec:  # match= aponta pra uma variável, igual Escolha/Caso
        case 1:
            print("-=-= CADASTRO DE PACIENTE =-=-\n")
            cpf = input("CPF: ")

            sql = "SELECT ID FROM PACIENTE WHERE CPF = %s"
            cursor.execute(sql, (cpf,))
            resultado = cursor.fetchall() #retorna para resultado; todas as linhas retornadas pela execução da query

            if len(resultado) != 0:  # se o tamanho da lista retornada para o banco for diferente de 0:
                print("CPF já cadastrado para outro paciente.")

            else:
                rg = input("RG: ")

                sql = "SELECT ID FROM PACIENTE WHERE RG = %s"
                cursor.execute(sql, (rg,))
                resultado = cursor.fetchall()

                if len(resultado) !=0:
                    print("RG já cadastrado para outr paciente.")

                else:

                    nome = input("Nome: ")
                    endereco = input("Endereço: ")
                    cep = input("CEP: ")
                    dt_nasc = input("Data de Nascimento: ")

                    while True:
                        print("\nGênero: ")
                        for chave, valor in generos.items():
                            print(f"{chave} - {valor}")

                        chave_genero = int(input("\nEscolha uma opção: "))

                        if chave_genero not in generos:
                            print("Opção Inválida!")
                            delay()
                            limpar_tela()

                        else:
                            break

                    telefone = input("Telefone: ")
                    email = input("E-mail: ")
                    responsavel = input("O paciente necessita de um responsável(S/N)? ")
                    if responsavel.upper() == 'S':
                        responsavel = input("Digite o nome do responsável: ")
                    else:
                        responsavel = None

                    sql = '''INSERT INTO paciente (CPF, RG, NOME, ENDERECO, CEP, DT_NASC, GENERO, TELEFONE, EMAIL, RESPONSAVEL) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                    valores = (cpf, rg, nome, endereco, cep, dt_nasc,
                               chave_genero, telefone, email, responsavel)

                    try:
                        cursor.execute(sql, valores)
                        conexao.commit()  # confirma a transação no SGBD
                        print(f"Paciente  {nome} cadastrado com sucesso!")

                    except Exception as e:
                        print(f"Erro: {e}")

        case 4:
            print("-=-= EXCLUSÃO DE PACIENTE =-=-\n")
            cpf = input("CPF: ")

            try:
                sql = "SELECT ID, NOME FROM PACIENTE WHERE CPF = %s"
                cursor.execute(sql, (cpf,))
                resultado = cursor.fetchall()  # retorna para resultado; todas as linhas retornadas pela execução da query

                if len(resultado) == 0:
                    print("Paciente não encontrado.")
                    delay()

                else:
                    id_paciente = resultado[0][0]
                    nome_paciente= resultado[0][1]

                    op_exclusao = int(input(f"\nDeseja excluir o paciente {nome_paciente}?\n1. Sim\n2. Não\n\nEscolha uma opção: "))

                    if op_exclusao == 1:
                        sql = "DELETE FROM PACIENTE WHERE ID = %s"
                        cursor.execute(sql, (id_paciente,))
                        conexao.commit()
                        input(f"\nPciente {nome_paciente} excluído\nPressione enter para continuar.")

                    elif op_exclusao == 2:
                        print ("Retornando ao menu principal")
                        delay()

                    else:
                        print("Opção inválida.")
                        delay()
            except Exception as e:
                print("Erro ", e)

elif op_menu == 2:
    print("-=-= ÁREA DE MÉDICOS =-=-")
    op_menu_sec = int(input(("1. Cadastrar\n2. Editar\n3. Consultar\n4. Excluir\n\nEscolha uma opção: ")))
    limpar_tela()

    match op_menu_sec:
        case 1:

            sql= "SELECT ID FROM MEDICO WHERE CRM = %s"
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

                        dt_nasc = input("Data de nascimento: ")
                        dt_admissao = input("Data de admissão: ")
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
        case 4:
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

    #case _:  # DEFAULT = ELSE
     #   print("Opção Inválida")

elif op_menu == 3:
    print("-=-= ÁREA DE CONSULTAS =-=-")
    op_menu_sec = int(input(("1. Cadastrar\n2. Editar\n3. Visualizar\n4. Excluir\n\nEscolha uma opção: ")))
    limpar_tela()

    match op_menu_sec:
        case 1:
            print("-=-= CADASTRO DE CONSULTA =-=-\n")

            while True:
                crm_medico = input("CRM do Médico: ")

                sql = "SELECT ID FROM MEDICO WHERE CRM = %s"
                cursor.execute(sql, (crm_medico,))
                resultado = cursor.fetchall()

                if len(resultado) == 0:
                    print("Médico não encontrado!")
                    delay()

                else:
                    id_medico = resultado[0][0]

                    sql = "SELECT STATUS_MEDICO FROM MEDICO WHERE ID = %s"
                    cursor.execute(sql, (id_medico,))
                    resultado = cursor.fetchall()
                    status_medico = resultado[0][0]

                    if status_medico == 'Inativo':
                        print("Não é possível marcar consulta para este médico, pois ele possui status Inativo!")
                        delay()

                    else:
                        cpf_paciente = input("CPF do paciente: ")

                        sql = "SELECT ID FROM PACIENTE WHERE CPF = %s"
                        cursor.execute(sql, (cpf_paciente,))
                        resultado = cursor.fetchall()

                        if len(resultado) == 0:
                            limpar_tela()
                            print("Paciente não encontrado!")
                            delay()
                            limpar_tela()

                        else:
                            id_paciente = resultado[0][0]
                            cod_consulta = input("Código da Consulta: ")

                            sql = "SELECT ID FROM CONSULTA WHERE COD_CONSULTA = %s"
                            cursor.execute(sql, (cod_consulta,))
                            resultado = cursor.fetchall()

                            if len(resultado) != 0:
                                limpar_tela()
                                print("Já existe consulta cadastrada com este código! Tente novamente...")
                                delay()

                            else:
                                dt_consulta = input("Data da Consulta (YYYY-MM-DD): ")
                                hr_consulta = input("Hora da Consulta (HH:MM:SS): ")
                                # Adicionar tratamento para inserção de DATA e HORA
                                # Adicionar validação para DATA E HORA disponíveis (medico e paciente)

                                vr_consulta = float(input("Valor da Consulta: "))

                                sql = '''INSERT INTO CONSULTA(COD_CONSULTA, DT_CONSULTA, HR_CONSULTA, 
                                            VR_CONSULTA, ID_MEDICO, ID_PACIENTE) VALUES (%s, %s, %s, %s, %s, %s)'''
                                valores = (cod_consulta, dt_consulta, hr_consulta, vr_consulta, id_medico, id_paciente)

                                cursor.execute(sql, valores)
                                conexao.commit()
                                print("Consulta cadastrada com sucesso!")

                                # INSERIR ESTRUTURA TRY-EXCEPT