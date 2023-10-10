import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs    
    while(True):
        city = input("Please choose the name of the city to analyse (chicago, new york city or washington):").lower()
        if(city in ['chicago', 'new york city', 'washington']):
            break
        else:
            print('Invalid input {}. Please choose the right city.'.format(city))         
    

    # get user input for month (all, january, february, ... , june)
    while(True):
        month = input('Please choose the name of the month (january, february, ... , june) to filter or "all" to not apply a month filter:').lower()
        if(month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']):
            break
        else:
            print('Invalid input {}. Please choose the right month or all.'.format(month))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while(True):
        day = input('Please choose the name of the day (monday, tuesday, ... sunday) to filter or "all" to not apply a day filter:').lower()
        if(day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']):
            break
        else:
            print('Invalid input {}. Please choose the right day or all.'.format(day))


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
    #Read the csv file
    df = pd.read_csv(CITY_DATA[city])

    # Convert to date time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Add new columns for filtering by month, day or hour
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['start_hour'] = df ['Start Time'].dt.hour

    #filter by month and/or day of week
    if month.lower() != 'all':
        df = df[df['month'].str.lower() == month]

    if day.lower() != 'all':
       df = df[df['day_of_week'].str.lower() == day]     
    print (df)
    return df


def time_stats(df:pd.DataFrame):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print("Most common month is {}".format(most_common_month))

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print("Most common day of week is {}".format(most_common_day_of_week))

    # display the most common start hour
    most_common_start_hour = df['start_hour'].mode()[0]
    print("Most common start hour is {}".format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df:pd.DataFrame):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("Most common start station is {}".format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("Most common end station is {}".format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    
    # Group and sort the dataframe to get the most frequent combination  
    most_frequent_combination = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print("Most frequent combination of Start and End Station is: \n {}".format(most_frequent_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df:pd.DataFrame):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total Travel Time in hours is: {}\n".format(total_travel_time / 3600.0))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean Travel Time in hours is: {}\n".format(mean_travel_time / 3600.0))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df:pd.DataFrame, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_of_user_types = df['User Type'].value_counts() 
    print("Counts of user types:\n {}\n".format(counts_of_user_types))

    # Washington has no gender and birth information
    if city.lower() != 'washington':
       
        # Display counts of gender   
        counts_of_gender = df['Gender'].value_counts() 
        print("Counts of gender:\n {}\n".format(counts_of_gender))

        #Some rows have null values in the birth column so I clean up the df
        df_without_na = df.dropna(subset=['Birth Year'])        

        # Display earliest, most recent, and most common year of birth
        earliest_year = df_without_na['Birth Year'].min()
        print("Earliest Birth Year is: {}".format(earliest_year))

        recent_year = df_without_na['Birth Year'].max()
        print("Most recent Birth Year is: {}".format(recent_year))

        common_year = df_without_na['Birth Year'].mode()[0]
        print("Most common Birth Year is: {}".format(common_year))


    else:
        print("There are no gender or birth data available for Washington")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df:pd.DataFrame):
    """Displays raw data if the user requests.
    
     Args:
        (pandas.DataFrame) df - Pandas DataFrame containing city data    
    """

    view_data = input("\nWould you like to view 5 rows of individual trip data? Enter yes or no: ").lower()
    row_count_to_display = 10
    start_loc = 0
    end_loc = row_count_to_display

    if (view_data == 'yes'):

        while(True):
            print(df.iloc[start_loc:end_loc])
            start_loc += row_count_to_display
            end_loc += row_count_to_display

            should_continue = input("\nDo you with to continue with 5 more rows? Enter yes or no: ").lower()

            if (should_continue == 'no'):
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
