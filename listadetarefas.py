import os
import json
from pathlib import Path
from datetime import datetime
 
print()
print("- - - - - - - - - - - - - - - - - - - - -")
print("- - - Bloco de Codigo: Tarefas      - - -")
print("- - - - - - - - - - - - - - - - - - - - -")
print()
 
MSG_DIGITE = 'Digite um número: '
MSG_ENTER = 'Aperte enter para continuar...'
MSG_TCHAU = 'Obrigado por usar o programa'

DATE_FORMAT = '%d/%m/%Y %H:%M'
 
exemplo = '[{"id": "0", "titulo" : "Cortar a grama","prioridade" : "baixa","status": "pendente","origem": "e-mail","data_conclusao": "", "data_criacao": "07/11/2025 21:11"}]'
 
 
def clear():
    match os.name:
        case "nt":
            os.system("cls")
        case "posix":
            os.system("clear")
 
class Prioridade:
    URGENTE = "urgente"
    ALTA = "alta"
    MEDIA = "media"
    BAIXA = "baixa"

    def get_sorted_list() -> list[str]:
        return [
            Prioridade.URGENTE,
            Prioridade.ALTA,
            Prioridade.MEDIA,
            Prioridade.BAIXA
        ]
 
 
class Status:
    PENDENTE = "pendente"
    FAZENDO = "fazendo"
    ARQUIVADA = "arquivada"
    CONCLUIDA = "concluida"
    EXCLUIDA = "excluida"

    def get_sorted_list() -> list[str]:
        return [
            Status.PENDENTE,
            Status.FAZENDO,
            Status.ARQUIVADA,
            Status.CONCLUIDA,
            Status.EXCLUIDA
        ]
 
 
class Tarefa:
    id: int
    titulo: str
    prioridade: Prioridade
    status: Status
    origem: str
    data_conclusao: str = ""
    data_criacao: str
 
 
class ListaDeTarefas(list[Tarefa]):
    def __init__(self, json_file="") -> None:
        if json_file == '':
            return
 
        des_taref: list[dict] = json.loads(json_file)
 
        for dado in des_taref:
            tarefa = Tarefa()
            tarefa.id = dado["id"]
            tarefa.titulo = dado["titulo"]
            tarefa.prioridade = dado["prioridade"]
            tarefa.status = dado["status"]
            tarefa.origem = dado["origem"]
            tarefa.data_criacao = dado["data_criacao"]
            tarefa.data_conclusao = dado["data_conclusao"]
 
            self.append(tarefa)
 
    def to_json(self) -> str:
        target = []
        for tarefa in self:
            tar = {
                "id": tarefa.id,
                "titulo": tarefa.titulo,
                "prioridade": tarefa.prioridade,
                "status": tarefa.status,
                "origem": tarefa.origem,
                "data_criacao": tarefa.data_criacao,
                "data_conclusao": tarefa.data_conclusao
            }
            target.append(tar)
 
        return json.dumps(target)
 
def gerar_id(list_tarefas: ListaDeTarefas):
    list_id = []
    for tarefa in list_tarefas:
        list_id.append(int(tarefa.id))
    return max(list_id) + 1

def str_para_int(num : str) -> int | None:
    valor = None
    try:
        valor = int(num)
    except:
        valor = None
    return valor

# Como eu forcei o uso de strings como forma de indentificar prioridades e status
# essa função existe para classificar a importancia de cada tipo por ordem de lista
def classificar_tarefas_por_lista_ordenada(list_dict : ListaDeTarefas, key : str, sorted_list : list[str]) -> ListaDeTarefas:
    converted_list : ListaDeTarefas = []

    for tarefa in list_dict:
        if not hasattr(tarefa, key):
            raise Exception("Função não encontrou a chave no dicionario")
    else:
        pass # Language server não deixa eu ter a Intellisense nessa função se eu não colocar essa linha

    for type in sorted_list:
        for tarefa in list_dict:
            if getattr(tarefa, key) == type:
                converted_list.append(tarefa)
    
    return converted_list
 
 
def cli_printar_tarefas(list_tarefas: ListaDeTarefas):
    clear()
    for tarefa in list_tarefas:
        print(f'ID: {tarefa.id}')
        print(f'Título: {tarefa.titulo}')
        print(f'Prioridade: {tarefa.prioridade}')
        print(f'Status: {tarefa.status}')
        print(f'Origem: {tarefa.origem}')
        print(f'Data de criação: {tarefa.data_criacao}')
        print(f'Conclusão (se vazia então não esta concluída): {
              tarefa.data_conclusao}')
        print()
    input("\n" + MSG_ENTER)
 
 
def cli_file_interface_msg():
    print("Escolha uma opção")
    print()
    print("1 - Abra um arquivo de tarefas valido (pode ser arquivo .json")
    print("2 - Comece uma lista de tarefas do zero")
    print("3 - Use um exemplo")
    print("4 - Sair do programa")
    print()
 
 
def cli_file_interface() -> ListaDeTarefas:
    cli_file_interface_msg()
 
    match input(MSG_DIGITE):
        case '1':
            file_path = input(
                "Digite o caminho que o arquivo esta localizado: ")
            try:
                file = open(file_path, 'r')
                file_contents = file.read()
                file.close()
                return ListaDeTarefas(file_contents)
            except FileNotFoundError:
                print('Arquivo não encontrado, voltando a interface...')
                input(MSG_ENTER)
                clear()
                return cli_file_interface()
            except Exception as e:
                print(f'Erro desconhecido: {e}')
                input(MSG_ENTER)
                clear()
                return cli_file_interface()
        case '2':
            return ListaDeTarefas('')
        case '3':
            return ListaDeTarefas(exemplo)
        case '4':
            print(MSG_TCHAU)
            exit(0)
        case _:
            print("Resposta invalida, digite um número listado abaixo:")
            return cli_file_interface()
 
 
def cli_adicionar_tarefa(lista: ListaDeTarefas):
    clear()
    tarefa = Tarefa()
    tarefa.titulo = input("Digite o titulo da tarefa nova: ")
    while True:
        tarefa.prioridade = input(
            "Digite a prioridade da tarefa (Valores aceitos: urgente, alta, media, baixa): ")
        if tarefa.prioridade in [Prioridade.URGENTE, Prioridade.ALTA, Prioridade.MEDIA, Prioridade.BAIXA]:
            break
        else:
            print("Valor invalido digite denovo")
 
    tarefa.origem = input(
        "Digite a origem da tarefa (Pode ser email, telefone, etc...): ")
    tarefa.status = Status.PENDENTE
    tarefa.id = gerar_id(lista)

    data_agora = datetime.now()
    tarefa.data_criacao = data_agora.strftime(DATE_FORMAT)
 
    print("Tarefa adicionada!")
    input("Aperte enter para continuar...")
    lista.append(tarefa)
    return cli_lista_interface(lista)
 
 
def cli_visualizar_tarefas(lista: ListaDeTarefas):
    lista_classificada = classificar_tarefas_por_lista_ordenada(lista, "prioridade", Prioridade.get_sorted_list())
    lista_filtrada = []

    for tarefa in lista_classificada:
        if tarefa.status == Status.PENDENTE:
            lista_filtrada.append(tarefa)
 
    cli_printar_tarefas(lista_filtrada)
 
    return cli_lista_interface(lista)
 
 
def cli_mudar_estado_tarefa(lista: ListaDeTarefas):
    lista_nova = lista
 
    id_select = input(
        'Digite a ID da tarefa que queira modificar (deve ser número inteiro): ')
    id_int = str_para_int(id_select)
    if id_int is None:
        print('ID digitado invalido, escreva um número inteiro.')
        return cli_mudar_estado_tarefa(lista)

    for tarefa in range(0, len(lista_nova)):
        if lista_nova[tarefa].id == id_select or lista_nova[tarefa].id == id_int:
            print(f'ID Encontrada: {lista_nova[id_int].titulo}')
            while True:
                status_mod = input(
                    "Escolha um dos estados que deseja modificar na tarefa (Opções: concluida, pendente, fazendo, arquivada, excluida): ")
                if status_mod in Status.get_sorted_list():
                    if status_mod == Status.CONCLUIDA:
                        data = datetime.now()
                        lista_nova[id_int].data_conclusao = data.strftime(DATE_FORMAT)
                    elif status_mod == Status.FAZENDO or status_mod == Status.PENDENTE:
                        lista_nova[id_int].data_conclusao = ""
                    lista_nova[id_int].status = status_mod
                    print("Lista De Tarefas atualizada")
                    input(MSG_ENTER)
                    break
                else:
                    print("Valor errado, Digite denovo")
            break
    else:
        print('ID não encontrado, voltando a interface')
        input(MSG_ENTER)
 
    return cli_lista_interface(lista_nova)
 
 
def cli_mudar_prioridade_tarefa(lista):
    lista_nova = lista
 
    id_select = input(
        'Digite a ID da tarefa que queira modificar (deve ser número inteiro): ')
    id_int = str_para_int(id_select)
    if id_int is None:
        print('ID digitado invalido, escreva um número inteiro.')
        return cli_mudar_prioridade_tarefa(lista)
 
    for tarefa in range(0, len(lista_nova)):
        if lista_nova[tarefa].id == id_select or lista_nova[tarefa].id == id_int:
            print(f'ID Encontrada: {lista_nova[id_int].titulo}')
            while True:
                prioridade_mod = input(
                    "Escolha uma prioridade que deseja designar para a tarefa (Opções: urgente, alta, media, baixa): ")
                if prioridade_mod in Prioridade.get_sorted_list():
                    lista_nova[id_int].prioridade = prioridade_mod
                    print("Lista De Tarefas atualizada")
                    input(MSG_ENTER)
                    break
                else:
                    print("Valor errado, Digite denovo")
            break
    else:
        print('ID não encontrado, voltando a interface')
        input(MSG_ENTER)
 
    return cli_lista_interface(lista_nova)
 
 
def cli_limpar_tarefas(lista: ListaDeTarefas):
    lista_nova = lista
    lista_tar: ListaDeTarefas = []
    clear()
 
    for tarefa in lista_nova:
        if tarefa.status == Status.EXCLUIDA:
            lista_tar.append(tarefa)
 
    print('As seguintes tarefas irão ser deletadas: ')
    for tar in lista_tar:
        print('\n')
        print(f'Titulo: {tar.titulo}')
        print(f'ID: {tar.id}')
        print(f'Data de Conclusão: {tar.data_conclusao}')
 
    match input("Deseja continuar? (Sim ou Não): "):
        case 'Sim' | 'sim' | 's':
            for tar in lista_tar:
                lista_nova.remove(tar)
        case 'Não' | 'Nao' | 'nao' | 'n':
            print("Voltando a interface...")
            input(MSG_ENTER)
            pass
        case _:
            print("Resposta invalida, responda denovo")
            input(MSG_ENTER)
            return cli_limpar_tarefas(lista)
 
    return cli_lista_interface(lista_nova)
 
 
def cli_salvar_arquivo(lista: ListaDeTarefas):
    clear()
    match input('Pretende salvar o arquivo? (Opções: Sim, Não): '):
        case 'Sim' | 'sim' | 's':
            caminho = input(
                'Qual caminho você deseja salvar o programa? (Digite . para escolher a pasta que o terminal reside): ')

            nome = input(
                'Qual nome tu deseja aplicar para o arquivo? (inclua a extensão tambem): ')
            try:
                cam_path = Path(caminho + '\\')
                cam_path.mkdir(parents=True, exist_ok=True)
                file = open(caminho + '\\' + nome, 'w')
                file.write(lista.to_json())
                file.close()
            except Exception as e:
                print(f'Erro inesperado: {e}')
                print("Escreva denovo")
                input(MSG_ENTER)
                return cli_salvar_arquivo(lista)
            print(MSG_TCHAU)
            return exit(0)
        case 'Não' | 'Nao' | 'nao' | 'n':
            print(MSG_TCHAU)
            return exit(0)
        case _:
            print("Resposta invalida, responda denovo")
            input(MSG_ENTER)
            return cli_salvar_arquivo(lista)
 
def cli_lista_interface_msg():
    print("O que deseja fazer com o arquivo?")
    print()
    print("1 - Adicionar tarefas")
    print("2 - Visualizar tarefas disponiveis")
    print("3 - Modificar estado de uma tarefa")
    print("4 - Modificar prioridade de uma tarefa")
    print("5 - Listar todas as tarefas")
    print("6 - Limpar Tarefas Excluidas")
    print("7 - Sair do programa")
    print()
 
 
def cli_lista_interface(lista: ListaDeTarefas):
    clear()
    cli_lista_interface_msg()
 
    match input(MSG_DIGITE):
        case '1':
            return cli_adicionar_tarefa(lista)
        case '2':
            return cli_visualizar_tarefas(lista)
        case '3':
            return cli_mudar_estado_tarefa(lista)
        case '4':
            return cli_mudar_prioridade_tarefa(lista)
        case '5':
            cli_printar_tarefas(lista)
            return cli_lista_interface(lista)
        case '6':
            return cli_limpar_tarefas(lista)
        case '7':
            return cli_salvar_arquivo(lista)
        case _:
            print("Opção Invalida")
 
 
def tarefas():
    list_tarefas: ListaDeTarefas
 
    list_tarefas = cli_file_interface()
 
    list_tarefas = cli_lista_interface(list_tarefas)
 
 
tarefas()