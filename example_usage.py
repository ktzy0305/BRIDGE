from db.schema import Post, Topic

help_seeker_posts = [node for node in Post.nodes.fetch_relations("written_by", "belongs_to").filter(post_order = 1)]

from bridge_framework import dialogue_generation

dialogue_generation(
    help_seeker_posts,
    "./data/conversations/dialogues.json",
    max_turn_count=30,
    batch_size=5
)