import torch
from langchain.llms import HuggingFacePipeline
from transformers import (
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    pipeline,
)

# TODO Look into other models that are available
model_id = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(
    model_id,
    load_in_8bit=True,  # optional, depending on GPU RAM
)

pipe = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=100,
)

local_llm = HuggingFacePipeline(pipeline=pipe)

local_llm("What is the capital of France?")


llm_chain = LLMChain(
    prompt=prompt,
    llm=local_llm,
)
question = "What is the capital of England?"
print(llm_chain.run(question))
