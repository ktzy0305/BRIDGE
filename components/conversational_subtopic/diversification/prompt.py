CONVERSATIONAL_SUBTOPIC_DIVERSIFICATION_PROMPT = """
# TASK

You are given a thread on a digital mental health forum as well as its topic. The thread contains a sequence of posts, in which the first post is always written by Help Seeker and that subsequent posts are responses that are written by other supporters including Professional Counsellors. The Help Seeker may also follow up in the subsequent posts.

In addition, a you are given a persona and list of distinct conversational topics. The persona encapsulates the mental health profile of the help seeker while each provided conversational subtopic represents a focused area of discussion that maintains contextual relevance to the forum thread.

Typically, a dialogue between two individuals begins with some conversational topic and eventually transitions to other conversational topics. Imagine a dialogue between the given persona and a therapist about each of the provided conversational subtopics. 

Your task is to predict {n} new distinct conversational topics that represent potential future directions for the dialogue. The new conversational topics should be specific and take into consideration the evolving emotional needs and situational needs of the given persona. 


# INSTRUCTIONS

1. Write the newly generated conversational topics as an array of the 'ConversationalSubtopic' class into the 'conversational_subtopics' variable.
2. Each instance of the 'ConversationalSubtopic' class contains the 'subtopic' field and the 'type' field. 
3. For this task, every instance will have the 'type' field set as 'Diversified'.


# INPUTS
- Existing list of conversational topics: {conversational_subtopics}

- Persona: {persona}

- Topic: {topic}

- Chronological Sequence of Posts (Forum Topic Thread): 

{forum_topic_thread}

"""