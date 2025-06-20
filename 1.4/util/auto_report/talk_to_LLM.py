"""
File: talk_to_LLM.py
Author: Chuncheng Zhang
Date: 2025-06-19
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Talk to LLM to generate auto report.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-06-19 ------------------------
# Requirements and constants
from ollama import Client, ChatResponse


host = 'http://192.168.3.38:11434'
# %% ---- 2025-06-19 ------------------------
# Function and class


# %% ---- 2025-06-19 ------------------------
# Play ground
# 创建客户端实例
client = Client(host=host)
print(f'连接到 Ollama 服务器: {host}')

# 使用chat方法
response: ChatResponse = client.chat(
    model='deepseek-r1:32b',
    messages=[
        {
            'role': 'user',
            'content': '请用python写一段代码，可获取A股所有的股票代码。',
        },
    ]
)

print(response['message']['content'])
# 或直接访问响应对象的字段
print(response.message.content)

# %% ---- 2025-06-19 ------------------------
# Pending


# %% ---- 2025-06-19 ------------------------
# Pending
