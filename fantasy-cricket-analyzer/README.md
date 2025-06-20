# 🏏 Fantasy Cricket Player Analyzer

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-In--Development-orange)

## 🔍 Overview

**Fantasy Cricket Player Analyzer** is a Python-based analysis tool that helps fantasy cricket enthusiasts make informed decisions by analyzing player performances using historical match data from **CricSheet** and intelligent agents built with **CrewAI**.

This project processes local JSON match data and evaluates players based on performance trends, consistency, and fantasy value metrics, ultimately ranking players based on a calculated **fantasy score**.

---

## ✨ Key Features

- 🎯 **Performance Analysis**  
  Analyze players’ recent and historic performances, including match format, opponent, and venue-specific stats.

- 📊 **Consistency Metrics**  
  Evaluate players' consistency across a range of recent matches to determine reliability.

- 💸 **Fantasy Value Scoring**  
  Calculate a composite fantasy score using CrewAI-powered agents and recommend top-performing players.

- 📂 **Modular Design**  
  Built with extensibility in mind — easily plug in new agents, data sources, or scoring logic.

---

## 🗂 Project Structure



## Project Structure
```
fantasy-cricket-analyzer
├── src
│ ├── main.py # Main entry point
│ ├── agents/
│ │ ├── performance_agent.py # Performance-based evaluation logic
│ │ ├── consistency_agent.py # Consistency scoring logic
│ │ └── value_agent.py # Final scoring and ranking logic
│ ├── data/
│ │ └── cricsheet_loader.py # Loads JSON data from CricSheet
│ ├── analysis/
│ │ └── player_analysis.py # Orchestrates full player analysis pipeline
│ └── utils/
│ └── helpers.py # Helper functions and utilities
├── requirements.txt # Python dependencies
└── README.md # Project documentation
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/fantasy-cricket-analyzer.git
   ```
2. Navigate to the project directory:
   ```
   cd fantasy-cricket-analyzer
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python src/main.py
```
Follow the prompts to input your analysis criteria and receive player recommendations.
Sample JSON Format
[
  {
    "match_id": "match_001",
    "player": "Virat Kohli",
    "runs": 75,
    "balls_faced": 50,
    "wickets": 0,
    "venue": "Wankhede",
    "format": "T20",
    "date": "2023-04-10",
    "opponent": "Australia"
  },
  {
    "match_id": "match_002",
    "player": "Jasprit Bumrah",
    "runs_conceded": 24,
    "wickets": 3,
    "overs": 4,
    "venue": "Eden Gardens",
    "format": "ODI",
    "date": "2023-05-15",
    "opponent": "England"
  }
]
To switch to online datasets or shared storage in the future, consider:

Uploading data to a remote repository or database

Using public CricSheet datasets via APIs or hosted files

## Future Enhancements
Live data integration from APIs

Interactive web dashboard

ML-based player score prediction

Venue-specific team strategy suggestions


## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## Acknowledgements
CricSheet.org for open-access cricket match data

CrewAI for intelligent agent framework

## License
This project is licensed under the MIT License - see the LICENSE file for details.