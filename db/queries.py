from neomodel import (config, db)
from typing import Any, Dict, List

import os

try:
    username = os.environ.get("NEO4J_USERNAME")
    password = os.environ.get("NEO4J_PASSWORD")
    uri = os.environ.get("NEO4J_URI")
    neo4j_protocol = os.environ.get("NEO4J_PROTOCOL")
    database_url = "{}{}:{}@{}".format(neo4j_protocol, username, password, uri)
    config.DATABASE_URL = database_url

except Exception as e:
    print("Failed to set up environment variables", exc_info=True)
    raise e



def fetch_all_posts_in_topic(topic_id: int) -> List[Dict[str, Any]]:
    query = """        
    MATCH (u: User) -[:WROTE] ->(p: Post) -[:BELONGS_TO] -> (t: Topic) -[:IS_CATEGORIZED_AS] -> (subcat: Subcategory)
    WHERE t.topic_id = $topic_id
    RETURN t.topic, subcat.name, u.username, u.user_role, p.post_id, p.post_content
    ORDER BY p.post_order ASC
    """
    
    params = {
        "topic_id": topic_id,
    }
    
    try: 
        results, meta = db.cypher_query(query, params)
        data = []
        
        for res in results:
            topic, subcategory, username, user_role, post_id, post_content = res
            row_data = {
                "topic" : topic,
                "subcategory" : subcategory,
                "username" : username,
                "user_role" : user_role,
                "post_id" : post_id,
                "post_content" : post_content
            }
            data.append(row_data)
        return data
    except Exception as e:
        print("Failed to fetch posts")
        raise e