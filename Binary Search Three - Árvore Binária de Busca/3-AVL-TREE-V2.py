class TreeNode(object):
    def __init__(self, data) -> None:
        self.data = data
        self.right = None
        self.left = None
        self.height = 0

    def __str__(self) -> str:
        return str(self.data)

    def is_leaf(self):
        return self.right is None and self.left is None

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
        if hasattr(perc, perc_sufixo):
            while getattr(perc, perc_sufixo):
                perc = getattr(perc, perc_sufixo)
            return perc

    def max_value(self) -> TreeNode:
        return self.__get_min_max(self.root, "right")

    def min_value(self) -> TreeNode:
        return self.__get_min_max(self.root, "left")

    def __get_successor(self, perc) -> TreeNode:
        return self.__get_min_max(perc.right, 'left')

    def __get_predeccessor(self, perc) -> TreeNode:
        return self.__get_min_max(perc.left, 'right')

    def __get_perc(self, perc, value, previous=None) -> tuple:
        if not perc:
            raise Exception("perc is not in tree")
        elif perc.data == value:
            return perc, previous  # retona o perc e o anterior se o valor dele for igual ao que eu estou procurando
        elif value < perc.data:
            return self.__get_perc(perc.left, value, perc)
        else:
            return self.__get_perc(perc.right, value, perc)

    def __delete_both(self, subtree):
        substitute = self.__get_successor(subtree)
        substitute, previous_substitute = self.__get_perc(subtree, substitute.data)
        substitute.left = subtree.left
        if subtree.right is not substitute:
            if substitute.right:
                previous_substitute.left = substitute.right
            else:
                previous_substitute.left = None
            substitute.right = subtree.right
        subtree.right = None
        subtree.left = None
        return substitute

    def __delete(self, subtree, value):
        if not subtree:
            raise Exception('Value is not in tree.')
            # return subtree
        if value < subtree.data:
            subtree.left = self.__delete(subtree.left, value)
        elif value > subtree.data:
            subtree.right = self.__delete(subtree.right, value)
        else:
            # é uma folha - não tem filhos
            if subtree.is_leaf():
                return None
            # Tem filho na esquerda
            if not subtree.right:
                subtitute = subtree.left
                root = None
                return subtitute
            # Tem filho na direita
            elif not subtree.left:
                sustitute = subtree.right
                root = None
                return sustitute
            #Tem os dois filhos
            else:
                subtree = self.__delete_both(subtree)


        if subtree is None:  # esse aqui é pra recusividade
            return subtree

        subtree.height = 1 + max(self.get_height(subtree.left), self.get_height(subtree.right))

        balance_factor = self.__get_balance(subtree)
        if balance_factor not in [-1, 0, 1]:
            return self.__balance(subtree, balance_factor)

        return subtree

    def delete(self, value):
        # fazer uma correção caso ele seja a raiz, para o balancemento não dar errado
        self.root = self.__delete(self.root, value)
        self.total -= 1

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
            return -1
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
for i in range(0, 15, 2):
    avl_tree.insert(i)
print(avl_tree)

avl_tree.delete(10)
print(avl_tree)
