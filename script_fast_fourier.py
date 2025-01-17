import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import scipy.fft as spf
import numpy as np

s = 1 # marker size

input_path = 'input/'
output_path = 'output/'
fig, axes = plt.subplots(figsize=(16,9), nrows=3)

sns.set_theme(rc={
    'legend.markerscale': 5,
    'legend.fontsize': 6,
    })

for root, dirs, files in os.walk(top=input_path):
    for file in files:

        label = str(file)
        file_path = input_path+file
        df=pd.read_csv(file_path, delimiter=';', decimal=',', skiprows=20, names=['Time', 'Fr', 'Fa', 'Ft'])
        df = df[df['Time'] > 1]
        df = df[df['Time'] < 5]

        for column in df.columns:
            df[column] = df[column].astype('float64')

        df = df.reset_index()
        cut_off_low = 2
        cut_off_high = 150
        sr = 300
        N = len(df.index)
        n = np.arange(N)
        T = N/sr
        freq = n/T

        xf = spf.fftfreq(N, T)

        for i, force in enumerate(['Ft', 'Fa', 'Fr']):
            yf = df[force]
            yf = spf.fft(df[force])
            yf_filtered = yf
            yf_filtered[np.abs(freq) < cut_off_low] = 0
            yf_filtered[np.abs(freq) > cut_off_high] = 0

            axes[i].stem(freq, np.abs(yf_filtered), markerfmt=' ')
            axes[i].title.set_text(force)
            axes[i].set_xlabel('Frequency (Hz)')
            axes[i].set_xlim(cut_off_low, cut_off_high)



plt.tight_layout()
plt.savefig(f'{output_path}FFT_Forces.png', dpi=150)




