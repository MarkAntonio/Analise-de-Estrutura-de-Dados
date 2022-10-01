class _No:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

    def __str__(self):
        return f'{self.valor} -> {self.proximo}'


class ListaSimples:
    def __init__(self):
        self.inicio = None
        self.tamanho = 0  # criei uma varíavel no contrutor (var. glob. da classe) que será um somatório para o tamanho;

    def __str__(self):
        return f'[{self.inicio}]'

    def tamanho(self):
        return self.tamanho

    def adicionar(self, valor):
        no = _No(valor)
        if not self.inicio:  # se for None eu posso começar pelo inicio.
            self.inicio = no       # se ele não for None quer dizer que tem algo na lista, então não posso sobreescrever
            # aqui o inicio recebe a classe nó, logo vira um objeto
        else:  # caso já exista algo na lista
            perc = self.inicio  # percorredor aponta para o self.inicio (logo ele é um objeto por enquanto)
            while perc.proximo is not None:  # enquanto o apontador apontar para algum valor
                perc = perc.proximo  # o percorredor agora aponta para o próximo nó
            perc.proximo = no  # o percorredor aponta para o objeto e pode acessá-lo agora
        self.tamanho += 1  # como a função adicionar() só roda uma vez, cada vez que roda é + 1 no tamanho;

    def inserir(self, index, valor):  # para inserir algo eu preciso saber do tamanho
        if index >= self.tamanho:  #caso o index seja maior ou igual ao tamanho, eu adiciono sempre no fim da lista;
            self.adicionar(valor)  # aqui tem que ser a função geral do contrutor (__init__),pois se eu colocar o nome
            # da variável, a proima variável não dará certo, porque essa é uma função que a lista pode ter qualquer nome
            return
        no = _No(valor)
        if index == 0:
            no.proximo = self.inicio  # o apontador inicial passa a apontar para o inicio da lista
            self.inicio = no  # agora o inicio (head) passa a ser um novo objeto vazio com o valor que passei
        else:  # se o index não for nem zero e nem no final da lista (maior ou do tamanho da lista)
            perc = self.inicio  # criarei um percorredor que começará apontando para o início (head)
            for i in range(index - 1):  # agora o farei um laço até um nó até do nó do index
                perc = perc.proximo  # o percoredor passa a aponta para o próximo nó
            no.proximo = perc.proximo  # o apontador do início passa a pontar para o apontador do percorredor
            perc.proximo = no  # e o perc agora aponta para o nó que aponta para o próximo que o perc estava
        self.tamanho += 1  # tamanho ganha + 1 um pois adicionei um valor, independente do nó da lista

    def get_index(self, index):
        # perc = self.inicio
        # index = 0
        # while perc.proximo is not None:
        #     if valor == perc.valor:
        #         return index
        #     perc = perc.proximo
        #     index += 1   # minha forma (confundi com o get_value)
        if self.tamanho == 0:  # se o tamanho for zero
            raise IndexError('Não existe elementos na lista')
        perc = self.inicio  # agora sim podemos usar o perc para apontar para o inicio da lista
        for i in range(index):  # o "i" só vai até o index que passei, pois preciso que ele percorra e aponte o nó
            perc = perc.proximo
        return perc.valor  # retorno o valor no nó que o perc está apontado baseado no index que passei

    def editar_index(self, index, valor):
        if self.tamanho == 0:
            raise IndexError('Não existe elementos na lista')  # quando ele lança uma excessão, o código para
        perc = self.inicio
        for i in range(index):
            perc = perc.proximo
        perc.valor = valor

    def remover_index(self, index=None):  # se eu não passar o index ele será None
        if self.tamanho == 0:
            raise ValueError('Não existe elementos na lista')
        perc = self.inicio  # o percorredor aponta para o inicio
        if index is None:  # se o index for None eu direi que ele é o último nó da lista
            index = self.tamanho - 1  # o index passa a apontar para o último valor da lista
        if index == self.tamanho - 1:  # isso só acontecera se eu quiser remover o últimoe elemento da lista
            for i in range(index - 1):  # aqui o percorredor aponta para o nó antes do que eu quero apontar
                perc = perc.proximo
            perc.proximo = None
        elif index == 0:
            perc = self.inicio  # o percorredor aponta pro inicio
            self.inicio = self.inicio.proximo   # o inicio aponta para o próximo nó
            perc.proximo = None  # o primeiro nó aponta pra None (corta a ligação com o restante)
            # mas nesse momento não é necessário pois escopos locais são deletados quando a função termina
            # perc = None
        # perc será None e será coletado pelo lixo, mas não precisa dizer, pois quando a função encerra ele desaparece
        else:
            for i in range(index - 1):  # aqui o percorredor aponta para o nó antes do que eu quero apontar
                perc = perc.proximo
             # perc.proximo = perc.proximo.proximo  -> posso fazer assim, mas farei diferente pra ficar mais organizado
            aux = perc.proximo.proximo
            # perc.proximo.proximo = None -> não preciso dizer que perc.proximo.proximo é none porque quando terminar
            # a função ela será deletada, pois é escopo local
            perc.proximo = aux
            # aux = None
            # não preciso dizer que aux ou perc é None, pois quando terminar a função eles desaparecem
            # (escopo local da função)


lista = ListaSimples()
lista.adicionar(10)
lista.adicionar('Samuel')
lista.adicionar(10.43)
print(lista)
print(lista.tamanho)
lista.inserir(58, "Ethanyel")
lista.inserir(4, 24)
lista.inserir(2, -65)
# lista -> [10, Samuel, 10.43, -65, Ethanyel, 24]
print(lista)
print(lista.get_index(1))
print(lista.get_index(0))
print(lista.get_index(4))
print('*' * 20)
testelista = [35, 52, 12, 45]
print(testelista.index(52))  # percebi que a função index do python retorna o index pelo valor e não retorna o valor
                                # pelo index. percebi também que se tiver um valor ex: 35, e eu procurar o valor 3, ele
                                # reparte o 35, vê que o 3 está em 35 pois 3 concatenado com o 5 é 35. porém ele não
                                # retorna nada, nem que ele está e nem faz um raise ValueError('Value is not in list'),
                                # mas o código não consegue prosseguir.
testelista[-1] = 101  # da mesma forma na função de editar o valor da lista pelo index, caso o index não exista, ele só
                     # trava mas não esta lançando nenhuma excessão
print(testelista)
testelista.pop()
print(testelista)
print('*' * 20)
lista.editar_index(4, 100.1)
# lista -> [10, Samuel, 10.43, -65, 100.1, 24]
print(lista)
lista.remover_index()
print(lista)
lista.remover_index(2)
print(lista)
lista.remover_index(0)
print(lista)
