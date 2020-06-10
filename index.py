class Node(object):
    '''
    Базовый узел объекта.
    Каждый узел хранит ключи и значения. Ключи не являются уникальными для                 
    каждого значения,поскольку такие значения хранятся в виде списка под 
    каждым ключом.	
    Атрибуты: order (int): максимальное количество ключей, которое может   
    содержать каждый узел.
    '''
    keys: object

    def __init__(self, order):
        self.order = order
        self.keys = []
        self.values = []
        self.leaf = True

    def add(self, key, value):
        '''
        Добавляет пару ключ-значений к узлу.
        '''
        if not self.keys:
            self.keys.append(key)
            self.values.append([value])
            return None

        for i, item in enumerate(self.keys):
            if key == item:
                self.values[i].append(value)
                break

            elif key < item:
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.values = self.values[:i] + [[value]] + self.values[i:]
                break
    # i отстаёт на одно значение, key[i] - i+1й элемент списка -> элемент №4
            elif i + 1 == len(self.keys):
                self.keys.append(key)
                self.values.append([value])
                break

    def split(self):
        '''
        Разбивает узел на две части и сохраняет их как дочерние узлы.
        '''
        left = Node(self.order)
        right = Node(self.order)
        mid = self.order // 2 - 1
	
        left.keys = self.keys[:mid]
        left.values = self.values[:mid]

        right.keys = self.keys[(mid):]
        right.values = self.values[(mid):]

        self.keys = [right.keys[0]]

        right.keys = right.keys[1:]
        right.values = right.values[1:]

        self.values = [left, right]
        self.leaf = False

    def is_full(self):
        '''
        Возвращает True, если узел заполнен.
        '''
        return len(self.keys) == self.order

    def show(self, counter=0):
        '''
        Печатает ключи на каждом уровне.
        '''
        print(counter, str(self.keys))

        if not self.leaf:
            for item in self.values:
                item.show(counter + 1)

class BPlusTree(object):
    '''
    B+ tree object, состоящий из узлов.
    Узлы будут автоматически разделены на два, после заполнения. Когда 
    Происходит раскол, ключ будет 'плавать' вверх и будет вставлен в  
    родительский узел для того,чтобы действовать как стержень.
    Атрибуты:
        order (int): максимальное количество ключей, которое модет содержать 
    каждый узел.
    '''
    def __init__(self, order=8):
        self.root = Node(order)

    def _find(self, node, key):
        '''
        Для данного узла и ключа возвращает индекс, где ключ должен быть
        вставлен и список значений по этому индексу.
        '''
        for i, item in enumerate(node.keys):
            if key < item:
                return node.values[i], i

        return node.values[i + 1], i + 1

    def _merge(self, parent, child, index):
        '''
        Для родительского и дочернего узла извлекает свободый элемент из 
        дочернего и вставляет в ключи родителя. Вставляет значения от 
        ребенка в значения родителя.
        '''
        parent.values.pop(index)
        pivot = child.keys[0]

        for i, item in enumerate(parent.keys):
            if pivot < item:
                parent.keys = parent.keys[:i] + [pivot] + parent.keys[i:]
                parent.values = parent.values[:i] + child.values +                    
                parent.values[i:]
                break

            elif i + 1 == len(parent.keys):
                parent.keys += [pivot]
                parent.values += child.values
                break

    def insert(self, key, value):
        '''
        Вставляет пару ключ-значений после перехода к конечному узлу.
        Если листовой узел заполнен, разделяет листвой узел на две части 
        '''
        parent = None
        child = self.root

        while not child.leaf:
            parent = child
            child, index = self._find(child, key)

        child.add(key, value)

        if child.is_full():
            child.split()

            if parent and not parent.is_full():
                self._merge(parent, child, index)

    def retrieve(self, key):
        '''
        Возвращает значение для данного ключа и None, если ключ не 
        существует    
        '''
        child = self.root

        while not child.leaf:
            child, index = self._find(child, key)

        for i, item in enumerate(child.keys):
            if key == item:
                return child.values[i]

        return None

    def show(self):
        '''
        Печатает ключи на каждом уровне.
        '''
        self.root.show()

def demo_node():
    print('Initializing node...')
    node = Node(order=4)

    print('\nInserting key a...')
    node.add('a', 'alpha')
    print('Is node full?', node.is_full())
    node.show()

    print('\nInserting keys b, c, d...')
    node.add('b', 'bravo')
    node.add('c', 'charlie')
    node.add('d', 'delta')
    print('Is node full?', node.is_full())
    print(len(node.keys))
    node.show()

    print('\nSplitting node...')
    node.split()
    node.show()

def demo_bplustree():
    print('Initializing B+ tree...')
    bplustree = BPlusTree(order=4)

    print('\nB+ tree with 1 item...')
    bplustree.insert('a', 'alpha')
    bplustree.show()

    print('\nB+ tree with 2 items...')
    bplustree.insert('b', 'bravo')
    bplustree.show()

    print('\nB+ tree with 3 items...')
    bplustree.insert('c', 'charlie')
    bplustree.show()

    print('\nB+ tree with 4 items...')
    bplustree.insert('d', 'delta')
    bplustree.show()

    print('\nB+ tree with 5 items...')
    bplustree.insert('e', 'echo')
    bplustree.show()

    print('\nB+ tree with 6 items...')
    bplustree.insert('f', 'foxtrot')
    bplustree.show()

    print('\nRetrieving values with key e...')
    print(bplustree.retrieve('e'))

if __name__ == '__main__':
    demo_node()
    print('\n')
    demo_bplustree()
