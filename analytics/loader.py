import pandas as pd


def load_habit_data(checkmarks_path, habits_path, scores_path):
    """Load and merge all habit data files"""
    # Load habits metadata
    habits_meta = pd.read_csv(habits_path)
    habit_names = habits_meta['Name'].tolist()

    # Load checkmarks data
    checkmarks = pd.read_csv(checkmarks_path, parse_dates=['Date'])
    checkmarks = checkmarks.melt(id_vars='Date', var_name='Habit', value_name='Value')
    checkmarks = checkmarks[checkmarks['Habit'].isin(habit_names)]

    # Load scores data
    scores = pd.read_csv(scores_path, parse_dates=['Date'])
    scores = scores.melt(id_vars='Date', var_name='Habit', value_name='Score')
    scores = scores[scores['Habit'].isin(habit_names)]

    # Merge dataframes
    df = pd.merge(checkmarks, scores, on=['Date', 'Habit'], how='left')

    # Add habit metadata
    df = pd.merge(
        df, habits_meta[['Name', 'Color']], left_on='Habit', right_on='Name', how='left'
    )
    df = df.drop(columns=['Name'])

    # Convert and extract date components
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['Weekday'] = df['Date'].dt.weekday

    # Create completion flag based on habit type
    def determine_completion(row):
        if row['Value'] == -1:  # Missing data
            return False
        if row['Habit'] in ['Stay away from sugar', 'Quit coffee']:  # Boolean habits
            return row['Value'] == 2
        return row['Value'] > 0  # Numerical habits

    df['Completed'] = df.apply(determine_completion, axis=1)

    return df
