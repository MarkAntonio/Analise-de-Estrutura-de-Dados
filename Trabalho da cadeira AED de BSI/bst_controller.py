from binary_tree import *
from time import sleep
from random import randint


def interface() -> str:
    menu_creation('Menu')
    print(' [1] - Criar Nova Árvore\n'  # ok
          ' [2] - Adicionar Valor\n'  # ok
          ' [3] - Remover Valor\n'  # ok
          ' [4] - Transformar a Árvore em Lista\n' # ok
          ' [5] - Transformar Lista em Árvore\n'  # ok
          ' [6] - Balancear Árvore\n'  # ok
          ' [7] - Total de Elementos\n'  # ok
          ' [8] - Altura da Árvore\n'  # ok
          ' [9] - Tipo do Elemento\n'  # ok
          '[10] - Imprimir Árvore\n'  # ok
          '[11] - Minimo/Máximo Valor da Árvore\n'  # ok
          '[12] - Sucessor ou Predecessor\n'
          '[13] - Buscar Elemento\n'
          '[14] - Deletar Árvore\n'
          '[15] - Sair do Programa')
    print('=' * 40)
    option = input('Digite a opção desejada: ')
    menu_footer()
    return option


def exception_control(value):
    value = str(value)
    if not value.isnumeric():
        if value.replace('-', '').isdigit():
            return True
        print(f'Valor "{value.strip()}" incorreto.\nDigite somente números.' if value != "" else
              'Você não digitou nada. Tente novamente.')
        return False
    else:
        return True


def menu_creation(msg: str) -> None:
    msg = f' {msg} '
    print(f'{msg:=^40}')


def menu_footer() -> None:
    print('=' * 40, '\n')


def choice() -> bool:
    while True:
        print('=' * 40)
        print('Deseja continuar?\n'
                       '[1] - Sim\n'
                       '[2] - Não')
        option = input('Digite a opção desejada: ')
        if exception_control(option):
            option = int(option)
            if option == 1:
                print('=' * 40)
                return True
            elif option == 2:
                print('=' * 40)
                return False
            else:
                print('=' * 40)
                print('Opção incorreta.')



def try_again():
    print('Deseja realizar a operação novamente?')
    option = input('Se sim digite o valor. Se não, digite N: ')
    while True:
        if option.upper() == 'N':
            return False, None
        aproved = exception_control(option)
        if aproved:
            return True, option
        option = input('\nSe sim digite o valor. Se não, digite N: ')

def controller() -> None:
    print('Iniciando o Programa...\n'
          'UFRPE - UAST\n'
          'Trabalho Sobre a Árvore Binária de Busca (2ª VA)\n'
          'Disciplina: AED 2021.2\n'
          'Professor: Héldon José\n'
          'Aluno: Marco Antonio')
    tree = lista = None
    while True:
        sleep(1)
        option = interface()
        if exception_control(option):
            option = int(option)
        else:
            continue
        if option in [2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14] and tree is None:
            # caso não exista árvore, não é possível realizar essas opções
            print('Não é possível realizar essa operação pois, ainda não existe nenhuma árvore.\n'
                  'Tente criar uma nova árvore!\n')
            continue

        if tree is not None:

            if option in [3, 4, 6, 7, 8, 9, 10, 11, 12, 13] and len(tree) == 0:
                print('Ainda não existe elementos na Árvore para realizar essa operação.')
                continue

            if tree is len(tree) <= 2 and option in [6, 7]:
                print('A árvore não tem elementos suficientes para estar desbalanceada.')
                continue

        match option:
            case 1:
                if tree is not None:
                    print('A árvore já existe...')
                else:
                    tree = BinaryTree()
                    print('Árvore criada. Adicione elementos nela!')
            case 2:
                menu_creation('Adicionar Valores')
                value = input('Digite um valor numérico: ')
                if exception_control(value):
                    tree.add(int(value))
                    print(f'Valor {value} adicionado.\n')
                while True:
                    flag, value = try_again()
                    if not flag:
                        break
                    tree.add(int(value))
                    print(f'Valor {value} adicionado.\n')
                menu_footer()
            case 3:
                menu_creation('Remover Valor')
                value = input('Digite um valor numérico: ')
                if exception_control(value):
                    tree.remove(int(value))
                    print(f'Valor {value} removido.\n')
                while True:
                    flag, value = try_again()
                    if not flag:
                        break
                    tree.remove(int(value))
                    print(f'Valor {value} removido.\n')
                    if len(tree) == 0:
                        print('\nNão há mais elementos na árvore.')
                        break

                menu_footer()
            case 4:
                menu_creation('Árvore em Lista')
                lista = tree.get_list()
                print('Operação realizada.')
                print(f'Sua lista é:\n {lista}')
                menu_footer()
            case 5:
                menu_creation('Lista em Árvore')
                while True:
                    print('[1] - Usar Lista Existente\n'
                          '[2] - Criar Lista Aleatória\n')
                    option = (input('Digite a opção desejada: '))
                    if exception_control(option):
                        option = int(option)
                        break
                    else:
                        continue
                if option == 1:
                    if lista is not None:
                        print(f'Sua lista é: {lista}')
                        new_lista = lista
                    else:
                        print('Não há lista existente.\n')
                        option = 2
                if option == 2:
                    print('Criando lista aleatória...')
                    new_lista = DoublyLinkedList()
                    sleep(1)
                    for element in range(10):
                        value = randint(0, 101)
                        new_lista.append_item(value)
                    print(f'Sua lista é: {new_lista}')
                if tree is not None:
                    print('Essa operação apagará todos os dados da árvore e adicionará os da lista.')
                    opc = choice()
                else:
                    tree = BinaryTree()
                    print('Árvore criada.')
                    opc = True
                if opc:
                    tree.create_tree_from_list(new_lista)
                    print('Árvore carregada com êxito!')
                    menu_footer()
            case 6:
                is_balanced = tree.balance(True)
                if is_balanced:
                    print('A árvore já está balanceada. '
                          '\nAdicione ou remova valores e tente novamente.\n')
                else:
                    tree.balance()
                    print('Árvore balanceada com êxito!\n')
            case 7:
                print(f'Total de elementos da árvore: {tree.total}\n')
            case 8:
                print(f'Altura da árvore: {tree.height}\n')
            case 9:
                menu_creation('Tipo do Elemento')
                value = input('Digite um valor da árvore para saber o seu tipo: ')
                if exception_control(value):
                    value = int(value)
                element = tree.search(value)
                if not element.is_leaf():
                    if element is tree.root:
                        print('Esse elemento é a raiz da árvore (é o pai de todos os outros nós e não possui pai). \n'
                              'Ele pode ter filhos ou não.\n')
                    else:
                        print('Esse valor é uma subávore (possui filhos): ')
                else:
                    print('Esse valor é uma folha da árvore (não possui filhos).')
                menu_footer()
            case 10:
                menu_creation('Imprimir Árvore')
                print('[1] - Impressão Pre Order\n'
                      '[2] - Impressão In Order\n' 
                      '[3] - Impressão Post Order\n'
                      '[4] - Impressão Interativa')
                menu_footer()
                while True:
                    option = input('Digite a opção desejada: ')
                    if exception_control(option):
                        option = int(option)
                    match option:
                        case 1:
                            tree.ordem(tree.root, 'pre')
                            print()
                        case 2:
                            print(tree)
                        case 3:
                            tree.ordem(tree.root, 'post')
                            print()
                        case 4:
                            tree.print()
                        case _:
                            print('Opção incorreta')
                            continue
                    break
                menu_footer()
            case 11:
                print(f'O maior valor é: {tree.max_value().data}\n'
                      f'O menor valor é: {tree.min_value().data}\n' if len(tree) > 1 else
                      f'Só existe um valor na lista, sendo assim tanto o menor quanto o maior é: {tree.root.data}\n')
            case 12:
                if len(tree) == 1:
                    print('Ainda não há elementos suficientes para realizar essa operação.\n'
                          'Tente adicionar mais um.\n')
                    continue
                menu_creation('Sucessor e Predecessor')
                value = input('Digite um valor da árvore: ')
                if exception_control(value):
                    value = int(value)
                element = tree.search(value, search_mode=True)
                print()
                if element is None:
                    print('Esse valor não existe. Tente novamente.\n')
                    continue
                if element.is_leaf():
                    print('Esse elemento não tem sucessor nem predecessor na árvore.\n')
                    continue
                if element.right:
                    print(f'O sucessor de {value} na árvore é: {tree.search(value, "successor")}')
                else:
                    print('Esse elemento não tem sucessor na árvore.')
                if element.left:
                    print(f'O predecessor de {value} na árvore é: {tree.search(value, "predeccessor")}')
                else:
                    print('Esse elemento não tem predecessor na árvore.')

                menu_footer()
            case 13:
                menu_creation('Busca na Árvore')
                value = input('Digite um valor da árvore: ')
                if exception_control(value):
                    value = int(value)
                element = tree.search(value, search_mode=True)
                if not element:
                    print('Valor não existente.\n')
                else:
                    print(f'Valor {element.data} encontrado!\n')
                menu_footer()
            case 14:
                menu_creation('Deletar Árvore')
                if tree is not None:
                    print('Essa operação apagará todos os dados da árvore e adicionará os da lista.')
                    opc = choice()
                    if opc:
                        tree = None  # fiz assim pra meu programa não bugar (ele bugar se eu der - del tree)
                        print('Árvore deletada com êxito!')
                        menu_footer()
            case 15:
                print("Obrigado por usar nosso serviço.\nSaindo do Programa...")
                break
            case _:
                print(f'Opção {option} incorreta. Tente novamente')


controller()
