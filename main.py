import pandas as pd                                         #? importing important libraries
import matplotlib.pyplot as plt
import re
import streamlit as st
from io import StringIO
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, show

#! basic configurations
st.set_page_config(
    page_title="QTX reader",
    page_icon="🔹",
    layout="wide",
    initial_sidebar_state="collapsed")

#! App header
st.header("QTX file reader & color-graph display")


#! QTX file uploader
qtx_file = st.file_uploader("Upload QTX format file only:", type=['qtx'], accept_multiple_files=True, help="Supports multiple files upload")

#! std illuminants for comparison
d65 = pd.read_csv('d65.csv').set_index('wavelength')                                            #? dataframing D65 values
inca = pd.read_csv('inca.csv').set_index('wavelength')                                          #? dataframing INCA values
merged_illum = d65.join(inca, on='wavelength', how='right', lsuffix='_D65', rsuffix='_INCA')    #? merging D65 & INCA dataframes
#st.dataframe(inca)


#! QTX file opener
try:
    #! converting qtx data to raw string
    string_data = ""                                                        #? empty variable for string holding
    for f in qtx_file:                                                      #? looping over every line in the file
        stringio = StringIO(f.getvalue().decode("utf-8"))                   #? extracting & decoding every line to utf-8
        string_data = string_data + '\n' + stringio.read()                  #? appending string variable

    #! qtx raw data display 
    with st.expander('Raw data: ', expanded=False):                         #? displaying raw data of color std
        st.write(string_data)
    
    #! values extraction using regex
    std_name = re.findall("STD_NAME=(.+)", string_data)                     #? extracting the color stds name
    list_ref_low = re.findall("STD_REFLLOW=(\d+),", string_data)            #? lowest wavelength value
    list_ref_pts = re.findall("STD_REFLPOINTS=(\d+),", string_data)         #? total wavelength points
    list_ref_inter = re.findall("STD_REFLINTERVAL=(\d+),", string_data)     #? interval between wavelengths
    list_ref_vals = re.findall("BAT_R=|STD_R=(.+)[,\s]", string_data)       #? reflectance values match
    #st.write(list_ref_vals.strip(','))

    #! color std selection & pre-display processing section
    col1, col2 = st.columns(2)                                                          #? making two columns
    name_select = col1.selectbox("Select Color Std", std_name)                          #? stds list display
    std_i = std_name.index(name_select)                                                 #? selected index of std
    ref_low, ref_pts, ref_inter = int(list_ref_low[std_i]), int(list_ref_pts[std_i]), int(list_ref_inter[std_i])        #? int:variable assignment to std data points
    ref_high = ref_low + ref_pts * ref_inter                                            #? highest wavelength calculation
    y_ref_val_list = [rval for rval in list_ref_vals[std_i].split(',') if rval.strip()] #? assigning 'y' for dataframe
    x_wave_list = list(range(ref_low, ref_high, ref_inter))                             #? assigning 'x' for dataframe
    sd_df = pd.DataFrame(y_ref_val_list, index=x_wave_list, columns=[name_select])      #? dataframing 'x' & 'y'
    sd_df[name_select] = sd_df[name_select].astype('float64')                           #? converting ref values to float 
    combi_df = merged_illum.join(sd_df, how='right')                                    #? color display(wip)
    color = col2.color_picker('Color Display (wip)', '#ffffff')

    #! Toggle to show illuminants
    p = figure(width=600, height=300, background_fill_color="#0e1118", border_fill_color='#0e1118', outline_line_color='#ffffff', y_range=(0, 100))
    p.outline_line_color = "white"                                          #? plot styling elements
    p.outline_line_width = 5
    p.outline_line_alpha = 1
    p.xaxis.axis_label = "Wavelength(λ)"
    p.xaxis.axis_label_text_color = "white"
    p.xaxis.major_label_text_color = "white"
    p.yaxis.axis_label = "Reflectance(%)"
    p.yaxis.axis_label_text_color = "white"
    p.yaxis.major_label_text_color = "white"
    x = combi_df.index                                                      #? assigning 'x' value
    if col1.checkbox("Show Illuminants"):                                   #? checkbox for showing std illuminants
        for i, col in enumerate(combi_df.columns):                          #? looping over every column in combi_df
            if col != name_select:                                          #? checking 'ref_val' columns
                combi_df[col] = combi_df[col].apply(lambda x:x*100/combi_df[col].max()) #? applying the relative function on 'ref_val' columns
                y = combi_df.iloc[:, i]                                     #? assigning 'y' value
                p.line(x, y, line_width=2, color="#7f0000", legend_label=col) #? line plot for every illuminant
        p.line(x, y=combi_df[name_select], line_width=3, color="#01f700", legend_label=name_select) #? line plot for only color std
    else:
        y = combi_df[name_select]                                           #? assigning 'y' value
        p.line(x, y, line_width=3, color="#01f700", legend_label=name_select) #? line plot for only color std
    p.legend.location = "top_left"
    p.legend.label_text_color = "white"
    p.legend.border_line_width = 1
    p.legend.border_line_color = "white"
    p.legend.border_line_alpha = 0.5
    p.legend.background_fill_color = "white"
    p.legend.background_fill_alpha = 0.1
    col2.bokeh_chart(p)

    #! tabular data
    with col1.expander('Table', expanded=False):                            #? displaying dataframe
        st.dataframe(combi_df)

except:
    st.write("Waiting for your upload !")                                   #? exception handling