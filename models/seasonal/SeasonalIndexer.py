import numpy as np
from enum import Enum

class SeasonalIndexer(object):
    """
    Seasonal Indexer. Responsible to find the seasonal index of a data point inside its data set
    """
    def __init__(self,num_seasons):
        self.num_seasons = num_seasons

    def get_season_of_data(self,data):
        pass

    def get_season_by_index(self,inde):
        pass

    def get_data_by_season(self, data, indexes):
        pass

    def get_index_by_season(self, indexes):
        pass

    def get_data(self, data):
        pass


class LinearSeasonalIndexer(SeasonalIndexer):
    def __init__(self,seasons):
        super(LinearSeasonalIndexer, self).__init__(len(seasons))
        self.seasons = seasons

    def get_season_of_data(self,data):
        return self.get_season_by_index(np.arange(0, len(data)).tolist())

    def get_season_by_index(self,index):
        ret = []
        if not isinstance(index, (list, np.ndarray)):
            season = (index % self.seasons[0]) + 1
        else:
            for ix in index:
                if self.num_seasons == 1:
                    season = (ix % self.seasons[0])
                else:
                    season = []
                    for seasonality in self.seasons:
                        #print("S ", seasonality)
                        tmp = ix // seasonality
                        #print("T ", tmp)
                        season.append(tmp)
                    #season.append(rest)

        ret.append(season)

        return ret

    def get_index_by_season(self, indexes):
        ix = 0;

        for count,season in enumerate(self.seasons):
            ix += season*(indexes[count])

        #ix += indexes[-1]

        return ix

    def get_data(self, data):
        return data


class DataFrameSeasonalIndexer(SeasonalIndexer):
    def __init__(self,index_fields,index_seasons, data_fields):
        super(DataFrameSeasonalIndexer, self).__init__(len(index_seasons))
        self.fields = index_fields
        self.seasons = index_seasons
        self.data_fields = data_fields

    def get_season_of_data(self,data):
        #data = data.copy()
        ret = []
        for ix in data.index:
            season = []
            for c, f in enumerate(self.fields, start=0):
                if self.seasons[c] is None:
                    season.append(data[f][ix])
                else:
                    a = data[f][ix]
                    season.append(a // self.seasons[c])
            ret.append(season)
        return ret

    def get_season_by_index(self,index):
        raise Exception("Operation not available!")

    def get_data_by_season(self, data, indexes):
        for season in indexes:
            for c, f in enumerate(self.fields, start=0):
                if self.seasons[c] is None:
                    data = data[data[f]== season[c]]
                else:
                    data = data[(data[f] // self.seasons[c]) == season[c]]
        return data[self.data_fields]

    def get_index_by_season(self, indexes):
        raise Exception("Operation not available!")

    def get_data(self, data):
        return data[self.data_fields].tolist()

    def set_data(self, data, value):
        data.loc[:,self.data_fields] = value
        return data

class DateTime(Enum):
    year = 1
    month = 2
    day_of_month = 3
    day_of_year = 4
    day_of_week = 5
    hour = 6
    minute = 7
    second = 8


class DateTimeSeasonalIndexer(SeasonalIndexer):
    def __init__(self,date_field, index_fields, index_seasons, data_fields):
        super(DateTimeSeasonalIndexer, self).__init__(len(index_seasons))
        self.fields = index_fields
        self.seasons = index_seasons
        self.data_fields = data_fields
        self.date_field = date_field

    def strip_datepart(self, date, date_part, resolution):
        if date_part == DateTime.year:
            tmp = date.year
        elif date_part == DateTime.month:
            tmp = date.month
        elif date_part == DateTime.day_of_year:
            tmp = date.timetuple().tm_yday
        elif date_part == DateTime.day_of_month:
            tmp = date.day
        elif date_part == DateTime.day_of_week:
            tmp = date.weekday()
        elif date_part == DateTime.hour:
            tmp = date.hour
        elif date_part == DateTime.minute:
            tmp = date.minute
        elif date_part == DateTime.second:
            tmp = date.second

        if resolution is None:
            return tmp
        else:
            return  tmp // resolution

    def get_season_of_data(self, data):
        # data = data.copy()
        ret = []
        for ix in data.index:
            date = data[self.date_field][ix]
            season = []
            for c, f in enumerate(self.fields, start=0):
               season.append( self.strip_datepart(date, f, self.seasons[c]) )
            ret.append(season)
        return ret

    def get_season_by_index(self, index):
        raise Exception("Operation not available!")

    def get_data_by_season(self, data, indexes):
        raise Exception("Operation not available!")

    def get_index_by_season(self, indexes):
        raise Exception("Operation not available!")

    def get_data(self, data):
        return data[self.data_fields].tolist()

    def set_data(self, data, value):
        raise Exception("Operation not available!")