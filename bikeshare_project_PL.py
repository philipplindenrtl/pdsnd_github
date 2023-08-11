import time
import pandas as pd
import numpy as np

CITY_CSV = {'chicago': 'chicago.csv',
             'new york City': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
def check_data_entry(prompt, valid_entries):
    try:
        while True:
            user_input = input(prompt).lower()
            if user_input in valid_entries:
                print("Great! You've chosen: {}\n".format(user_input))
                return user_input
            else:
                print("It looks like your entry is incorrect.")
                print("Let's try again!")
    except Exception as e:
        print("There seems to be an issue with your input:", e)

def get_filters():
    print("Hello! Let's explore some US bikeshare data!")

    valid_cities = CITY_CSV.keys()
    prompt_cities = "Choose one of the 3 cities (chicago, new york city, washington): "
    city = check_data_entry(prompt_cities, valid_cities)

    valid_months = ['all', 'january', 'february', 'march', 'april']
    prompt_month = "Choose a month (all, january, february, march, april): "
    month = check_data_entry(prompt_month, valid_months)

    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    prompt_day = "Choose a day (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday): "
    day = check_data_entry(prompt_day, valid_days)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    filename = CITY_CSV[city]
    df = pd.read_csv(filename)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        month_num = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['Month'] == month_num]

    if day != 'all':
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df - Pandas DataFrame containing city data
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['Month'].mode()[0]
    print('Most Common Month:', common_month)

    common_day = df['Day of Week'].mode()[0]
    print('Most Common Day of Week:', common_day)

    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        df - Pandas DataFrame containing city data
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station:', common_start_station)

    common_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station:', common_end_station)

    df['Start-End Combination'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip = df['Start-End Combination'].mode()[0]
    print('Most Frequent Trip:', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        df - Pandas DataFrame containing city data
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)

    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        df - Pandas DataFrame containing city data
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print('Counts of User Types:\n', user_types)

    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print('Counts of Gender:\n', gender_counts)
    else:
        print('Gender information not available for this city.')

    if 'Birth Year' in df:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        print('Earliest Birth Year:', earliest_birth_year)
        print('Most Recent Birth Year:', most_recent_birth_year)
        print('Most Common Birth Year:', common_birth_year)
    else:
        print('Birth year information not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def display_raw_data(df, start_row):
    """
    Displays 5 lines of raw data from a DataFrame, starting from a given row index.

    Args:
        df - Pandas DataFrame containing city data
        start_row - Starting row index for displaying data
    """
    print('\nDisplaying raw data...\n')
    print(df.iloc[start_row:start_row + 5])
    print('-' * 40)

# ... (previous code) ...

def main():
    """
    Main function to run the bikeshare analysis program.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        start_row = 0  # Starting row for raw data display

        while True:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            display_raw = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
            if display_raw.lower() == 'yes':
                display_raw_data(df, start_row)
                start_row += 5

                if start_row >= len(df):
                    print("No more raw data to display.")
                    break
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
