import pandas as pd
import glob
import os
from functools import reduce

# Find all names of our data files in csv format (all csv data has the format of 2 columns, 1st column being DATE, 
# Second column being the feature we believe that is important for our model). In order to merge all these seperate
# featrue values into a single csv (pandas DataFrame) file for futher data cleaning and processing before the modeling,
# phase, we loop through all the file names (saved into a list) and reading them into the pandas DataFrame one at a 
# time while joining them based on the "DATE" column.

# The following is a new way of joining our data into one single dataframe object.
# Find all names of our data files in csv format (all csv data has the format of 2 columns, 1st column being DATE, 
# Second column being the feature we believe that is important for our model). In order to merge all these seperate
# featrue values into a single csv (pandas DataFrame) file for futher data cleaning and processing before the modeling,
# phase, we loop through all the file names (saved into a list) and reading them into the pandas DataFrame one at a 
# time while joining them based on the "DATE" column.

# Initialize an empty DataFrame object to build up into a complete dataframe with all needed features through merging other feature dataframes
df = pd.DataFrame()
# locate the directory path where the data are located on the local machine
wd = os.path.abspath('FeatureData')
# find all the data in csv format under the located directory and save them as a list variable
all_files = glob.glob(wd + '/*.csv')
# Open all the csv feature data as a Pandas DataFrame and saving it inside a list variable
df_list = [pd.read_csv(file) for file in all_files]
# Expand the initialized DataFrame by assigning it the second column of all the feature data file as a new column
# omitting the DATE column to avoid problems caused by different DATE format
for fileIndex in range(len(df_list)):
    df[df_list[fileIndex].columns[1]] = df_list[fileIndex][df_list[fileIndex].columns[1]]
# Add the DATE column into the expanded dataframe with the correct format (the same as our training and testing dataset)
##### Continued on the next few cells #####




# The format of DATES in the training and testing data sets provided by synchrony FINANCIAL are in the for of:
#                                                  '01/month/year'
# As all other feature data are found with a corresponding DATE with Month being from January (01) ~ December (12)
# and Year from 1992 (92) ~ 2017 (17) and with the first day of the month (01).
# Thus, the next step is to create a pandas Series object representing the DATE in the corresponding string format

# create the month list with strings representing 1 ~ 12 with a '0' prefix
month = ['0%d' % s for s in range(1,13) ]
# create a new list with the substring constructed by the last two characters in the string to fit the month string 
# representation in the testin and training data sets and we are done for the month
months = [m[-2:] for m in month]

# As above with the month, we do the similar process with the year.
# creat a list of string representation of the year with range from 1992 ~ 2017
year = [str(y) for y in range(1992, 2018)]
# create the years list with the correct format of the year's strings by saving all the year element's substring 
# constructed by the last two characters of the string
years = [y[-2:] for y in year]


# Create the DATE list with the same string formats as the training and testing data set
# by looping through the months and years list 
DATE = ['01/%s/%s' % (month, year) for year in years for month in months]
# Turn the list into a Pandas Series Object so we can join it with the main dataframe
DATE = pd.Series(DATE)
# Join the DATE Series with the main dataframe, so the dataframe would have the "DATE" column
df["DATE"] = DATE


# We have a few features which are recorded in a seasonal style, thus we will expand them so that the data for each
# sesaon would be the same for each months in that season.

# In order to work with the Seasonal Data, need to change it into monthly presentation (Each tuple data times three)
# We solve it by replicating each row of data 3 times and saving these replicated data into a new list
# then transform the list into a pandas Series. This would expand the seasonal data into monthly data.
# then we simply join this series into the main dataframe as a new column

# change into the directory where the seasonal Data featrues csv data files are located
wd = os.path.abspath("Seasonal Data to be changed")
# save all the csv files in the files_list
files_list = glob.glob( wd + '/*.csv')
# read all files into an dataframe and save dataframes to the df_list
df_list = [pd.read_csv(file) for file in files_list]
# create the data_list where we will put the monthly data expanded by the seasonal data in
data_list = []
# loop through each of the pandas dataframe to access the feature data Series (all based on the column with index 1)
for i in range(len(df_list)):
    seasonal_data_series = df_list[i][df_list[i].columns[1]]
    # for the data values in these data seriesexpand each of them (appending) 3 times into the data_list
    for data in seasonal_data_series:
        for expand in range(3):
            data_list.append(data)
    # create a pandas Series from the data_list
    new_data_series = pd.Series(data_list)
    # Add the new pandas series into the main dataframe as a new column
    df[df_list[i].columns[1]] = new_data_series


# save the dataframe from memory to local disk as "AllFeaturesData.csv"
df.to_csv("AllFeaturesData.csv", index = False)



# Adding in the target variable to the main data file.
# To do so we append the 2 feature files of training and testing dataset, appending testing data set after the training
# data set so that the DATE order aligns with the main merged feature data file.

# read in the csv file we which we used OpenRefine to change all string representation of numbers to numeric data
df = pd.read_csv("AllFeaturesData-csv.csv")

# change into the directory where the Testing and Training data are located
wd = os.path.abspath("TrainTestingData")
# save all the excel (.xlsm) files in the files_list
files_list = glob.glob( wd + '/*.xlsm')
# Individually pick out the training and testing dataset
files_list[1] # Training dataset with DATES from (1992/01/01 ~ 2015/12/01)
files_list[0] # Testing Dataset with DATES from (2016/01/01 ~ 2017/12/01)
# read them into dataframes
df_train = pd.read_excel(files_list[1])
df_test = pd.read_excel(files_list[0])
# Instantiate an empty dataframe used to append both training and testing data set to it to extract the target variable's
# value as pandas series object for merging into the main dataframe later
df_main = pd.DataFrame()
df_main = df_main.append(df_train)
df_main = df_main.append(df_test)
# reindex to to get rid of duplicated index so we can merge the needed feature column to the main dataframe
df_main = df_main.reset_index()
# Merge it into the main dataframe, and change its type to integer
df[df_main.columns[2]] = df_main[df_main.columns[2]]
map(int,df[df_main.columns[2]])


# Save dataframe to "AllFeaturesData-csv.csv", ommitting its index
df.to_csv("AllFeaturesData-csv.csv", index = False)

