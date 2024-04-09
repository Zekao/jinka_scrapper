import pandas as pd

def remove_unnecessary_columns(df):
    '''
        Remove unnecessary columns from the dataframe

        @param: 
        - df dataframe containing the announces
        
        @return: data
    '''
    return df[['source', 'owner_type', 'rent', 'area', 'room', 'type', 'city', 'stops', 'id', 'source_description']]

def format_table(token, df):
    '''
        @param:
        - token: token used to get the announces (config.TOKEN)
        - df: dataframe containing the announces
        This function will format the id to a correct format in order to redirect to the announce page

        It will also only keep the name of the stops, we don't need the rest
    
        @return: Edited dataframe
    '''

    df['id'] = df.apply(lambda row: f"https://www.jinka.fr/alert_result?token={token}&ad={row['id']}", axis=1)
    # add a column called lines containing the lines of the stops and locate it after the stops column
    df['lines'] = df.apply(lambda row: [stop['lines'] for stop in row['stops']], axis=1)
    # change the position of the lines column
    cols = list(df.columns)
    cols.insert(8, cols.pop(cols.index('lines')))
    df = df[cols]

    df['stops'] = df.apply(lambda row: [stop['name'] for stop in row['stops']], axis=1)
    df = df.rename(columns={'id': 'link'})
    return df

def clean_table(token, df):
    '''
        @param:
        - token: token used to get the announces (config.TOKEN)
        - df: dataframe containing the announces

        @return: Edited dataframe
    '''
    df = remove_unnecessary_columns(df)
    df = format_table(token, df)
    return df