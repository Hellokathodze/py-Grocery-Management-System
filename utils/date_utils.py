from datetime import datetime


class DateUtils:

    @staticmethod
    def get_day_of_week():

        now = datetime.now()
        return now.strftime("%A")

    @staticmethod
    def get_month():

        return datetime.now().month

    @staticmethod
    def get_season(month):

        if month in [12, 1, 2]:
            return "Winter"

        elif month in [3, 4, 5]:
            return "Summer"

        elif month in [6, 7, 8]:
            return "Monsoon"

        else:
            return "Autumn"

    @staticmethod
    def get_current_date():

        return datetime.now()