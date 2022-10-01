
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

    def __get_perc(self, perc, value, previous=None) -> tuple:
        if not perc:
                raise Exception("perc is not in tree")
        elif perc.data == value:
            return perc, previous  # retona o perc e o anterior se o valor dele for igual ao que eu estou procurando
        elif value < perc.data:
            return self.__get_perc(perc.left, value, perc)
        else:
            return self.__get_perc(perc.right, value, perc)

    def get(self, value) -> _Node:
        perc, previous = self.__get_perc(self.root, value)  # chama a função privada
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

