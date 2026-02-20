
from collections import defaultdict

from bisect import bisect_left, bisect_right


class ConsistentHashing:
    def __init__(self, maxLength):
        self.maxLength = maxLength
        self.nodes = []
        self.data = {}
        self.node_positions = defaultdict(list)
        self.replica = defaultdict(list)
    
    def getPrevNextNodes(self, position):
        prevNode = None
        nextNode = None

        valueList = [node[1] for node in self.nodes]


        prev_idx = bisect_left(valueList, position)
        if prev_idx < len(valueList) and valueList[prev_idx] == position:
            prev_idx -= 1
        
        next_idx = bisect_right(valueList, position)
        
        
        prevNode = self.nodes[prev_idx] if prev_idx >= 0  else None
        nextNode = self.nodes[next_idx] if next_idx < len(self.nodes) else None

        if prevNode is None and self.nodes:
            prevNode = self.nodes[-1]
        if nextNode is None and self.nodes:
            nextNode = self.nodes[0]
        print(f"Previous Node: {prevNode}, Next Node: {nextNode}")
        return prevNode, nextNode
    
    def _addNode(self, node, position=None):

        print(f"Adding node: {node} at position: {position}")
        if position is None:
            position = hash(node) % self.maxLength
            print(f"Node: {node} has no position specified, assigned position: {position}")
        self.nodes.append((node, position))
        self.nodes.sort(key=lambda x: x[1])
        if len(self.nodes) == 1:
            self.node_positions[node] = []
            return
        prevNode,nextNode = self.getPrevNextNodes(position)
        
        if nextNode is None:
            print(f"No next node found for position: {position}, no keys reassigned")
            return
   
        list_of_keys = self.node_positions.get(nextNode[0], []).copy()
     
        for idx in list_of_keys:
         
            if idx[1] <= position:
                
                self.data[idx[0]] = [node, position]
                self.node_positions[node].append([idx[0], idx[1]])
                print(f"Key: {idx[0]} is reassigned to node: {node} at position: {position}")
                self.node_positions[nextNode[0]].remove(idx)
    

    def addNode(self, node, position=None,virtual_nodes=1):
      for i in range(virtual_nodes):
         virtual_node = f"{node}_{i}"
         self._addNode(virtual_node, position)
    
    def _removeNode(self, node, node_position):
        
       
        prevNode, nextNode = self.getPrevNextNodes(node_position)

        self.nodes.remove((node, node_position))

        if len(self.nodes) == 0:
            self.data.clear()
            self.node_positions.clear()
            print("All nodes removed, data cleared")
            return
           
        if node not in self.node_positions:
            print(f"No keys assigned to node: {node}, no keys reassigned")
            return
        for idx in self.node_positions.get(node, []):
            if nextNode:
                self.data[idx[0]] = [nextNode[0], nextNode[1]]
                self.node_positions[nextNode[0]].append([idx[0], idx[1]])
                print(f"Key: {idx[0]} is reassigned to node: {nextNode[0]} at position: {nextNode[1]}")
            else:
                self.data[idx[0]] = [prevNode[0], prevNode[1]]
                self.node_positions[prevNode[0]].append([idx[0], idx[1]])
                print(f"Key: {idx[0]} is reassigned to node: {prevNode[0]} at position: {prevNode[1]}")
        del self.node_positions[node]

    def removeNode(self, node):
        print(f"Removing node: {node}")

        nodesList = []
        for n, pos in self.nodes:
            if node in n:
                nodesList.append((n, pos))
        if not nodesList:
            print(f"Node: {node} not found")
            return
        for n, pos in nodesList:
            self._removeNode(n, pos)
 
    def replicate(self, key, node, replication_factor):
        if replication_factor <= 0:
            return
        realNodes = set([n[0].split('_')[0] for n in self.nodes])
        node_name = node.split('_')[0]
        cnt = 0
        for i in realNodes:
            if node_name not in i:
                self.replica[key].append(i)
                print(f"Key: {key} is replicated to node: {i}")
                cnt += 1
                if cnt >= replication_factor:
                    break     

    def getNode(self,key,replication_factor=0):

        if not self.nodes:
            return None
        
        if key in self.data:
            print(f"Key: {key} is already assigned to node: {self.data[key][0]} at position: {self.data[key][1]}")
            return self.data[key]
        
        position = hash(key) % self.maxLength
        print(f"Key: {key} has position: {position}")
        nodeValue = None
        for node, node_position in self.nodes:
            if position <= node_position:
                self.data[key] = [node,node_position]
                self.node_positions[node].append([key,position])
                print(f"Key: {key} is assigned to node: {node} at position: {node_position}")
                nodeValue = node
                break
        if nodeValue is None:
            # If position is greater than all node positions, assign to the first node
            self.data[key] = [self.nodes[0][0], self.nodes[0][1]]
            self.node_positions[self.nodes[0][0]].append([key,position])
            print(f"Key: {key} is assigned to node: {self.nodes[0][0]} at position: {self.nodes[0][1]}")
        
        self.replicate(key,nodeValue,replication_factor)

        return nodeValue
        

if __name__ == "__main__":
    print("----------Consistent Hashing----------")

    ds = ConsistentHashing(maxLength = 1000)
    
    # ds.addNode("Node1", 100)
    # ds.addNode("Node2", 200)
    # ds.addNode("Node3", 800)

    # ds.getNode("Key1")
    # ds.getNode("Key2")
    # ds.getNode("Key3")

    # ds.addNode("Node4", 500)
    # ds.addNode("Node5", 300)

    # ds.getNode("Key1")
    # ds.getNode("Key2")
    # ds.getNode("Key3")

    # ds.removeNode("Node2")
    # ds.removeNode("Node3")

    # ds.getNode("Key1")
    # ds.getNode("Key2")
    # ds.getNode("Key3")

    ds.addNode("Node1",virtual_nodes=3)
    ds.addNode("Node2",virtual_nodes=5)
    ds.addNode("Node3",virtual_nodes=2)

    ds.getNode("Key1")
    ds.getNode("Key2")
    ds.getNode("Key3")

    ds.addNode("Node4",virtual_nodes=4)
    ds.addNode("Node5",virtual_nodes=3)

    ds.getNode("Key1")
    ds.getNode("Key2")
    ds.getNode("Key3")  

    ds.removeNode("Node2")
    ds.removeNode("Node3")

    ds.getNode("Key1")
    ds.getNode("Key2")
    ds.getNode("Key3")







    
    


