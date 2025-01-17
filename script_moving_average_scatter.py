import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import configparser




# Configure the variables for time in the graphs
config = configparser.ConfigParser()
config.read('config.ini')
time_criteria_begin = config.getint('section_time_parameters', 'time_criteria_begin')
time_criteria_end = config.getint('section_time_parameters', 'time_criteria_end')
ma_window = config.getint('section_time_parameters',  'ma_window')
Y_lim_Std = config.getint('section_time_parameters', 'Y_lim_Std')
Y_max_Std = config.getint('section_time_parameters', 'Y_max_Std')

t= config.getint('section_time_parameters', 't')

Y_lim_Ft= config.getint('section_time_parameters', 'Y_lim_Ft')
Y_max_Ft= config.getint('section_time_parameters', 'Y_max_Ft')+t

Y_lim_Fa= config.getint('section_time_parameters', 'Y_lim_Fa')
Y_max_Fa= config.getint('section_time_parameters', 'Y_max_Fa')+t

Y_lim_Fr= config.getint('section_time_parameters', 'Y_lim_Fr')
Y_max_Fr= config.getint('section_time_parameters', 'Y_max_Fr')+t


s = 1 # marker size
#ma_window = 50 # Timeframe for moving average, last number of datapoints
input_path = 'input/'
output_path = 'output/'
n_rows = 3
n_cols = 2

custom_palette = sns.color_palette('Paired', 8)
substrates = ['361', '362', '363', '364_', '364A', '366', '364B723A', '364B723B']
Edges = ['E1', 'E2', 'E3', 'E4', 'E5']
colors_dict = {
'366': custom_palette[0],
'361': custom_palette[1],
'362': custom_palette[2],
'363': custom_palette[3],
'364A': custom_palette[4],
'364_': custom_palette[5],
'364B723A': custom_palette[6],
'364B723B': custom_palette[7]
}



# Loop through files in input folder
for root, dirs, files in os.walk(top=input_path):
    
    

    
    fig, axes = plt.subplots(figsize=(16,9), nrows=n_rows, ncols=n_cols)


#
    # Plot aestethics
    #sns.set_style('white')
    sns.set_theme(rc={
        'figure.facecolor': 'white',
        'grid.color': '#000000',
        'legend.markerscale': 5,
        'legend.fontsize': 6,
        'axes.grid': True,
        'grid.linestyle': '--',      # solid
        'grid.linewidth': 1.0,          # in points
        'grid.alpha':     0.1,     # transparency, between 0.0 and 1.0
        })
   
    #Går igenom alla mappar från /input-mappen
    for file in files:
        label = str(file)
        print(label)
        file_path = str(root + '/' + file)
        df=pd.read_csv(file_path, delimiter=';', decimal=',', skiprows=20, names=['Time [s]', 'Fr', 'Fa', 'Ft'])
        df = df[df['Time [s]'] < 60]
        # Make sure data is in correct format
        for column in df.columns:
            df[column] = df[column].astype('float64')

        # Section to calculate moving averages for the different forces
        forces = ['Ft', 'Fa', 'Fr']
        for i, force in enumerate(forces):
            df[f'MA_{force}'] = abs(df[force].rolling(window=ma_window).mean())
            df[f'MAStd_{force}'] = df[force].rolling(window=ma_window).std()

            for substrate in substrates:
                if substrate in label:
                    sns.scatterplot(data=df, x='Time [s]', y=f'MA_{force}', s=s, label=label, ax=axes[i, 0], legend=True, color=colors_dict[substrate]).set_ylabel(f'{force} [N]')
                    sns.scatterplot(data=df[(df['Time [s]'] > time_criteria_begin) & (df['Time [s]'] < time_criteria_end)], x='Time [s]', y=f'MAStd_{force}', s=s, label=label, ax=axes[i, 1], legend=True, color=colors_dict[substrate]).set_ylabel(f'Std.dev. of {force} [N]')
        
 

            
            
            
            

    # Definierar axlarna och att ett grid behövs i plotten
    for j in range(n_cols):
        for i in range(n_rows):
            axes[i, j].grid(alpha=0.2)
            axes[i, 1].set_ylim(Y_lim_Std,Y_max_Std)
        axes[0, 0].set_ylim(Y_lim_Ft,Y_max_Ft)
        axes[1, 0].set_ylim(Y_lim_Fa,Y_max_Fa)
        axes[2, 0].set_ylim(Y_lim_Fr,Y_max_Fr)
        
        
    subfolder = root.replace('input/', '')
    plt.suptitle(subfolder)
    plt.tight_layout()
    plt.savefig(f'{output_path}Moving_average_'+subfolder+'.png', dpi=150)
    plt.clf()
    
        
        

        #plt.savefig(f'{output_path},name= subfolder, dpi=150)

        #plt.savefig(f'{output_path}Moving_Average_Forces.png', dpi=150)
