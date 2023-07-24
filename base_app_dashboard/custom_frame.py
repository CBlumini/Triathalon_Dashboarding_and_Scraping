# https://stackoverflow.com/questions/15535655/optional-arguments-in-initializer-of-python-class

import pandas as pd


class ProcessedData:


    def __init__(self, df=None, url=None, cutoff_year=1):
        self.df = df
        self.url = url
        self.cutoff_year = cutoff_year
        self.cleaned_data = None
        self.gendered_data = None

        if url is not None:
            self.df = pd.read_csv(url, header=0, index_col=None)

    # create class methods
    @classmethod
    def determine_agegroup(cls, row):
        start_ages = [10, 18, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85]
        end_ages = [17, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 84, 100]
        age = int(row['Age'])
        for start, stop in zip(start_ages, end_ages):
            if start <= age <= stop:
                return '%d-%d' % (start, stop)

    @classmethod
    def convertTime(cls, time):
        temp = time.split(':')
        timeMinutes = (int(temp[0]) * 60) + int(temp[1]) + int(temp[2]) / 60
        return timeMinutes



    def get_piechart_data(self, df):
        datapie = df
        datapie['Age Group'] = datapie.apply(ProcessedData.determine_agegroup, axis=1)
        return datapie

    def get_cleaned_data(self, cutoff_year=None):
        if cutoff_year is None:
            self.cleaned_data = self.df[self.df['Age'] > self.cutoff_year]
        else:
            self.cleaned_data = self.df[self.df['Age'] > cutoff_year]
        return self.cleaned_data

    def get_gendered_data(self, gender, cutoff_year=None):
        """Get a dataset filter to just Males or Females
        Must specify a string of either 'Male' or 'Female'"""
        if cutoff_year is None:
            self.gendered_data = self.get_cleaned_data(self.cutoff_year)
            self.gendered_data = self.gendered_data[self.gendered_data['Gender'] == gender]
        else:
            self.gendered_data = self.get_cleaned_data(cutoff_year)
            self.gendered_data = self.gendered_data[self.gendered_data['Gender'] == gender]
        return self.gendered_data

    @staticmethod
    def get_time_data(bare_frame):

        # convert to integers
        bare_frame["Swim Minutes"] = bare_frame["Swim"].apply(ProcessedData.convertTime)
        bare_frame["T1 Minutes"] = bare_frame["T1"].apply(ProcessedData.convertTime)
        bare_frame["Bike Minutes"] = bare_frame["Bike"].apply(ProcessedData.convertTime)
        bare_frame["T2 Minutes"] = bare_frame["T2"].apply(ProcessedData.convertTime)
        bare_frame["Run Minutes"] = bare_frame["Run"].apply(ProcessedData.convertTime)
        # bare_frame["Elapsed Minutes"] = bare_frame["Chip Elapsed"].apply(convert_time)

        # create cumulative times
        bare_frame["Swim+T1"] = round(bare_frame["Swim Minutes"] + bare_frame["T1 Minutes"], 2)
        bare_frame["Plus Bike"] = round(bare_frame["Swim+T1"] + bare_frame["Bike Minutes"], 2)
        bare_frame["Plus T2"] = round(bare_frame["Plus Bike"] + bare_frame["T2 Minutes"], 2)
        bare_frame["Total"] = round(bare_frame["Plus T2"] + bare_frame["Run Minutes"], 2)

        return bare_frame