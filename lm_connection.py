from g4f.client import Client
from g4f.Provider import You, Bing, HuggingChat, PerplexityLabs


def ask_gpt(message: str):
    client = Client(provider=You)
    response = client.chat.completions.create(
        model="",
        messages=[
            {"role": "user", "content": message}
        ],
    )
    return response.choices[0].message.content


# def change_text(text):
#     print('starting transformation')
#     answer = ask_gpt(CHANGE_TEXT_SYS_PROMPT + text)
#     print(answer)
#     return answer

# print(ask_gpt('придумай 5 тем для поста в блог на тему "создание собственного бренда"'))