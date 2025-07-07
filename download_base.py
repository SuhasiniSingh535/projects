import os
os.environ["HF_HOME"] = r"D:\hf_cache"  # Optional, ensures download cache is on D:

from transformers import AutoModelForCausalLM, AutoTokenizer

base_model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
save_dir = r"E:\model_storage\tinyllama_base"  # ensure this drive has >3 GB

# Load and save tokenizer
tokenizer = AutoTokenizer.from_pretrained(base_model)
os.makedirs(save_dir, exist_ok=True)
tokenizer.save_pretrained(save_dir)

# Load model
model = AutoModelForCausalLM.from_pretrained(base_model)
# Save model binary
model.save_pretrained(save_dir, safe_serialization=False)

print("✅ Base model saved to:", save_dir)
