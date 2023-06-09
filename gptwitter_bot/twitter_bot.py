import tweepy
from gptwitter_bot.trackers import BudgetTracker, StatTracker
from gptwitter_bot.cost_calculator import CostCalculator
from gptwitter_bot.user_interaction_index import UserInteractionIndex


class TwitterBot:
    def __init__(self, api_key, api_key_secret, access_token, access_token_secret, budget_tracker, handle, models, cost_calculator):
        self.auth = tweepy.OAuthHandler(api_key, api_key_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.twitter_api = tweepy.API(self.auth)
        self.budget_tracker = budget_tracker
        self.stat_tracker = StatTracker()
        self.handle = handle
        self.models = models
        self.cost_calculator = cost_calculator
        self.user_interaction_index = UserInteractionIndex()


    def generate_response(self, prompt, model_key):
        tokens = self.cost_calculator.count_tokens(prompt)
        cost = self.cost_calculator.calculate_cost(tokens)
        if self.budget_tracker.can_spend(cost):
            self.budget_tracker.spend(cost)
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

    def get_topic_summary(self, tweet_text):
        prompt = f"Summarize the topic of the following tweet: \"{tweet_text}\""
        tokens = self.cost_calculator.count_tokens(prompt)
        cost = self.cost_calculator.calculate_cost(tokens)

        if self.budget_tracker.can_spend(cost):
            self.budget_tracker.spend(cost)
            response = openai.Completion.create(
                engine=self.models["gpt_3_5_turbo"],
                prompt=prompt,
                temperature=0.7,
                max_tokens=50,
                n=1,
                stop=None,
                top_p=1,
            )
            return response.choices[0].text.strip()
        else:
            return "Insufficient budget for topic summary"


    def send_tweet(self, tweet_text):
        tokens = self.cost_calculator.count_tokens(tweet_text)
        cost = self.cost_calculator.calculate_cost(tokens)

        if self.budget_tracker.can_spend(cost):
            self.budget_tracker.spend(cost)
            self.twitter_api.update_status(status=tweet_text)
            print(f"Tweet sent: {tweet_text}")
        else:
            print("Insufficient budget to send the tweet")

    def start_stream(self, keywords):
        listener = TwitterBotStreamListener(api=self.twitter_api, twitter_bot=self)
        stream = tweepy.Stream(auth=self.auth, listener=listener)
        stream.filter(track=keywords, is_async=True)



class TwitterBotStreamListener(tweepy.StreamListener):
    def __init__(self, api, twitter_bot):
        super().__init__(api)
        self.twitter_bot = twitter_bot

    def on_status(self, status):

        if hasattr(status, "retweeted_status"): 
            return

        # Record user interaction

        user_id = status.user.id
        followers_count = status.user.followers_count
        tweet_timestamp = status.created_at
        # TODO Integrate 'should_spend' before doing this to evaluate if we should or not ; then update the index if you do
        topic_summary = self.twitter_bot.get_topic_summary(user_question)
        self.twitter_bot.user_interaction_index.record_interaction(user_id, followers_count, tweet_timestamp, topic_summary)

        # Respond (or not)
        self.twitter_bot.budget_tracker.reset_budget_cycle()

        user_question = status.text
        prompt = f"User asked: {user_question}\n{self.twitter_bot.handle} response:"
        model_key = "gpt_4_8k"
        tokens = self.twitter_bot.cost_calculator.count_tokens(prompt)
        cost = self.twitter_bot.cost_calculator.calculate_cost(tokens)

        if self.twitter_bot.budget_tracker.can_spend(cost):
            response = self.twitter_bot.generate_response(prompt, model_key)

            if response:
                self.twitter_bot.budget_tracker.spend_tracker.log_tweet(status.id)
                reply = f"@{status.user.screen_name} {response}"
                self.api.update_status(status=reply, in_reply_to_status_id=status.id)

    def on_error(self, status_code):
        if status_code == 420:
            return False

