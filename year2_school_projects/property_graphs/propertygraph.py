"""
File: propertygraph.py
Description: An implementation of a PropertyGraph consisting of
Node and Relationship objects. Nodes and Relationships carry
properties. Property graphs are used to represent connected knowledge.
"""
class Node:
    def __init__(self, name, category, props=None):
        """ Class constructor """
        # sets name category and properties
        self.name = name
        self.category = category
        self.props = props


    def __getitem__(self, key):
        """ Fetch a property from the node using []
        return None if property doesn't exist """
        if self.props:
            # gets property
            return self.props[key]
        else:
            # returns none if property doesn't exist
            return None

    def __setitem__(self, key, value):
        """ Set a node property with a specified value using [] """
        # sets the key to value of a node
        self.props[key] = value
        return Node(self.name, self.category, self.props)

    def __eq__(self, other):
        """ Two nodes are equal if they have the same
        name and category irrespective of their properties """
        # if the names and categories are te same
        return self.name == other.name and self.category == other.category

    def __hash__(self):
        """ By making Nodes hashable we can now
        store them as keys in a dictionary! """
        # citation for how to use hash function: https://stackoverflow.com/questions/17585730/what-does-hash-do-in-python
        return hash((self.name, self.category))

    def __repr__(self):
        """ Output the node as a string in the following format:
        name:category<tab>properties.
        Note: __repr__ is more versatile than __str__ """
        # prints different f strings based on props
        if self.props:
            return f'{self.name}:{self.category}\t{self.props}'
        else:
            return f'{self.name}:{self.category}'

class Relationship:
    def __init__(self, category, props=None):
        """ Class constructor """
        # Sets categories and properties
        self.category = category
        self.props = props

    def __getitem__(self, key):
        """ Fetch a property from the node using []
        return None if property doesn't exist """
        if self.props:
            # Returns props[key] if property exists
            return self.props[key]
        else:
            return None

    def __setitem__(self, key, value):
        """ Set a node property with a specified value using [] """
        # Sets a value to dictionary using key, value
        self.props[key] = value
        return Relationship(self.category, self.props)

    def __repr__(self):
        """ Output the relationship as a string in the following format:
        :category<space>properties.
        Note: __repr__ is more versatile than __str__ """
        # Uses fstring to format string
        if self.props:
            return f'{self.category} {self.props}'
        else:
            return f'{self.category}'
class PropertyGraph:
    def __init__(self):
        """ Construct an empty property graph """
        # initializes empty dictionary
        self.graph = {}

    def add_node(self, node):
        """ Add a node to the property graph """
        # Initializes empty list for nodes
        self.graph[node] = []
        return self.graph

    def add_relationship(self, src, targ, rel):
        """ Connect src and targ nodes via the specified directed relationship.
        If either src or targ nodes are not in the graph, add them.
        Note that there can be many relationships between two nodes! """
        # Checks if src and targ are already present in the node and adds if not
        if src not in self.graph.keys():
            self.graph[src] = []
        if targ not in self.graph.keys():
            self.graph[targ] = []
        # Appends key and value to dictionary
        return self.graph[src].append((targ, rel))

    def get_nodes(self, name=None, category=None, key=None, value=None):
        """ Return the SET of nodes matching all the specified criteria.
        If the criterion is None it means that the particular criterion is ignored.
        """
        # Initializes empty node list
        node_list = []
        # Iterates through nodes using key values
        for node in self.graph.keys():
            # If all conditions are present
            if name and category is not None and key is not None and value is not None:
                # Checks if current node matches
                if node.name == name and node.category == category and node.props[key] == value:
                    # appends node to list
                    node_list.append(node)
            # Checks if name is present
            if name and category is not None:
                if node.name == name and node.category == category:
                    node_list.append(node)
            # Checks if category is present
            if category and name is None:
                if node.category == category:
                    node_list.append(node)
            # Checks if name and category are None
            if name and category is None:
                if name == node.name:
                    node_list.append(node)
        return set(node_list)

    def adjacent(self, node, node_category=None, rel_category=None):
        """ Return a set of all nodes that are adjacent to node.
        If specified include only adjacent nodes with the specified node_category.
        If specified include only adjacent nodes connected via relationships with
        the specified rel_category """
        # Initiales empty adjacency list
        adjacent_node_list = []
        # Iterates through the node and adjacent node relationship tuple
        for obj_node, adjacent_nodes in self.graph.items():
            # If the node and category are not present
            if node_category and rel_category is None:
                # If the node and object names are equal
                if obj_node.name == node.name:
                    # If there is more than one relationship for that node and the categories match
                    if len(adjacent_nodes) >= 1 and obj_node.category == node_category:
                        # Appends each node to list
                        adjacent_node_list = [node for node in adjacent_nodes]
            # If the rel_category is present
            if rel_category and node_category is None:
                if obj_node.name == node.name:
                    # If there is one relationship for that node
                    if len(adjacent_nodes) >= 1:
                        for single_node in adjacent_nodes:
                            # accesses the rel_category from the adjacent node inside the tuple
                            if rel_category == single_node[1].category:
                                adjacent_node_list.append(single_node)
            # if the node and category are present
            if node_category and rel_category:
                if obj_node.name == node.name:
                    # If there is one relationship for that node
                    if len(adjacent_nodes) >= 1:
                        for single_node in adjacent_nodes:
                            # accesses the rel_category from the adjacent node inside the tuple
                            if rel_category == single_node[1].category and obj_node.category == node_category:
                                adjacent_node_list.append(single_node)
            # If there is no node or rel_category present
            if node_category is None and rel_category is None:
                if obj_node.name == node.name:
                    if len(adjacent_nodes) >= 1:
                        adjacent_node_list = [node for node in adjacent_nodes]

        return set(adjacent_node_list)

    def subgraph(self, nodes):
        """ Return the subgraph as a PropertyGraph consisting of the specified
        set of nodes and all interconnecting relationships """
        # creates sub for propertygraph object
        sub = PropertyGraph()
        # Iterates through input nodes
        for node in nodes:
            # Adds nodes to graph
            sub.add_node(node)
            # If the node is in the graph already
            if node in self.graph.keys():
                # Iterates through relationship tuple in adjacency list
                for relationship_tuple in self.adjacent(node):
                    # If the adjacent node is in graph
                    if relationship_tuple[0] in nodes:
                        # Adds relationship
                        sub.add_relationship(node, relationship_tuple[0], relationship_tuple[1])
        return sub

    def __repr__(self):
        """ A string representation of the property graph
        Properties are not displaced.
        Node
        Relationship Node
        Relationship Node
        .
        .
        etc.
        Node
        Relationship Node
        Relationship Node
        .
        .
        etc.
        .
        .
        etc.
        """
        # citation to add to an empty string: https://discuss.python.org/t/how-to-make-an-addition-operetion-using-f-strings/16034/3
        graph_string = ""
        for node, relationship_nodes in self.graph.items():
            graph_string += f'"{node}"\n'
            for adjacent_node, relationship_node in relationship_nodes:
                graph_string += f'"{relationship_node} {adjacent_node}""\n'
        return graph_string

