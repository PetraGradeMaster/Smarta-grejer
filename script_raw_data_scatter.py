import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

s = 1 # marker size

input_path = 'input/'
output_path = 'output/'
fig, ax = plt.subplots(figsize=(16,12), nrows=3)


# Plot aestethics
sns.set_theme(rc={
    'legend.markerscale': 5,
    'legend.fontsize': 6,
    'axes.grid': True,
    'grid.linestyle': '--',      # solid
    'grid.linewidth': 1.0,          # in points
    'grid.alpha':     0.1,     # transparency, between 0.0 and 1.0
    'grid.color': '#000000',
    })

for root, dirs, files in os.walk(top=input_path):
    for file in files:

        label = str(file)
        file_path = input_path+file
        df=pd.read_csv(file_path, delimiter=';', decimal=',', skiprows=20, names=['Time [s]', 'Fr', 'Fa', 'Ft'])
        df = df[df['Time [s]'] < 90]

        for column in df.columns:
            df[column] = df[column].astype('float64')


        # Section to calculate moving averages for the different forces
        forces = ['Ft', 'Fa', 'Fr']
        for i, force in enumerate(forces):
            sns.scatterplot(data=df, x='Time [s]', y=force, s=s, label=label, ax=ax[i], legend=True).set_ylabel(f'{force} [N]')


for ax in ax:
    ax.grid(alpha=0.2)

plt.tight_layout()
plt.savefig(f'{output_path}Raw_Scatter_Forces.png', dpi=150)




