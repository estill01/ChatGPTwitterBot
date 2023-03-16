class UserInteractionIndex:
    def __init__(self):
        self.user_interactions = {}

    def record_interaction(self, user_id, followers_count, tweet_timestamp, topic_summary):
        if user_id not in self.user_interactions:
            self.user_interactions[user_id] = []

        last_interaction = self.user_interactions[user_id][-1] if self.user_interactions[user_id] else None
        followers_delta = followers_count - last_interaction["followers_count"] if last_interaction else 0
        time_delta = tweet_timestamp - last_interaction["timestamp"] if last_interaction else None

        interaction = {
            "timestamp": tweet_timestamp,
            "followers_count": followers_count,
            "followers_delta": followers_delta,
            "time_delta": time_delta,
            "topic_summary": topic_summary,
        }

        self.user_interactions[user_id].append(interaction)

