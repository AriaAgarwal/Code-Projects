
'''
File: city_api.py
Description: The primary API for intersecting with the city dataset

'''

import pandas as pd
import numpy as np


class CITY_API:
    # creates object of city_api
    city = None

    # Abigail and Aria
    def load_city(self, *filename):
        """ Loads and cleans initial data to create city dataframe
           Args:
               filename: List of filenames that can be any length
           Returns:
               new_city (dataframe): A clean dataframe with information about all cities given
        """
        # Initializes empty list
        city_list = []
        # iterates through files in filename
        for file in filename[0]:
            # Reads the csv to load data and appends dataframe to list
            self.city = pd.read_csv(file)
            city_list.append(self.city)
        # Concatenates dataframes in list and drops NaN values
        city_full = pd.concat(city_list)
        city = city_full.dropna(how='any')
        # Drops columns that are not needed for analysis
        city = city_full.drop(
        columns=['preciptype', 'sunrise', 'sunset', 'description', 'icon', 'severerisk', 'moonphase', 'stations'])
        # Uses pd.get_dummies to turn categorical conditions into numerical values to indicate if
        # the given condition is present
        # citation: https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html
        new_city = pd.get_dummies(city, columns=['conditions'], dtype='float')
        # Uses pd.to_datetime to convert dates from strings to datetime objects
        # citation: https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
        new_city["datetime"] = pd.to_datetime(new_city["datetime"])

        name_list = [name.split(",")[0].capitalize() for name in new_city["name"].values]
        new_city["name"] = name_list
        self.city = new_city

        return new_city

    # Sheryl
    def get_city_features(self):
        """ Gets city weather features from dataframe
            Args:
                none
            Returns:
                feature (list): List of city weather features used for cards in panel
                                (ex: tempmin, humidity, dew)
        """
        feature = list(self.city.columns)
        return feature

    # Aria
    def get_user_filtered_features(self, feature, date_range, city_checkbox):
        """ Creates filtered dataframe based on input from widget
            Args:
                feature (string): Weather attribute such as temp, humidity, snow
                date_range (tuple): The start and end date range for filtering
                city_checkbox (list): List of cities to render graph for
            Returns:
                date_feature_df (dataframe): Filtered dataframe with the date, feature
                and cities for given parameters
        """
        # gets the start and end date, then converts dates to datetime64 type
        start_date = date_range[0]
        end_date = date_range[1]
        # citation: https: // stackoverflow.com / questions / 23755146 / why - does - pandas -return -timestamps - instead - of - datetime - objects - when - calling - pd - to
        # citation: https://stackoverflow.com/questions/13703720/converting-between-datetime-timestamp-and-datetime64
        # converts to datetime64 objects to match with the datatype stored in dataframe
        start_datetime64_date = np.datetime64(start_date)
        end_datetime64_date = np.datetime64(end_date)

        # filters dataframe for the start and end date
        date_df = self.city[(self.city['datetime'] >= start_datetime64_date) &
                                       (self.city['datetime'] <= end_datetime64_date)]
        # if a city is selected
        if city_checkbox:
            city_list = []
            # iterates through selected cities
            for city in city_checkbox:
                # filters the date dataframe for the given city and appends to list
                city_list.append((date_df[date_df["name"] == city]))
            # concatenates all dataframes in list to get a dataframe with the correct date range and cities
            city_df = pd.concat(city_list)

            # filters the new dataframe for the given feature
            feature_df = (city_df[feature])
            # creates dictionary by extracting the values from the features and city dataframes
            date_feature_dict = {"name" : city_df["name"].values, feature : feature_df.values, "datetime": city_df["datetime"].values}
            # converts the dictionary to dataframe
            date_feature_df = pd.DataFrame(date_feature_dict)
        # if no city is selected, just uses the feature and date
        else:
            feature_df = (date_df[feature])
            date_feature_df = pd.concat([date_df["datetime"], feature_df], axis=1)

        return date_feature_df

def main():
    # makes city_api object
    city_api = CITY_API()

if __name__ == '__main__':
        main()
