class ConsistencyAgent:
    def __init__(self, player_data):
        self.player_data = player_data

    def run(self):
        # Return a dict: player -> runs per ball (as a simple consistency metric)
        return dict(
            zip(
                self.player_data['player'],
                self.player_data['runs'] / self.player_data['balls']
            )
        )

    def calculate_consistency(self):
        consistency_metrics = {}
        for _, row in self.player_data.iterrows():
            player = row['player']
            runs = row['runs']
            balls = row['balls']
            # Example: consistency as runs per ball
            consistency_metrics[player] = runs / balls if balls else 0
        return consistency_metrics