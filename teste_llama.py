import transformers
import torch

model_id = "meta-llama/Meta-Llama-3-8B"

HF_TOKEN='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'

pipeline = transformers.pipeline(
  "text-generation",
  model="meta-llama/Meta-Llama-3-8B",
  model_kwargs={"torch_dtype": torch.bfloat16},
  device="cuda",
)