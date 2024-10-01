# Group Level Analysis
import numpy as np
import pandas as pd
import emoji
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from PIL import Image
from wordcloud import WordCloud

def top_statictics(chat):
    # Total Messages
    total_messages = chat.shape[0]

    # Total Media Shared
    total_media = chat[chat['Message'] == "<Media omitted>"].shape[0]

    # Total chats
    total_chats = total_messages - total_media

    # Total Emojis
    def count_emojis(text):
        count = 0
        for char_ in text:
            if emoji.is_emoji(char_):
                count += 1
        return count

    total_emojis = chat['Message'].apply(count_emojis).sum()

    # Total Words and Links
    def count_words_and_links(text: str) -> int:
        link_count, word_count = 0, 0
        words = text.split()

        for word in words:
            if word.startswith("https://"):
                link_count += 1
            else:
                word_count += 1

        return word_count, link_count

    words_only_chat = chat[chat['Message'] != "<Media omitted>"]

    words_and_links_tp = words_only_chat['Message'].apply(count_words_and_links)

    total_words, total_links = 0, 0
    for count in words_and_links_tp:
        total_words += count[0]
        total_links += count[1]

    total_words = np.abs(total_words - total_emojis)

    colors = [
        "", "orange", "lightblue", "orange", "lightgreen", "violet",
        "orange", "lightpink", "lightyellow", "lightgray"
    ]
    fig = go.Figure(go.Sunburst(
        labels=["Total Messages", 'Total Chats', 'Total Media', 'Total Links', 'Total Words', 'Total Emojis'],
        parents=[""] + ['Total Messages'] * 3 + ['Total Chats'] * 2,
        values=[total_messages, total_chats, total_media, total_links, total_words, total_emojis],
        marker=dict(colors=colors)
    ))

    # Update layout for tight margins
    fig.update_layout(margin=dict(t=10, l=10, r=10, b=10))

    return fig, total_messages, total_words, total_media, total_links, total_emojis

def monthly_timeline(chat):
    months_dict = { 1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December" }
    month_and_year_group = chat.groupby(['Month', 'Year'])
    month_and_year_name = month_and_year_group.count()[['Name']].sort_index(level = ['Year', 'Month']).reset_index()
    month_and_year_name['Month'] = month_and_year_name['Month'].map(months_dict)
    month_and_year_name['Month_and_Year'] = month_and_year_name['Month'] + ' 20' + month_and_year_name['Year'].astype(np.str_)

    fig = go.Figure(data = go.Scatter
        (
            x = month_and_year_name['Month_and_Year'],
            y = month_and_year_name['Name'],
            name = "Monthly Chat Insights",
            mode = 'lines+markers',
            marker = dict(size=9),
            line=dict(width=1.5),
            hovertemplate="%{y}: %{x}"
        )
    )
    fig.update_layout(
        height=500, 
        width=1000,
        xaxis_title = "Monthly Timeline ➡️",
        yaxis_title = "Message Count ➡️",
        title="Monthly Chat Insights 📅",
        title_x=0.5,
        template="plotly_white",
        margin = dict(l=40, r=40)
    )

    return fig


def weekly_timeline(chat):
    chat = chat.reset_index()
    unique_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    weekly_chat_count = []

    i = 0
    while i < chat.shape[0]:
        current_day = chat.loc[i, 'Day']
        message_count = 0

        while current_day == 'Sunday': # Handling case if starting day is sunday
            message_count += 1
            i += 1
            if i >= chat.shape[0]:
                weekly_chat_count.append(message_count)
                break
            current_day = chat.loc[i, 'Day']

        while current_day != 'Sunday': # Handling case if starting day is not a sunday
            message_count += 1
            i += 1
            if i >= chat.shape[0]:
                weekly_chat_count.append(message_count)
                break
            current_day = chat.loc[i, 'Day']
        if i >= chat.shape[0]:
            break
        weekly_chat_count.append(message_count)
    
    fig = go.Figure(data = go.Scatter
        (
            x = np.arange(1, len(weekly_chat_count) + 1),
            y = weekly_chat_count,
            name = "Weekly Chat Insights",
            mode='lines+markers',
            marker=dict(size=7),
            line=dict(width=1.5),
            hovertemplate="%{y} chats: week %{x}"
        )
    )

    fig.update_layout(
        height=500, 
        width=1000,
        xaxis_title="Weekly Timeline ➡️",
        yaxis_title="Message Count ➡️",
        title="Weekly Chat Insights 📅",
        title_x=0.5,
        template="plotly_white",
        margin = dict(l=10, r=10)
    )
    return fig

# Monthly and Daily Engagement Analysis
def monthly_daily_engagement(chat):
    day_chat_analysis = chat.groupby('Day')['Name'].count()
    month_chat_analysis = chat.groupby('Month_name')['Name'].count()

    fig = make_subplots(rows=1, cols=2)

    fig.add_trace(go.Bar
        (
            x = day_chat_analysis.index,
            y = day_chat_analysis,
            name = "Days",
            showlegend=False
        ), row = 1, col = 1
    )
    fig.update_xaxes(title_text='Days ➡️', row=1, col=1)
    fig.update_yaxes(title_text='Message Count ➡️', row=1, col=1)


    fig.add_trace(go.Bar
        (
            x = month_chat_analysis.index,
            y = month_chat_analysis,
            name = "Months",
            showlegend=False
        ), row = 1, col = 2
    )
    fig.update_xaxes(title_text='Months ➡️', row=1, col=2)
    fig.update_yaxes(title_text='Message Count ➡️', row=1, col=2)


    fig.update_layout(
    height=500, 
    width=1000,
    title="Monthly and Daily Engagement Analysis 📊",
    title_x=0.5,
    template="plotly_white",
    margin = dict(l=10, r=10),
    )

    return fig

# Weekly activity map
def weekly_activity_map(chat):
    pvt = chat.pivot_table(
            index = 'Day',
            columns = 'Hour',
            values = 'Year',
            aggfunc = "count"
    ).fillna(0).astype(np.int64)
    pvt.columns = [f"{i-1} - {i}" for i in pvt.columns]

    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (15, 5))
    sns.heatmap(pvt, annot=True, ax=ax)
    ax.set_xlabel("Chats over Time(Hours)")
    ax.set_ylabel("Days")
    ax.set_title("User Messaging Trends over Time(Hours)")
    return fig

# Cumulative Messages Count over Time
def cumulative_message_count(chat):
    monthname_date_group = chat.groupby(['Month_name', "Date"])['Name'].count().reset_index()

    fig = go.Figure(data = go.Scatter
        (
            y = monthname_date_group['Name'].cumsum(),
            mode='lines',
            name='cumulative message count',
            marker=dict(size=10)
        )
    )
    fig.update_layout(
        height = 500, 
        width = 1000,
        xaxis_title = "Days ➡️",
        yaxis_title = "Message Count ➡️",
        title = "Cumulative Message Count over Days 📊",
        title_x = 0.5,
        template = "plotly_white",
        margin = dict(l=20, r=20)
    )
    return fig

# Most active group members
def most_active_group_member(chat):
    name_group_media = chat.groupby("Name").count().sort_values('Message', ascending = False) # Total Messages
    name_group_only_media = chat[chat['Message'] == "<Media omitted>"].groupby("Name").count() # Total text messages

    name_group_df = name_group_media.join(name_group_only_media, lsuffix='_left', rsuffix='_right').fillna(0)

    name_group_with_emojis = chat.groupby('Name')
    emoji_dict = {name: group for name, group in name_group_with_emojis}

    total_emojis_dict = {}
    for member in emoji_dict:
        messages = emoji_dict[member]['Message']
        
        count = 0

        for message in messages:
            for char_ in message:
                if emoji.is_emoji(char_):
                    count += 1
        
        total_emojis_dict[member] = count

    emoji_df = pd.DataFrame(
        {
            'name':total_emojis_dict.keys(),
            'emoji_count':total_emojis_dict.values()
        }
    )

    emoji_bins = pd.cut(np.array(emoji_df['emoji_count']), bins=5, labels=[
            "Rarely Used",
            "Occasionally Used",
            "Moderately Used",
            "Frequently Used",
            "Highly Active"
        ]
    )
    emoji_df['emoji_bins'] = emoji_bins

    name_group_df = pd.merge(left = name_group_df, right = emoji_df, left_index=True, right_on='name', how = 'inner').reset_index()

    top_25_active_members = name_group_df.head(25) if name_group_df.shape[0] >= 25 else name_group_df.shape[0]

    top_25_active_members = top_25_active_members.rename(columns = {
        'Message_left': 'Total Messages',
        'Message_right': 'Total Media Files Shared',
        'emoji_bins': 'Emoji User'
    })

    fig = px.scatter(
        top_25_active_members, 
        x = "Total Messages",
        y = "name", 
        size="Total Media Files Shared", 
        color="Emoji User",
        size_max=60,
        hover_name="name"
    )
    fig.update_layout(
        width = 1000,
        height = 700,
        xaxis_title = "Messages Count ➡️",
        yaxis_title = "Group Members ➡️",
        title = "Most Active Group Members 👨‍👩‍👧‍👦",
        title_x = 0.5,
        legend = dict(title = "Emoji Users 🙂‍↔️"),
        template="plotly_white"
    )
    return fig, name_group_df

# Cumulative Engagement of top 5 members
def cumulative_engagement_most_active_members(chat, name_group_df):
    name_monthname_day_group = chat.groupby(["Name", "Month_name", "Day"]).count().reset_index()
    fig = go.Figure()

    for i in range(5):
        member = name_monthname_day_group[name_group_df.loc[i, 'name'] == name_monthname_day_group['Name']]
        fig.add_trace(go.Scatter
            (
                y = member["Message"].cumsum(),
                mode='lines',
                name=str(member.iloc[0]['Name'])
            )
        )

    fig.update_layout(
        height=500, 
        width=1000,
        xaxis_title = "Days ➡️",
        yaxis_title = "Messages Count ➡️",
        title="Cumulative Messaging behavour of Most Active User 📈",
        title_x=0.5,
        template="plotly_white",
        margin = dict(l=10, r=10)
    )
    return fig

# most_common_words_and_emojis
def most_common_words_and_emojis(chat):
    word_frequency = dict()
    word_count = np.array(chat[chat['Message'] != '<Media omitted>']['Message'])

    for word in word_count:
        lst = word.split()
        for word in lst:
            try:
                word_frequency[word] += 1
            except KeyError:
                word_frequency[word] = 1

    most_common_words = pd.DataFrame(
        {
            'words':word_frequency.keys(),
            'count':word_frequency.values()
        }
    ).sort_values('count', ascending = False)
    fig1 = go.Figure(
    go.Bar
        (
            y = most_common_words.head(10)['count'],
            x = most_common_words.head(10)['words'],
            name='most_common_words'
        )
    )
    fig1.update_layout(
        height=500, 
        width=1000,
        xaxis_title = "Words ➡️",
        yaxis_title = "Word Count ➡️",
        title="Most Common Words 📊",
        title_x=0.5,
        template="plotly_white",
        margin = dict(l=10, r=10)
    )

    most_common_emojis = {}
    for i in range(most_common_words.shape[0]):
        for char_ in most_common_words.loc[i, 'words']:
            if emoji.is_emoji(char_):
                try:
                    most_common_emojis[char_] += 1
                except KeyError:
                    most_common_emojis[char_] = 1

    most_common_emojis = pd.DataFrame(
        {
            'emojis':most_common_emojis.keys(),
            'count':most_common_emojis.values()
        }
    ).sort_values('count', ascending = False)

    fig2 = go.Figure(
    go.Bar
        (
            y = most_common_emojis.head(10)['count'],
            x = most_common_emojis.head(10)['emojis'],
            name='most_common_words'
        )
    )
    fig2.update_layout(
        height=500, 
        width=1000,
        xaxis_title = "Emojis ➡️",
        yaxis_title = "Emojis Count ➡️",
        title="Most Common Emojis 🙂‍↔️",
        title_x=0.5,
        template="plotly_white",
    margin = dict(l=10, r=10)
    )
    return fig1, fig2

# Word Cloud
def wordcloud(chat):
    word_frequency = dict()
    word_count = np.array(chat[chat['Message'] != '<Media omitted>']['Message'])

    for word in word_count:
        lst = word.split()
        for word in lst:
            try:
                word_frequency[word] += 1
            except KeyError:
                word_frequency[word] = 1

    alice_mask = np.array(Image.open("logo.png"))

    wc = WordCloud(background_color="white", max_words=5000, mask=alice_mask)
    # generate word cloud
    wc.generate_from_frequencies(word_frequency)

    # show
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (10, 10))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    return fig
