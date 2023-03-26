################################################################################ 
# IMPORTING DEPENDENCIES
################################################################################
from __future__ import annotations
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import date
import datetime
from plotly.subplots import make_subplots
from dateutil import parser
import matplotlib.pyplot as plt

################################################################################
# TITLE, HEADER & SIDEBAR
st.set_page_config(page_title = "deviceSumaryReport", page_icon = "📈", layout = "wide")


#Choosing Regions
regionSidebar = st.sidebar.multiselect("Select The Region :", options = ["US","UK"])


#TABLE STYLES
# style
th_props = [
  ('font-size', '14px'),
  ('text-align', 'center'),
  ('font-weight', 'bold'),
  ('color', '#080808'),
  ('background-color', '#00aac7')
  ]
                               
td_props = [
  ('font-size', '12px')
  ]
                                 
styles = [
  dict(selector="th", props=th_props),
  dict(selector="td", props=td_props)
  ]
################################################################################
# COLUMN DIVISIONS 
################################################################################
# These are a part of the streamlit lbrary
# With the help of the below columns, we can customise the position of the plots/header of plots in the dashboard
dashboardTitle, dontUse1 = st.columns((1, 0.00000001))
dashboardTitle, dontUse1 = st.columns((1, 0.00000001))
topMarkdown, dontUse2 = st.columns((1, 0.00000001))
selectedRegion, devicesCount, selectedDateHeader = st.columns((1,1.45,1))
bottomMarkdown, dontUse3 = st.columns((1, 0.00000001))

# MAIN PLOT COLUMNS
dontUse8, header1, dontUse14 = st.columns((0.58,2,0.001))
dontUse9, plot1, dontUse15 = st.columns((0.15,2,0.001))
dontUse10, header2, dontUse16 = st.columns((0.52,2,0.001))
dontUse11, plot2, dontUse17 = st.columns((0.15,2,0.001))
dontUse12, header3, dontUse18 = st.columns((0.35,2,0.001))
dontUse13, plot3, dontUse19 = st.columns((0.15,2,0.001))
dontUse26, RegionSummary = st.columns((0.00000001,1))
    

markdowns, dontUse20 = st.columns((0.00000001,1))
dontUse21, centerHeader1, dontUse22 = st.columns((0.35,2,0.001))
dontUse23, sunburst = st.columns((0.00000001,1))

dontUse24, centerHeader2, dontUse25 = st.columns((0.65,2,0.001))
dontUse26, tabularParentDataCol = st.columns((0.00000001,1))

dontUse24, centerHeader3, dontUse25 = st.columns((0.45,2,0.001))
dontUse26, tabularDirectTenantDataCol = st.columns((0.00000001,1))

dontUse24, dateError = st.columns((0.0000000000001, 1))

#Title
with dashboardTitle :
        st.markdown("""---""")
        st.markdown("<h2 style = 'text-align : center; color : Cyan;'>Device Summary Dashboard</h2>", unsafe_allow_html=True)
        st.markdown("""---""")
# Getting List of Total Amazon Last Mile Devices
def amazonUS():
    amz_query = '''select b.manufacturer_device_id,a.device_id as MDID_seq,c.tenant_display_name,d.name from(
    select device_id,tenant_id from ndvehicledeviceconfigurations
    where (tenant_id in (select managed_tenant_id from ndtenanttenant where managing_tenant_id in ('2254'))
    or tenant_id in ('2254'))
    )a
    left join nddevicemaster b
    on a.device_id = b.manufacturer_device_id_seq
    left join ndtenantmaster c
    on a.tenant_id = c.tenant_id
    left join nddevicestatemaster d on
    d.id = b.state_id
    '''
    prod_db=psycopg2.connect(database="beta-prod-idms-db", user="postgres-ro", password="w6jduvhV6Qz9",host="pg-production-ro.netradyne.info", port="5432")
    amazonUS_ = pd.read_sql_query(non_amz_query,con=prod_db)
    amazonUS_ = pd.DataFrame(data=amazonUS_)
    return amazonUS_
def amazonUK():
    amz_query = '''select b.manufacturer_device_id,a.device_id as MDID_seq,c.tenant_display_name,d.name from(
    select device_id,tenant_id from ndvehicledeviceconfigurations
    where (tenant_id in (select managed_tenant_id from ndtenanttenant where managing_tenant_id in ('3422'))
    or tenant_id in ('3422'))
    )a
    left join nddevicemaster b
    on a.device_id = b.manufacturer_device_id_seq
    left join ndtenantmaster c
    on a.tenant_id = c.tenant_id
    left join nddevicestatemaster d on
    d.id = b.state_id
    '''
    prod_db=psycopg2.connect(database="beta-prod-idms-db", user="postgres-ro", password="w6jduvhV6Qz9",host="pg-production-ro.netradyne.info", port="5432")
    amazonUK_ = pd.read_sql_query(non_amz_query,con=prod_db)
    amazonUK_ = pd.DataFrame(data=amazonUK_)
    return amazonUK_
for i in regionSidebar:
            if i == 'US':
                df = amazonUS()
                df.rename(columns = {'manufacturer_device_id':'Count of Devices','name':' '},inplace=True)
                pivot = df.pivot_table(columns = [' '],values=['Count of Devices'],aggfunc = 'count')
                pivot['Total Count of devices'] = pivot.values.sum()
                first_col = pivot.pop('Total Count of devices')
                pivot.insert(0, 'Total Count of devices', first_col)
                hide_dataframe_row_index = """
                            <style>
                            .row_heading.level0 {display:none}
                            .blank {display:none}
                            </style>
                            """
                st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
                with RegionSummary :
                    st.subheader(":green[US Amazon Device Summary]")
                    pivot = pivot.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
                    st.table(pivot)
                    series = df[' '].value_counts()
                    df_result = pd.DataFrame(series)
                    df_result = df_result.reset_index()
                    df_result.columns = ['State', 'Total']
                    fig = px.pie(df_result, values='Total', names='State', title='US Device Summary',color_discrete_sequence=px.colors.sequential.RdBu)
                    if(st.button("Click here to US Summary as charts!")):    
                            fig.show()
                    st.markdown("""---""")
                    
                
            elif i == 'UK':
                df = amazonUK()
                df.rename(columns = {'manufacturer_device_id':'Count of Devices','name':' '},inplace=True)
                pivot = df.pivot_table(columns = [' '],values=['Count of Devices'],aggfunc = 'count')
                pivot['Total Count of devices'] = pivot.values.sum()
                first_col = pivot.pop('Total Count of devices')
                pivot.insert(0, 'Total Count of devices', first_col)
                pivot = pd.DataFrame(pivot)
                hide_dataframe_row_index = """
                            <style>
                            .row_heading.level0 {display:none}
                            .blank {display:none}
                            </style>
                            """
                st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
                with RegionSummary :
                    st.subheader(":red[UK Amazon Device Summary]")
                    pivot = pivot.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
                    st.table(pivot)
                    series = df[' '].value_counts()
                    df_result = pd.DataFrame(series)
                    df_result = df_result.reset_index()
                    df_result.columns = ['State', 'Total']
                    fig = px.pie(df_result, values='Total', names='State', title='UK Device Summary',color_discrete_sequence=px.colors.sequential.RdBu)
                    if(st.button("Click here to view UK Summary as charts!")):    
                            fig.show()
                    st.markdown("""---""")
