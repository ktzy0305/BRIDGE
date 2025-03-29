from db.populate import populate_db

import os

# Populate Neo4J Database
populate_db(os.path.join(os.getcwd(), "data", "forum", "forum_data_for_dialogue_generation_small.csv"))