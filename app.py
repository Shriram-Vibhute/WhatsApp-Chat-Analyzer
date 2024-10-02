# Importing required libraries
from preprocessing import preprocessor
import streamlit as st
import helper

st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <div style="border-radius: 7px; background-color: #1f2023; color: white; padding:15px">
        <h1 style='font-family: "Courier New", Courier, monospace; color: white;'>
            🐦‍🔥ChatWise
        </h1>
        <h4 style='font-weight: bold;; font-family: "Courier New", Courier, monospace; color: white;'>Transform Your
            Chats into Actionable Analytics...!
        </h4>
        <p>
            Gain valuable insights into your chats with enhanced visualizations 📶, comprehensive statistics 📊, and
            complete PDF export 📑 capabilities.
        </p>
        <p style="border-radius: 7px; background-color: rgb(227, 232, 232); color: black; padding:15px">
            🔐 No chat data is transmitted to a server. All processing occurs locally within your browser for maximum
            privacy and security.
        </p>
        <div style = "display: flex; align-items: center; border-radius: 7px; background-color: rgb(227, 232, 232); color: black; padding:15px 0px 15px, 0px; padding:15px">
            <div>📌 This project is open-source and all code is public on github.</div>
            <div style = "padding-left: 7px;"><a href="https://github.com/Shriram-Vibhute/WhatsApp-Chat-Analyzer" class="fa fa-github" style="color: black; font-size: 25px; background-color: transparent; text-decoration:none;"></a></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# How to use this app 
uploaded_file = st.file_uploader("Choose a file")
# Sidebar Structure
# sb = st.sidebar
# st.title('Whatsapp Chat Analysis')
# uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # DataFrame Creation
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    chat = preprocessor(data)
    chat.text_edit()
    chat.date_time_edit()
    chat.dataframe_creation_edit()
    dataframe = chat.chat

    names = ["Chad", "Sam", "Dante", "Tony", "Dominic", "Brian", "Letty", "Mia", "Roman", "Tej", "Luke", "Deckard", "Giselle" ,"Han", "Sean", "Cipher", "Jakob", "Elena", "Ramsey", "Nobody", "Angela", "Jessie", "Johnny", "Leon", "Vince", "Lynda", "Rita", "Tego"]

    actual = dataframe['Name'].unique()

    mapped = {
        actual[i] : names[i] for i in range(actual.shape[0])
    }
    dataframe['Name'] = dataframe['Name'].map(mapped)

    # Fetching all users
    user_list = chat.chat['Name'].unique().tolist()
    user_name = st.multiselect("Select Multiple Users", user_list, placeholder="Overall")

    if len(user_name) > 0:
        dataframe = chat.chat[chat.chat['Name'].isin(user_name)]

    start_analysis_btn = st.button('Start Analysis 📊', type = 'secondary')

    # Analysis
    if start_analysis_btn:

        # Top Statictics
        fig, total_messages, total_words, total_media, total_links, total_emojis = helper.top_statictics(dataframe)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.write("📲 Total Messages - {}".format(total_messages))
        with col2:
            st.write(" 📌 Total Words - {}".format(total_words))
        with col3:
            st.write("🖼️ Total Media - {}".format(total_media))
        with col4:
            st.write(" 🔗 Total Links - {}".format(total_links))
        with col5:
            st.write(" 🙂‍↔️ Total Emojis - {}".format(total_emojis))
        st.plotly_chart(fig)

        # Monthly Timeline
        fig = helper.monthly_timeline(dataframe)
        st.plotly_chart(fig) 

        # Weekly Timeline
        fig = helper.weekly_timeline(dataframe) 
        st.plotly_chart(fig)

        # Monthly and Daily Engagement Analysis
        fig = helper.monthly_daily_engagement(dataframe)      
        st.plotly_chart(fig)

        # Weekly activity map
        fig = helper.weekly_activity_map(dataframe)
        st.pyplot(fig)

        # Cumulative Messages Count over Time
        fig = helper.cumulative_message_count(dataframe)
        st.plotly_chart(fig)

        # Most active group Members
        if user_name == "Overall":
            fig, name_group_df = helper.most_active_group_member(dataframe)
            st.plotly_chart(fig)

            # Cumulative Engagement of top 5 members
            fig = helper.cumulative_engagement_most_active_members(dataframe, name_group_df)
            st.plotly_chart(fig)

        # most_common_words_and_emojis
        fig1, fig2 = helper.most_common_words_and_emojis(dataframe)
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig1)
        with col2:
            st.plotly_chart(fig2)
        
        # Word Cloud
        fig = helper.wordcloud(dataframe)
        st.pyplot(fig)
        

# Footer Structure

st.markdown(
    """
        <div style = "display: flex; justify-content: center; align-items: center; border-radius: 7px;">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            <a href = "https://in.linkedin.com/in/shriram-vibhute"><i class="fa fa-linkedin" style = "font-size:25px; padding: 10px"></i></a>
            <a href = "https://x.com/shriram_vibhute"><i class="fa fa-twitter" style = "font-size:25px; padding: 10px"></i></a>
            <a href = "https://github.com/Shriram-Vibhute"><i class="fa fa-github" style = "font-size:25px; padding: 10px"></i></a>
            <a href = #><i class="fa fa-facebook-square" style = "font-size:25px; padding: 10px"></i></a>
            <a href = #><i class="fa fa-instagram" style = "font-size:25px; padding: 10px"></i></a>
            <a href = "https://www.kaggle.com/shriramvibhute"><div style = "font-size: 26px; font-weight: bold;">K</div></a>
        </div>   
        <div style = "display: flex; justify-content: center; align-items: center;>
            <p style = "font-weight:bold; font-size: 18px;">Thanks 🩵 for using our website. We will meet once again 👋🏻 </p>
        </div> 
    """,
    unsafe_allow_html=True
)