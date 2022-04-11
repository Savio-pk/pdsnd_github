import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['all','january', 'february', 'march', 'april', 'may', 'june']
days = ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def seconds_to_days(seconds):
    """
    Converts seconds into days, hours, minutes, and seconds 
    Args:
        (float) seconds - total number of seconds
    Returns:
        (str) day_hour_min_sec - string contains number of days. hours, minutes, and seconds in the total number of seconds provided
    """
    # get number of days in the total number of seconds (one day is 24h*60m*60s = 86400 secs)
    days = int(seconds/86400) 

    # get the remaining seconds from number of days
    seconds = seconds%86400

    # get number of hours in the remaining number of seconds (one hour is 60m*60s = 3600 secs)
    hours = int(seconds/3600) 

    # get the remaining seconds from number of hours
    seconds = seconds%3600

    #get number of minutes in the remaining number of seconds (one min is 60 secs)
    minutes = int(seconds/60)

    # get the remaining seconds from number of minutes
    seconds = int(seconds%60)

    return "{} Days, {} Hours, {} Minutes, and {} Seconds".format(days, hours, minutes, seconds)


def check_data_entry(prompt, valid_entries):
    """
    Asks user to type some input and verify if the entry typed is valid.
    Since we have 3 inputs to ask the user in get_filters(), it is easier to write a function.
    Args:
        (str) prompt - message to display to the user
        (list) valid_entries - list of string that should be accepted 
    Returns:
        (str) user_input - the user's valid input
    """
    try:
        while True:
            user_input = str(input(prompt)).lower()
            if user_input in valid_entries:
                print("Your entry is: {}\n".format(user_input.title()))
                return user_input
            else:
                print("Sorry, I didn't catch that. Try again.\n")
    except:
        print("Seems like there is an issue with your input. Please try again")


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("\nHello! Let's explore some US bikeshare data!\n")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    prompt = "Would you like to see data for Chicago, New York City, or Washington:\n"
    valid_entries = CITY_DATA
    city = check_data_entry(prompt, valid_entries)

    # get user input for month (all, january, february, ... , june)
    prompt = "Which Month? All, January, February, March, April, May, or June:\n"
    valid_entries = months
    month = check_data_entry(prompt, valid_entries)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    prompt = "Which Day? All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday:\n"
    valid_entries = days
    day = check_data_entry(prompt, valid_entries)

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    #df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) 

        # filter by month to create the new dataframe
        df = df.loc[ df['month'] == month ]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[ df['day_of_week'] == day.title() ]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most common month
    most_common_month = months[ int(df['month'].mode()) ]
    print("Most Common Month: {}\n".format(most_common_month.title()))

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0] 
    print("Most Common Day of Week: {}\n".format(most_common_day.title()))

    # display the most common start hour
    start_hours = df['Start Time'].dt.hour
    most_common_start_hour = start_hours.mode()[0] 
    print("Most Common Start Hour (0-23): {}\n".format(most_common_start_hour))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print("Most Commonly Used Start Station: ({})\n".format(most_common_start))

    # display most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print("Most Commonly Used End Station: ({})\n".format(most_common_end))

    # display most frequent combination of start station and end station trip
    most_freq_start_end = df.groupby(['Start Station','End Station']).size().idxmax()
    print("Most Frequent Combination Of Start Station And End Station Trip: ({}) TO ({})\n".format(most_freq_start_end[0], most_freq_start_end[1]))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()
    if 'Trip Duration' in df:
        # display total travel time
        total_travel_time_seconds = df['Trip Duration'].sum()
        print("Total Travel Time in seconds: {}".format(total_travel_time_seconds))
        total_travel_time = seconds_to_days(total_travel_time_seconds) 
        print("Total Travel Time: {}\n".format(total_travel_time))

        # display mean travel time
        Mean_travel_time_seconds = df['Trip Duration'].mean()
        print("Mean Travel Time in seconds: {}".format(Mean_travel_time_seconds))
        Mean_travel_time = seconds_to_days(Mean_travel_time_seconds)
        print("Mean Travel Time: {}\n".format(Mean_travel_time))

    else:
        print("No Trip Duration Information Available\n")

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df:
        user_types_counts = df['User Type'].value_counts()
        print("Counts Of User types:\n{}\n".format(user_types_counts))
    else:
        print("No User Type Information Available\n")

    # Display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print("Counts Of Gender:\n{}\n".format(gender_counts))
    else:
        print("No Gender Information Available\n")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print("Earliest Year Of Birth: {}\n".format(int(df['Birth Year'].min())))
        print("Most Recent Year Of Birth: {}\n".format(int(df['Birth Year'].max())))
        print("Most Common Year of Birth: {}\n".format(int(df['Birth Year'].mode()[0])))
    else:
        print("No Birth Year Information Available\n")

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Asks if the user would like to see 5 rows of the data."""

    view_data = str(input("\nWould you like to view 5 rows of individual trip data? Enter yes or no: \n")).lower()
    start_loc = 0
    while(view_data == 'yes'):
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_data = str(input("\nWould you like to view 5 more rows? Enter yes or no: \n")).lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = str(input('\nWould you like to restart? Enter yes or no: \n')).lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()