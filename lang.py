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





def create_prompt(prompt):

  prompt_template=f'''RULES: You are a savage, disrespectful and witty assistant. Always rephrase a sentence into a funny, creatively sarcastic way.
  The output sentence should be witty, savage, insulting of the code issue.

  Issue: {prompt}

  SARCASTIC COMMENT:
  '''
  return prompt_template

def get_comment(message):
    ai_msg = llm.invoke(create_prompt(message))
    print(ai_msg.content)
    return ai_msg