import os
from datetime import datetime
from .loader import load_habit_data
from .analyzer import generate_monthly_report
from .visualizer import (
    plot_overall_progress,
    plot_habit_strengths,
    visualize_monthly_report,
    plot_habit_trends,
)
from .reporter import save_monthly_report, generate_summary


def main():
    # Configuration
    DATA_DIR = 'data'
    OUTPUT_DIR = 'output'

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load data
    print("Loading habit data...")
    habit_data = load_habit_data(
        checkmarks_path=os.path.join(DATA_DIR, 'Checkmarks.csv'),
        habits_path=os.path.join(DATA_DIR, 'Habits.csv'),
        scores_path=os.path.join(DATA_DIR, 'Scores.csv'),
    )

    # Create visualizations
    print("Generating visualizations...")
    plot_overall_progress(habit_data, OUTPUT_DIR)
    plot_habit_strengths(habit_data, OUTPUT_DIR)

    # Generate monthly report
    current_year = datetime.now().year
    current_month = datetime.now().month
    print(f"Generating monthly report for {current_month}/{current_year}...")

    monthly_comparison = generate_monthly_report(
        habit_data, current_year, current_month
    )
    save_monthly_report(monthly_comparison, current_year, current_month, OUTPUT_DIR)
    visualize_monthly_report(
        habit_data, monthly_comparison, current_year, current_month, OUTPUT_DIR
    )

    # Generate habit trends
    print("Generating habit trends...")
    for habit in habit_data['Habit'].unique():
        plot_habit_trends(habit_data, habit, OUTPUT_DIR)

    # Generate summary report
    print("Generating summary report...")
    generate_summary(habit_data, OUTPUT_DIR)

    # Completion message
    print("\nAnalysis complete! All outputs saved to 'output' directory:")
    print(f"- Overall progress heatmap: {OUTPUT_DIR}/habit_completion_history.png")
    print(f"- Habit strength trends: {OUTPUT_DIR}/habit_score_trends.png")
    print(
        f"- Monthly visual report: {OUTPUT_DIR}/monthly_report_{current_year}_{current_month}.png"
    )
    print(
        f"- Monthly CSV report: {OUTPUT_DIR}/monthly_habit_report_{current_year}_{current_month}.csv"
    )
    print(f"- Individual habit trends: {OUTPUT_DIR}/habit_trend_*.png")
    print(f"- Habit summary: {OUTPUT_DIR}/habit_summary.csv")


if __name__ == "__main__":
    main()
