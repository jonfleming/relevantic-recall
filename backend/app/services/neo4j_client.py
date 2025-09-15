import os
from neo4j import GraphDatabase

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "relevantic_password")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def upsert_entity(tx, name, entity_type="Thing"):
    tx.run("""
    MERGE (e:Entity {name: $name})
    ON CREATE SET e.type = $entity_type
    RETURN e
    """, name=name, entity_type=entity_type)

def upsert_relation(tx, source, relation, target, weight=1.0, user_id=None, session_id=None):
    tx.run(
        """
        MATCH (a:Entity {name: $source}), (b:Entity {name: $target})
        MERGE (a)-[r:RELATED {verb: $relation}]->(b)
        ON CREATE SET r.weight = $weight, r.user_id = $user_id, r.session_id = $session_id
        ON MATCH SET r.weight = r.weight + $weight
        RETURN r
        """,
        source=source, target=target, relation=relation, weight=weight, user_id=user_id, session_id=session_id
    )

def insert_fact(source_name, relation, target_name, weight=1.0, user_id=None, session_id=None):
    with driver.session() as session:
        session.write_transaction(upsert_entity, source_name)
        session.write_transaction(upsert_entity, target_name)
        session.write_transaction(upsert_relation, source_name, relation, target_name, weight, user_id, session_id)
