class Node(object):
    def __init__(self, parent = None, id = None, child =[], data = None, type = any):
        self.parent = parent
        self.child = child
        self.id = id
        self.type = type
        self.data = data
    
    def add_child(self,name, data):
        new_child = Node(data=data, id=name,type = any, parent=self)
        self.child.append(new_child)
        return new_child

ode = Node(parent=None, id="S", data=None,)
print(ode.id, ode.child)
ode.add_child("sup", "hey")
print(ode.child[0].id)