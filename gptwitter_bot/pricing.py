class Pricing:
    def __init__(self, model, prompt_cost, completion_cost=None):
        self.model = model
        self.prompt_cost = prompt_cost
        self.completion_cost = completion_cost or prompt_cost

