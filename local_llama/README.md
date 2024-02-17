## Installation

### Mac OSX

For Mac Metal GPU Install, see: https://github.com/abetlen/llama-cpp-python/blob/main/docs/install/macos.md

### WSL 2 with CUDA Support for my RTX 4090

```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir
```

## Sample Script

See main.py for something more fleshed out and interactive.

```python
import os
from llama_cpp import Llama

# Choose a model to use
models_dir = '/home/william/personal/llama.cpp/models'
model = 'mistral-7b-v0.1.Q8_0.gguf'
model_path = os.path.join(models_dir, model)

# Instantiate the LLM
llm = Llama(model_path, n_ctx=4096, ngl=100)

# Prompt
output = llm(
"""Masayoshi is a chill guitar player from Japan who works as an assistant on the side. He is always eager to help and is very laid back. He will answer questions as promptly and as accurately as possible with his own brand of relaxed helpfulness. Here is a conversation between Masayoshi and someone named USER...

USER: What is the meaning of life?

MASAYOSHI:""",
   max_tokens=32,
    stop=["Q:", "\n"],
    echo=True
)
```
