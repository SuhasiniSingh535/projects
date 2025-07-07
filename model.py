from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel  # If you're using adapter from LoRA

# Load your base TinyLlama model from local storage
base_dir = r"E:\model_storage\tinyllama_base"
lora_dir = r"C:\Users\suhas\ncert-chatbot\tiny_ncert_lora"


tokenizer = AutoTokenizer.from_pretrained(base_dir, use_fast=True)
base_model = AutoModelForCausalLM.from_pretrained(base_dir)

# Wrap with LoRA adapter if applicable
model_obj = PeftModel.from_pretrained(base_model, lora_dir)

# ✅ Ensure pad token is set
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model_obj.generation_config.pad_token_id = tokenizer.pad_token_id

def generate_text(prompt, max_tokens=400, temperature=0.4):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(model_obj.device)
    output_ids = model_obj.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_new_tokens=max_tokens,
        temperature=temperature,
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id
    )
    text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return text[len(prompt):].strip()
