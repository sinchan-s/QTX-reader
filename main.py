import pandas as pd
import matplotlib.pyplot as plt
import re
import streamlit as st
from io import StringIO

#! basic configurations
st.set_page_config(
    page_title="QTX reader",
    page_icon="🔹",
    layout="wide",
    initial_sidebar_state="collapsed")

st.header("QTX file reader & color-graph display")


#! QTX file uploader
qtx_file = st.file_uploader("Upload QTX format file only:", type=['qtx'], accept_multiple_files=True, help="Supports multiple files upload")
d65 = pd.read_csv('d65.csv').set_index('wavelength')
d65_max = d65['ref_val'].max()
d65['std_D65'] = d65['ref_val'].apply(lambda x:x*100/d65_max)
d65 = d65.drop('ref_val', axis=1)
inca = pd.read_csv('inca.csv').set_index('wavelength')
inca_max = inca['ref_val'].max()
inca['std_INCA'] = inca['ref_val'].apply(lambda x:x*100/inca_max)
inca = inca.drop('ref_val', axis=1)
merged_illum = d65.join(inca, on='wavelength', how='right')
#st.dataframe(merged_illum)
#! QTX file opener
try:
    #! converting qtx data to raw string
    with st.expander('Raw data: ', expanded=False):
        string_data = ""
        for f in qtx_file:
            stringio = StringIO(f.getvalue().decode("utf-8"))
            string_data = string_data + '\n' + stringio.read()
        st.write(string_data)
    #! values extraction using regex
    std_name = re.findall("STD_NAME=(.+)", string_data)
    list_ref_low = re.findall("STD_REFLLOW=(\d+),", string_data)
    list_ref_pts = re.findall("STD_REFLPOINTS=(\d+),", string_data)
    list_ref_inter = re.findall("STD_REFLINTERVAL=(\d+),", string_data)
    list_ref_vals = re.findall("STD_R[=,](.+)", string_data)
    #! color std selection & graph display
    name_select = st.selectbox("Select Color", std_name)
    std_i = std_name.index(name_select)
    ref_low, ref_pts, ref_inter = int(list_ref_low[std_i]), int(list_ref_pts[std_i]), int(list_ref_inter[std_i])
    ref_high = ref_low + ref_pts * ref_inter
    y_ref_val_list = str(list_ref_vals[std_i]).split(',')
    x_wave_list = list(range(ref_low, ref_high, ref_inter))
    sd_df = pd.DataFrame(y_ref_val_list, index=x_wave_list, columns=[name_select])
    sd_df[name_select] = sd_df[name_select].astype('float64')
    combi_df = merged_illum.join(sd_df, how='right', lsuffix='_std', rsuffix='_illum')
    st.dataframe(combi_df)
    #! columnized sections
    col1, col2 = st.columns(2)
    col1.line_chart(combi_df)
    color = col2.color_picker('Standard Color', '#ffffff')
except:
    st.write("Waiting for your upload !")