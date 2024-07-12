import streamlit as st
import helper
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns


import preprocessor

st.sidebar.title('Whatsapp Chat Analyzer')
upload_file=st.sidebar.file_uploader('Upload your Whatsapp Chat', type='txt')
if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)
    #st.table(df.head(10))
    #fetching unique senders
    sender_list= df['Sender'].unique().tolist()
    sender_list.sort()
    sender_list.insert(0, 'Overall')
    selected_user=st.sidebar.selectbox('Show analysis with respect to:', sender_list)
    if st.sidebar.button("Show Analysis"):
        num_msg,num_words,num_media,num_links=helper.fetch_stats(selected_user,df)
        st.title('Top Statistics')
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.subheader('Total Messages')
            st.subheader(num_msg)
        with col2:
            st.subheader('Total Words')
            st.subheader(num_words)
        with col3:
            st.subheader('Total Media')
            st.subheader(num_media)
        with col4:
            st.subheader('Total Links')
            st.subheader(num_links)

    #time analysis

        st.title('Time Analysis')
        st.write('When are the most messages sent?')
        timeline=helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['Message'], marker='o', color='r')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #day analysis
        st.title('Day Analysis')
        st.write('Which day of the week are the most messages sent?')
        day_analysis=helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(day_analysis['Date'], day_analysis['Message'], color='g')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #week analysis
        st.title('Activity Map')
        col1,col2=st.columns(2)
        with col1:
            st.title('Week Analysis')
            st.write('Which week day are the most messages sent?')
            week_analysis=helper.weekly_timeline(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(week_analysis['week_name'], week_analysis['Message'], color='brown', alpha=0.7, edgecolor='black', linewidth=2)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.title('Monthly Analysis')
            st.write('Which month are the most messages sent?')
            month_analysis=helper.monthly_timeline_activity(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(month_analysis['month'], month_analysis['count'], color='orange', alpha=0.7, edgecolor='black', linewidth=2)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        #msg activity heatmap
        st.title('Message Activity Heatmap')
        heatmap=helper.msg_activity_heatmap(selected_user,df)
        fig, ax = plt.subplots(figsize=(20, 10))
        sns.heatmap(heatmap.pivot_table(index='week_name', columns='period', values='Message', aggfunc='count').fillna(0),ax=ax)
        plt.yticks(rotation='horizontal')
        st.pyplot(fig)

        #finding the busiest users in a group(group leve)
        if selected_user=='Overall':
            st.title('Busiest Users')
            x,new_df=helper.most_busy_users(df)
            fig,ax=plt.subplots(figure=(100,100))
            plt.xticks(rotation='vertical')
            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='purple')
                st.pyplot(fig)
            with col2:
                st.table(new_df)
        #heatmap of messages activity



        #word cloud
        st.title('Word Cloud')
        wc = helper.create_word_cloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(wc, interpolation='bilinear')
        st.pyplot(fig)
        #most common words
        st.title('Most Common Words')
        common_words_df=helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(common_words_df[0], common_words_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #emoji
        st.title('Most Common Emoji')
        emoji_df=helper.emoji_helper(selected_user,df)
        col1,col2=st.columns(2)
        with col1:
            st.table(emoji_df.head(15))
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1], labels=emoji_df[0], autopct='%1.1f%%', startangle=140)
            st.pyplot(fig)











