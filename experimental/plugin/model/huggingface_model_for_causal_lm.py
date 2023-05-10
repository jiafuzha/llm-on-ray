import transformers

from .model import Model

class HuggingFaceModelForCausalLM(Model):
    def __call__(self, config):
        name = config.get("name")
        if name is None:
            raise ValueError("Model config error, config should contain a model name")
        model_config = config.get("config", {})
        model = transformers.AutoModelForCausalLM.from_pretrained(name, **model_config)
        return model