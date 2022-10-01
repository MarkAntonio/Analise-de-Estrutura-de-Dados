import sys
from doublyLinkedList_Tree import DoublyLinkedList


# árvore completa é quando as folhas estão no mesmo nível
# - o maior valor fica na direta, o menor fica na esquerda
# - geralmente árvore binária de busca não aceita valores repetidos
# - a cada passo na árvore, eu elimino 50%
# - para adicionar, a árvore tem um custo maior que a lista, mas para buscar ela tem um custo bem menor
# - filhos, pais, raíz, nó e folha
# - folha não tem filho, raíz tem filho
# - o maior valor é sempre uma folha à direita ou uma raíz que não tem uma folha à direita mas pode ter à esquerda
# - o menor valor é sempre uma folha à esquerda ou uma raíz que não tem uma folha à esquerda mas pode ter à direta
# - Uma árvore tem altura e nível


class _Node:  # Cria o nó
    def __init__(self, data) -> None:
        self.data = data
        self.left = None
        self.right = None

    def __str__(self) -> str:
        return f'{self.data}'

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None
        # se left e right forem nome ele retorna True. Se um deles não for None ele retorna False


class BinaryTree:  # cria a classe BinaryTree
    def __init__(self) -> None:
        self.root = None
        self.total = 0

    # ================================== perc ==============================

    def __get_perc(self, perc, value, search_mode=False, previous=None) -> tuple | None:
        if not perc:
            if search_mode:
                return perc, None
            else:
                raise Exception("perc is not in tree")
        elif perc.data == value:
            return perc, previous  # retona o perc e o anterior se o valor dele for igual ao que eu estou procurando
        elif value < perc.data:
            return self.__get_perc(perc.left, value,  search_mode, perc)
        else:
            return self.__get_perc(perc.right, value, search_mode, perc)

    def get(self, value, search_mode) -> _Node:
        perc, previous = self.__get_perc(self.root, value, search_mode)  # chama a função privada
        return perc  # retorona somente o perc (Escolha minha)

    # ============================ mínimo e máximo =================================================

    def __get_min_max(self, perc, perc_sufixo) -> _Node:
        if hasattr(perc, perc_sufixo):  # verifida se o objeto (perc) tem o atributo (perc_sufixo_
            while getattr(perc, perc_sufixo):  # se entrar, ele cria um loop enquando o objeto tiver esse atributo
                perc = getattr(perc, perc_sufixo)  # aqui o objeto recebe o próprio objeto naquele atributo
            return perc  # quando o laço acaba ele retorna perc

    def max_value(self) -> _Node:
        return self.__get_min_max(self.root, "right")  # chama a função privada passando o atributo "right"

    def min_value(self) -> _Node:
        return self.__get_min_max(self.root, "left")  # chama a função privada passando o atributo "left"

    def __add(self, root_node, node) -> _Node:  # função recursiva para adicionar um valor
        if not root_node:  # se não tiver nenhum elemento ele retorna o nó que será a raiz
            return node
        else:
            if node.data < root_node.data:
                root_node.left = self.__add(root_node.left, node)
            else:
                root_node.right = self.__add(root_node.right, node)
        return root_node

    def add(self, data) -> None:  # função para adicionar valores na árvore
        node = _Node(data)  # criar o objeto node
        self.root = self.__add(self.root, node)  # chama a afunção privada
        self.total += 1  # no final da função privada ele soma + 1 ao total de elementos

    def __get_successor(self, perc=None) -> _Node:  # função privada para obter o sucessor
        if not perc:
            perc = self.root.right
        return self.__get_min_max(perc.right, 'left')
        # chama a função privada passando o perc.right e dizendo que ele quer o mínimo (por conta do atibuto "left")

    def __get_predeccessor(self, perc=None) -> _Node:  # função privada para obter o predecessor
        if not perc:
            perc = self.root.left
        return self.__get_min_max(perc.left, 'right')

    def search(self, value, type=None, search_mode=False):
        if type is None:
            return self.get(value, search_mode)
        elif type == 'successor':
            return self.__get_successor(self.get(value, search_mode)).data
        elif type == 'predeccessor':
            return self.__get_predeccessor(self.get(value, search_mode)).data

    # chama a função privada passando o perc.left e dizendo que ele quer o máximo (por conta do atibuto "right")

    def ordem(self, raiz, order='in') -> None:  # imprime o elemento na ordem desejada (pre, in ou post)
        if not raiz:
            return
        if order == 'pre':
            print(raiz, end=' ')
        self.ordem(raiz.left, order)
        if order == 'in':
            print(raiz, end=' ')
        self.ordem(raiz.right, order)
        if order == 'post':
            print(raiz, end=' ')

    def __str__(self) -> str:
        self.ordem(self.root)
        return ''

    def __len__(self):
        return self.total

    def print(self):
        self.printHelper(self.root, '', True)

    def printHelper(self, currPtr, indent, last):
        if currPtr is not None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            print(currPtr.data)
            self.printHelper(currPtr.left, indent, False)
            self.printHelper(currPtr.right, indent, True)

    def __remove_leaf(self, node, previous_node) -> None:  # caso o nó seja uma folha
        if node.data < previous_node.data:
            previous_node.left = None
        else:
            previous_node.right = None

    def __remove_one_child(self, node, previous_node) -> None:  # se o nó tiver só um filho
        if node is self.root:  # se o nó for a raiz
            if node.left:
                self.root = node.left
                node.left = None
            elif node.right:
                self.root = node.right
                node.right = None
        elif node.left:
            if node.left.data < previous_node.data:
                previous_node.left = node.left
            else:
                previous_node.right = node.left
            node.left = None
        elif node.right:
            if node.right.data < previous_node.data:
                previous_node.left = node.right
            else:
                previous_node.right = node.right
            node.right = None

    def __remove_two_children(self, node, previous_node) -> None:  # se o nó tiver os 2 filhos
        # ==============================================================================================================
        # aqui eu não usei o predecessor, porque se ele não tiver o filho à direita, ele cai no caso que só tem um filho
        # logo ele nunca vai cair nessa função.
        # ==============================================================================================================
        substitute = self.__get_successor(node)  # aqui eu pego o sucessor
        substitute, previous_substitute = self.__get_perc(node, substitute.data)
        # aqui ele pega o sucessor novamente (porque eu passo o valor do substituto pra ele) e o antereior do sucessor
        substitute.left = node.left
        if node.right is not substitute:  # se a direita do nó não for o sucessor
            if substitute.right:
                previous_substitute.left = substitute.right
            else:
                previous_substitute.left = None
            substitute.right = node.right

        if node is self.root:  # se o nó for a raiz
            self.root = substitute
        else:
            if substitute.data < previous_node.data:
                previous_node.left = substitute
            else:
                previous_node.right = substitute
        node.right = None
        node.left = None

    def __remove(self, node, previous_node) -> None:
        if node.is_leaf():  # se o nó é folha
            self.__remove_leaf(node, previous_node)
        elif node.left is None or node.right is None:  # se só tem um filho
            self.__remove_one_child(node, previous_node)
        else:  # Se cair aqui, logo ele tem os 2 filhos
            self.__remove_two_children(node, previous_node)

    def remove(self, data) -> None:
        node, previous_node = self.__get_perc(self.root, data)
        if self.total == 0:  # se a árvore estiver vazia ele não faz nada
            print('Tree has not elements')
            return
        elif self.total == 1:  # se só existir um elemento, quer dizer que ele é a raiz.
            self.root = None
            self.total -= 1
            return
        self.__remove(node, previous_node)
        self.total -= 1

    def __get_list(self, root, lista) -> DoublyLinkedList:
        if not root:
            return
        self.__get_list(root.left, lista)
        lista.append_item(root.data)
        self.__get_list(root.right, lista)
        return lista

    def get_list(self) -> DoublyLinkedList:
        return self.__get_list(self.root, DoublyLinkedList())

    def create_tree_from_list(self, lista: list | DoublyLinkedList):
        self.root = None
        self.total = 0
        for element in lista:
            self.add(element)
        self.balance()
        # print('Congratulations! The tree was successfuly created.')

    def __get_height(self, subtree):
        if not subtree:
            return -1
        if subtree.is_leaf():
            return 0
        else:
            # funcionam como contadores
            left_level = 1 + self.__get_height(subtree.left)
            right_level = 1 + self.__get_height(subtree.right)
            # return max((left_level, right_level))  # ele coloca os dois valores numa tupla e retorna o maior
            return left_level if left_level > right_level else right_level

    @property
    def height(self, data=None):
        if not data:
            node = self.root
        else:
            node = self.get(data)
        return self.__get_height(node)

    def __get_balance_factor(self, subtree):
        return self.__get_height(subtree.left) - self.__get_height(subtree.right)

    def __left_rotation(self, subtree):
        subtree, subtree_previous = self.__get_perc(self.root, subtree.data)
        substitute = subtree.right

        if subtree_previous:  # se existe anterior, quer dizer que a subárvore não é a raiz
            self.__recovery_father(subtree, subtree_previous, substitute)
        else:
            self.root = substitute

        subtree.right = substitute.left  # se o substituto tem esquerda ele aponta, e se for none ele também será
        substitute.left = subtree

    def __recovery_father(self, subtree, subtree_previous, substitute):
        if subtree.data < subtree_previous.data:
            subtree_previous.left = substitute
        else:
            subtree_previous.right = substitute

    def __right_rotation(self, subtree):
        subtree, subtree_previous = self.__get_perc(self.root, subtree.data)
        substitute = subtree.left

        if subtree_previous:  # se existe anterior, quer dizer que a subárvore não é a raiz
            self.__recovery_father(subtree, subtree_previous, substitute)
        else:
            self.root = substitute

        subtree.left = substitute.right  # se o substituto tem esquerda ele aponta, e se for none ele também será
        substitute.right = subtree

    def __balance(self, subtree, verify_balanced, unbalanced_factors):
        if not subtree:
            return
        self.__balance(subtree.left, verify_balanced, unbalanced_factors)
        self.__balance(subtree.right, verify_balanced, unbalanced_factors)
        balance_factor = self.__get_balance_factor(subtree)
        if verify_balanced and balance_factor not in [-1, 0, 1]:
            unbalanced_factors.append_item(balance_factor)
        if verify_balanced and len(unbalanced_factors) == 0:
            return True  # quer dizer que a árvore já está balanceada

        # só vai cair aqui se eu não quiser verficar (só cai aqui quando houver desbalanceamento)
        while balance_factor not in [-1, 0, 1]:
            if balance_factor < -1:
                child = subtree.right
                child_balance_factor = self.__get_balance_factor(child)
                if child_balance_factor > 0:  # sinais diferentes do fator de balanceamento, rotação dupla
                    self.__right_rotation(child)
                    self.__left_rotation(subtree)
                else:
                    self.__left_rotation(subtree)  # Rotação anti-horária
            elif balance_factor > 1:
                child = subtree.left
                child_balance_factor = self.__get_balance_factor(child)
                if child_balance_factor < 0:  # sinais diferentes do fator de balanceamento, rotação dupla
                    # tenho que fazer isso por conta de um bug que acontece, e no final ainda fica desbalanceado
                    self.__left_rotation(child)
                    self.__right_rotation(subtree)
                else:
                    self.__right_rotation(subtree)  # Rotação horária
            balance_factor = self.__get_balance_factor(subtree)

    def balance(self, verify_balanced=False):
        unbalanced_factors = None
        if verify_balanced:
            unbalanced_factors = DoublyLinkedList()
        return self.__balance(self.root, verify_balanced, unbalanced_factors)

#
# tree = BinaryTree()
# lista = DoublyLinkedList()
# for i in range(15, 0, -1):
#     lista.append_item(i)
# tree.create_tree_from_list(lista)
#
# tree.balance()
