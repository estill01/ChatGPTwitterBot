from datetime import datetime, timedelta
from gptwitter_bot.treasury import Treasury

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
    def log_revenue(self, amount: float, source: str):
        self._log({"action": "revenue", "amount": amount, "source": source})


class SpendTracker(BaseTracker):
    def log_spend(self, amount: float, category: str):
        self._log({"action": "spend", "amount": amount, "category": category})


# TODO Probably want to create Treasury outside of BudgetTracker and then pass in a reference to it
class BudgetTracker(BaseTracker):
    def __init__(
        self,
        treasury: Treasury,
        initial_budget: float,
        budget_cycle_duration: datetime.timedelta = datetime.timedelta(days=30),
        auto_allocation: float = 0.0,
        spend_tracker: SpendTracker = None,
        revenue_tracker: RevenueTracker = None,
    ):
        super().__init__()
        self.treasury = treasury
        self.budget_cycle_duration = budget_cycle_duration
        self.auto_allocation = auto_allocation
        self.spend_tracker = spend_tracker or SpendTracker()
        self.revenue_tracker = revenue_tracker or RevenueTracker()
        self.budget_cycle_start_time = datetime.datetime.now()
        self.budget = initial_budget
        self.remaining_budget = initial_budget

    def can_spend(self, amount: float) -> bool:
        return amount <= self.remaining_budget

    def spend(self, amount: float):
        if self.can_spend(amount):
            self.remaining_budget -= amount
            self.spend_tracker.log_spend(amount)
        else:
            raise ValueError("Insufficient budget")

    def receive_allocation(self, amount: float):
        allocation_received = self.treasury.allocate_value(amount)
        self.remaining_budget += allocation_received
        if self.remaining_budget > self.budget:
            additional_budget = self.remaining_budget - self.budget
            self.increase_budget(additional_budget)
            print(f"Warning: Remaining budget ({self.remaining_budget}) is larger than the total budget ({self.budget}). Total budget has been updated.")

    def increase_budget(self, amount: float):
        self.budget += amount
        self.log_budget_increase(amount)

    def decrease_budget(self, amount: float):
        if amount <= self.total_budget:
            self.budget -= amount
            if self.budget < self.remaining_budget:
                difference = self.remaining_budget - self.budget
                self.remaining_budget = self.budget
                self.treasury.deposit_value(difference)
            self.log_budget_decrease(amount)
        else:
            raise ValueError("Insufficient budget")

    def set_budget(self, new_budget: float):
        if new_budget >= 0:
            diff = new_budget - self.budget
            if diff >= 0:
                self.increase_budget(diff)
            else:
                self.decrease_budget(abs(diff))
        else:
            raise ValueError("Invalid budget value")

    def remaining_budget_cycle_time(self) -> datetime.timedelta:
        time_since_cycle_start = datetime.datetime.now() - self.budget_cycle_start_time
        return self.budget_cycle_duration - time_since_cycle_start

    # TODO a bit funky that BudgetTracker is reaching into Treasury's domain and taking value rather than requesting it and getting approval
    def reset_budget_cycle(self):
        self.log_end_of_cycle_remaining_budget(self.remaining_budget)
        self.budget_cycle_start_time = datetime.datetime.now()
        allocated_value = self.treasury.allocate_value(self.auto_allocation)
        self.increase_budget(allocated_value)

    def change_budget_cycle_duration(self, new_duration: datetime.timedelta):
        self.log_budget_cycle_duration_change(self.budget_cycle_duration, new_duration)
        self.budget_cycle_duration = new_duration

    def log_budget_increase(self, amount: float):
        self._log({"action": "budget_increase", "amount": amount})

    def log_budget_decrease(self, amount: float):
        self._log({"action": "budget_decrease", "amount": amount})

    def log_end_of_cycle_remaining_budget(self, amount: float):
        self._log({"action": "end_of_cycle_remaining_budget", "amount": amount})

    def log_budget_cycle_duration_change(self, old_duration: datetime.timedelta, new_duration: datetime.timedelta):
        self._log({"action": "budget_cycle_duration_change", "old_duration": old_duration, "new_duration": new_duration})


