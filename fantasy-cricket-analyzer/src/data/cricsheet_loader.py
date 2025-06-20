import yaml
import pandas as pd

class CricSheetLoader:
    def __init__(self, url):
        self.url = url
        self.data = None

    def load_data(self):
        with open(self.url, 'r', encoding='utf-8') as f:
            self.data = yaml.safe_load(f)
        return self.data

    def parse_data(self, raw_data):
        player_stats = {}
        for inning in raw_data.get('innings', []):
            team = inning.get('team', 'Unknown')
            for delivery in inning.get('deliveries', []):
                for ball, info in delivery.items():
                    batsman = info.get('batsman')
                    runs = info.get('runs', {}).get('batsman', 0)
                    if batsman:
                        if batsman not in player_stats:
                            player_stats[batsman] = {'runs': 0, 'balls': 0, 'team': team}
                        player_stats[batsman]['runs'] += runs
                        player_stats[batsman]['balls'] += 1
        df = pd.DataFrame.from_dict(player_stats, orient='index')
        df.index.name = 'player'
        return df.reset_index()

parsed_data = None
print("Parsed data:", parsed_data)