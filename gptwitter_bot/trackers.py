import datetime
from tiktoken import Tokenizer, TokenizerConfig
from datetime import datetime, timedelta
from gptwitter_bot.pricing import Pricing

class BaseTracker:
    def __init__(self, data_type):
        self.data = []
        self.data_type = data_type

    def _log(self, data, timestamp=None):
        if timestamp is None:
            timestamp = datetime.datetime.now()
        data_entry = {"data": data, "timestamp": timestamp}
        self.data.append(data_entry)

    def get_rate(self, interval):
        now = datetime.datetime.now()
        start_time = now - datetime.timedelta(seconds=interval)

        total_amount = sum(
            data["data"] for data in self.data
            if data["timestamp"] >= start_time
        )

        return total_amount / interval

    def get_acceleration(self, interval1, interval2):
        rate1 = self.get_rate(interval1)
        rate2 = self.get_rate(interval2)
        return (rate2 - rate1) / (interval2 - interval1)


class TweetTracker(BaseTracker):
    def __init__(self):
        super().__init__("tweet_data")

    def log_tweet(self, timestamp=None):
        self._log(1, timestamp)


class RevenueTracker(BaseTracker):
    def __init__(self):
        super().__init__()

    def log_revenue(self, amount):
        self._log(amount)


class SpendTracker(BaseTracker):
    def __init__(self):
        super().__init__("spending_data")

    def log_spend(self, amount, timestamp=None):
        self._log(amount, timestamp)


class BudgetTracker(BaseTracker):
    def __init__(self, initial_budget, cycle_duration=timedelta(days=30), auto_allocation=None, spend_tracker=None, revenue_tracker=None):
        super().__init__()
        self.initial_budget = initial_budget
        self.cycle_duration = cycle_duration
        self.auto_allocation = auto_allocation or initial_budget
        self.spend_tracker = spend_tracker
        self.revenue_tracker = revenue_tracker
        self.start_date = datetime.now()
        self._allocation = self.initial_budget

    def remaining_time_in_cycle(self):
        now = datetime.now()
        time_since_start = now - self.start_date
        time_until_next_cycle = self.cycle_duration - time_since_start
        return time_until_next_cycle

    def in_new_cycle(self):
        return datetime.now() >= self.start_date + self.cycle_duration

    def reset_cycle(self):
        if self.in_new_cycle():
            self.start_date = datetime.now()
            self._allocation = self.auto_allocation

    def update_budget(self, tokens):
        cost = self.calculate_cost(tokens)
        remaining_budget = self._allocation - self.spend_tracker.total

        if remaining_budget >= cost:
            self.spend_tracker.log_spend(cost)
            self._log("spend", cost)
            return True

        return False

    def allocate_budget(self, amount):
        self._allocation += amount
        self._log("allocate", amount)

    def deallocate_budget(self, amount):
        if amount <= self._allocation:
            self._allocation -= amount
            self._log("deallocate", amount)
        else:
            raise ValueError("Cannot deallocate more than the current allocation.")

    def calculate_cost(self, tokens):
        return tokens * self.spend_tracker.pricing.completion_cost / 1000

    @property
    def remaining_budget(self):
        remaining_budget = self._allocation - self.spend_tracker.total
        return max(0, remaining_budget)

    def replenish_budget(self):
        if self.revenue_tracker:
            revenue = self.revenue_tracker.total
            allocation_amount = min(revenue, self.auto_allocation)
            self.allocate_budget(allocation_amount)
            self.revenue_tracker.reset_total()

    def should_replenish_budget(self):
        return self.in_new_cycle()

