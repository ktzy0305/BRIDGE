import logging
import os
import pandas as pd
from neomodel import (config, db)
from db.schema import User, Subcategory, Post, Tag, Topic
from tqdm import tqdm
from utils.load_env import load_environment_variable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    username = load_environment_variable("NEO4J_USERNAME")
    password = load_environment_variable("NEO4J_PASSWORD")
    uri = load_environment_variable("NEO4J_URI")
    neo4j_protocol = load_environment_variable("NEO4J_PROTOCOL")
    database_url = "{}{}:{}@{}".format(neo4j_protocol, username, password, uri)
    config.DATABASE_URL = database_url

except Exception as e:
    logger.error("Failed to set up environment variables", exc_info=True)
    raise e


def clear_all_nodes():
    """
    This function deletes all nodes in the neo4j database.
    """
    db.cypher_query("MERGE (n) DETACH DELETE (n)")


def populate_db(dataframe_path: str):
    """
    This function populates the neo4j database and is hardcoded to populate data based on the defined columns
    """
    
    # Clear existing data
    clear_all_nodes()

    # Load CSV to dataframe
    df = pd.read_csv(dataframe_path)

    # Create nodes and relationships
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Creating node from CSV rows"):
        # Create or get User node
        user_node = User.nodes.get_or_none(user_id=row['user_id'])
        if user_node is None:
            user_node = User(
                username = row['username'],
                user_id = row['user_id'],
                user_role = row['user_role'],
                user_title = row['user_title']
            ).save()

        # Create or get Topic node
        topic_node = Topic.nodes.get_or_none(topic_id=row['topic_id'])
        if topic_node is None:
            topic_node = Topic(
                topic_id = row['topic_id'],
                topic = row['topic'],
                url = row['url']
            ).save()

        # Create or get Subcategory node
        subcategory_node = Subcategory.nodes.get_or_none(
            name=row['subcategory'])
        if subcategory_node is None:
            subcategory_node = Subcategory(name=row['subcategory']).save()

        # Create Post node
        post_node = Post(
            post_id = row['post_id'],
            post_order = row['post_order'],
            post_content = row['post_content'],
            links_in_post = row['links_in_post'],
            number_of_likes = row['num_likes'],
        ).save()

        # Create DiscourseTag node
        discourse_tags = row['tags']
        if discourse_tags != "---":
            discourse_tags = discourse_tags.split(",")
            for tag in discourse_tags:
                tag_node = Tag.nodes.get_or_none(name=tag)
                if tag_node is None:
                    tag_node = Tag(name=tag).save()
                topic_node.is_tagged_with.connect(tag_node)

        # Create relationships
        user_node.wrote.connect(post_node)
        post_node.belongs_to.connect(topic_node)
        topic_node.is_categorized_as.connect(subcategory_node)

        # Create REPLIED_TO relationship if applicable
        if not pd.isna(row['replied_to_post_id']):
            if isinstance(row['replied_to_post_id'], str):
                replied_to_post_ids = row['replied_to_post_id'].split(";")
                for post_id in replied_to_post_ids:
                    replied_to_post_node = Post.nodes.get_or_none(
                        post_id=post_id
                    )
                    if replied_to_post_node:
                        post_node.replied_to_post.connect(replied_to_post_node)
            else:
                replied_to_post_id = row['replied_to_post_id']
                replied_to_post_node = Post.nodes.get_or_none(
                    post_id=replied_to_post_id
                )
                if replied_to_post_node:
                    post_node.replied_to_post.connect(replied_to_post_node)
                    
        # Direct Reply
        if not pd.isna(row['replied_to_post_id_direct']):
            direct_reply_to_post_id = row['replied_to_post_id_direct']
            direct_reply_to_post_node = Post.nodes.get_or_none(
                post_id=direct_reply_to_post_id
            )
            if direct_reply_to_post_node:
                post_node.direct_reply_to_post.connect(
                    replied_to_post_node
                )

        # Soft Reply
        if not pd.isna(row['replied_to_post_id_soft']):
            soft_replied_to_post_node = Post.nodes.get_or_none(
                post_id=row['replied_to_post_id_soft']
            )
            if soft_replied_to_post_node:
                post_node.soft_replied_to_post.connect(
                    soft_replied_to_post_node
                )

        # Quoted Post
        if not pd.isna(row['quoted_post_id']):
            if isinstance(row['quoted_post_id'], str):
                quoted_post_ids = row['quoted_post_id'].split(";")
                for post_id in quoted_post_ids:
                    quoted_post_node = Post.nodes.get_or_none(
                        post_id=post_id
                    )
                    if quoted_post_node:
                        post_node.quoted_post.connect(
                            quoted_post_node
                        )
            else:
                quoted_post_id = row['quoted_post_id']
                quoted_post_node = Post.nodes.get_or_none(
                    post_id=quoted_post_id
                )
                if quoted_post_node:
                    post_node.quoted_post.connect(
                        quoted_post_node
                    )

