import h5py
import numpy as np
import pandas as pd
import plotly.express as px

# read data out of h5py file and create visualization
with h5py.File('weather_data.h5', 'r') as hdf:

    # get overview of groups and items in groups
    base_items = list(hdf.items())
    grp_wd = hdf.get("wetterdienst.de")
    grp_wd_items = list(grp_wd.items())
    grp_wo = hdf.get("wetteronline.de")
    grp_wo_items = list(grp_wo.items())
    grp_lh = hdf.get("lufthamburg.de")
    grp_lh_items = list(grp_wo.items())

    # retrieve datasets and visualize content
    ## WETTERDIENST.DE
    # get each dataset
    wd_insert_datetime = hdf.get("wetterdienst.de/insert_datetime")
    wd_weather = hdf.get("wetterdienst.de/weather")
    wd_temperature = hdf.get("wetterdienst.de/temperature")
    wd_rainfall = hdf.get("wetterdienst.de/rainfall")

    # read datasets into arrays
    wd_insert_datetime = np.array(wd_insert_datetime)
    wd_insert_datetime = wd_insert_datetime.astype('datetime64', copy=False)
    wd_weather = np.array(wd_weather)
    wd_temperature = np.array(wd_temperature)
    wd_rainfall = np.array(wd_rainfall)

    # read arrays into pandas dataframe
    wd_df_1 = pd.DataFrame(wd_insert_datetime, columns=['insert_datetime'])
    wd_df_2 = pd.DataFrame(wd_weather, columns=['weather'])
    wd_df_3 = pd.DataFrame(wd_temperature, columns=['temperature'])
    wd_df_4 = pd.DataFrame(wd_rainfall, columns=['rainfall'])
    wd_df = pd.concat([wd_df_1, wd_df_2, wd_df_3, wd_df_4], axis=1, join="inner")

    # visualize development of data storage by 'insert_datetime'
    # temperature
    wd_fig_temp = px.line(x=wd_df['insert_datetime'], y=wd_df['temperature'],
                     title='Wetterdienst.de<br><sup>Temperature in °C</sup>')
    wd_fig_temp.update_layout(title_x=0.5,
                         plot_bgcolor='#f6f6f6',
                         yaxis_title='temperature in °C',
                         xaxis_title='insert datetime')
    wd_fig_temp.update_traces(line_color="#0096FF", line_width=3)
    wd_fig_temp.show()

    #rainfall
    wd_fig_rain = px.line(x=wd_df['insert_datetime'], y=wd_df['rainfall'],
                     title='Wetterdienst.de<br><sup>Amount of Rainfall in mm</sup>')
    wd_fig_rain.update_layout(title_x=0.5,
                         plot_bgcolor='#f6f6f6',
                         yaxis_title='amount of rainfall in mm',
                         xaxis_title='insert datetime')
    wd_fig_rain.update_traces(line_color="#bd34eb", line_width=3)
    wd_fig_rain.show()


    # WETTERONLINE.DE
    # get each dataset
    wo_temperature = hdf.get("wetteronline.de/temperature")
    wo_insert_datetime = hdf.get("wetteronline.de/insert_datetime")

    # read datasets into arrays
    wo_temperature = np.array(wo_temperature)
    wo_insert_datetime = np.array(wo_insert_datetime)
    wo_insert_datetime = wo_insert_datetime.astype('datetime64', copy=False)

    # read arrays into pandas dataframe
    wo_df_1 = pd.DataFrame(wo_insert_datetime, columns=['insert_datetime'])
    wo_df_2 = pd.DataFrame(wo_temperature, columns=['temperature'])
    wo_df = pd.concat([wo_df_1, wo_df_2], axis=1, join="inner")

    # visualize development of data storage by 'insert_datetime'
    wo_fig = px.line(x=wo_df['insert_datetime'], y=wo_df['temperature'],
                     title='Wetteronline.de<br><sup>Temperature in °C</sup>')
    wo_fig.update_layout(title_x=0.5,
                         plot_bgcolor='#f6f6f6',
                         yaxis_title='temperature in °C',
                         xaxis_title='insert datetime')
    wo_fig.update_traces(line_color="#2342db", line_width=3)
    wo_fig.show()


    # LUFT.HAMBURG.DE
    # get each dataset
    lh_temperature = hdf.get("luft.hamburg.de/temperature")
    lh_insert_datetime = hdf.get("luft.hamburg.de/insert_datetime")

    # read datasets into arrays
    lh_insert_datetime = np.array(lh_insert_datetime)
    lh_insert_datetime = lh_insert_datetime.astype('datetime64', copy=False)

    lh_temperature = np.array(lh_temperature)
    lh_temperature = np.reshape(lh_temperature, (-1,3))

    lh_df_1 = pd.DataFrame(lh_insert_datetime, columns=['insert_datetime'])
    lh_df_2 = pd.DataFrame(lh_temperature, columns=['temp billbrook', 'temp finkenwerder', 'temp marckmannstr'])

    lh_df = pd.concat([lh_df_1, lh_df_2], axis=1, join="inner")

    # visualize development of data storage by 'insert_datetime'
    lh_fig = px.line(lh_df, x='insert_datetime', y=['temp billbrook', 'temp finkenwerder', 'temp marckmannstr'],
                     title='Luft.Hamburg.de<br><sup>Temperature in °C</sup><br>')
    lh_fig.update_layout(title_x=0.5,
                         plot_bgcolor='#f6f6f6',
                         yaxis_title='temperature in °C',
                         xaxis_title='insert datetime',
                         legend_title_text="Weather Station")
    lh_fig.update_traces(line_width=3)
    # changing the label names
    names = ['Billbrook','Finkenwerder West', 'Marckmannstraße']
    for idx, name in enumerate(names):
        lh_fig.data[idx].name = name

    lh_fig.show()
