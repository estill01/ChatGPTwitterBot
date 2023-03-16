from tiktoken.tokenizer import Tokenizer 

class CostCalculator:
    def __init__(self, model_pricing: dict):
        self.model_pricing = model_pricing
        self.tokenizer = Tokenizer()

    def count_tokens(self, text: str):
        tokens = list(self.tokenizer.tokenize(text))
        return len(tokens)

    def calculate_cost(self, text: str, model: str):
        token_count = self.count_tokens(text)
        cost_per_token = self.model_pricing.get(model, 0.0)
        cost = token_count * cost_per_token
        return cost
