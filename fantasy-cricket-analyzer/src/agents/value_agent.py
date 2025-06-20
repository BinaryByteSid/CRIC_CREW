class ValueAgent:
    def __init__(self, performance_scores, consistency_scores):
        self.performance_scores = performance_scores
        self.consistency_scores = consistency_scores
        self.final_scores = {}

    def run(self):
        self.aggregate_scores()

    def aggregate_scores(self):
        for player in self.performance_scores:
            perf = self.performance_scores.get(player, 0)
            cons = self.consistency_scores.get(player, 0)
            # Example: weighted sum
            self.final_scores[player] = 0.7 * perf + 0.3 * cons

    def get_ranked_recommendations(self):
        # Return players sorted by final score
        return sorted(self.final_scores, key=self.final_scores.get, reverse=True)