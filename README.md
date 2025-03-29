# BRIDGE: Building a Realistic, In-Depth, Grounded and Explainable Mental Health Dialogue Dataset

BRIDGE is a framework to analyze mental health forum interactions and create realistic and in-depth dialogues between a help seeker and a counselor with explicit explanations for each utterance.

## Pre-requisites
1. Neo4J: Ensure that your Neo4J database is running before using BRIDGE.

## Set Up

1. Clone this repository

```
https://github.com/ktzy0305/BRIDGE.git
```

```
cd "path/to/BRIDGE/"
```

2. Install Dependencies

```
pip install -r requirements.txt
```

3. Environment Variables

Please ensure that your `.env` file contains the following variables.

```
# Local Neo4J DBMS
NEO4J_PROTOCOL=bolt://
NEO4J_URI=localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=dbpassword

# Assuming you want to use OpenAI's GPT
OPENAI_API_KEY=openaiapi
```

4. Populate The Database

You may refer to `example_populate.py`.

```
python example_populate.py
```

5. Dialogue Generation

You may refer to `example_usage.py`.

```
python example_usage.py
```

## Future Works

1. Create a version that does not depend on Neo4J.
2. Support other LLMs.