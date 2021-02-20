import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def wrong_input():
    """ outputs info before loop restarts, if user enters incorrect input """
    print("\nThat's not a valid choice.\n")

def get_filters():
    """
    asks which the user which city's data they want to review.
    Then asks which filter they want to apply to the data: month, day, or none.
    """

    while True:
        city = input('Please choose a city: Chicago, New York City, or Washington: ').lower()
        if city in ('chicago', 'new york city', 'washington'):
            print('')
            break
        else:
            wrong_input()

    while True:
        choice = input("Would you like to filter by month, day, or not at all (month/day/none)? ").lower()
        if choice == 'month':
            month = input("Please choose a month (January, February, March, April, May, June, or 'all'): ")
            if month.lower() in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
                day = 'all'
                break
            else:
                wrong_input()
        elif choice == 'day':
            day = input("Please choose a day of the week: (Monday, Tuesday, Wednesday, ..., or 'all'): ").lower()
            if day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
                month = 'all'
                break
            else:
                wrong_input()
        elif choice == 'none':
            month = 'all'
            day = 'all'
            break
        else:
            wrong_input()

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour of the day from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['weekday'] == day.title()]

    print("-"*40)
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    months = { 1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June' }

    # converting integer to name for output of months
    df['month'] = df['Start Time'].dt.month.map(months)

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("Most common month:", df['month'].mode()[0])

    # display the most common day of week
    print("Most common day:", df['weekday'].mode()[0])

    # display the most common start hour
    print("Most common start hour:", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    print("The most common Start Station is:", df['Start Station'].value_counts().idxmax())

    # display most commonly used end station
    print("The most common End Station is:", df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    print("The most common trip is:", df.groupby(['Start Station', 'End Station']).size().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    print("Total travel time:", df['Trip Duration'].sum())

    # display mean travel time
    print("Mean travel time:", df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # display counts of gender
    try:
        print("Gender information:")
        print(df['Gender'].fillna('no info').value_counts().to_string())
        print("")
    except:
        print("There is no gender info")
        print("")

    # removing rows with NaN from DataFrame
    df = df.dropna(axis=0)

    # display earliest, most recent, and most common year of birth
    try:
        print("Age information:")
        print("The most recent Birth Year is:", int(df['Birth Year'].max()))
        print("The most earliest Birth Year is:", int(df['Birth Year'].min()))
        print("The most common Birth Year is:", int(df['Birth Year'].mode()))
    except:
        print("There is no Birth Year info")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)

def raw_data(df):
    """
    Asks if user wants to see the raw data and returns data in sets of 5,
    asking after every 5 results if they want to see more
    """

    raw = input('Do you want to see the raw data (yes/no)? ').lower()
    while True:
        if raw == 'yes':
            i=0
            print(df.loc[i:i+4])
            for num in range(0,len(df.index)):
                more_data = input('Do you want to see more data (yes/no)? ').lower()
                if more_data == 'yes':
                    i+=5
                    print(df.loc[i:i+4])
                elif more_data.lower() == 'no':
                    break
                else:
                    wrong_input()
            break
        elif raw == 'no':
            break
        else:
            wrong_input()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # displays raw data, passing full data set rather than selected filter
        raw_data(pd.read_csv(CITY_DATA[city]))

        # asks if user wants to restart
        restart = input('\nWould you like to restart (yes/no)? ').lower()
        if restart == 'yes':
            pass
        elif restart == 'no':
            print("\nThanks for using. Goodbye!\n")
            break
        else:
            wrong_input()

if __name__ == "__main__":
	main()
