import pandas as pd


def compute_completion_rates(df, period='M'):
    """Compute completion rates for a given time period"""
    df_period = df.copy()
    df_period['Period'] = df_period['Date'].dt.to_period(period)

    completion = df_period[df_period['Completed']].groupby(['Period', 'Habit']).size()
    total = df_period.groupby(['Period', 'Habit']).size()

    rates = (completion / total).fillna(0).reset_index()
    rates.columns = ['Period', 'Habit', 'CompletionRate']
    return rates


def generate_monthly_report(df, year, month):
    """Generate monthly comparison report"""
    # Filter data for target and previous month
    target_month = df[(df['Year'] == year) & (df['Month'] == month)]

    # Calculate previous month
    if month == 1:
        prev_year, prev_month = year - 1, 12
    else:
        prev_year, prev_month = year, month - 1

    prev_month_data = df[(df['Year'] == prev_year) & (df['Month'] == prev_month)]

    # Compute completion rates
    def compute_rates(data):
        completion = data[data['Completed']].groupby('Habit')['Completed'].count()
        total = data.groupby('Habit')['Completed'].count()
        return (completion / total).fillna(0)

    current_rates = compute_rates(target_month)
    prev_rates = compute_rates(prev_month_data)

    comparison = pd.DataFrame(
        {'Current Month': current_rates, 'Previous Month': prev_rates}
    ).fillna(0)

    comparison['Change'] = comparison['Current Month'] - comparison['Previous Month']

    return comparison
