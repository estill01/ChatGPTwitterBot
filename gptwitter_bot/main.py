import openai
import tweepy
from config import (
    TWITTER_API_KEY, TWITTER_API_SECRET_KEY,
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET,
    OPENAI_API_KEY,
)
from gptwitter_bot.pricing import Pricing
from gptwiter_bot.budget_tracker import BudgetTracker
from gptwitter_bot.twitter_bot import TwitterBot, TwitterBotStreamListener

# TODO error check / check these work
openai.api_key = OPENAI_API_KEY
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


#TODO Fix this up.. / move to Pricing
openai_pricing = {
     "gpt_4_8k": Pricing("gpt-4-8k", 0.03, 0.06),
     "gpt_4_32k": Pricing("gpt-4-32k", 0.06, 0.12),
     "gpt_3_5_turbo": Pricing("gpt-3.5-turbo", 0.002),
     "dall_e_1024": Pricing("dall-e-1024", 0.02),
     "dall_e_512": Pricing("dall-e-512", 0.018),
     "dall_e_256": Pricing("dall-e-256", 0.016),
}

# TODO take this as args / set this in config
initial_budget = 50 - 10  # Total budget - server cost
handle = "@chatgpt"
# TODO fix this..
models = {
    "gpt_4_8k": "text-davinci-002",
}
chosen_pricing = openai_pricing["gpt_4_8k"]

twitter_bot = TwitterBot(initial_budget, chosen_pricing, handle, models)
stream_listener = TwitterBotStreamListener(api, twitter_bot)
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=[handle], is_async=True)
