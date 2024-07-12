import pandas as pd
import re
def preprocess(data):
    pattern = r"(\d{2}/\d{2}/\d{2}), (\d{1,2}:\d{2} [ap]m) - ([^:]+): (.*)" # regex pattern to extract date, time, author and message
    matches = re.findall(pattern, data)
    df = pd.DataFrame(matches, columns=['Date', 'Time', 'Sender', 'Message'])
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%y %I:%M %p')
    df['year'] = df['Datetime'].dt.year
    df['month'] = df['Datetime'].dt.month_name()
    df['day'] = df['Datetime'].dt.day
    df['hour'] = df['Datetime'].dt.hour
    df['minute'] = df['Datetime'].dt.minute
    df['month_num'] = df['Datetime'].dt.month
    df['week_name'] = df['Datetime'].dt.day_name()
    period = []
    for hour in df[['week_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period
    return df



