# import os
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings

import openai
import langchain
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # api_key="...",  # if you prefer to pass api key in directly instaed of using env vars
    # base_url="...",
    # organization="...",
    # other params...
)

from langchain_core.prompts import ChatPromptTemplate

# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You are a helpful assistant that translates {input_language} to {output_language}.",
#         ),
#         ("human", "{input}"),
#     ]
# )





#import random


# def create_prompt(prompt):
#     prompt_templates = [
#         f'''RULES: You are a savage, disrespectful, and witty assistant. Always rephrase a sentence into a funny, creatively sarcastic way.
#         The output sentence should be witty, savage, and insulting of the code issue.
#         Issue: {prompt}
#         SARCASTIC COMMENT:''',

#         f'''RULES: You are a snarky, clever, and brutally honest assistant. Transform any given sentence into a humorous, sarcastic critique.
#         The output should be smart, sharp, and mockingly disrespectful of the code issue.
#         Issue: {prompt}
#         SARCASTIC COMMENT:''',

#         f'''RULES: You are a sharp-tongued, irreverent, and cheeky assistant. Convert any given sentence into a hilarious, sarcastic remark.
#         The output must be amusing, cutting, and derisively critical of the code issue.
#         Issue: {prompt}
#         SARCASTIC COMMENT:''',

#         f'''RULES: You are a caustic, witty, and irreverent assistant. Reformulate any sentence into a sarcastic and funny critique.
#         The output should be scathing, clever, and mockingly insulting of the code issue.
#         Issue: {prompt}
#         SARCASTIC COMMENT:'''
#     ]

#     # Randomly select a prompt template
#     selected_template = random.choice(prompt_templates)
#     return selected_template

# def get_comment(message):
#     ai_msg = llm.invoke(create_prompt(message))
#     print(ai_msg.content)
#     return str(ai_msg.content) 


#imagine a few really sarcastic and insulting personalities. Imagine multiple that speak differently from each other and have different quirks and speaking styles. Randomly pick one of these. Using this personality, rephrase sentences in a funny, aggressive, and creatively sarcastic way. The output should sound like the random personality that you chose and should be insulting of the code issue

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "imagine a few really sarcastic and insulting personalities. Imagine multiple that speak differently from each other and have different quirks and speaking styles. Randomly pick one of these. Using this personality, rephrase sentences in a funny, aggressive, and creatively sarcastic way. The output should sound like the random personality that you chose and should be insulting of the code issue. Keep it short and within 25 words. Issue {prompt}"

        ),
        ("human", "{prompt}"),
    ]
)

chain = prompt | llm

def get_comment(message):
    ai_msg = chain.invoke(
    {
        "prompt": message,
    }
    )
    return str(ai_msg.content)