from  wordcloud import WordCloud
import re
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user,df):
    if selected_user=='Overall':
        #1number of msg
        num_msg=df.shape[0]
        #2number of words
        words = []
        for message in df['Message']:
            words.extend(message.split())
        num_words = len(words)
        #3number of media
        num_media = df[df['Message']=='<Media omitted>'].shape[0]
        #4number of links
        num_links = df[df['Message'].apply(lambda x: 'http' in x)].shape[0]
        return num_msg,num_words,num_media,num_links
    else:
        df=df[df['Sender']==selected_user]
        num_msg=df.shape[0]
        words = []
        for message in df['Message']:
            words.extend(message.split())
        num_words = len(words)
        num_media = df[df['Message']=='<Media omitted>'].shape[0]
        num_links = df[df['Message'].apply(lambda x: 'http' in x)].shape[0]
        return num_msg,num_words,num_media,num_links
def most_busy_users(df):
    x = df['Sender'].value_counts().head()
    df=round((df['Sender'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'Sender': 'percent'})
    return x,df.head(20)


def create_word_cloud(selected_user,df):
    with open('stop_hinglish.txt', 'r') as file:
        hinglish_stop_words = file.read()
    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]
    temp = df[df['Message'] != '<Media omitted>']
    temp = temp[temp['Message'] != '<This message was edited>']
    stop_words_list = re.split(r'\n', hinglish_stop_words)
    stop_words_list = [word for word in stop_words_list if word]
    def remove_stop_words(message):
        words = []
        for word in message.lower().split():
            if word not in stop_words_list:
                words.append(word)
        return ' '.join(words)

    wc=WordCloud(width=500,height=500,min_font_size=10, max_words=200, background_color='white')
    temp['Message']=temp['Message'].apply(remove_stop_words)
    df_wc=wc.generate(' '.join(temp['Message']))
    return df_wc

def most_common_words(selected_user,df):
    with open('stop_hinglish.txt', 'r') as file:
        hinglish_stop_words = file.read()
    if selected_user!='Overall':
        df=df[df['Sender']==selected_user]
    temp = df[df['Message'] != '<Media omitted>']
    temp = temp[temp['Message'] != '<This message was edited>']
    stop_words_list = re.split(r'\n', hinglish_stop_words)
    stop_words_list = [word for word in stop_words_list if word]
    words = []
    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words_list:
                words.append(word)
    common_words_df=pd.DataFrame(Counter(words).most_common(20))
    return common_words_df
def emoji_helper(selected_user,df):
    if selected_user!='Overall':
        df=df[df['Sender']==selected_user]
    emojis = []
    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df.head(10)

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['Message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline
def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]
    daily_time = df.groupby('Date').count()['Message'].reset_index()
    return daily_time

def weekly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]
    weekly_time = df.groupby('week_name').count()['Message'].reset_index()
    return weekly_time
def monthly_timeline_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]
    return df['month'].value_counts().reset_index()
def msg_activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]
    return df















