class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        # return f'{self.data}, {self.next}' if self.next else f'{self.data}'  não posso colocar assim, por que se não
        # recursão estoura caso eu queria colocar mais de 329 itens de uma só vez
        # return f'{self.data} ,{self.next}' como não estou usando a recursão, não preciso retornar nenhuma string.
        pass


class SimplyLinkedList:
    def __init__(self, tipo=None):
        self.head = None
        self.tale = None  # Adicionarei uma cauda à lista
        self.lenght = 0
        self.type = tipo

    def __str__(self):
        # return f'[{self.head}]' não posso colocar assim, por que se não a recursão estoura caso eu queria colocar
        # mais de 329 itens de uma só vez.
        if self.lenght == 0:
            return '[]'
        value_list = '['
        current_node = self.head
        while current_node.next:
            value_list += f'{current_node.data}, ' if type(current_node.data) != str else f"'{current_node.data}', "
            current_node = current_node.next
        value_list += f'{current_node.data}]' if type(current_node.data) != str else f"'{current_node.data}']"
        return value_list

    def __len__(self):
        return self.lenght

    def __getitem__(self, item):
        return self.get_value(item)

    def __setitem__(self, key, value):
        self.edit_value(key, value)

    def append_item(self, data):
        node = Node(data)
        if type(data) != self.type and self.type is not None:  # caso type for none, ele não entra
            raise TypeError(f'list only accepts type: {self.type}')
        if not self.tale:  # se a cauda for None (não existir ainda), a cabeça e a cauda apontarão para o mesmo nó com
            self.head = node  # o valor dado.
            self.tale = node
        else:  # se existir
            self.tale.next = node
            self.tale = node
        self.lenght += 1

    def lenght(self):
        return self.lenght

    def insert_item(self, index, data):
        if index >= self.lenght:
            self.append_item(data)
            return
        if index < 0:
            index += self.lenght# esse + 1 é só pra o insert funcionar igual ao do python
            if index < 0:  # se depois de eu somar com o tamanho o index ainda for menor que zero, eu digo que ele vai ser zero
                index = 0
        node = Node(data)
        if index == 0:
            node.next = self.head
            self.head = node
        else:
            current_node = self.head
            for i in range(index - 1):
                current_node = current_node.next
            node.next = current_node.next
            current_node.next = node
        self.lenght += 1

    def get_value(self, index):
        if self.lenght == 0:
            raise IndexError('this list has no item')
        if index < 0:
            index += self.lenght
        if index >= self.lenght or abs(index) > self.lenght:
            raise IndexError('list index out of range')
        current_node = self.head
        for i in range(index):
            current_node = current_node.next
        return current_node.data

    def get_index(self, value):
        if self.lenght == 0:
            raise IndexError('this list has no item')
        index = 0
        current_node = self.head
        while current_node.next is not None:
            if value == current_node.data:
                return index
            current_node = current_node.next
            index += 1
        if value == current_node.data:  # tive que colocar outro if, porque só com o if que está dentro do while ele não
            return index  # consegue verificar se a informação de cada nó é ou não igual ao meu valor.
        raise ValueError('value is not in list')

    def edit_value(self, index, new_value):
        if index < 0:
            index += self.lenght
        if index > self.lenght - 1 or index + self.lenght < 0:
            raise IndexError('index out of range')
        current_node = self.head
        for i in range(index):
            current_node = current_node.next
        current_node.data = new_value

    def remove_index(self, index=None):
        if self.lenght == 0:
            raise IndexError('remove_index from empty list')
        if index is None:
            index = self.lenght - 1
        if index < 0:
            index += self.lenght  #caso o index seja negativo, eu recebo o tamanho mais o index.
            # ex: index = -2; lenght = 5; 5 + (-2) = 3
        if index > self.lenght - 1 or index < 0:  # se o tamanho mais o index for menor que zero
            raise IndexError('index out of range')              # ele vai ter o index negativo, que não dá pra escolher

        if self.lenght == 1:  # se só existe um valor, a cabeça e a cauda apontam para o mesmo lugar.
            deleted_data = self.head.data
            self.head = None  # então eu tenho que cortar a ligação de ambas para deletar o nó.
            self.tale = None

            # obs se o index for 0 funciona da mesma forma
        elif index == 0:
            deleted_data = self.head.data
            self.head = self.head.next  # aqui a head e a tale apontam para o mesmo local (tamanho > que 1)
        elif index == self.lenght - 1:
            current_node = self.head
            while current_node.next.next:  # faço isso para parar um nó antes do final (tale)
                current_node = current_node.next
            deleted_data = self.tale.data
            self.tale = current_node
            self.tale.next = None
        else:
            current_node = self.head
            for i in range(index - 1):  # ele tem que parar um nó antes do que eu quero remover
                current_node = current_node.next  # (esse caso só cai se o index estiver no meio da lista)
            aux = current_node.next.next  # o auxiliar aponta para o nó a frente do que eu quero apagar
            deleted_data = current_node.next.data
            current_node.next = aux  # aqui o apontador deixa de apontar para o nó que eu quero a pagar e aponta para
            # o nó depois dele. assim eu apago o nó
        self.lenght -= 1
        return deleted_data  # aqui eu retorno a informação que foi deletada

    def remove_item(self, value):
        index = self.get_index(value)
        self.remove_index(index)

    def count_value(self, value):
        counter = 0
        current_node = self.head
        if value == current_node.data:
            counter += 1
        while current_node.next:
            current_node = current_node.next
            if value == current_node.data:
                counter += 1
        return counter

    def repeated_values(self):
        repeated_values = SimplyLinkedList()
        perc = self.head
        index = self.lenght - 1
        while perc.next:
            counter = 0  # coloco eles aqui porque preciso que eles sejam zerados
            aux = perc.next
            if perc.data not in repeated_values:  # verifico se o valor não está na lista de repetidos para eu não
                for i in range(index):            # o mesmo valor várias vezes.
                    if perc.data == aux.data:
                        counter += 1
                        if perc.data not in repeated_values:  # eu verifico se ele não está na lista de valores repetidos
                            repeated_values.append_item(perc.data)  # pra eu não contar várias vezes o mesmo
                    aux = aux.next
            if counter > 0:
                print(f'O valor {perc.data} repetiu {counter + 1} vezes')
            index -= 1  # faço isso pra ele não bugar e quando o número for verificado, ele não contrar mais ele
            perc = perc.next

    # def sort_lista(self, crescent=True):
    def sort_lista(self, reverse=False):
        if self.lenght <= 1:
            return
        if self.lenght == 2:
            if not reverse:
                if self.head.data > self.tale.data:
                    self.tale.next = self.head
                    self.head = self.tale
                    self.tale = self.tale.next
                    self.tale.next = None
            else:
                if self.head.data < self.tale.data:
                    self.tale.next = self.head
                    self.head = self.tale
                    self.tale = self.tale.next
                    self.tale.next = None
            return
        perc = self.head
        index = self.lenght - 1

        if not reverse:
            while perc.next:
                second_perc = perc.next
                menor_valor = perc
                for i in range(index):
                    if second_perc.data < menor_valor.data:
                        menor_valor = second_perc
                    second_perc = second_perc.next

                index -= 1
                if menor_valor.data == perc.data:
                    pass
                elif perc == self.head:
                    if perc.next == menor_valor: # se o perc estiver no inicio e o próximo for o menor valor
                        aux_depois = menor_valor.next
                        menor_valor.next = perc
                        perc.next = aux_depois
                        self.head = menor_valor
                    else:
                        aux_depois = menor_valor.next
                        aux_antes = self.head
                        while aux_antes.next != menor_valor:  # aqui eu verifico a posição de memória e não o valor
                            aux_antes = aux_antes.next
                        menor_valor.next = perc.next
                        aux_antes.next = perc
                        perc.next = aux_depois
                        self.head = menor_valor # é somente nessa ocasião que o head é o menor valor, e também é somente
                        #nela que eu preciso reconfigurar o head, porque das outras vezes ele já será o menor de todos,
                        # e o perc não vai começar mais nela, então não vai mudar o head.

                elif perc.next == menor_valor:  # se o menor valor for o proximo de perc
                    aux_depois = menor_valor.next
                    aux_antes_perc = self.head
                    while aux_antes_perc.next != perc:
                        aux_antes_perc = aux_antes_perc.next
                    menor_valor.next = perc
                    perc.next = aux_depois
                    aux_antes_perc.next = menor_valor
                else:
                    aux_depois = menor_valor.next
                    aux_antes_perc = aux_antes = self.head
                    while aux_antes_perc.next != perc:
                        aux_antes_perc = aux_antes_perc.next
                    while aux_antes.next != menor_valor:  # aqui eu verifico a posição de memória e não o valor
                        aux_antes = aux_antes.next

                    menor_valor.next = perc.next
                    perc.next = aux_depois
                    aux_antes.next = perc
                    aux_antes_perc.next = menor_valor

                perc = self.head
                while perc.next:
                    perc = perc.next
                self.tale = perc
                counter = (self.lenght - 1) - index #saber a posição que o perc estava
                perc = self.head
                for i in range(counter):
                    perc = perc.next
        else:
            while perc.next:
                second_perc = perc.next
                maior_valor = perc
                for i in range(index):
                    if second_perc.data > maior_valor.data:
                        maior_valor = second_perc
                    second_perc = second_perc.next

                index -= 1
                if maior_valor.data == perc.data:
                    pass
                elif perc == self.head:
                    if perc.next == maior_valor:  # se o perc estiver no inicio e o próximo for o menor valor
                        aux_depois = maior_valor.next
                        maior_valor.next = perc
                        perc.next = aux_depois
                        self.head = maior_valor
                    else:
                        aux_depois = maior_valor.next
                        aux_antes = self.head
                        while aux_antes.next != maior_valor:  # aqui eu verifico a posição de memória e não o valor
                            aux_antes = aux_antes.next
                        maior_valor.next = perc.next
                        aux_antes.next = perc
                        perc.next = aux_depois
                        self.head = maior_valor  # é somente nessa ocasião que o head é o menor valor, e também é somente
                        # nela que eu preciso reconfigurar o head, porque das outras vezes ele já será o menor de todos,
                        # e o perc não vai começar mais nela, então não vai mudar o head.

                elif perc.next == maior_valor:  # se o menor valor for o proximo de perc
                    aux_depois = maior_valor.next
                    aux_antes_perc = self.head
                    while aux_antes_perc.next != perc:
                        aux_antes_perc = aux_antes_perc.next
                    maior_valor.next = perc
                    perc.next = aux_depois
                    aux_antes_perc.next = maior_valor
                else:
                    aux_depois = maior_valor.next
                    aux_antes_perc = aux_antes = self.head
                    while aux_antes_perc.next != perc:
                        aux_antes_perc = aux_antes_perc.next
                    while aux_antes.next != maior_valor:  # aqui eu verifico a posição de memória e não o valor
                        aux_antes = aux_antes.next

                    maior_valor.next = perc.next
                    perc.next = aux_depois
                    aux_antes.next = perc
                    aux_antes_perc.next = maior_valor

                perc = self.head
                while perc.next:
                    perc = perc.next
                self.tale = perc
                counter = (self.lenght - 1) - index  # saber a posição que o perc estava
                perc = self.head
                for i in range(counter):
                    perc = perc.next


lista = SimplyLinkedList()
lista.append_item(10)
lista.append_item(18)
lista.append_item(4)
lista.append_item(0)
lista.append_item(5)
lista.append_item(3)
lista.append_item(0)
lista.append_item(-18)
lista.insert_item(-1, 129)
lista.sort_lista(reverse=True)
print(lista)
