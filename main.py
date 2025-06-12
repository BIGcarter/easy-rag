import os 
from embed import text_embedding
from pathlib import Path
from openai import OpenAI


embed_model_config = {
    'api_key': os.getenv('ALI_API_KEY'),
    'base_url': os.getenv('ALI_BASE_URL'),
    'model': 'text-embedding-v4',
}

query_client = OpenAI(
            api_key = os.getenv('ALI_API_KEY'),
            base_url = os.getenv('ALI_BASE_URL'),
                )
chat_model = 'qwen-plus-2025-04-28'



file = './test_novel.md'

INSTRUCTION = 'Given a web search query, retrieve relevant passages that answer the query.'
# QUERY = '牛顿刚刚穿越的时候，面对侍卫的包围，拿出了什么受到天子召见？'
QUERY = '牛顿做了什么之后受到天子赏识，从而掌管钦天监？'

query_prompt = f"{INSTRUCTION}\n{QUERY}"

embed = text_embedding(file=file, model_config=embed_model_config)
if not Path("./chroma.db").exists():
    embed.create_db()

search_results = embed.search_db(query_prompt)

system_prompt = '''你是个专业的文档检索助手，擅长从检索出来的文档中，找到对应的内容来回答用户的提问。
    检索文档将在<documents><\documents>中，用户的提问在<query><\query>中。
'''
prompt_template = '''
    <documents>
    {documents}
    <\documents>
    <query>
    {query}
    <\query>
'''

prompt = prompt_template.format(documents='\n'.join(search_results), query=QUERY)
completion = query_client.chat.completions.create(
    model = chat_model,
    messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': prompt}
    ]
)

print(f"用户提问：{QUERY}")
print("--------------------")
print("Answer:\n")
print(completion.choices[0].message.content)





