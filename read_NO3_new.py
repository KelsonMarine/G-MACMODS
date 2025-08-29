''' I didn't end up using this file anywhere.
Used data from https://www.ncei.noaa.gov/access/world-ocean-database-select/bin/dbsearch.pl with
Longitude from -150.3296 to -129.6753; Latitude from 60.6226 to 46.8237
and datasets: OSD,CTD,XBT,MBT,PFL,DRB,MRB,APB,UOR,SUR,GLD. I averaged the top 20 m'
I used https://geodesy.noaa.gov/library/pdfs/Special_Publication_No_281.pdf for water density in Yakutat (1.020 approx.)
and I think it is in g/L'''


DEPTH = 20
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

def main ():
    file = open("../nitrogen/NO3_new.csv")
    lines = file.readlines()
    dates = get_times(lines) #returns a list of time entries
    info_by_date = {}
    i = 0
    dates_in_datetime_format = []
    for date in dates: #gets list for one date
        i += 1
        year = date[0]
        month = date[1]
        day = date[2]
        hour = date[3]
        minute = date[4]
        datetime_version = datetime(year, month, day, hour, minute) #turns dates into datetime format
        dates_in_datetime_format.append(datetime_version)
    avg_NO3_top_20m = parse_ignoring_metadata(lines) #returns a list of the average depth for depths <=20 m per time entry (the depth at which kelp grows, according to GMACMODS)
    for i in range(len(avg_NO3_top_20m)):
        current_time = dates_in_datetime_format[i] # item i of a list containing datetime version of dates
        current_NO3 = avg_NO3_top_20m[i]
        info_by_date[current_time] = current_NO3 #gives a dict where keys are time and values are current NO3 (but some vals are N/A)
    top_20m_dict = {}
    for key in info_by_date:
        if info_by_date[key] != "N/A":
            top_20m_dict[key] = info_by_date[key] # makes a dict that doesn't have any values that are N/A
    timeseries = pd.Series(top_20m_dict)
    monthly_avg = timeseries.resample("MS").mean()
    print(monthly_avg)
    plt.scatter(monthly_avg.index, monthly_avg)
    plt.show()
    monthly_avg_df = monthly_avg.to_frame(name="NO3 concentration")
    monthly_avg_df.to_parquet("input data/NO3.parquet")


def parse_ignoring_metadata(lines):
    '''Takes in lines and only processes the data, ignoring metadata, then averages and returns a list of data for the uppermost 20m
    ocean water and appends that value or N/A if data is unavailable.'''
    processing = False
    averages = []
    NO3_top_20_m = []
    for line in lines:
        if "Prof-Flag" in line:
            processing = True
            continue
        if "END OF VARIABLES" in line:
            processing = False
            if NO3_top_20_m:
                sum_NO3 = sum(NO3_top_20_m)
                avg_NO3 = sum_NO3 / len(NO3_top_20_m) #averages NO3 concentrations in top 20 m water
                averages.append(avg_NO3)
                NO3_top_20_m = []
            else:
                averages.append("N/A")
            continue
        if processing:
            depth = depth_data(line)
            NO3_conc = NO3_data(line)
            if depth <= 20: #this is where the kelp grows
                NO3_top_20_m.append(NO3_conc)
    return averages



def NO3_data(line):
    '''Corrects units of NO3 concentration to mol/L.'''
    line = line.strip()
    line_data = line.split(",")
    NO3_conc = float(line_data[4])
    NO3_conversion = NO3_conc * (1 / 1000) # now in units micromol/g
    NO3_conversion = NO3_conversion * (1/1000000) #now in units mol/g
    NO3_conversion = NO3_conversion * 1.020 #1.020 is what I found for water density in Alaska, now in units of mol/L
    return NO3_conversion

def depth_data(line):
    '''Takes in a line of data and returns only the depth data as a float.'''
    line = line.strip()
    line_data = line.split(",")
    depth = float(line_data[1])
    return depth


def get_times(lines):
    '''Converts dates from decimal format to standard format. If they are at 24 hours, rounds up to the next day.'''
    dates = []
    date = []
    for line in lines:
        if len(date) == 5:
            dates.append(date)
            date = []
        if "Year" in line:
            year_data = line.split(",,")
            year = year_data[1]
            year = int(year.strip())
            date.append(year)
        if "Month" in line:
            month_data = line.split(",,")
            month = month_data[1]
            month = int(month.strip())
            date.append(month)
        if "Day" in line:
            day_data = line.split(",,")
            day = day_data[1]
            day = int(day.strip())
            date.append(day)
        if "Time" in line:
            time_data = line.split(",,")#gives the time and decimal hrs (UT) part
            times = time_data[1].split(",") #gives a list where 0th thing is time and 1st thing is 'decimal hrs (UT'
            time = times[0] #just the decimal time info
            hour_min_lst = time.split(".")
            hours = hour_min_lst[0].strip()
            hour = int(hours) #gives the hour (number before decimal)
            if hour > 23: #since the datetime won't accept a 24 hour value, adjust day/month/year as necessary
                if date[1] == 2 and date[2] < 28: #for february, ignoring leap year (it will just go into march either way), not last day of month
                    date[2] += 1 #increase day by one
                    hour = 0 #make it midnight
                    date.append(hour)
                elif date[1] == 4 or date[1] == 6 or date[1] == 9 or date[1] == 11 and date [2] < 30: #for months with 30 days, not last day of month
                    date[2] += 1
                    hour = 0
                    date.append(hour)
                elif date[1] == 1 or date[1] == 3 or date[1] == 5 or date[1] == 7 or date[1] == 8 or date[1] == 10 or date[1] == 12 and date [2] < 31: #31 day long months, not last day of month
                    date[2] += 1
                    hour = 0
                    date.append(hour)
                elif date[1] == 12 and date[2] == 31: #last day of the year case
                    date[0] += 1 #increase year by 1
                    date[1] = 1 #make it january
                    date[2] = 1
                    hour = 0
                    date.append(hour)
                else: #if it's the last date of the month
                    date[1] +=1 #increase the month by 1
                    date[2] = 1 #make it the 1st
                    hour = 0 #midnight
                    date.append(hour)
            else:
                date.append(hour)
            minute_decimal = hour_min_lst[1] #gets minutes in form of decimal of an hour ie .2 hours or .533 hours
            if minute_decimal == 60:
                date[3] += 1
            else:
                divisor = int(10 ** len(minute_decimal)) # gets divisor that works with any decimal length minutes decimal
                minute = int((((int(minute_decimal)) * 60) / divisor)) # converts into the standard value of minutes
                date.append(minute)
    return dates




if __name__ == "__main__":
    main()