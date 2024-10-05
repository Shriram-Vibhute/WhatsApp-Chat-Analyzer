import numpy as np
import pandas as pd
import re

class preprocessor:
    def __init__(self, file_name):
        self.data = file_name
        self.file_name = file_name
        self.chat = None
        self.member_name = None
        self.member_chat = None
        self.date_ = None
        self.month = None
        self.year = None
        self.hour = None
        self.minute = None
        self.whatsapp_msg = None, 
        self.people_msg = None,
        self.whatsapp_msg_date = None, 
        self.people_msg_date = None
        self.months_dict = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }
    
    def text_edit(self):
        pattern = r"\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s\w{1,2}\s-\s"
        message_text = re.split(pattern, self.data)[1:]
        message_date = re.findall(pattern, self.data)

        self.whatsapp_msg, self.people_msg = [], []
        self.whatsapp_msg_date, self.people_msg_date = [], []

        for i in range(len(message_text)):
            if message_text[i].find(":") == -1:
                self.whatsapp_msg.append(message_text[i])
                self.whatsapp_msg_date.append(message_date[i])
            else:
                self.people_msg.append(message_text[i])
                self.people_msg_date.append(message_date[i])
        
        pattern = r"()"
        self.member_name, self.member_chat = [], []
        for i in range(len(self.people_msg)):
            data = self.people_msg[i].split(": ")
            self.member_name.append(data[0])
            self.member_chat.append(data[1][:-1])
        
        return self
    
    def date_time_edit(self):
        pattern = r"(\d{2}/\d{2}/\d{2}),\s(\d{1,2}:\d{2})\s(\w{2})"
        self.date_, self.month, self.year = [], [], []
        self.hour, self.minute = [], []

        for i in range(len(self.people_msg_date)):
            fetch_all = re.search(pattern, self.people_msg_date[i])

            # group 1 - date, month and year
            date_pattern = r"(\d{2})/(\d{2})/(\d{2})"
            full_date = re.search(date_pattern, fetch_all.group(1))
            self.date_.append(full_date.group(1))
            self.month.append(full_date.group(2))
            self.year.append(full_date.group(3))

            # group 3 - format
            format_ = fetch_all.group(3)

            # group 2 - hour, minutes
            full_time = fetch_all.group(2).split(":")
            if format_ == 'pm':
                self.hour.append(int(full_time[0]) + 12)
                self.minute.append(int(full_time[1]))
            else:
                self.hour.append(int(full_time[0]))
                self.minute.append(int(full_time[1]))

        return self

    def dataframe_creation_edit(self):
        self.chat = pd.DataFrame(
            {
                'Name': self.member_name,
                'Message': self.member_chat,
                'Date': self.date_,
                'Month': self.month,
                'Year': self.year,
                'Hour': self.hour,
                "Minute": self.minute
            }
        )

        dtype_mapping = {
            'Name': np.str_,
            'Message': np.str_,
            'Date': np.int32,
            'Month': np.int32,
            'Year': np.int32,
            'Hour': np.int32,
            'Minute': np.int32
        }
        self.chat = self.chat.astype(dtype_mapping)

        self.chat["Day"] = (self.chat['Date'].astype(np.str_) + r'/' + self.chat['Month'].astype(np.str_) + r'/' + self.chat['Year'].astype(np.str_)).apply(lambda x: pd.to_datetime(x).day_name())

        self.chat['Month_name'] = self.chat['Month'].map(self.months_dict)

        return self