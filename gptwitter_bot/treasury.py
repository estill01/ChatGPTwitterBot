from gptwitter_bot.trackers import BaseTracker

class Treasury(BaseTracker):
    def __init__(self, initial_value: float = 0.0):
        super().__init__()
        self.value = initial_value

    def receive_value(self, amount: float):
        self.value += amount
        self.log_received_value(amount)

    def allocate_value(self, amount: float):
        if self.value >= amount:
            self.value -= amount
            self.log_allocated_value(amount)
            return amount
        else:
            raise ValueError("Insufficient value in the treasury")

    def log_received_value(self, amount: float):
        self._log({"action": "received_value", "amount": amount})

    def log_allocated_value(self, amount: float):
        self._log({"action": "allocated_value", "amount": amount})

