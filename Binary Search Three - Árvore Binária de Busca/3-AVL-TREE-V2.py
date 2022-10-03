class TreeNode(object):
    def __init__(self, data) -> None:
        self.data = data
        self.right = None
        self.left = None
        self.height = 1

    def __str__(self) -> str:
        return str(self.data)

class AVLTree(object):
    def __init__(self) -> None:
        self.total = 0
        self.root = None

    def __str__(self) -> str:
        self.__order(self.root)
        return ''

    def __len__(self) -> int:
        return self.total

    def __insert(self, subtree, node) -> TreeNode:
        if not subtree:
            return node
        if node.data < subtree.data:
            subtree.left = self.__insert(subtree.left, node)
        else:
            subtree.right = self.__insert(subtree.right, node)
        subtree.height = 1 + max(self.get_height(subtree.left), self.get_height(subtree.right))

        balance_factor = self.__get_balance(subtree)
        if balance_factor not in [-1, 0, 1]:
            return self.__balance(subtree, balance_factor)

        return subtree

    def insert(self, value) -> None:
        node = TreeNode(value)
        self.root = self.__insert(self.root, node)
        self.total += 1

    def __get_min_max(self, perc, perc_sufixo) -> TreeNode:
        if hasattr(perc, perc_sufixo):  # verifida se o objeto (perc) tem o atributo (perc_sufixo_
            while getattr(perc, perc_sufixo):  # se entrar, ele cria um loop enquando o objeto tiver esse atributo
                perc = getattr(perc, perc_sufixo)  # aqui o objeto recebe o próprio objeto naquele atributo
            return perc  # quando o laço acaba ele retorna perc

    def max_value(self) -> TreeNode:
        return self.__get_min_max(self.root, "right")  # chama a função privada passando o atributo "right"

    def min_value(self) -> TreeNode:
        return self.__get_min_max(self.root, "left")  # chama a função privada passando o atributo "left"

    def preorder(self) -> None:
        self.__order(self.root, 'pre')

    def inorder(self) -> None:
        self.__order(self.root)

    def postorder(self) -> None:
        self.__order(self.root, 'post')

    def __order(self, root, type='in') -> None:
        if not root:
            return
        if type == 'pre':
            print(root, end=' ')
        self.__order(root.left)
        if type == 'in':
            print(root, end=' ')
        self.__order(root.right)
        if type == 'post':
            print(root, end=' ')

    def get_height(self, root) -> int:
        if not root:
            return 0
        return root.height

    def __get_balance(self, subtree) -> int:
        if not subtree:
            return 0
        return self.get_height(subtree.left) - self.get_height(subtree.right)

    def __right_rotation(self, subtree) -> TreeNode:
        substitute = subtree.left
        subtree.left = substitute.right  # se o substituto tem esquerda ele aponta, e se for none ele também será
        substitute.right = subtree

        self.__set_height_rotation(subtree, substitute)
        return substitute

    def __set_height_rotation(self, subtree, substitute) -> None:
        subtree.height = 1 + max(self.get_height(subtree.left), self.get_height(subtree.right))
        substitute.height = 1 + max(self.get_height(substitute.left), self.get_height(substitute.right))

    def __left_rotation(self, subtree) -> TreeNode:
        substitute = subtree.right
        subtree.right = substitute.left  # se o substituto tem esquerda ele aponta, e se for none ele também será
        substitute.left = subtree
        self.__set_height_rotation(subtree, substitute)
        return substitute

    def __balance(self, subtree, balance_factor) -> TreeNode:
        if balance_factor < -1:
            child = subtree.right
            child_balance_factor = self.__get_balance(child)
            if child_balance_factor > 0:  # sinais diferentes do fator de balanceamento, rotação dupla
                child = self.__right_rotation(child)
                return self.__left_rotation(subtree)
            else:
                return self.__left_rotation(subtree)  # Rotação anti-horária
        elif balance_factor > 1:
            child = subtree.left
            child_balance_factor = self.__get_balance(child)
            if child_balance_factor < 0:  # sinais diferentes do fator de balanceamento, rotação dupla
                # tenho que fazer isso por conta de um bug que acontece, e no final ainda fica desbalanceado
                child = self.__left_rotation(child)
                return self.__right_rotation(subtree)
            else:
                return self.__right_rotation(subtree)  # Rotação horária
        # caso não fique balanceado direito, fazer isso abaixo
        # balance_factor = self.__get_balance(subtree)
        # if balance_factor not in [-1, 0, 1]:
        #     self.__balance(subtree, balance_factor)


avl_tree = AVLTree()
for number in range(0, 20, 2):
    avl_tree.insert(number)
print(avl_tree)
