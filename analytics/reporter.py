import pandas as pd
import os


def save_monthly_report(comparison, year, month, output_dir='output'):
    """Save monthly report as CSV"""
    # Convert to percentage format
    csv_report = comparison.copy()
    csv_report['Current Month'] = (csv_report['Current Month'] * 100).round(1)
    csv_report['Previous Month'] = (csv_report['Previous Month'] * 100).round(1)
    csv_report['Change'] = (csv_report['Change'] * 100).round(1)

    # Rename columns
    csv_report.rename(
        columns={
            'Current Month': 'Current Month (%)',
            'Previous Month': 'Previous Month (%)',
            'Change': 'Change (%)',
        },
        inplace=True,
    )

    # Save to output directory
    os.makedirs(output_dir, exist_ok=True)
    csv_report.to_csv(
        os.path.join(output_dir, f'monthly_habit_report_{year}_{month}.csv')
    )

    return csv_report


def generate_summary(df, output_dir='output'):
    """Generate summary statistics and save to file"""
    # Compute overall completion rates
    completion_rates = (
        df.groupby('Habit')['Completed'].mean().sort_values(ascending=False)
    )

    # Compute current streak
    def compute_streak(group):
        group = group.sort_values('Date', ascending=False)
        streak = 0
        for completed in group['Completed']:
            if completed:
                streak += 1
            else:
                break
        return streak

    streaks = df.groupby('Habit').apply(compute_streak).sort_values(ascending=False)

    # Create summary dataframe
    summary = pd.DataFrame(
        {'Completion Rate': completion_rates, 'Current Streak': streaks}
    )

    # Format as percentages
    summary['Completion Rate'] = summary['Completion Rate'].apply(lambda x: f"{x:.1%}")

    # Save to output directory
    os.makedirs(output_dir, exist_ok=True)
    summary.to_csv(os.path.join(output_dir, 'habit_summary.csv'))

    return summary
