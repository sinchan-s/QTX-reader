import pandas as pd
import matplotlib.pyplot as plt
import re
import streamlit as st

# basic configurations
st.set_page_config(
    page_title="QTX reader",
    page_icon="Q",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.header("QTX file reader & color-graph display")

qtx_file = st.file_uploader("Upload qtx format file only", type=['qtx', 'QTX'], accept_multiple_files=False,
                            help="Only upload QTX file")


# def qtx_reader(qfile):
with open('test.QTX') as f:
    lines = f.read()
    z = re.findall("STD_REFLLOW=(\d+),", lines)
    a = re.findall("STD_REFLPOINTS=(\d+),", lines)
    b = re.findall("STD_REFLINTERVAL=(\d+),", lines)
    c = re.findall("STD_R[=,](.+)", lines)
    if z:
        for i, j in enumerate(z):
            ref_low = int(z[i])
            ref_pts = int(a[i])
            ref_intv = int(b[i])
            ref_val_list = str(c[i]).split(',')
            wave_list = [k for k in range(ref_low, ref_low + ref_pts * ref_intv, ref_intv)]
            # print('Wavelength values: ', wave_list)
            # print('Reflectance values: ', ref_val_list)
            sd_df = pd.DataFrame(ref_val_list, index=wave_list, columns=['ref_val'])
            sd_df['ref_val'] = sd_df['ref_val'].astype('float64')
            print(sd_df)
            st.write(sd_df.info())
            # st.pyplot(sd_df)

'''
try:
    if qtx_file is not None:
        st.write("File Preview:")
        qtx_reader(qtx_file)
        # q_file = QtxReader(file_upload)
        # QtxReader.val_finder()
except:
    st.write("Unable to preview file !!")
'''