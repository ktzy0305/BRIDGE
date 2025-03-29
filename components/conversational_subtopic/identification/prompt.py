CONVERSATIONAL_SUBTOPIC_IDENTIFICATION_PROMPT = """
# TASK

You are given a thread on a digital mental health forum as well as its given topic. The thread contains a sequence of posts, in which the first post is always written by Help Seeker and that subsequent posts are responses that are written by other supporters including Professional Counsellors. The Help Seeker may also follow up in the subsequent posts.

The nature of a mental health support forum thread allows for multi-faceted discussions revolving the help seeker’s concerns. As an expert in psychology, you are tasked to break down narratives in the thread and identify {n} distinct conversational topics, each representing a focused area of discussion. Please ensure that each conversational subtopic maintains contextual relevance to the forum thread whilst being sufficiently specific for a meaningful dialogue.


# INSTRUCTIONS

1. Write your identified conversational topics as an array of the 'ConversationalSubtopic' class into the 'conversational_subtopics' variable. 
2. Each instance of the 'ConversationalSubtopic' class contains the 'subtopic' field and the 'type' field. 
3. For this task, every instance will have the 'type' field set as ‘Identified’.


# INPUTS

Topic: {topic}

Username: {username}

Forum Topic Thread: 

{forum_topic_thread}

"""