import json
import os
import yaml
from collections import defaultdict
from agents.performance_agent import PerformanceAgent  # <-- Added import

def get_powerplay_score(overs, powerplays):
    for pp in powerplays:
        if pp.get("type") == "mandatory":
            start = pp.get("from")
            end = pp.get("to")
            start_over = int(str(start).split('.')[0])
            start_ball = int(str(start).split('.')[1])
            end_over = int(str(end).split('.')[0])
            end_ball = int(str(end).split('.')[1])
            runs = 0
            wickets = 0
            current_over = 0
            for over in overs:
                if current_over < start_over or current_over > end_over:
                    current_over += 1
                    continue
                for i, delivery in enumerate(over.get("deliveries", [])):
                    if (current_over == start_over and i+1 < start_ball):
                        continue
                    if (current_over == end_over and i+1 > end_ball):
                        continue
                    runs += delivery.get("runs", {}).get("total", 0)
                    if "wickets" in delivery:
                        wickets += len(delivery["wickets"])
                current_over += 1
            return runs, wickets, start, end
    return 0, 0, None, None

def main():
    while True:
        print("Select data source:")
        print("1. RECENT MATCHES")
        print("2. IPL MATCHES")
        print("3. Exit")
        source = input("Enter 1, 2, or 3: ")
        if source == "3":
            break

        match = input("Enter the match ID (e.g., '524916'): ")
        if not match:
            continue

        if source == "1":
            folder = r"C:\Users\sidha\OneDrive\Desktop\CRIC_CREW\NEW DATA"
        elif source == "2":
            folder = r"C:\Users\sidha\OneDrive\Desktop\IPL DATA"
        else:
            print("Invalid source selection.\n")
            continue

        file_path = rf"{folder}\{match}.json"
        print("Trying to open:", file_path)
        print("File exists:", os.path.exists(file_path))
        try:
            if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                with open(file_path, "r", encoding="utf-8") as f:
                    data_json = yaml.safe_load(f)
            else:
                with open(file_path, "r", encoding="utf-8") as f:
                    data_json = json.load(f)
        except FileNotFoundError:
            print("File not found. Please enter a valid match ID.\n")
            continue

        info = data_json.get("info", {})
        teams = info.get("teams", [])
        venue = info.get("venue", "Unknown venue")
        match_type = info.get("match_type", "Unknown type")
        event = info.get("event", {}).get("name", "Unknown event")
        outcome = info.get("outcome", {})
        winner = outcome.get("winner", "No result")
        date = info.get("dates", ["Unknown date"])[0]
        player_of_match = info.get("player_of_match", ["Unknown"])
        if isinstance(player_of_match, list):
            player_of_match = player_of_match[0] if player_of_match else "Unknown"

        print(f"\nMatch: {teams[0]} vs {teams[1]}")
        print(f"Event: {event}")
        print(f"Venue: {venue}")
        print(f"Date: {date}")
        print(f"Match Type: {match_type}")
        print(f"Winner: {winner}")
        print(f"Player of the Match: {player_of_match}\n")

        global_player_scores = defaultdict(int)
        global_bowler_wickets = defaultdict(int)
        global_player_fours = defaultdict(int)
        global_player_sixes = defaultdict(int)
        global_fielding_stats = defaultdict(lambda: defaultdict(int))

        for inning in data_json.get("innings", []):
            team = inning.get("team", "Unknown team")
            print(f"--- {team} Innings ---")
            total_runs = 0
            total_wickets = 0
            total_overs = len(inning.get("overs", []))
            player_scores = defaultdict(int)
            player_balls = defaultdict(int)
            player_fours = defaultdict(int)
            player_sixes = defaultdict(int)
            bowler_wickets = defaultdict(int)
            bowler_runs = defaultdict(int)
            bowler_balls = defaultdict(int)
            bowler_extras = defaultdict(int)
            bowler_extras_types = defaultdict(lambda: defaultdict(int))
            fielding_stats = defaultdict(lambda: defaultdict(int))
            partnerships = defaultdict(int)
            extras_total = 0
            extras_types = defaultdict(int)
            fall_of_wickets = []
            current_pair = None
            pair_runs = 0
            score_at_ball = 0

            for over in inning.get("overs", []):
                for delivery in over.get("deliveries", []):
                    runs = delivery.get("runs", {}).get("total", 0)
                    batter = delivery.get("batter")
                    bowler = delivery.get("bowler")
                    non_striker = delivery.get("non_striker")
                    batter_runs = delivery.get("runs", {}).get("batter", 0)
                    extras = delivery.get("runs", {}).get("extras", 0)
                    extras_total += extras
                    player_scores[batter] += batter_runs
                    player_balls[batter] += 1
                    if batter_runs == 4:
                        player_fours[batter] += 1
                    if batter_runs == 6:
                        player_sixes[batter] += 1
                    if bowler:
                        bowler_runs[bowler] += runs
                        bowler_balls[bowler] += 1
                        bowler_extras[bowler] += extras
                        # Extras by type
                        for ext_type in ["wides", "legbyes", "byes", "noballs"]:
                            if "extras" in delivery and ext_type in delivery["extras"]:
                                val = delivery["extras"][ext_type]
                                bowler_extras_types[bowler][ext_type] += val
                                extras_types[ext_type] += val
                    total_runs += runs
                    score_at_ball += runs
                    # Partnerships
                    if batter and non_striker:
                        pair = tuple(sorted([batter, non_striker]))
                        partnerships[pair] += runs
                        current_pair = pair
                        pair_runs += runs
                    # Wickets
                    if "wickets" in delivery:
                        total_wickets += len(delivery["wickets"])
                        if bowler:
                            bowler_wickets[bowler] += len(delivery["wickets"])
                        for wicket in delivery["wickets"]:
                            kind = wicket.get("kind", "unknown")
                            player_out = wicket.get("player_out", "unknown")
                            fielders = wicket.get("fielders", [])
                            fielder_names = [f.get("name") for f in fielders if "name" in f]
                            fall_of_wickets.append({
                                "over": over["over"],
                                "score": score_at_ball,
                                "player_out": player_out,
                                "kind": kind,
                                "bowler": bowler,
                                "fielders": fielder_names
                            })
                            # Fielding stats
                            if kind == "caught":
                                for fielder in fielder_names:
                                    fielding_stats[fielder]["catches"] += 1
                            if kind == "run out":
                                for fielder in fielder_names:
                                    fielding_stats[fielder]["run outs"] += 1
                            if kind == "stumped":
                                for fielder in fielder_names:
                                    fielding_stats[fielder]["stumpings"] += 1
                        # New partnership starts after wicket
                        pair_runs = 0

            print(f"{team}: {total_runs}/{total_wickets} in {total_overs} overs")
            # Powerplay score
            powerplays = inning.get("powerplays", [])
            if powerplays:
                pp_runs, pp_wickets, pp_start, pp_end = get_powerplay_score(inning.get("overs", []), powerplays)
                print(f"  Powerplay ({pp_start} to {pp_end}): {pp_runs}/{pp_wickets}")
            # Player scores
            print("Player scores:")
            for player, runs in sorted(player_scores.items(), key=lambda x: -x[1]):
                balls = player_balls[player]
                fours = player_fours[player]
                sixes = player_sixes[player]
                sr = (runs / balls * 100) if balls else 0
                print(f"  {player}: {runs} ({balls} balls, {fours}/4s, {sixes}/6s, SR: {sr:.2f})")
            # Use PerformanceAgent here
            player_data = {
                'player': list(player_scores.keys()),
                'runs': list(player_scores.values())
            }
            perf_agent = PerformanceAgent(player_data)
            performance_scores = perf_agent.run()
            print("PerformanceAgent scores (player -> runs):")
            for player, score in performance_scores.items():
                print(f"  {player}: {score}")
            # Best batter
            if player_scores:
                best_batter = max(player_scores.items(), key=lambda x: x[1])
                print(f"Best batter: {best_batter[0]} ({best_batter[1]} runs)")
                runs_vs_bowler = defaultdict(int)
                for over in inning.get("overs", []):
                    for delivery in over.get("deliveries", []):
                        batter = delivery.get("batter")
                        bowler = delivery.get("bowler")
                        runs = delivery.get("runs", {}).get("batter", 0)
                        if batter == best_batter[0] and bowler:
                            runs_vs_bowler[bowler] += runs
                print(f"Runs by {best_batter[0]} against each bowler:")
                for bowler, runs in sorted(runs_vs_bowler.items(), key=lambda x: -x[1]):
                    print(f"  {bowler}: {runs}")
            # Bowling details
            print("Bowler performance:")
            for bowler in sorted(bowler_balls, key=lambda x: -bowler_wickets[x]):
                balls = bowler_balls[bowler]
                overs = balls // 6 + (balls % 6) / 6
                runs_conceded = bowler_runs[bowler]
                wickets = bowler_wickets[bowler]
                econ = runs_conceded / overs if overs else 0
                print(f"  {bowler}: {overs:.1f} overs, {runs_conceded} runs, {wickets} wickets, Econ: {econ:.2f}")
                print(f"    Extras: {bowler_extras[bowler]} (", end="")
                print(", ".join(f"{k}: {v}" for k, v in bowler_extras_types[bowler].items()), end="") if bowler_extras_types[bowler] else print("none", end="")
                print(")")
            if bowler_wickets:
                best_bowler = max(bowler_wickets.items(), key=lambda x: x[1])
                print(f"Best bowler: {best_bowler[0]} ({best_bowler[1]} wickets)")
            # Extras
            print(f"Total extras: {extras_total} (", end="")
            print(", ".join(f"{k}: {v}" for k, v in extras_types.items()), end="") if extras_types else print("none", end="")
            print(")")
            # Fall of wickets
            print("Fall of wickets:")
            for fow in fall_of_wickets:
                print(f"  Over {fow['over']}, Score {fow['score']}: {fow['player_out']} ({fow['kind']}) by {fow['bowler']}", end="")
                if fow['fielders']:
                    print(f", fielders: {', '.join(fow['fielders'])}", end="")
                print()
            # Partnerships
            print("Partnerships:")
            for pair, runs in partnerships.items():
                print(f"  {' & '.join(pair)}: {runs} runs")
            # Fielding details
            print("Fielding:")
            for fielder, stats in fielding_stats.items():
                details = ", ".join(f"{k}: {v}" for k, v in stats.items())
                print(f"  {fielder}: {details}")

            # Aggregate stats for the full match
            for player, runs in player_scores.items():
                global_player_scores[player] += runs
            for player, wickets in bowler_wickets.items():
                global_bowler_wickets[player] += wickets
            for player, fours in player_fours.items():
                global_player_fours[player] += fours
            for player, sixes in player_sixes.items():
                global_player_sixes[player] += sixes
            for fielder, stats in fielding_stats.items():
                for k, v in stats.items():
                    global_fielding_stats[fielder][k] += v
            print()

        # OUTSIDE the innings loop: recommend fantasy team for the full match
        print("Recommended Fantasy Team (Full Match):")
        # Top 3 batters by runs
        top_batters = sorted(global_player_scores.items(), key=lambda x: -x[1])[:3]
        print("  Top Batters:")
        for i, (player, runs) in enumerate(top_batters, 1):
            print(f"    {i}. {player} ({runs} runs)")

        # Top 3 bowlers by wickets
        top_bowlers = sorted(global_bowler_wickets.items(), key=lambda x: -x[1])[:3]
        print("  Top Bowlers:")
        for i, (player, wickets) in enumerate(top_bowlers, 1):
            print(f"    {i}. {player} ({wickets} wickets)")

        # Top 3 all-rounders: players who scored runs and took wickets
        all_rounders = [
            (player, global_player_scores[player], global_bowler_wickets[player])
            for player in set(global_player_scores) & set(global_bowler_wickets)
            if global_player_scores[player] > 0 and global_bowler_wickets[player] > 0
        ]
        all_rounders = sorted(all_rounders, key=lambda x: (-(x[1] + x[2]*20)))[:3]
        print("  All-rounders:")
        if all_rounders:
            for i, (player, runs, wickets) in enumerate(all_rounders, 1):
                print(f"    {i}. {player} ({runs} runs, {wickets} wickets)")
        else:
            print("    None")
        print()

        # Advanced Fantasy Recommendation
        POINTS = {
            "run": 1,
            "wicket": 25,
            "four": 1,
            "six": 2,
            "catch": 8,
            "stumping": 12,
            "run_out": 12,
        }

        fantasy_points = defaultdict(int)
        for player, runs in global_player_scores.items():
            fantasy_points[player] += runs * POINTS["run"]
        for player, wickets in global_bowler_wickets.items():
            fantasy_points[player] += wickets * POINTS["wicket"]
        for player, fours in global_player_fours.items():
            fantasy_points[player] += fours * POINTS["four"]
        for player, sixes in global_player_sixes.items():
            fantasy_points[player] += sixes * POINTS["six"]
        for player, stats in global_fielding_stats.items():
            fantasy_points[player] += stats.get("catches", 0) * POINTS["catch"]
            fantasy_points[player] += stats.get("stumpings", 0) * POINTS["stumping"]
            fantasy_points[player] += stats.get("run outs", 0) * POINTS["run_out"]

        top_fantasy = sorted(fantasy_points.items(), key=lambda x: -x[1])[:11]
        print("Dream Fantasy XI (by fantasy points):")
        for i, (player, pts) in enumerate(top_fantasy, 1):
            print(f"  {i}. {player} ({pts} pts)")
        print()

        # Player of the match stats
        print(f"Player of the Match: {player_of_match}")
        for inning in data_json.get("innings", []):
            player_scores = defaultdict(int)
            player_balls = defaultdict(int)
            player_fours = defaultdict(int)
            player_sixes = defaultdict(int)
            # Bowling stats
            bowler_balls = defaultdict(int)
            bowler_runs = defaultdict(int)
            bowler_wickets = defaultdict(int)
            bowler_extras = defaultdict(int)
            for over in inning.get("overs", []):
                for delivery in over.get("deliveries", []):
                    batter = delivery.get("batter")
                    bowler = delivery.get("bowler")
                    batter_runs = delivery.get("runs", {}).get("batter", 0)
                    runs = delivery.get("runs", {}).get("total", 0)
                    extras = delivery.get("runs", {}).get("extras", 0)
                    if batter == player_of_match:
                        player_scores[batter] += batter_runs
                        player_balls[batter] += 1
                        if batter_runs == 4:
                            player_fours[batter] += 1
                        if batter_runs == 6:
                            player_sixes[batter] += 1
                    if bowler == player_of_match:
                        bowler_balls[bowler] += 1
                        bowler_runs[bowler] += runs
                        bowler_extras[bowler] += extras
                        if "wickets" in delivery:
                            bowler_wickets[bowler] += len(delivery["wickets"])
            # Print batting stats if available
            if player_of_match in player_scores:
                print(f"  Batting: {player_scores[player_of_match]} runs, {player_balls[player_of_match]} balls, {player_fours[player_of_match]}/4s, {player_sixes[player_of_match]}/6s")
            # Print bowling stats if available
            if player_of_match in bowler_balls:
                balls = bowler_balls[player_of_match]
                overs = balls // 6 + (balls % 6) / 6
                runs_conceded = bowler_runs[player_of_match]
                wickets = bowler_wickets[player_of_match]
                extras = bowler_extras[player_of_match]
                econ = runs_conceded / overs if overs else 0
                print(f"  Bowling: {overs:.1f} overs, {runs_conceded} runs, {wickets} wickets, {extras} extras, Econ: {econ:.2f}")
        print()

if __name__ == "__main__":
    main()