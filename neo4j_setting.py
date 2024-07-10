from neo4j import GraphDatabase

import os
from dotenv import load_dotenv
load_dotenv()

driver = GraphDatabase.driver(os.environ["NEO4J_URI"],auth=(os.environ["NEO4J_USER"],os.environ["NEO4J_PASSWORD"]))

query = """
merge (A:persion) return A
"""

results, summary, keys = driver.execute_query(query, database_="neo4j")

print(results)
print(summary)
print(keys)