# habits-visualizer

Visualization and analysis for data from open source project [Loop Habits Tracker app](https://github.com/iSoron/uhabits).

## Features

- 📊 Overall progress heatmap
- 📈 Habit strength trend visualization
- 📅 Monthly comparison reports
- 🔍 Individual habit trend analysis
- 📝 Summary statistics and streaks
- 💾 CSV exports for further analysis

## Quick Start

1. Place your Loop Habits export files in `data/` directory:
   - `Checkmarks.csv`
   - `Habits.csv`
   - `Scores.csv`

2. Install dependencies:

```bash
pip install pandas matplotlib numpy
```  

3. Run the analysis:

```bash

python run.py
```

## Output Files

All outputs will be saved in the `output/` directory.
File Pattern and Description:

- `habit_completion_history.png` Heatmap of all habits over time
- `habit_score_trends.png` Trend lines for habit scores
- `monthly_report_YYYY_MM.png` Visual monthly comparison
- `monthly_habit_report_YYYY_MM.csv` Tabular monthly completion rates
- `habit_trend_<NAME>.png` Detailed trend for each habit
- `habit_summary.csv` Overall statistics and streaks

### Example Output

Habit Heatmap
Overall progress visualization

Monthly Report
Monthly habit performance comparison

### Customization

Modify run_analysis.py to:

    Change date ranges for monthly reports

    Adjust visualization styles

    Add custom analysis metrics

## Requirements

    Python 3.7+

    pandas

    matplotlib

    numpy

## License

MIT License - use freely, credit appreciated.
