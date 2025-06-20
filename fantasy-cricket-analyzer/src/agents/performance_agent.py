class PerformanceAgent:
    def __init__(self, player_data):
        self.player_data = player_data

    def run(self):
        # Return a dict: player -> runs
        return dict(zip(self.player_data['player'], self.player_data['runs']))

    def get_performance_scores(self):
        current_form_score = self.calculate_current_form()
        past_performance_score = self.calculate_past_performance()
        venue_specific_score = self.calculate_venue_specific_stats()
        
        total_score = current_form_score + past_performance_score + venue_specific_score
        return total_score

    def calculate_current_form(self):
        # Logic to calculate current form score
        return 0  # Placeholder for actual score calculation

    def calculate_past_performance(self):
        # Logic to calculate past performance score
        return 0  # Placeholder for actual score calculation

    def calculate_venue_specific_stats(self):
        # Logic to calculate venue-specific score
        return 0  # Placeholder for actual score calculation