# remote repository location: https://github.com/Skreech666/pdsnd_github

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to filter the data by.
    
    Inputs:
        First letter of city name
        First two letters of month
        First two letters of day

    Returns:
        (str) city - name of the city to load data from
        (str) month - name of the month to filter by, or "all" for no filter
        (str) day - name of the day of week to filter by, or "all" for no filter
    """
    print('\n\nHello! Let\'s explore some US bikeshare data!\n')
    x,y,z = 0,0,0  
    
    # get user input for city (chicago, new york city, washington).
    while x == 0:        
        cityInput = input('Which city would you like to see data for: Chicago, New York City or Washington?\n(Enter first letter): ')
        cityt = {'c':'chicago', 'n':'new york city', 'w':'washington'}
        try:
            city = cityt[cityInput[0:1].lower()]
        except Exception as e:    
            print('\n\nInvalid Value.\n\nPlease try again\n\n')
        else:
            x = 1   
    
    # get user input for month
    while y == 0:
        monthInput = input('\nWhich month would you like to see Data for: January, February, March, April, May, June or All?\n(Enter first two letters): ')
        montht = {'ja':'january', 'fe':'february', 'ma':'march', 'ap':'april', 'ma':'may', 'ju':'june', 'al':'all'}
        try:
            month = montht[monthInput[0:2].lower()]
        except Exception as e:    
            print('\n\nInvalid Value.\n\nPlease try again\n\n')
        else:
            y = 1 
            
    # get user input for day of week    
    while z == 0:
        dayInput = input('\nWhich day would you like to see Data for: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or All ?\n(Enter first two letters): ')
        dayt = {'su':'sunday', 'mo':'monday', 'tu':'tuesday', 'we':'wednesday', 'th':'thursday', 'fr':'friday', 'sa':'saturday', 'al':'all'}
        try:
            day = dayt[dayInput[0:2].lower()]
        except Exception as e:    
            print('\n\nInvalid Value.\n\nPlease try again\n\n')
        else:
            z = 1      
    print('\n',' - '*30,'\n') 
    
    return city, month, day


def load_data(city, month, day):
    print('Loading City data...\n')
    """
    Loads data for the specified city and filters by month and day where requested.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start_hour'] = df['Start Time'].dt.hour
    #df['end_hour'] = df['End Time'].dt.hour
       

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
        df = df[df['day_of_week'] == day.title()]

    return df




def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel.
		Returns:
				Month with the most trips
				The day of the week most travelled on
				Most common hour travel started on
	"""

    print('\nCalculating The Most Frequent Times of Travel...\n\n')
    start_time = time.time()

    # display the most common month
    monthtr = {1:'january', 2:'february', 3:'march', 4:'april', 5:'may', 6:'june'}
    if month == 'all':
        mt = monthtr[df['month'].mode()[0]]
        print('The month with the highest number of trips is: {}.\n'.format(mt.capitalize()))
    else:
        print('Month filter applied: {}.\n'.format(month.capitalize()))
        
    # display the most common day of week
    if day == 'all':
        print('The day of the week most travelled on is: {}.\n'.format(df['day_of_week'].mode()[0]))
    else:
        print('Day filter applied: {}.\n'.format(day.capitalize()))

    # display the most common start hour
    s = df['start_hour'].mode()[0]
    if s == 0:
        sh = '12 am'
    elif s == 12:
        sh = '12 pm'
    elif s < 12:
        sh = '{} am'.format(s)
    else:
        sh = '{} pm'.format(s-12)
    
    print('The most common hour travel started on is: {}.\n'.format(sh))
    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    input('Press Enter to continue...\n')
    print('\n',' - '*30,'\n')

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used Start Station is: {}.\n'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most commonly used End Station is: {}.\n'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    
    dd = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('The most commonly used Start and End Station combination is: \n\n{}'.format(dd))
    
   
    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    input('Press Enter to continue...\n')
    print('\n',' - '*30,'\n')
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n\n')
    start_time = time.time()

    # display total travel time
    print('Users hired cycles for a total of {} minutes!\n'.format(int((df['Trip Duration'].sum())/60)))

    # display mean travel time
    print('The average trip length was {} minutes.\n'.format(int(df['Trip Duration'].mean()/60)))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    input('Press Enter to continue...\n')
    print('\n',' - '*30,'\n')
    
def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    print('Breakdown of trips by User Type: \n\n{}.\n'.format(df['User Type'].value_counts()))

    # Display counts of gender
    
    if city != 'washington':
        print('Breakdown of trips by Gender: \n\n{}.\n'.format(df['Gender'].value_counts()))
         
        # Display earliest, most recent, and most common year of birth
        df_u =  df['User Type'] == 'Subscriber'
        df_user = df[df_u].copy()
        print('The Earliest year of birth is {}.\n\nThe most recent year of birth is {}.\n\nThe most common year of birth is {}.\n'.format(int(df_user['Birth Year'].min()), int(df_user['Birth Year'].max()), int(df_user['Birth Year'].mode()[0])))
    else:
        print('No Gender or Birth Year data available.\n')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    input('Press Enter to continue...\n')
    print('\n',' - '*30,'\n')

def see_raw(df):
    """Function to return rows of raw data where requested"""
    t = 0
    u = 9
    end = 0
    xx = input('Would you like see ten rows of raw data? Enter yes: ')
    while end == 0:
        if xx[0:1].lower() != 'y':
            end = 1 
        else:   
            print(df.loc[t:u,:])
            t += 5
            u += 5 
            xx = input('Enter yes to see ten more rows of raw data: ')   
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        see_raw(df)
        
        restart = input('\nEnter yes to restart.\n')
        if restart[0:1].lower() != 'y':
            break


if __name__ == "__main__":
	main()