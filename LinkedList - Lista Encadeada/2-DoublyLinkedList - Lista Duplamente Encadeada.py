class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.previous = None

    # def __str__(self):
    #     return f'{self.data}, {self.next}' if self.next else f'{self.data}'


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tale = None
        self.lenght = 0

    def __str__(self):
        if self.lenght == 0:
            return '[]'
        value_list = '['
        perc = self.head
        while perc.next:
            value_list += f'{perc.data}, ' if type(perc.data) != str else f"'{perc.data}', "
            perc = perc.next
        value_list += f'{perc.data}]' if type(perc.data) != str else f"'{perc.data}']"
        return value_list

    def __len__(self):
        return self.lenght

    def __getitem__(self, index):
        return self.get_value(index)

    def __setitem__(self, key, value):
        self.edit_value(key, value)

    def _percorrer(self, perc, counter, next):
        for i in range(counter):
            if next:
                perc = perc.next
            else:
                perc = perc.previous
        return perc

    def _get_perc_index(self, index):
        if index > self.lenght - 1 or index < 0:
            raise IndexError('index out of range')
        if index == 0:
            return self.head
        elif index == self.lenght - 1:
            return self.tale
        else:
            half = (self.lenght - 1) // 2
            if index <= half:
                next = True
                perc = self.head
                count = index
            else:
                next = False
                perc = self.tale
                count = (self.lenght - 1) - index
            return self._percorrer(perc, count, next)

    def _get_perc_value(self, value):
        index = self.get_index(value)
        return self._get_perc_index(index)

    def _get_index_by_perc(self, perc):
        if perc is self.head:
            return 0
        if perc is self.tale:
            return self.lenght - 1
        current_node = self.head
        while current_node.next:
            if perc is current_node:
                return self.get_index(perc.data)
            current_node = current_node.next

    def append_item(self, data):
        node = Node(data)
        if self.lenght == 0:
            self.head = node
            self.tale = node
            self.lenght += 1
            return
        self.tale.next = node  # o próximo (tanto da cauda quando da cabeça) aponta para o novo nó
        aux = self.tale  # coloco um auxiliar para guardar a posição do nó que a cauda está
        self.tale = self.tale.next  # a cauda aponta para o próximo, que é o novo nó
        self.tale.previous = aux  # o anterior da cauda agora aponta para o nó que a cauda estava
        self.lenght += 1

    def get_index(self, data):
        if self.lenght == 0:
            raise IndexError('list is empty')
        index_start = 0
        index_end = self.lenght - 1
        perc_start = self.head
        perc_end = self.tale
        if self.lenght % 2 == 0:
            for i in range(self.lenght // 2):
                if perc_start.data == data:
                    return index_start
                if perc_end.data == data:
                    return index_end
                perc_start = perc_start.next
                perc_end = perc_end.previous
                index_start += 1
                index_end -= 1
        else:
            while perc_start != perc_end:
                if perc_start.data == data:
                    return index_start
                if perc_end.data == data:
                    return index_end
                perc_start = perc_start.next
                perc_end = perc_end.previous
                index_start += 1
                index_end -= 1
            if perc_start.data == data:
                return index_start
        raise IndexError(f'{data} not exists')

    def get_value(self, index):
        # if index < 0:
        #     index += self.lenght
        # if index > self.lenght - 1 or index + self.lenght < 0:
        #     raise IndexError('index out of range')
        return self._get_perc_index(index).data

    def edit_value(self, index, new_value):
        if index < 0:
            index += self.lenght
        if index > self.lenght - 1 or index + self.lenght < 0:
            raise IndexError('index out of range')

        perc = self._get_perc_index(index)
        perc.data = new_value

    def insert_item(self, index, data):
        if index >= self.lenght:
            self.append_item(data)
            self.lenght += 1
            return

        node = Node(data)
        if index == 0:
            node.next = self.head
            self.head.previous = node
            self.head = node
            self.lenght += 1
            return

        if index < 0:
            index += self.lenght + 1 # esse + 1 é só pra o insert funcionar igual ao do python
            if index < 0:  # se depois de eu somar com o tamanho o index ainda for menor que zero, eu digo que ele vai ser zero
                index = 0

        perc = self._get_perc_index(index - 1) # é o index - 1 porque eu quero o perc anterior
        # ao nó que eu quero inserir.
        if index <= self.lenght // 2:
            aux = perc.next
            aux.previous = node
            perc.next = node
            node.previous = perc
            node.next = aux
        else:
            aux = perc.previous
            aux.next = node
            perc.previous = node
            node.next = perc
            node.previous = aux
        self.lenght += 1

    def remove_index(self, index=None):
        if self.lenght == 0:
            raise IndexError('list is empty')
        if index is None:
            index = self.lenght - 1
        if index < 0:
            index += self.lenght
        if index > self.lenght - 1 or index < 0:
            raise IndexError('index out of range')
        if index == self.lenght - 1:
            deleted_data = self.tale.data
            aux = self.tale.previous
            self.tale.previous = None
            aux.next = None
            self.tale = aux
        elif index == 0:
            deleted_data = self.head.data
            self.head = self.head.next
            self.head.previous = None
        else:
            perc = self._get_perc_index(index - 1) #index - 1 porque eu quero parar uma casa antes
            # do nó que eu quero apagar

            if index <= (self.lenght - 1 // 2):
                aux = perc.next
                deleted_data = aux.data
                aux.previous = None
                perc.next = aux.next
                aux.next.previous = perc
                aux = None
            else:
                aux = perc.previous
                deleted_data = aux.data
                aux.next = None
                perc.previous = aux.previous
                aux.previous.next = perc
                aux.previous = None
        self.lenght -= 1
        return deleted_data

    def remove_item(self, value):
        index = self.get_index(value)
        self.remove_index(index)

    def count_item(self, value):
        counter = 0
        perc = self.head
        while perc.next:
            if perc.data == value:
                counter += 1
            perc = perc.next
        if perc.data == value:
            counter += 1
        return counter

    def repeated_items(self):
        if self.lenght == 0:
            raise IndexError('list is empty')
        repeated_values = DoublyLinkedList()
        perc = self.head
        index = self.lenght - 1
        while perc.next:
            counter_repeated = 0  # toda vez eu tenho que zerar a contagem.
            aux = perc.next
            for i in range(index):
                if perc.data == aux.data:
                    counter_repeated += 1
                aux = aux.next
            if counter_repeated > 0 and perc.data not in repeated_values:
                repeated_values.append_item(perc.data)
                print(f'value {perc.data} has repeated {counter_repeated + 1} times.')
            index -= 1
            perc = perc.next

    def _sorting(self, p, perc, perc_anterior):
        if perc is self.tale and self.lenght == 2:
            perc.next = perc_anterior
            perc_anterior.previous = perc
            perc.previous = None
            perc_anterior.next = None
            self.head = perc
            self.tale = perc_anterior
        elif perc_anterior is self.head:
            perc_anterior.next = perc.next
            perc.next.previous = perc_anterior
            perc_anterior.previous = perc
            perc.next = perc_anterior
            perc.previous = None
            self.head = perc
        elif perc is self.tale:
            perc.next = perc_anterior
            perc_anterior.previous.next = perc
            perc.previous = perc_anterior.previous
            perc_anterior.previous = perc
            perc_anterior.next = None
            self.tale = perc_anterior
        else:
            perc_anterior.next = perc.next
            perc.previous = perc_anterior.previous
            perc.next.previous = perc_anterior
            perc.next = perc_anterior
            perc_anterior.previous.next = perc
            perc_anterior.previous = perc
        p -= 1
        perc_anterior = perc.previous
        return p, perc, perc_anterior

    def sort_lista(self, reverse=False):
        if self.lenght <= 1:
            return

        if not reverse:
            for p in range(1, self.lenght):
                perc = self._get_perc_index(p)
                perc_anterior = perc.previous
                while p > 0 and perc_anterior.data > perc.data:
                    p, perc, perc_anterior = self._sorting(p, perc, perc_anterior)
        else:
            for p in range(1, self.lenght):
                perc = self._get_perc_index(p)
                perc_anterior = perc.previous
                while p > 0 and perc_anterior.data < perc.data:
                    p, perc, perc_anterior = self._sorting(p, perc, perc_anterior)


lista = DoublyLinkedList()
lista.append_item(9)
lista.append_item(0)
lista.append_item(0)
lista.append_item(45)
lista.append_item(3)
lista.append_item(4)
lista.append_item(1)
lista.append_item(2)
lista.append_item(1)
lista.append_item(-17)
lista.append_item(-4)
lista.append_item(3)
lista.append_item(-4)
print(lista)
lista.sort_lista()
print(lista)
