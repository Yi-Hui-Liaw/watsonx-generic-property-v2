DEFAULT_SYSTEM_PROMPT = """
You are an expert Q&A system that is trusted around the world. Always answer the query using the provided context information, and not prior knowledge.
Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. 
"""


SQL_SYSTEM_PROMPT = """
You are a coding assistant helping an analyst answer questions over business data in SQL. More specifically, the analyst provides you a database schema (tables in the database along with their column names and types) and asks a question about the data that can be solved by issuing a SQL query to the database. In response, you write the SQL statement that answers the question. 
You do not provide any commentary or explanation of what the code does, just the SQL statement ending in a semicolon.
"""


def build_prompt(question, system_prompt):
    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
    BOS, EOS = "<s>", "</s>"
    prompt = "".join([B_SYS, system_prompt, E_SYS, question]).strip()
    return f"{BOS}{B_INST} {prompt} {E_INST}"

def build_prompt_llama3(history, system_prompt, context, contextual_prompt, json_assert=None, window=8):
    if len(history) > window:
        trunc = -window
    else:
        trunc = 0
    map_roles = {"u": "user", "a": "assistant", "s": "system"}
    chat = "\n".join(["<|start_header_id|>{}<|end_header_id|>{}<|eot_id|>".format(map_roles[list(x.keys())[0]], list(x.values())[0]) for x in history][trunc:])
    contextual_prompt = contextual_prompt.replace("{{context}}", context)
    p  = PROMPT_TEMPLATE.replace("{{system_prompt}}", system_prompt).replace("{{chat}}", chat).replace("{{contextual_prompt}}", contextual_prompt)
    if json_assert is not None:
        p = p + "\n" + json_assert
    return p

PROMPT_TEMPLATE = """
<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>{{system_prompt}}<|eot_id|>
{{chat}}
<|start_header_id|>assistant<|end_header_id|>
"""



QUESTION_TEMPLATE = """
Context information is below.
---------------------
{{context}}
---------------------

Given only the context information and no prior knowledge, answer the query in a brief and concise manner using only one sentence.  

Avoid statements like 'Based on the context, ...' or 'According to the provided context ...', or anything along those lines.

If you don't know the answer to a query, say "I do not know".

If the user did not ask a question, you should reply accordingly in a conversational manner. 

Query: {{question}} 
 
Response: 

"""


TELL_ME_MORE_TEMPLATE = """
Context information is below.
---------------------
{{context}}
---------------------

Given only the context information and no prior knowledge, answer the query in a brief and concise manner.  

Avoid statements like 'Based on the context, ...' or 'According to the provided context ...', or anything along those lines.

If you don't know the answer to a query, say "I do not know".

If the user did not ask a question, you should reply accordingly in a conversational manner.

Query: {{question}} 
 
Response: 

"""

DIRECT_ANSWER_TEMPLATE = """
Given only the answer and no prior knowledge, rephrase the question and answer below in a brief and concise manner.

Response with the full name of the property, Residensi Zig, The Connaught One or The MINH.

Question: What is the number of available units at The MINH?

Answer: 312

Response: The number of available units is 312.

Question: {{question}} 
 
Answer: {{answer}}

Response: 

"""

DIRECT_ANSWER_TEMPLATE_v1 = """
Given only the answer and no prior knowledge, rephrase the question and answer below in a brief and concise manner.

Response with the full name of the property, Residensi Zig, The Connaught One or The MINH.

Question: What is the number of available units at The MINH?

Answer: 312

Response: The number of available units is 312.

Question: {{question}} 
 
Answer: {{answer}}

Response: 

"""

DIRECT_ANSWER_TEMPLATE_v2 = """
Given only the answer and no prior knowledge, summarize the answer to the question below in a brief and concise manner. The answer is provided as a list of JSON records.

Question: 
How many units cost less than 500k?

Answer:
[{"COUNT(*)":0,"property_name":"minh"},{"COUNT(*)":126,"property_name":"zig"},{"COUNT(*)":524,"property_name":"connaught"}]

Response: 
0 units cost less than 500k at minh, 126 units cost less than 500k at zig, and 524 units cost less than 500k at connaught.

Question: 
How many units cost more than 1mil?

Answer:
[{"COUNT(*)":0,"property_name":"connaught"},{"COUNT(*)":0,"property_name":"zig"},{"COUNT(*)":496,"property_name":"minh"}]

Response: 
0 units cost more than 1 mil at connaught, 0 units cost more than 1 mil at zig, and 496 units cost more than 1 mil at minh.

Question: 
{{question}} 
 
Answer: 
{{answer}}

Response: 
"""

ROUTING_TEMPLATE = """
Classify the following question into one of these options. 

Note that the table columns for transactional queries are as follows:

- Property_Name refers the name of the unit.
- Layout refers to the layout type of each unit, generally indicated using a letter, or a letter and a number (eg 'TYPE A', 'TYPE A1', 'TYPE D2'). There is a fixed set of layout types for a given property and each unit will fall under one the layout types.
- Status refers to whether or not the unit is still available. Valid entries include "Available", "Hold" and "Signed".
- Block refers to block of the building. Valid entries include 'BLOCK A', 'BLOCK B', 'BLOCK C' and so on.
- Price refers to the listed price of the unit, and is usually a six or seven digit integer.

Each table for the transactional queries corresponds to a real estate property, such as a condominium building. For example, the "zig" table corresponds to a specific condominium. Each row in the tables corresponds to a unit within the real estate property. There are 3 real estate properties, namely Residensi Zig, The Minh and The Connaught One. 

Therefore, questions related to the topics above should be classified as 1. Questions not covered by the table columns above should be classified as 3 if it is property-related, and as 4 if it is a non-property related question.

1) Transactional query
3) Property specific general query
4) General query

Question: How many available units for Residensi Zig?

Answer: 1

Question: How many available units are there?

Answer: 1

Question: when will the minh be completed?

Answer: 3

Question: How many blocks exist at property?

Answer: 1

Question: What is the maximum price of units?

Answer: 1

Question: Does it have a swimming pool

Answer: 3

Question: how much are the fees?

Answer: 3

Question: where are the nearest malls?

Answer: 3

Question: {{question}}

Answer:
"""

SQL_TEMPLATE = """
Given the following SQL tables.

CREATE TABLE zig (
    Property_Name text,
    Layout text,
    Status text,
    Block text,
    Price double
);

CREATE TABLE minh (
    Property_Name text,
    Layout text,
    Status text,
    Block text,
    Price double
);

CREATE TABLE connaught (
    Property_Name text,
    Layout text,
    Status text,
    Block text,
    Price double
);

Each table corresponds to a real estate property, such as a condominium building. 

For example, the "zig" table corresponds to a specific condominium. Each row in the tables corresponds to a unit within the real estate property. 

The property may be slightly misspelled or rephrased in the question. For example, "Emporis Residences" may be called "emporis" or "residensi emporis" etc.

Valid entry requirements for each column in the tables:

- Property_Name refers the name of the unit.
- Layout refers to the layout type of each unit, generally indicated using a letter, or a letter and a number (eg 'TYPE A', 'TYPE A1', 'TYPE D2'). There is a fixed set of layout types for a given property and each unit will fall under one the layout types.
- Status refers to whether or not the unit is still available. Valid entries include "Available", "Hold" and "Signed".
- Block refers to block of the building. Valid entries include 'BLOCK A', 'BLOCK B', 'BLOCK C' and so on.
- Price refers to the listed price of the unit, and is usually a six or seven digit integer.

The user question may be phrased as a question, command, or request.

By default, take the union of all tables unless a property name is defined in the question. Never join the tables on any column. 

Write a single SQL statement that answers the following question: {{question}}.

"""

CUSTOM_RESPONSE_TEMPLATE = """

Image List:

- the-connaught-one/pool-lounge.jpg

- the-connaught-one/gym.jpg

- the-connaught-one/play-area.jpg

- the-connaught-one/aerial-night.jpg

- the-connaught-one/drop-off.jpg

- the-connaught-one/lobby.jpg

- the-connaught-one/mid-balcony.jpg

- the-connaught-one/mrt-night.jpg

- the-connaught-one/parcel-room.jpg

- the-connaught-one/pool-top.jpg

- the-connaught-one/retail-cafe.jpg

- the-minh/drop-off.jpg

- the-minh/garden.jpg

- the-minh/gym.jpg

- the-minh/play-area-indoor.jpg

- the-minh/play-area-outdoor.jpg

- residensi-zig/gamers-room.jpg

- residensi-zig/gym.jpg

- residensi-zig/parcel-lounge.jpg

- residensi-zig/play-area.jpg

- residensi-zig/pool-1.jpg

- residensi-zig/pool-2.jpg

----------------------------------------------------------------
Instructions:

Given the above images. Select one or more images which illustrates the facility from the text description. The images are provided in the format <property_name/facility_name>. Just because the property name is a match, does not mean that the facility is also a match. 

If none of the images illustrate the facility, respond "None". Otherwise, provide your answers as a list of strings.
----------------------------------------------------------------
Description: Yes, The Connaught One has a swimming pool.

Response: ['the-connaught-one/pool-lounge.jpg']

Description: MINH has a gym.

Response: ['the-minh/gym.jpg']

Description: The MINH has a play area and play ground.

Response: ['the-minh/play-area-outdoor.jpg', 'the-minh/play-area-indoor.jpg']

Description: There is a spa at Zig.

Response: None

Description: There is a sauna at connaught.

Response: None

Description: There is a kitchen at connaught.

Response: None

Description: The Residensi Zig has a pool area and pool lounge.

Response: ['residensi-zig/pool-1.jpg', 'residensi-zig/pool-2.jpg']

Description: {{description}}
"""

PROPERTY_TEMPLATE = """
Classify the following question into one of these properties. The property may be slightly misspelled or rephrased in the question. If the question does not contain any property name, respond "NONE".

- residensi-zig
- the-connaught-one
- the-minh
- NONE

Question: Zig got any unit available?

Answer: residensi-zig

Question: the-connaught size range is what?

Answer: the-connaught-one

Question: where is the parking lot?

Answer: NONE

Question: Is Residensi Zig expensive?

Answer: residensi-zig

Question: connaught price is what?

Answer: the-connaught-one

Question: minh expensive?

Answer: the-minh

Question: {{question}} 

Answer:

"""
