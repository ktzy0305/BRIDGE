TURN_BASED_CONVERSATION_PROMPT = """
# 1. TASK

You are tasked with simulating a back and forth dialogue between Persona A and Persona B for {n} conversation turns, with Persona A always speaking first, followed by Persona B. 


# 2. INFORMATION

You are given the following information:
- Personality profiles of two personas, Persona A and Persona B
- Conversational topic which guides the tone, focus and subject of the dialogue
- Contextual information, which explains the purpose and rationale of generating the conversation.
- Forum Topic Thread, a chronological sequence of posts within a forum topic that serves as the reference material to help you with generating dialogues for each persona. Specifically, each dialogue line in the Forum Topic Thread made by the 'Help Seeker' can be helpful for generating dialogues for Persona A. Whereas each dialogue line made by the 'Professional' can be helpful for generating dialogues for Persona B.


# 3. REQUIREMENTS

## A. REFERENCING REQUIREMENTS

When generating dialogues, follow these strict referencing rules

### A.1. FORUM REFERENCES
- REQUIRED: For any utterance that uses content from the forum topic thread
- FORUM REFERENCE TYPES:
  a) EXACT QUOTES
  - When utterances use sentences from the forum thread that match precisely
  - Example:
    Forum: "I am feeling overwhelmed from work"
    Utterance: "I am feeling overwhelmed from work"

  b) SIMILAR CONTENT/PARAPHRASING
  - When expressing similar ideas or meanings
  - When adapting or building upon forum content
  - Examples:
    Forum: "I am feeling overwhelmed from work"
    Similar utterances requiring reference:
    - "I've been overwhelmed with the workload"
    - "The amount of work is overwhelming me"
    - "My work responsibilities are becoming overwhelming"
    
  c) THERAPEUTIC RESPONSES (Specific to Persona B)
  - When using similar therapeutic techniques as forum responses
  - When mirroring counseling approaches seen in forum replies
  - When employing similar validation/reflection patterns
  - When suggesting comparable coping strategies
  - Examples:
    Forum: "It sounds like you're trying to manage multiple responsibilities at once"
    Similar therapeutic responses requiring reference:
    - "I hear that you're juggling many tasks"
    - "Managing multiple responsibilities can be challenging"
    - "It seems you're dealing with a lot at once"

- ATTRIBUTION
  * Exact quote matching: Copy and paste the exact sentence(s) used
  * Complete attribution: Include the username and the Post ID
  * Format (For BOTH exact quotes AND similar content):
    - source: "Forum"
    - post_id: [number]
    - username: [exact username]
    - sentence: [exact quoted text]
    - reason: [For similar content: Explain how your utterance relates to/adapts the original] 
      - For Persona B: Include explanation of adapted therapeutic technique when applicable

### A.2. AI GENERATED CONTENT
- REQUIRED: For any utterance not directly quoting the forum:
  * Source attribution: Mark as "AI Generated"
  * Detailed reasoning: Explain how the utterance:
    - Connects to previous dialogue
    - Reflects persona traits
    - Advances the conversation
  * Format:
    - source: "AI Generated"
    - post_id: -1
    - username: ""
    - sentence: ""
    - reason: [detailed explanation]
   
        
### A.3. VERIFICATION STEP
Before finalizing each utterance, verify:
- Forum quotes match the source text exactly
- All forum-sourced content has complete attribution
- AI-generated content includes clear reasoning
- For Persona B: Therapeutic responses reference similar counseling approaches from forum


### A.4. PER-TURN VERIFICATION

Before completing each dialogue turn, verify:
- All forum quotes are exact matches
- Forum references include complete attribution
- AI-generated content has detailed reasoning
- Utterances align with persona profiles
- Dialogue maintains natural flow
- For Persona B: Check for similar therapeutic patterns requiring reference
- For Persona B: Verify therapeutic approach documentation

### REFERENCE EXAMPLES

FORUM REFERENCE EXAMPLE:
Utterance: "I've been overwhelmed by work lately."
Reference:
  source: "Forum"
  post_id: 18578
  username: "StressedUser123"
  sentence: "I've been feeling overwhelmed with work lately."
  reason: ""

AI GENERATED EXAMPLE:
Utterance: "Have you considered trying meditation to help manage your stress?"
Reference:
  source: "AI Generated"
  post_id: -1
  username: ""
  sentence: ""
  reason: "Generated this therapeutic suggestion based on Persona B's counseling background and previous discussion of stress management techniques. This response builds on the client's expressed feelings of being overwhelmed.
 

## B. DIALOGUE REQUIREMENTS

We want to simulate a realistic conversation between two personas Persona A and B as given above. The dialogues should
- Be Realistic and Diverse: While we provide a reference source, the generated conversation should diversify from the original source by creating new, plausible conversation plots and responses that stay aligned with the original topic while simulating realistic emotional exchanges.
- Showcase Behavioural Alignment: Persona A's utterances should reflect their personality profile and how people with similar traits might interact within an emotional support context. You may draw inspiration from the observed behavioural patterns without replicating exact forum interactions.
- Maintain Supportive Tone for Persona B: Persona B's responses to Persona A’s expressions should maintain a therapeutic and empathetic tone, resembling a professional therapist's supportive behaviour. The content in Persona B's responses should be based on counselling or therapy theory or approaches.


## C. EXPECTED OUTPUT

Every conversation turn should be recorded in the 'conversation_turns' variable which is of 'List[ConversationTurn]' type.

### DATA TYPES FOR OUTPUT

#### ConversationTurn

Each conversation turn denoted by the 'ConversationTurn' object type MUST contain these 4 attributes:
- The turn number denoted by 'turn_number'
- The current speaker denoted by 'speaker_name' (use the name in the given persona profile)
- The utterance made by the current speaker denoted by 'utterance'
- Information source for the utterance made by the current speaker denoted by 'utterance_source'

#### UtteranceSource

Utterance Source Attributes denoted by 'UtteranceSource':
- 'source' describes where the utterance is originally forum. Indicate either 'Forum' or 'AI Generated'
- 'post_id' indicates which Post ID does the utterance reference from the forum topic. (Fill this if the source is 'Forum', otherwise assign it a value of '-1') 
- 'username' states which username does the utterance reference from the forum topic. (Fill this if the source is 'Forum', otherwise leave it as an empty string '')
- 'sentence' states which sentence(s) does the utterance reference from the forum topic (Fill this if the source is 'Forum', otherwise leave it as an empty string '') 
- 'reason' Reason for generating the utterance (Fill this if the source is 'AI Generated', otherwise leave it as an empty string '')


# 4. INPUTS

Persona A: 

{persona_a}

Persona B: 

{persona_b}

Conversational Topic: 

{conversational_subtopic}

Forum Topic Thread: 

{forum_topic_thread}

"""


PERSONA_B_INFORMATION = """
Occupation: Therapist

Key Traits:
- Understanding and patient: A calm and attentive therapist who takes time to fully listen to their patients and establishes a safe space for their clients to express themselves freely.
- Empathetic: The therapist establishes an empathetic connection with their clients to foster a warm and trusting relationship.
- Collaborative: The therapist believes in working alongside their clients to help uncover insights into their thoughts, emotions and behaviours. They also respect the client's boundaries and decision making at their own pace.
- Goal Oriented: The therapist is goal oriented as they envision goals that the client can work towards to in their mental health journey.

Chain of thought:
1. Establish rapport with his or her client at the start of each therapy session.
2. Balances between responding empathetically and gathering information about the client, but he or she will always respect the boundaries established by the patient.
3. The therapist along with the client will dive deeper into conversational subtopics, explore thoughts, emotions, behaviours and coping mechanisms. However, do be realistic and ensure that the conversation reflects the nature of a 30min to 1hr therapy session.
4. The therapist would envision goals that the client can work towards to, provide advice such as guidance or coping techniques.
5. Keep the dialogue realistic within the context of a therapy session. This means avoiding too many subtopics and maintaining focus on specific issues raised by Persona A. 
6. Sessions should feel natural and have a progression: start with rapport-building, move to deeper exploration, and conclude with goal-setting or reflection.
"""