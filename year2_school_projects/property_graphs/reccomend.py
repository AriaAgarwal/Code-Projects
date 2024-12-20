"""
/Users/ariaagarwal/anaconda3/envs/ds/bin/python /Users/ariaagarwal/Desktop/reccomend.py
Original Graph
 "Emily:Person"
"Knows Spencer:Person""
"Bought Database Design:Book	{'price': '195.00'}""
"Spencer:Person"
"Knows Emily:Person""
"Knows Brendan:Person""
"Bought Cosmos:Book	{'price': '17.00'}""
"Bought Database Design:Book	{'price': '195.00'}""
"Brendan:Person"
"Bought Database Design:Book	{'price': '195.00'}""
"Bought DNA and You:Book	{'price': '11.50'}""
"Paxtyn:Person"
"Bought The Life of Cronkite:Book	{'price': '29.95'}""
"Bought Database Design:Book	{'price': '195.00'}""
"The Life of Cronkite:Book	{'price': '29.95'}"
"Database Design:Book	{'price': '195.00'}"
"Trevor:Person"
"Bought Database Design:Book	{'price': '195.00'}""
"Bought Cosmos:Book	{'price': '17.00'}""
"Cosmos:Book	{'price': '17.00'}"
"DNA and You:Book	{'price': '11.50'}"

Subgraph containing Spencer and the books to be recommended
 "Spencer:Person"
"DNA and You:Book	{'price': '11.50'}"

New property graph with Spencer linked to the recommended books.
 "Spencer:Person"
"Recommendation DNA and You:Book	{'price': '11.50'}""
"DNA and You:Book	{'price': '11.50'}"


Process finished with exit code 0

"""

from propertygraph import PropertyGraph
from propertygraph import Node
from propertygraph import Relationship

def build_graph(graph):
    """ Creates original Property graph
                Parameters
                graph : Property graph object
    """
    # Create Node objects of category Person
    emily = Node("Emily", "Person")
    spencer = Node("Spencer", "Person")
    brendan = Node("Brendan", "Person")
    trevor = Node("Trevor", "Person")
    paxtyn = Node("Paxtyn", "Person")

    # Create Node objects for category Book
    cosmos = Node("Cosmos", "Book", {"price": "17.00"})
    database = Node("Database Design", "Book", {"price": "195.00"})
    cronkite = Node("The Life of Cronkite", "Book", {"price": "29.95"})
    dna = Node("DNA and You", "Book", {"price": "11.50"})

    # Define Relationships
    bought = Relationship("Bought")
    knows = Relationship("Knows")

    # Add Relationships between people and books they bought
    graph.add_relationship(emily, spencer, knows)
    graph.add_relationship(spencer, emily, knows)
    graph.add_relationship(spencer, brendan, knows)
    graph.add_relationship(paxtyn, cronkite, bought)
    graph.add_relationship(paxtyn, database, bought)
    graph.add_relationship(trevor, database, bought)
    graph.add_relationship(trevor, cosmos, bought)
    graph.add_relationship(brendan, database, bought)
    graph.add_relationship(brendan, dna, bought)
    graph.add_relationship(spencer, cosmos, bought)
    graph.add_relationship(spencer, database, bought)
    graph.add_relationship(emily, database, bought)

    return graph


def get_book_recommendations(graph, person):
    """ Gets book recommendations for specified person
                    Parameters
                    graph : Property graph object
                    person: Node object that represents
                    person you want recommendations for
    """
    # Find all the books Spencer bought
    books_bought = []
    # Gets nodes adjacent to spencer that have relationship "bought"
    book_bought_rel = graph.adjacent(person, "Person", "Bought")
    # Extracts the book from results
    for one_bought_relation in book_bought_rel:
        book = one_bought_relation[0].name
        books_bought.append(book)

    # Finds all the people that person knows
    recommendations = []
    # Gets nodes adjacent to Spencer with relationship "knows"
    for friend_tuple in graph.adjacent(person, "Person", "Knows"):
        # Gets the books that each friend has bought
        book_relations = graph.adjacent(list(friend_tuple)[0], "Person", "Bought")
        for one_relation in book_relations:
            book = one_relation[0].name
            # If the book has not already been bought by Spencer
            if book not in books_bought:
                recommendations.append(book)
    # Returns a set to get unique books
    return set(recommendations)


def build_nodes_subgraph(orig_graph, person, books_recommendation):
    """ Builds the subgraph of recommended books for Spencer
            Parameters
            orig_graph : Property graph object that has original relations
            person: Node object that represents
                person you want recommendations for
            book_recommendations: list of recommend books
    """
    # Appends the person (spencer) to the graph nodes list
    graph_nodes = []
    graph_nodes.append(person)

    # Iterates through book recommendations and get the book node
    for book_name in books_recommendation:
        # Gets the nodes from the original graph that are the book names from the recommended list
        book_node = list(orig_graph.get_nodes(book_name))[0]
        # Appends node to the list
        graph_nodes.append(book_node)

    # Creates subgraph as an object of propertygraph
    recommendations_sg = orig_graph.subgraph(graph_nodes)

    return recommendations_sg


def add_relation(new_graph, rel_name):
    """Adds the relationship to recommended books for Spencer
                Parameters
                new_graph : Property graph with just the nodes
                rel_name: Recommendation Relationship object
        """
    # Creates new Relationship object
    rel = Relationship(rel_name)

    # Iterates through the people and books in the subgraph
    for person in new_graph.get_nodes(category="Person"):
        for book in new_graph.get_nodes(category="Book"):
            # Adds relationship between person and book
            new_graph.add_relationship(person, book, rel)

    return new_graph


if __name__ == "__main__":
    # Creates original graph object
    graph = PropertyGraph()
    book_graph = build_graph(graph)
    print("Original Graph", "\n", book_graph)

    # Get the book recommendations based on books bought by the people known to the Spencer
    person = list(book_graph.get_nodes("Spencer"))[0]
    books_recommendation = get_book_recommendations(book_graph, person)

    #  Subgraph containing Spencer and the books to be recommended
    nodes_sg = build_nodes_subgraph(book_graph, person, books_recommendation)
    print("Subgraph containing Spencer and the books to be recommended", "\n", nodes_sg)

    # Add Recommend relationships to the new PropertyGraph
    relationship_sg = add_relation(nodes_sg, "Recommendation")
    print("New property graph with Spencer linked to the recommended books.", "\n", relationship_sg)
