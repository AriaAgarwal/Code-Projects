"""
Property Graph Unit tests using pytest
"""

import pytest
from propertygraph import Node, Relationship, PropertyGraph

@pytest.fixture
def P():
    # Creates a Node object with the name Spencer and category of Person
    return Node("Spencer", "Person")

@pytest.fixture
def P2():
    # Creates a Node object with the name Spencer and category of Person
    return Node("Mary", "Person")
@pytest.fixture
def B():
    # Creates Node object with the name Cosmo, category of Book and property as a dictionary with a price
    return Node("Cosmo", "Book", {"price": "35"})

@pytest.fixture
def B2():
    # creates Node object that has the name Algebra, is a book and has an empty list of properties
    return Node("Algebra", "Book", {})
@pytest.fixture
def R():
    # creates Relationship object with the relationship bought
    return Relationship("Bought", {"year_bought": "2024"})

@pytest.fixture
def G():
    # Creates property graph object
    return PropertyGraph()

def test_constructor(P, B, R, G):
    """ Tests the constructor to determine if objects were created properly
    Parameters
    P : Node object to represent a Person
    B: Node object to represent a Book
    R: Relationship object to represent a Relationship
    G: PropertyGraph opbect to represent a PropertyGraph
    """
    # checks if constuctor was able to create Node objects
    assert isinstance(P, Node), "Constructor failed to create a Node object"

    # Checks if Constructor assigns Node attributes correctly
    assert isinstance(B, Node), "Constructor failed to create a Node object"
    assert B.name == "Cosmo", "Constructor did not assign name correctly"
    assert B.category == "Book", "Constructor did not assign book correctly"
    assert B.props == {"price": "35"}, "Constructor did not assign props correctly"

    # checks if constuctor was able to create Relationship and PropertyGraph objects
    assert isinstance(R, Relationship), "Constructor failed to create a Relationship object"
    assert R.category == "Bought", "Constructor failed to assign category correctly"
    assert isinstance(G, PropertyGraph), "Constructor failed to create a PropertyGraph object"

def test_getitem(P, B, R):
    """ Tests getting the item of Nodes and Relationships
    Parameters
    P : Node object to represent a Person
    B: Node object to represent a Book
    R: Relationship object to represent a Relationship
    """
    # Checks if the price was able to
    assert B["price"] == "35", "Failed to get item"
    # If there are no properties should return None
    assert P["price"] == None, "If there is no property, should be None"
    # Only nodes that are Book nodes should have properties
    if P.category == "Person":
        assert P.props == None, "If the Node is Person category, should not have a properties"

    # Gets the property for Relationship for given key value
    assert R["year_bought"] == "2024", "Failed to assign property to Relationship"
    R.props = None
    assert R["year_bought"] == None, "If there are no properties, should be none"

def test_setitem(B2, B, R):
   """ Tests getting the item of Nodes and Relationships
    Parameters
    B2 : Node object to represent a Book
    B: Node object to represent a Book
    R: Relationship object to represent a Relationship
   """
   # tests adding a property to a node that does not have any yet
   B2["price"] = "35"
   assert B2["price"] == "35", "The value was not set correctly"

   # testing adding more properties to exisitng properties
   B["author"] = "Ocean Vuong"
   assert B["author"] == "Ocean Vuong", "The value was not set"

   # Adding a new property to relationship - who the book was reccomended to Spencer by
   R["reccomended_by"] = "Aria"
   assert R["reccomended_by"] == "Aria", "The value was not set"


def test_eq(P,B):
    """ Checks if the names are compared accurately
        Parameters
        P : Node object to represent a Person
        B: Node object to represent a Book
        R: Relationship object to represent a Relationship
    """
    # Checks if the names are compared accurately
    assert P.name == P.name, "Equality of names failed"
    assert B.name == B.name, "Equality of names failed"
    # Checks if the categories are compared accurately
    assert P.category == P.category, "Equality of categories failed"
    assert B.category == B.category, "Equality of categories failed"

    # Checks if the name and categories are compared accurately
    assert P.name != B.name, "Inequality of names failed"
    assert P.category != B.category, "Inequality of category failed"

    # Checks with both conditions together
    assert P == P, "Equality of entire node failed"
    assert B == B, "Equality of entire node failed"
    assert B != P, "Inquality of entire node failed"

    # If the name and category is the same but properties are different
    P.name = B.name
    P.category = B.category
    assert P == B, "Should be the same irrespective of the Properties being different"

def test_hash(P,B):
    """ Checks if the hash values are compared accurately
            Parameters
            P : Node object to represent a Person
            B: Node object to represent a Book
    """
    # If the name and category is different, hash values should not match
    assert hash(P) != hash(B), "Hash values should not match"

    # If the name and category is the same hash values should match
    P.name = B.name
    P.category = B.category
    assert hash(P) == hash(B), "Hash values should match irrespective of different Properties"


def test_add_node(P, G):
    """ Checks if the nodes are added properly"""
    # adds a node P
    G.add_node(P)
    assert P in G.graph.keys(), "Failed to add node"

def test_add_relationship(P, B, G, R, B2):
    """ Checks if the relationship values are added
    P : Node object to represent a Person
    B: Node object to represent a Book
    G: PropertyGraph opbect to represent a PropertyGraph
    R: Relationship object to represent a Relationship
    B2: Node object to represent a Book
    """
    # Adds relationship between Spencer and Cosmo which is he Bought it
    G.add_relationship(P,B,R)
    # Checks if keys were actually added
    assert P in G.graph.keys(), "Failed to add key"
    assert B in G.graph.keys(), "Failed to add key"
    for value in G.graph.values():
        if value:
            # Checks if tuple was added correctly
            assert value[0] == (B, R), "Failed to add tuple value"
    # Checks if correct amount of graphs were added
    assert len(G.graph.values()) == 2 ,"Failed to add 2 nodes, one for Spencer and one for the Book"

    # Test to make new relationship and target node while keeping the source node the same
    R1 = Relationship("Read", {"Author": "Rick"} )
    G.add_relationship(P,B2,R1)
    for value in G.graph.values():
        # Iterates through values in graph dictionary
        # If value
        if value:
            # If there is more than 1 value
            if len(value) >= 1:
                # Should be two tuples/nodes for Spencer now to Cosmo and Algebra
                assert len(value) == 2, "Didn't add second node"
    # Should be 3 nodes total, 1 for Spencer one for Cosmo and one for Algebra
    assert len(G.graph.values()) == 3, "Failed to add 3 nodes, one for Spencer and 2 for the Books"
    # checks to see if B2 was added
    assert B2 in G.graph.keys(), "Did not add B2 even though was missing from keys"

    # Checks to see if new Person is added in add_relationship if not added in add_node
    P2 = Node("Aria", "Person")
    G.add_relationship(P2, B2, R1)
    assert P2 in G.graph.keys(), "Did not add P2 even though was missing from keys"
    assert len(G.graph.values()) == 4, "Failed to add 4 nodes, 2 for People and 2 for the Books"


def test_get_node(P, P2, B, B2, R, G):
    """ Checks if nodes can be extracted
        P : Node object to represent a Person
        P2 : Node object to represent a Person
        B: Node object to represent a Book
        B2: Node object to represent a Book
        G: PropertyGraph opbect to represent a PropertyGraph
        R: Relationship object to represent a Relationship
    """
    # Adds relationships
    G.add_relationship(P, B, R)
    G.add_relationship(P, B2, R)
    G.add_relationship(P2, B2, R)
    # Checks if there are 4 nodes, 2 books and 2 people
    assert len(G.graph.values()) == 4, "Did not create correct number of nodes"
    # Checks when all parameters are given
    assert len(G.get_nodes("Cosmo", "Book", "price", "35")) == 1, "Did not get correct number of nodes"
    # Checks when only name and category are given
    assert len(G.get_nodes("Mary", "Person")) == 1, "Did not get correct number of nodes"
    assert len(G.get_nodes("Spencer", "Person")) == 1 , "Did not get correct number of nodes"
    # Checks when only category is given
    assert len(G.get_nodes(category = "Person")) == 2, "Did not get correct number of nodes"
    # Checks when only name is given
    assert len(G.get_nodes(name="Spencer")) == 1, "Did not get correct number of nodes"

def test_adjacent_nodes(P, P2, B, B2, R, G):
    """ Checks for adjacent nodes
            P : Node object to represent a Person
            P2 : Node object to represent a Person
            B: Node object to represent a Book
            B2: Node object to represent a Book
            G: PropertyGraph opbect to represent a PropertyGraph
            R: Relationship object to represent a Relationship
        """
    # Adds relationships
    G.add_relationship(P, B, R)
    G.add_relationship(P, B2, R)
    G.add_relationship(P2, B2, R)
    # Checks if there are 4 nodes, 2 books and 2 people
    # checks when node and category are given
    assert len(G.graph.values()) == 4, "Did not create correct number of nodes"
    assert len(G.adjacent(P, "Person")) == 2, "Did not get correct number of nodes"
    assert len(G.adjacent(P2, "Person")) == 1, "Did not get correct number of nodes"
    # checks when node, category and relation are given
    assert len(G.adjacent(P, "Person", "Bought")) == 2, "Did not get correct number of nodes"
    # checks when node is given
    assert len(G.adjacent(P)) == 2, "Did not get correct number of nodes"
    # checks when category is not given
    assert len(G.adjacent(P, None, "Bought")) == 2, "Did not get correct number of nodes"

def test_subgraph(P,P2,B,B2,R,G):
    # Creates graph using property graph object
    G.add_relationship(P, B, R)
    G.add_relationship(P, B2, R)
    G.add_relationship(P2, B2, R)

    # creates subgraph of larger graph
    sg = G.subgraph([P2, B2])
    # checks if the right keys are in subgraph nodes
    assert P2 in sg.graph.keys()
    assert B2 in sg.graph.keys()


def test_repr(P,B,R,G):
    """Tests printing out the string representation"""
    # Testing Node printing with and without properties
    assert repr(P) == "Spencer:Person", "Representation failed"
    assert repr(B) == "Cosmo:Book\t{'price': '35'}", "Representation Failed"

    # Testing Relationship printing with and without properties
    assert repr(R) == "Bought {'year_bought': '2024'}"
    R.props = None
    assert repr(R) == "Bought"

    # Testing string representation of graph
    R = Relationship("Bought")
    G.add_relationship(P, B, R)
    assert repr(G) == ('"Spencer:Person"\n'
    '"Bought Cosmo:Book\t{\'price\': \'35\'}""\n'
    '"Cosmo:Book\t{\'price\': \'35\'}"\n')
