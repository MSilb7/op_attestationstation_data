#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from shroomdk import ShroomDK
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import date

load_dotenv()

API_KEY = os.getenv('FLIPSIDE_SHROOMDK_KEY')

# Initialize `ShroomDK` with your API Key
sdk = ShroomDK(API_KEY)


# In[ ]:


# https://app.flipsidecrypto.com/velocity/queries/db09836f-54c8-4063-8ce9-3d4f27d246e4
# Read the above sql from a file and assign to `sql` variable
sql_statement = open("sql/attestation_query.sql").read()

# Run the query against Flipside's query engine 
# and await the results
go_to_next_page = True
start_page_number = 1
start_page_size = 100_000
df_list = []
while go_to_next_page:
        query_result_set = sdk.query(sql_statement, page_number= start_page_number, page_size= start_page_size)
        records = query_result_set.records
        print('num records: ' + str(query_result_set.run_stats.record_count) + ' | page: ' + str(start_page_number))
        if not records:
                go_to_next_page = False
                break #get out
        elif query_result_set.run_stats.record_count < start_page_size: # at max
                go_to_next_page = False
        else:
               start_page_number = start_page_number+1 #go to next page
        # Append df
        rdf = pd.DataFrame(records)
        df_list.append(rdf)

data_df = pd.concat(df_list)
data_df.sample(10)


# In[ ]:


today = date.today().strftime("%m_%d_%Y")
fn = 'attestation_data_' + today + '.csv'
print(fn)
data_df.to_csv(fn, escapechar='\\')


# In[ ]:


# ! jupyter nbconvert --to python pull_attestations_shroomdk.ipynb

