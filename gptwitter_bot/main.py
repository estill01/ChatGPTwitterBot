
import openai
import tweepy
from config import (
    TWITTER_API_KEY, TWITTER_API_SECRET_KEY,
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET,
    OPENAI_API_KEY,
)
from gptwitter_bot.trackers import BudgetTracker
from gptwitter_bot.twitter_bot import TwitterBot, TwitterBotStreamListener
from gptwitter_bot.cost_calculator import CostCalculator
import datetime

openai.api_key = OPENAI_API_KEY
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


# TODO .. make this better
initial_budget = 50 - 10  # Total budget - server cost

# Create a BudgetTracker instance
budget_tracker = BudgetTracker(
    initial_budget=initial_budget,
    budget_cycle_duration=datetime.timedelta(days=30),
    auto_allocation=0.0,
)

# Initialize the CostCalculator with pricing information -- TODO Move this into the CostCalculator class as defaults
pricing = {
    "gpt_3_5_turbo": (0.002, 0.002),
}
cost_calculator = CostCalculator(pricing=pricing)

handle = "@chatgpt"
models = {
    "gpt_3_5_turbo": "gpt-3.5-turbo"
}

twitter_bot = TwitterBot(api_key=TWITTER_API_KEY,
                         api_key_secret=TWITTER_API_SECRET_KEY,
                         access_token=TWITTER_ACCESS_TOKEN,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
                         budget_tracker=budget_tracker,
                         handle=handle,
                         models=models,
                         cost_calculator=cost_calculator)

keywords = [handle]
twitter_bot.start_stream(keywords)

