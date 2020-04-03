import time
import pandas as pd
import numpy as np


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('-'*40)
    
    # initializing variables and creating lists for loops
    
    city, month, day = '', '', ''
    city_list = ['chicago','new york city','washington','los_angeles']
    months_list = ['january', 'february','march','april','may','june','all']
    days_list = ['mo','tu','we','th','fr','sa','su','all']
    
    # getting city from the user (used later for filtring the data) 
    
    while True:
        city = input("Select the city please: Chicago, New York City, Los Angeles or Washington? ")
        if city.lower().strip() in city_list:
            break
        else:
            print("Invalid value, try again!")
            
    # asking user for filters: both and none skips to next function
    while True:
        filters = input("Would you like to apply filters? Please choose: both, day, month or none?")
        filters = filters.lower().strip()
        if filters in ['both','none','day','month']:
            break
    if filters == 'both' or filters == 'month':
        # getting month form the user  
        while True:
            month = input('Select the month: January, February, March, April, May, June or type \'all\' to access all months data ')
            if month.lower().strip() in months_list:
                print(month)
                break
            else:
                print("Invalid value, try again!")
    if filters == "both" or filters == "day":   
    # getting day form the user 
        while True:
            day = input('Select the day of the week: Mo, Tu, We, Th, Fr, Sa, Su or type all to access \'all\' days of the week data ')
            if day.lower().strip() in days_list:
                break
            else:
                print("Invalid value, try again!")
    # handling 'none situations and copleting day and month filters
    if filters == "none":
        day = "all"
        month = "all"
    if filters == "day":
        month = "all"
    if filters == 'month':
        day = 'all'
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
    df = pd.read_csv(city.strip().replace(" ", "_").lower()+'.csv')
    
    # conveting Start Time column to datetime for further data extracting
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # creating new columns: month and day of the week from 'Start Time'
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    # combing Start Station and End Station to get Route column
    df['Route'] = df['Start Station'].astype(str) + " --- " + df['End Station'].astype(str)
    # data filtering by month selected by user 
    if month != 'all':
        months = ['january','february','march','april','may','june']
        month = months.index(month) + 1
        # creating new dataframe filtering by months
        df = df[df['month']==month]
    # data filtering by day selected by user 
    if day != 'all':
        # creating list of days and new dataframe filtered by day
        days = ['mo','tu','we','th','fr','sa','su']
        df = df[df['day_of_week']==days.index(day)]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # creating months dictionary and calculating the mode
    month_dict = {'1':'January','2':'February','3':'March','4':'April','5':'May','6':'June'}
    month_mode = str(df.month.mode()[0])
    for key,value in month_dict.items():
        if key == month_mode:
            month_name = value
            break
    print("Most common month is: " + month_name)

    # creating days of week dictionary and calculeting mode
    days_dict = {'0':'Monday','1':'Tuesday','2':'Wednesday','3':'Thursday','4':'Friday','5':'Saturday','6':'Sunday'}
    day_week = str(df.day_of_week.mode()[0])
    for key, value in days_dict.items():
        if key == day_week:
            day_name = value
            break
    print("The most common day of week is: " + day_name)

    # displaying the most common start hour
    print("The most common start hour is: " + str(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # displaying the mode of Start and End Station columns
    start_station = str(df['Start Station'].mode()[0])
    print("The most common start station is: " + start_station)
    
    end_station = str(df['End Station'].mode()[0])
    print("The most common end station is: " + end_station)

    # display most frequent combination of start station and end station route from Route column
    route = str(df['Route'].mode()[0])
    print("The most popular route is: " + route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # summing trip duration and calculating metrics - days, hours, minutes and seconds
    days_travel, hours_travel, minutes_travel, seconds_travel = 0,0,0,0
    sum_travel  = int(df['Trip Duration'].sum())
    days_travel = sum_travel//(60*60*24)
    hours_travel = (sum_travel%(60*60)%24)
    minutes_travel = (sum_travel%(60*60)//60)
    seconds_travel = (sum_travel%(60*60)%60)
    print("Total time traveled is: {} days, {} hours, {} minutes and {} seconds".format(days_travel, hours_travel, minutes_travel, seconds_travel))
    # displaying mean time from trip duration column in divided into minutes and seconds 
    mean_travel = int(df['Trip Duration'].mean())
    minutes_mean = mean_travel//60
    seconds_mean = mean_travel%60
    print("Avarage travel time is {} minutes and {} seconds".format(minutes_mean, seconds_mean))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # checking user types which is available in all files
    print('-'*40)
    print("Please find users user type statistics below:")
    user_types = df.groupby(['User Type'])['User Type'].count()
    print(user_types) 

    # checking if dataframe has columns needed for comptuation
    
    if 'Gender' not in df:
        print('-'*40)
        print("For {} there are no available data about users age and gender".format(city.title()))
    else:
        # getting data about user age or gender
        print('-'*40)
        user_gender = df.groupby(['Gender'])['Gender'].count()        
        print("Please find users gender statistics below:")
        print(user_gender)
        print('-'*40)
        print('The oldest user was born in: ' + str(int(df['Birth Year'].min())))
        print('The youngest user was born in: ' + str(int(df['Birth Year'].max())))
        print('The avarage year of birth is: ' + str(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
# listing 5 records by user at one time
def listing_records(df): 
    x = 0
    more_x = ""
    while True:
        ans_data = input("Would you like to see {} 5 rows of data? Enter yes or no.\n".format(more_x))
        if ans_data.lower() == 'yes':
            more_x = "next"
            print(df[x:x+5])
            x += 5
        else:
            break           
                
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        listing_records(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
