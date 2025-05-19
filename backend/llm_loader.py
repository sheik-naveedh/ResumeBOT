from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline

def load_local_llm():
    model_name = "tiiuae/falcon-rw-1b"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device=-1,  
        max_new_tokens=300,
        do_sample=True,
        temperature=0.5,
        top_p=0.9
    )

    return HuggingFacePipeline(pipeline=pipe)