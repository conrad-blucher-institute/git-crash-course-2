import pandas as pd
import numpy as np

df = pd.read_csv('https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=RAS&data=all&year1=2020&month1=1&day1=1&year2=2020&month2=2&day2=4&tz=Etc%2FUTC&format=onlycomma&latlon=no&elev=no&missing=empty&trace=0.0001&direct=no&report_type=3')

df_sample = df[df['valid'].str.contains('2020-01')].set_index('valid')
df_sample['pitches'] = (df_sample['drct']/2).apply(np.deg2rad).apply(np.sin).apply(np.arcsin).apply(np.rad2deg)/90*600+200
df_sample.index = pd.to_datetime(df_sample.index)
df_sample = df_sample.resample('5min').ffill().rolling('4h').mean(True)

durations = (1/(1+df_sample['sknt'])*100).apply(int)+1

audio_data = (durations.apply(np.arange).explode()/durations*df_sample['pitches']*2*np.pi).values

print(audio_data)