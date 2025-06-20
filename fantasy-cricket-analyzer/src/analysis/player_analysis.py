class PlayerAnalysis:
    def __init__(self, performance_agent, consistency_agent, value_agent):
        self.performance_agent = performance_agent
        self.consistency_agent = consistency_agent
        self.value_agent = value_agent
        self.results = {}

    def analyze_players(self, player_data):
        self.performance_agent.run(player_data)
        self.consistency_agent.run(player_data)
        self.value_agent.run()

        self.results['performance_scores'] = self.performance_agent.get_performance_scores()
        self.results['consistency_metrics'] = self.consistency_agent.calculate_consistency()
        self.results['ranked_recommendations'] = self.value_agent.get_ranked_recommendations()

    def get_analysis_results(self):
        return self.results