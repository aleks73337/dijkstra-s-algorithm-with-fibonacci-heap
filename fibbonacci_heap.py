from typing import Any
import numpy as np
from numpy.core.defchararray import add

class Node:
    def __init__(self, key : int, value : Any) -> None:
        self.key = key
        self.value = value
        self.parent = None
        self.child = None
        self.left = None
        self.right = None
        self.degree = 0
        self.mark = False
    
    def __str__(self) -> str:
        return f"key: {self.key} "\
                f"parent: {self.parent is not None} "\
                f"child: {self.child is not None}, "\
                f"left: {self.left is not None}, "\
                f"right: {self.right is not None}, "\
                f"degree: {self.degree}, "\
                f"mark: {self.mark}"


class FibonacciHeap:
    def __init__(self) -> None:
        self.root_list = None
        self.min_node = None
        self.total_num_elements = 0
    
    def __add_to_root_list(self, node : Node):
        if self.root_list is None:
            self.root_list = node
        else:
            node.right = self.root_list.right
            node.left = self.root_list
            self.root_list.right.left = node
            self.root_list.right = node
    
    def __remove_from_root_list(self, node : Node):
        if not self.root_list:
            raise Exception("Root list is empty")
        if self.root_list == node:
            if self.root_list == self.root_list.right:
                self.root_list = None
                return
            else:
                self.root_list = node.right
        node.left.right = node.right
        node.right.left = node.left
        return

    def __itterate(self, head : Node = None):
        if head is None:
            head = self.root_list
        current = head
        while True:
            yield current
            if current is None:
                break
            current = current.right
            if (current == head):
                break

    def __find_min_node(self):
        if self.root_list is None:
            return None
        else:
            min = self.root_list
            for x in self.__itterate(self.root_list):
                if x.key < min.key:
                    min = x
            return min
    
    def __consolidate(self):
        if self.root_list is None:
            return
        ranks_mapping = [None] * self.total_num_elements
        nodes = [el for el in self.__itterate(self.root_list)]
        for node in nodes:
            degree = node.degree
            while ranks_mapping[degree] != None:
                other = ranks_mapping[degree]
                if node.key > other.key:
                    node, other = other, node
                self.__merge_nodes(node, other)
                ranks_mapping[degree] = None
                degree += 1
            ranks_mapping[degree] = node
        return
    
    def __merge_nodes(self, node1 : Node, node2 : Node):
        self.__remove_from_root_list(node2)
        node2.left = node2.right = node2
        self.__add_to_child_list(node1, node2)
        node1.degree += 1
        node2.parent = node1
        node2.mark = False
        return

    def __add_to_child_list(self, parent : Node, node : Node):
        if parent.child is None:
            parent.child = node
        else:
            node.right = parent.child.right
            node.left = parent.child
            parent.child.right.left = node
            parent.child.right = node

    def __remove_from_child_list(self, parent : Node, node : Node):
        if parent.child == parent.child.right:
            parent.child = None
        elif parent.child == node:
            parent.child = node.right
            node.right.parent = parent
        node.left.right = node.right
        node.right.left = node.left

    def __cut(self, node : Node, parent : Node):
        self.__remove_from_child_list(parent, node)
        parent.degree -= 1
        self.__add_to_root_list(node)
        node.parent = None
        node.mark = False
    
    def __cascading_cut(self, node : Node):
        parent = node.parent
        if parent is not None:
            if parent.mark is not None:
                parent.mark = True
            else:
                self.__cut(node, parent)
                self.__cascading_cut(parent) 

    def insert(self, key : int, value : Any) -> Node:
        newNode = Node(key, value)
        newNode.left = newNode.right = newNode
        self.__add_to_root_list(newNode)
        if self.min_node is not None:
            if self.min_node.key > newNode.key:
                self.min_node = newNode
        else:
            self.min_node = newNode
        self.total_num_elements += 1
        return newNode

    def deleteMin(self):
        min_node = self.min_node
        if min_node is not None:
            if min_node.child is not None:
                children = [el for el in self.__itterate(min_node.child)]
                for i in range(len(children)):
                    self.__add_to_root_list(children[i])
                    children[i].parent = None
            self.__remove_from_root_list(min_node)
            self.total_num_elements -= 1
            self.__consolidate()
            if min_node == min_node.right:
                self.min_node = None
                self.root_list = None
                # pass
            else:
                self.min_node = self.__find_min_node()
        return min_node.key if (min_node is not None) else None, min_node.value if (min_node is not None) else None
    
    def decreaseKey(self, node : Node, value : int):
        if value >= node.key:
            raise Exception("You can't decrease key on bigger value then now")
        node.key = value
        p = node.parent
        if p and (node.key < p.key):
            self.__cut(node, p)
            self.__cascading_cut(p)
        
        if node.key < self.min_node.key:
            self.min_node = node
        return

if __name__ == "__main__":
    heap = FibonacciHeap()
    for i in range(100):
        n = heap.insert(i)
        heap.decreaseKey(n, i - 10)
    for i in range(100):
        n = heap.deleteMin()
        print(n)