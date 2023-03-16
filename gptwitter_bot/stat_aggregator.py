class StatAggregator:
    def __init__(self, spend_tracker, tweet_tracker, budget_tracker):
        self.spend_tracker = spend_tracker
        self.tweet_tracker = tweet_tracker
        self.budget_tracker = budget_tracker

    def get_spend_rate(self, interval):
        return self.spend_tracker.get_rate(interval)

    def get_tweet_rate(self, interval):
        return self.tweet_tracker.get_rate(interval)

    def get_budget_rate(self, interval):
        return self.budget_tracker.get_rate(interval)

    def get_spend_acceleration(self, interval1, interval2):
        return self.spend_tracker.get_acceleration(interval1, interval2)

    def get_tweet_acceleration(self, interval1, interval2):
        return self.tweet_tracker.get_acceleration(interval1, interval2)

    def get_budget_acceleration(self, interval1, interval2):
        return self.budget_tracker.get_acceleration(interval1, interval2)


