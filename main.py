import pandas as pd
import matplotlib.pyplot as plt
import re
import streamlit as st
from io import StringIO

# basic configurations
st.set_page_config(
    page_title="QTX reader",
    page_icon="🔹",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.header("QTX file reader & color-graph display")


# QTX file uploader
qtx_file = st.file_uploader("Upload QTX format file only:", type=['qtx'], accept_multiple_files=False,
                            help="Only upload QTX file")

# QTX file opener
try:
    # converting qtx data to raw string
    stringio = StringIO(qtx_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    with st.expander('Raw data: ', expanded=False):
        st.write(string_data)
    # values extraction using regex
    std_name = re.findall("STD_NAME=(.+)", string_data)
    list_ref_low = re.findall("STD_REFLLOW=(\d+),", string_data)
    list_ref_pts = re.findall("STD_REFLPOINTS=(\d+),", string_data)
    list_ref_int = re.findall("STD_REFLINTERVAL=(\d+),", string_data)
    list_ref_vals = re.findall("STD_R[=,](.+)", string_data)
    # color std selection & graph display
    name_select = st.selectbox("Select Color", std_name)
    std_i = std_name.index(name_select)
    ref_low, ref_pts, ref_int = int(list_ref_low[std_i]), int(list_ref_pts[std_i]), int(list_ref_int[std_i])
    ref_max = ref_low + ref_pts * ref_int
    y_ref_val_list = str(list_ref_vals[std_i]).split(',')
    x_wave_list = [k for k in range(ref_low, ref_max, ref_int)]
    sd_df = pd.DataFrame(y_ref_val_list, index=x_wave_list, columns=[name_select])
    sd_df[name_select] = sd_df[name_select].astype('float64')
    st.line_chart(sd_df)
    color = st.color_picker('Standard Color', '#00f900')
except:
    st.write("Upload a QTX file !")