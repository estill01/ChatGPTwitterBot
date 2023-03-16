import tweepy
from ratelimiter import RateLimiter
from gptwitter_bot.pricing import Pricing
from gptwitter_bot.budget_tracker import BudgetTracker


class TwitterBot:
     def __init__(self, budget, pricing, handle, models):
         self.rate_limiter = RateLimiter(max_calls=20, period=3600)  # Limit to 20 calls per hour
         self.budget_tracker = BudgetTracker(budget, pricing)
         self.handle = handle
         self.models = models

    def generate_response(self, prompt, model_key):
        tokens = self.budget_tracker.calculate_tokens(prompt, 150)
        if self.budget_tracker.update_budget(tokens):
            with self.rate_limiter:
                response = openai.Completion.create(
                    engine=self.models[model_key],
                    prompt=prompt,
                    temperature=0.7,
                    max_tokens=150,
                    n=1,
                    stop=None,
                    top_p=1,
                )
            return response.choices[0].text.strip()


class TwitterBotStreamListener(tweepy.StreamListener):
     def __init__(self, api, twitter_bot):
         super().__init__(api)
         self.twitter_bot = twitter_bot

     def on_status(self, status):
         # TODO Fix; currently ignores retweets AND replies
         if hasattr(status, "retweeted_status") or status.in_reply_to_status_id:
             return

         # Check if you're allowed to replenish budget (i.e. it's been >= 30 days)
         self.twitter_bot.budget_tracker.replenish_budget()

         user_question = status.text
         prompt = f"User asked: {user_question}\n{self.twitter_bot.handle} response:"
         # TODO Fix -- choose model more dynamically
         model_key = "gpt_4_8k"  
         tokens = self.twitter_bot.budget_tracker.calculate_tokens(prompt, 150)
         if self.twitter_bot.budget_tracker.update_budget(tokens):
             response = self.twitter_bot.generate_response(prompt, model_key)

         if response:
             reply = f"@{status.user.screen_name} {response}"
             self.api.update_status(status=reply, in_reply_to_status_id=status.id)

     def on_error(self, status_code):
         if status_code == 420:
             return False

