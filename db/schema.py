from neomodel import (
    StructuredNode, StringProperty, IntegerProperty,
    RelationshipTo, RelationshipFrom, StructuredRel
)

# Relationships
class BelongsToRel(StructuredRel):
    pass

class WroteRel(StructuredRel):
    pass

class IsCategorizedAsRel(StructuredRel):
    pass

class IsTaggedWithRel(StructuredRel):
    pass

class RepliedToRel(StructuredRel):
    pass

# Nodes
class User(StructuredNode):
    """
    Represents a user in Let's Talk
    """
    username = StringProperty(unique_index=True)
    user_id = IntegerProperty(unique_index=True)
    user_role = StringProperty()
    user_title = StringProperty()
    wrote = RelationshipTo('Post', 'WROTE', model=WroteRel)


class Topic(StructuredNode):
    """
    Represents a topic on Let's Talk (similar to a forum thread)
    
    Numerical Constraints:
    - Each topic contain up to n posts where n >= 1.
    - Each topic is subcategorised under a under "Ask a Therapist"
    - Each topic may be tagged with up to n user defined tags where n >= 1.
    """
    topic_id = IntegerProperty(unique_index=True)
    topic = StringProperty()
    url = StringProperty()
    is_categorized_as = RelationshipTo('Subcategory', 'IS_CATEGORIZED_AS', model=IsCategorizedAsRel)
    is_tagged_with = RelationshipTo('Tag', 'IS_TAGGED_WITH', model=IsTaggedWithRel)
    has_posts = RelationshipFrom('Post', 'BELONGS_TO', model=BelongsToRel)


class Subcategory(StructuredNode):
    """
    Represents a subcategory of the Ask a Therapist category of Let's Talk
    """
    name = StringProperty(unique_index=True)
    has_topics = RelationshipFrom('Topic', 'IS_CATEGORIZED_AS', model=IsCategorizedAsRel)


class Tag(StructuredNode):
    """
    Represents the user defined tags used to tag a topic.
    """
    name = StringProperty(unique_index=True)
    has_topics = RelationshipFrom('Topic', 'IS_TAGGED_WITH', model=IsTaggedWithRel)


class Post(StructuredNode):
    """
    Represents a post written by an user
    """
    post_id = IntegerProperty(unique_index=True)
    post_order = IntegerProperty()
    post_content = StringProperty()
    links_in_post = StringProperty()
    number_of_likes = IntegerProperty()
    written_by = RelationshipFrom('User', 'WROTE', model=WroteRel)
    belongs_to = RelationshipTo('Topic', 'BELONGS_TO', model=BelongsToRel)
    replied_to_post = RelationshipTo('Post', 'REPLIED_TO', model=RepliedToRel)
    direct_reply_to_post = RelationshipTo('Post', 'DIRECT_REPLY_TO')
    soft_replied_to_post = RelationshipTo('Post', 'SOFT_REPLIED_TO')
    quoted_post = RelationshipTo('Post', 'QUOTED')
