import hashlib

class ConsistentHashing:
    def _init_(self, num_slots=512):
        """
        Initialize the ConsistentHashing class.
        
        Parameters:
        num_slots (int): The number of slots in the hash ring. Default is 512.
        """
        self.num_slots = num_slots
        self.nodes = []  # List to store the nodes and their virtual replicas

    def _hash_virtual(self, node, replica):
        """
        Generate a hash value for a virtual replica of a node.
        
        Parameters:
        node (str): The identifier of the physical node.
        replica (int): The replica number of the node.
        
        Returns:
        int: The hashed key value.
        """
        # Convert the node identifier to a hash value using MD5
        node_hash = int(hashlib.md5(node.encode('utf-8')).hexdigest(), 16)
        # Calculate the position of the virtual node on the hash ring
        return (node_hash + replica + 2 * replica**2 + 25) % self.num_slots

    def add_node(self, node):
        """
        Add a physical node and its virtual replicas to the hash ring.
        
        Parameters:
        node (str): The identifier of the physical node.
        """
        # Add virtual nodes for the given physical node
        for i in range(9):  # Using K = 9 for 9 virtual replicas
            hashed_key = self._hash_virtual(node, i)
            self.nodes.append((hashed_key, node))  # Append (hashed_key, node) tuple
        # Sort the list of nodes to maintain the order on the hash ring
        self.nodes.sort()

    def remove_node(self, node):
        """
        Remove a physical node and its virtual replicas from the hash ring.
        
        Parameters:
        node (str): The identifier of the physical node to be removed.
        """
        # Filter out the node and its virtual replicas from the nodes list
        self.nodes = [n for n in self.nodes if n[1] != node]

    def get_node(self, key):
        """
        Get the physical node responsible for the given key.
        
        Parameters:
        key (int): The key for which the node is to be found.
        
        Returns:
        str: The identifier of the responsible physical node.
        """
        if not self.nodes:
            return None  # Return None if no nodes are available

        # Hash the key to find its position on the hash ring
        key_hash = key % self.num_slots
        # Find the first node with a hash value greater than or equal to the key_hash
        for h in self.nodes:
            if key_hash <= h[0]:
                return h[1]
        # If no such node is found, return the first node in the list (wrap around the ring)
        return self.nodes[0][1]
