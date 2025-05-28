import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import calendar
from matplotlib.colors import LinearSegmentedColormap


def plot_overall_progress(df, output_dir='output'):
    """Create habit completion heatmap"""
    # Prepare data
    habit_pivot = df.pivot_table(
        index='Habit', columns='Date', values='Score', fill_value=np.nan
    )

    # Create colormap
    colors = ["#e0e0e0", "#FFCC80", "#FF9800", "#4CAF50"]
    cmap = LinearSegmentedColormap.from_list("habit_cmap", colors)

    # Plot heatmap
    plt.figure(figsize=(16, 10))
    plt.imshow(
        habit_pivot, aspect='auto', cmap=cmap, vmin=0, vmax=1, interpolation='none'
    )

    # Formatting
    plt.title('Habit Completion History', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Habits', fontsize=12)

    # Set x-axis ticks
    dates = habit_pivot.columns
    quarter_indices = [
        i for i, d in enumerate(dates) if d.month % 3 == 1 and d.day == 1
    ]
    plt.xticks(
        quarter_indices,
        [dates[i].strftime('%b %Y') for i in quarter_indices],
        rotation=45,
    )

    # Set y-axis ticks
    plt.yticks(range(len(habit_pivot.index)), habit_pivot.index)

    # Add colorbar
    cbar = plt.colorbar()
    cbar.set_label('Habit Score', rotation=270, labelpad=20)

    plt.tight_layout()

    # Save to output directory
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'habit_completion_history.png'), dpi=100)
    plt.close()


def plot_habit_strengths(df, output_dir='output'):
    """Plot habit strength trends"""
    plt.figure(figsize=(14, 8))

    # Get habit colors
    habit_colors = df.drop_duplicates('Habit').set_index('Habit')['Color']

    for habit in df['Habit'].unique():
        habit_data = df[df['Habit'] == habit].sort_values('Date')
        plt.plot(
            habit_data['Date'],
            habit_data['Score'],
            label=habit,
            color=habit_colors.loc[habit],
            linewidth=2.5,
        )

    plt.title("Habit Strength Over Time", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Habit Score (0-1)", fontsize=12)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True, alpha=0.3)

    # Format dates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.xticks(rotation=45)

    plt.tight_layout()

    # Save to output directory
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, "habit_score_trends.png"), dpi=100)
    plt.close()


def visualize_monthly_report(df, comparison, year, month, output_dir='output'):
    """Create visual monthly report"""
    # Calculate previous month
    if month == 1:
        prev_year, prev_month = year - 1, 12
    else:
        prev_year, prev_month = year, month - 1

    # Create figure
    fig, axes = plt.subplots(2, 1, figsize=(14, 12))
    fig.suptitle(
        f'Habit Report: {calendar.month_name[month]} {year} vs {calendar.month_name[prev_month]} {prev_year}',
        fontsize=18,
        y=0.98,
    )

    # Completion rate comparison
    habit_colors = df.drop_duplicates('Habit').set_index('Habit')['Color']
    colors = [habit_colors.loc[h] for h in comparison.index]

    comparison[['Current Month', 'Previous Month']].plot.bar(
        ax=axes[0], color=['#4CAF50', '#2196F3'], width=0.8
    )
    axes[0].set_title('Completion Rate Comparison', fontsize=14)
    axes[0].set_ylabel('Completion Rate', fontsize=12)
    axes[0].set_ylim(0, 1.1)
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(axis='y', alpha=0.2)

    # Add value labels
    for i, (_, row) in enumerate(comparison.iterrows()):
        axes[0].text(
            i,
            row['Current Month'] + 0.03,
            f"{row['Current Month']:.0%}",
            ha='center',
            fontsize=9,
        )
        axes[0].text(
            i,
            row['Previous Month'] - 0.05,
            f"{row['Previous Month']:.0%}",
            ha='center',
            fontsize=9,
            color='#2196F3',
        )

    # Improvement highlights
    changes = comparison['Change'].sort_values(ascending=False)
    changes.plot.bar(ax=axes[1], color=np.where(changes >= 0, '#4CAF50', '#F44336'))
    axes[1].set_title('Monthly Change in Completion Rate', fontsize=14)
    axes[1].set_ylabel('Change (percentage points)', fontsize=12)
    axes[1].axhline(0, color='black', linewidth=0.8)
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(axis='y', alpha=0.2)

    # Add value labels
    for i, val in enumerate(changes):
        axes[1].text(
            i,
            val + (0.02 if val >= 0 else -0.05),
            f"{val:.0%}",
            ha='center',
            fontsize=9,
            color='black' if val == 0 else None,
        )

    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Save to output directory
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, f'monthly_report_{year}_{month}.png'), dpi=100)
    plt.close()


def plot_habit_trends(df, habit_name, output_dir='output'):
    """Plot detailed trend for a specific habit"""
    habit_data = df[df['Habit'] == habit_name].sort_values('Date')
    habit_color = df[df['Habit'] == habit_name]['Color'].iloc[0]

    fig, ax1 = plt.subplots(figsize=(14, 8))

    # Plot raw values
    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylabel('Raw Value', color=habit_color, fontsize=12)
    ax1.plot(
        habit_data['Date'], habit_data['Value'], 'o-', color=habit_color, markersize=6
    )
    ax1.tick_params(axis='y', labelcolor=habit_color)

    # Plot scores
    ax2 = ax1.twinx()
    ax2.set_ylabel('Score (0-1)', color='#303030', fontsize=12)
    ax2.plot(
        habit_data['Date'], habit_data['Score'], 's--', color='#303030', markersize=4
    )
    ax2.tick_params(axis='y', labelcolor='#303030')
    ax2.set_ylim(0, 1.1)

    plt.title(f'Trend Analysis: {habit_name}', fontsize=16)
    plt.grid(True, alpha=0.3)

    # Format dates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.xticks(rotation=45)

    plt.tight_layout()

    # Save to output directory
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, f'habit_trend_{habit_name}.png'), dpi=100)
    plt.close()
