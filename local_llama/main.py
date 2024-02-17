import os
import dataclasses
from llama_cpp import Llama

# Choose a model to use
models_dir = './models'
model = 'mistral-7b-v0.1.Q8_0.gguf'
model_path = os.path.join(models_dir, model)

# Instantiate the LLM
llm = Llama(model_path, n_ctx=4096, n_gpu_layers=100)

prompt_tpl = """Masayoshi is a chill guitar player from Japan who works as an assistant on the side. He is always eager to help and is very laid back. He will answer questions as promptly and as accurately as possible with his own brand of relaxed helpfulness. Here is a conversation between Masayoshi and someone named USER...

USER: {prompt}

MASAYOSHI:"""

@dataclasses.dataclass
class Message:
    speaker: str
    text: str

@dataclasses.dataclass
class ChatManager:
    history: list = dataclasses.field(default_factory=list)

    def add(self, prompt, response):
        self.history.append((prompt, response))

    def __str__(self):
        return '\n'.join([f'{prompt}\n{response}\n' for prompt, response in self.history])


def handle_prompt(prompt):
    expanded_prompt = prompt_tpl.format(prompt=prompt)
    result = llm(
        expanded_prompt,
        max_tokens=2048,
        stop=["USER:"],
        echo=True
    )
    output = result['choices'][0]['text']
    return output.replace(expanded_prompt, '').strip()


if __name__ == '__main__':
    exit = 0
    chat_history = ChatHistory()
    while not exit:
        prompt = input()
        if prompt == 'exit':
            exit = 1
        else:
            output = handle_prompt(prompt)
            chat_history.add(prompt, output)
            print(output)
    print(chat_history)
