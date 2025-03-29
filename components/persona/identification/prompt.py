PERSONA_INDENTIFICATION_PROMPT = """
# TASK

You are given a post written by someone who is seeking support on a digital mental health forum. Your task is to read the post then identify and propose a persona by filling up the requirements details (given later) based on the information available on the forum post and by imagining the help seeker's personality if they went for therapy.


# REQUIREMENTS 

1. The required details for a persona are: 
- name: The name of the persona, as inferred from the post
- age range: Provide a numerical range (eg: 16-20, 21-25, 31-35, etc...)
- gender: Either 'Female', 'Male' or 'Non-Binary'
- background: Describe in detail the personal background of the persona, such as their occupation, family, or their past experiences. 
- mental health symptoms: Describe in detail, the mental health symptoms and personal struggles the persona is facing.
- perspective: How the persona sees or interprets their situation based on their mental and emotional viewpoint (a.k.a their thought process)
- motivations: What does the persona want to achieve or avoid and why
- emotional state: The emotions that the help seeker is going through.
- needs: The resources, support or solution the persona needs to address or alleviate their struggles and improve their overall wellbeing.
- conversational_stance: Based on the persona's current emotions and perspective about their situation, how would they interact with a therapist
- type: Indicate the type of the persona as 'Identified'

2. If the post lacks information for any of the required details needed to construct a persona, please fill up the details with information that is coherent and relevant based on what you can identify about the persona from given post.

3. Ensure that the persona's emotional state, mental health syptoms, personal struggles and experiences are aligned with the given post.

4. You must always return valid JSON fenced by a markdown code block. Do not return any additional text.


# INPUTS

Topic: {topic}

Written By: {username}

Post: {post}

"""