PERSONA_DIVERSIFICATION_PROMPT = """
# TASK

You are given the following information:
1. A forum post written by someone who is seeking support on a digital mental health forum.
2. An original persona that was identified based on the contents of the forum post.
3. A list of conversational subtopics that are contextually relevant to the forum post.

Your task is to create {n} new realistic and diverse personas that retain the core mental health profile of the original persona but differ in terms of demographic details, life context and personality traits.


# REQUIREMENTS

1. Ensure each  diversified persona retains the key emotional triggers and emotional states from the original persona. For example, contextual triggers (eg: conflict with a close friend, heartbreak from a romantic interest) should be kept in the diversified persona.
2. Each diversified persona should exhibit an emotional state that closely mirrors the Help Seeker’s emotional profile described in the original persona.
3. Vary the diversified persona’s background, demographics and environment (eg: different relationship history, workplace vs college)
- Each persona’s occupation or day-to-day context must be unique from all other personas generated in this session. 
- If you have already created a software engineer in a big city, you must choose a different occupation (e.g., teacher, freelance artist, local business owner) and a different setting (e.g., rural area, suburban environment, overseas).
4. Distinguish their motivations, perspectives and needs.
5. Each newly created diversified persona should be suitable to characterize someone who would engage meaningfully in a conversation about the themes from the forum post and provided conversational topics.
6. The required details for a persona are: 
- name: Assign a unique name that is different from the original persona (do not reuse names between requests)
- age range: Provide a numerical range (eg: 16–20, 21–25, 26–30, etc…)
- gender: Either Male, Female or Non-Binary
- background: Describe in detail the personal background of the persona, such as their occupation, family, or their past experiences. 
- mental health symptoms: Describe in detail, the mental health symptoms and personal struggles that the persona is facing.
- perspective: How the persona sees or interprets their situation based on their mental and emotional viewpoint (a.k.a their thought process)
- motivations: What does the persona want to achieve or avoid and why
- emotional state: The emotions that the help seeker is going through.
- needs: The resources, support or solution the persona needs to address or alleviate their struggles and improve their overall wellbeing.
- conversational_stance: Based on the persona's current emotions and perspective about their situation, how would they interact with a therapist
- type: Set the type of the persona as 'Diversified'
7. Add all the generated personas into the 'personas' variable as a list.
8. You must always return valid JSON fenced by a markdown code block. Do not return any additional text.


# NO DRIFTING
- Do NOT eliminate the emotional triggers of the original persona from the diversified persona’s emotional profile.
- The diversified persona should keep the same root cause of emotional distress as the original persona


# INPUTS

1. Original Persona: {original_persona}

2. Conversational Topics: {conversational_subtopics}

3. Post: {post}

"""