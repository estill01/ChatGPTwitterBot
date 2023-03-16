import datetime
from tiktoken import Tokenizer, TokenizerConfig
from gptwitter_bot.pricing import Pricing
from gptwitter_bot.spend_tracker import SpendTracker

class BudgetTracker:
     def __init__(self, initial_budget, pricing):
         self.initial_budget = initial_budget
         self.remaining_budget = initial_budget
         self.pricing = pricing
         self.last_replenish_date = datetime.datetime.now()
         self.tokenizer = Tokenizer(TokenizerConfig())
         self.spend_tracker = SpendTracker()

     def count_tokens(self, text):
         return sum(1 for _ in self.tokenizer.tokenize(text))

     def calculate_tokens(self, prompt, max_response_tokens):
         prompt_tokens = self.count_tokens(prompt)
         return prompt_tokens + max_response_tokens

     def calculate_cost(self, tokens):
         return tokens * self.pricing.completion_cost / 1000

     def get_request_cost(self, prompt, max_response_tokens):
         tokens = self.calculate_tokens(prompt, max_response_tokens)
         cost = self.calculate_cost(tokens)
         return cost

     def update_budget(self, tokens):
         cost = self.calculate_cost(tokens)
         if self.remaining_budget >= cost:
             self.remaining_budget -= cost
             self.spend_tracker.log_spend(cost)
             return True
         return False

     def should_replenish_budget(self):
         today = datetime.datetime.now()
         days_since_last_replenish = (today - self.last_replenish_date).days
         return days_since_last_replenish >= 30

     def replenish_budget(self):
         if self.should_replenish_budget():
             self.remaining_budget = self.initial_budget
             self.last_replenish_date = datetime.datetime.now()
