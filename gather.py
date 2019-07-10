# Opens SQL database chat.db and loads into panda
# Returns formated pandas dataframe
# Needs to open messages, handle, and chat?
# IN messages, replace handle with numbers from handle table. (ROWID, ID)

import sqlite3
import pandas as pd

path = "/Users/john/Desktop/chat.db"


def populate_frame(file): # IF handle is zero, it is sent from you
    conn = sqlite3.connect(file)
    frame = pd.read_sql_query("select * from message;", conn)
    handle = pd.read_sql_query("select ROWID, id from handle;", conn)
    frame = clean_null(frame)
    row = 0
    for message in frame["handle_id"]:
        if message != 0:
            temp = handle.loc[handle['ROWID'] == message]
           #temp = handle['id'].where(handle['ROWID'] == message)
            temp = temp.to_dict('list')
            frame.iloc[row, frame.columns.get_loc('handle_id')] = temp['id'][0]
        row += 1
    return frame


def clean_null(df):  # Removes Null text cells from DataFrame
    df = df.dropna(subset=['text'])
    return df


def on_date(df, start, end):  # pass in dataframe, date(in Core Data timestamp):
    # returns another dataframe of messages on a date
    return df.query('@start <= date_delivered < @end')  # Needs to be range of dates, like x < date < y


def is_me(df):  # returns dateframe of text sent by you
    return df.query('is_from_me == 1')


def is_emote(df): # returns dataframe of emotes
    return df.query('is_emote == 1')


def find_convo(df, number):  # returns text conversation with number, where number includes the country code
    return df.query('handle_id == @number')


def is_groupchat(df, roomname=''):  # returns a specified group chat if roomname is available, else returns df with all
    # group chats.
    df = df.query('cache_roomname != NULL')
    if not roomname:
        return df.query('cache_roomname == @roomname')
    else:
        return df


if __name__ == '__main__':
    df = populate_frame(path)
    # print(df[['text', 'handle_id']])
    df = clean_null(df)
    # print(df[['text', 'handle_id']])
    #df = is_emote(df)
    df = df[['text', 'handle_id']]
    print(df)
