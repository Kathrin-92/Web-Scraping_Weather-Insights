import parse_wetterdienst as wd
import parse_wetteronline as wo
import parse_lufthamburg as lh
import h5py
import numpy as np
import os
import logging

# creating log file
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path, 'scrapes-log.log')

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(filename)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)


try:
    # write new hdf5 file and load with data
    filename_hdf = os.path.join(dir_path, 'weather_data.h5')
    with h5py.File(filename_hdf, 'w-') as hdf:

        dt = h5py.special_dtype(vlen=str)

        ### WETTERDIENST.DE
        # create group
        grp_wd = hdf.create_group("wetterdienst.de")

        # set attributes/metadata for group
        grp_wd.attrs['SOURCE'] = 'Data collected from the website: ' \
                                 'https://www.wetterdienst.de/Deutschlandwetter/Hamburg/Aktuell/ '
        grp_wd.attrs['DATA COLLECTION'] = 'Data collected through web scraping from Dec 12, 2022 to Dec 13, 2022. ' \
                                          'The data were retrieved every hour, always on the hour. '

        # create datasets
        wd_datetime = np.array([wd.insert_datetime], dtype=dt)
        weather = np.array([wd.weather_container], dtype=dt)

        wd_insert_datetime = grp_wd.create_dataset("insert_datetime", (1,), data=wd_datetime, maxshape=(None,))
        wd_weather = grp_wd.create_dataset("weather", (1,), data=weather, maxshape=(None,))
        wd_temperature = grp_wd.create_dataset("temperature", (1,), data=wd.temp_container, maxshape=(None, ))
        wd_rainfall = grp_wd.create_dataset("rainfall", (1,), data=wd.rainfall_container, maxshape=(None,))

        # set attributes/metadata to datasets
        wd_temperature.attrs['COLUMN NAME'] = 'temperature'
        wd_temperature.attrs['UNIT OF MEASUREMENT'] = '°C'
        wd_temperature.attrs['DATATYPE'] = 'float'

        wd_rainfall.attrs['COLUMN NAME'] = 'amount of rainfall'
        wd_rainfall.attrs['UNIT OF MEASUREMENT'] = 'mm'
        wd_rainfall.attrs['DATATYPE'] = 'float'

        wd_weather.attrs['COLUMN NAME'] = 'weather description'
        wd_weather.attrs['UNIT OF MEASUREMENT'] = 'description of weather condition in text format'
        wd_weather.attrs['DATATYPE'] = 'str'

        wd_insert_datetime.attrs['COLUMN NAME'] = 'datetime of insert'
        wd_insert_datetime.attrs['UNIT OF MEASUREMENT'] = 'datetime in format ("%Y-%m-%d %H:%M:%S")'
        wd_insert_datetime.attrs['DATATYPE'] = 'str'


        ### WETTERONLINE.DE
        # create group
        grp_wo = hdf.create_group("wetteronline.de")

        # set attributes/metadata for group
        grp_wo.attrs['SOURCE'] = 'Data on temperature was collected from the website: ' \
                                 'https://www.wetteronline.de/wetter/hamburg '
        grp_wo.attrs['DATA COLLECTION'] = 'Data collected through web scraping from Dec 12, 2022 to Dec 13, 2022. ' \
                                          'The data were retrieved every hour, always on the hour. '

        # create datasets for groups
        wo_datetime = np.array([wo.insert_datetime], dtype=dt)
        wo_insert_datetime = grp_wo.create_dataset("insert_datetime", (1,), data=wo_datetime, maxshape=(None,))
        wo_temperature = grp_wo.create_dataset("temperature", (1,), data=wo.temp_container, maxshape=(None,))

        # set attributes/metadata to datasets
        wo_temperature.attrs['COLUMN NAMES'] = 'temperature'
        wo_temperature.attrs['UNITS OF MEASUREMENT'] = 'temperature: °C'
        wo_temperature.attrs['DATATYPE'] = 'float'

        wo_insert_datetime.attrs['COLUMN NAME'] = 'datetime of insert'
        wo_insert_datetime.attrs['UNIT OF MEASUREMENT'] = 'datetime in format ("%Y-%m-%d %H:%M:%S")'
        wo_insert_datetime.attrs['DATATYPE'] = 'str'


        ### LUFT.HAMBURG.DE
        # create group
        grp_lh = hdf.create_group("luft.hamburg.de")

        # set attributes/metadata for group
        grp_lh.attrs['SOURCE'] = 'Data on temperature was collected from the website: ' \
                                 'https://luft.hamburg.de/clp/meteorologie/clp1/meteorology/tmp ' \
                                 'Temperature data refer to three Hamburg weather stations: Billbrook, ' \
                                 'Finkenwerder-West and Marckmannstrasse '
        grp_lh.attrs['DATA COLLECTION'] = 'Data collected through web scraping from Dec 12, 2022 to Dec 13, 2022. ' \
                                          'The data were retrieved every hour, always on the hour. '

        # create datasets for groups
        lh_datetime = np.array([lh.insert_datetime], dtype=dt)
        lh_insert_datetime = grp_lh.create_dataset("insert_datetime", (1,), data=lh_datetime, maxshape=(None,))
        lh_temperature = grp_lh.create_dataset("temperature", (3,), data=lh.data_luft_hamburg, maxshape=(None,))

        # set attributes/metadata to datasets
        lh_temperature.attrs['COLUMN NAMES'] = 'temperature billbrook; temperature finkenwerder-west; temperature marckmannstraße'
        lh_temperature.attrs['UNITS OF MEASUREMENT'] = 'temperature is measured in °C'
        lh_temperature.attrs['DATATYPE'] = 'float'

        lh_insert_datetime.attrs['COLUMN NAME'] = 'datetime of insert'
        lh_insert_datetime.attrs['UNIT OF MEASUREMENT'] = 'datetime in format ("%Y-%m-%d %H:%M:%S")'
        lh_insert_datetime.attrs['DATATYPE'] = 'str'

except FileExistsError:
    filename_hdf = os.path.join(dir_path, 'weather_data.h5')
    with h5py.File(filename_hdf, 'a') as hdf:
        dt = h5py.special_dtype(vlen=str)

        ### WETTERDIENST.de
        # get datasets
        wd_temperature = hdf.get("wetterdienst.de/temperature")
        wd_rainfall = hdf.get("wetterdienst.de/rainfall")
        wd_insert_datetime = hdf.get("wetterdienst.de/insert_datetime")
        wd_weather = hdf.get("wetterdienst.de/weather")

        # add new values to datasets
        wd_datetime = np.array([wd.insert_datetime], dtype=dt)
        weather = np.array([wd.weather_container], dtype=dt)

        wd_insert_datetime.resize(wd_insert_datetime.shape[0] + 1, axis=0)
        wd_insert_datetime[-1:,] = wd_datetime

        wd_weather.resize(wd_weather.shape[0] + 1, axis=0)
        wd_weather[-1:,] = weather

        wd_temperature.resize(wd_temperature.shape[0] + 1, axis=0)
        wd_temperature[-1:,] = wd.temp_container

        wd_rainfall.resize(wd_rainfall.shape[0] + 1, axis=0)
        wd_rainfall[-1:,] = wd.rainfall_container

        ### WETTERONLINE.de
        # get datasets
        wo_temperature = hdf.get("wetteronline.de/temperature")
        wo_insert_datetime = hdf.get("wetteronline.de/insert_datetime")

        # add new values to datasets
        wo_datetime = np.array([wo.insert_datetime], dtype=dt)

        wo_insert_datetime.resize(wo_insert_datetime.shape[0] + 1, axis=0)
        wo_insert_datetime[-1:,] = wo_datetime

        wo_temperature.resize(wo_temperature.shape[0] + 1, axis=0)
        wo_temperature[-1:,] = wo.temp_container

        ### LUFT.HAMBURG.DE
        # get datasets
        lh_temperature = hdf.get("luft.hamburg.de/temperature")
        lh_insert_datetime = hdf.get("luft.hamburg.de/insert_datetime")

        # add new values to datasets
        lh_datetime = np.array([lh.insert_datetime], dtype=dt)

        lh_insert_datetime.resize(lh_insert_datetime.shape[0] + 1, axis=0)
        lh_insert_datetime[-1:,] = lh_datetime

        lh_temperature.resize(lh_temperature.shape[0] + 3, axis=0)
        lh_temperature[-3:,] = lh.data_luft_hamburg


logger.info("Data successfully fetched")

