import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from matplotlib.patches import Patch



def color(row):
    c_dict = {'waiting_time':'#E64646', 'processing_time':'#E69646', 'queuing_time':'#34D05C'}
    return c_dict[row['legend']]


def visu_calender(N,a,d,q,schedule) :
    '''
    input : N,a,d,q  --> data of the problem
            schedule --> a schedule

    output : matplotlib fig --> use of the function barh
    '''

    # N,a,d,q = instance_creation(N,a,d,q)


    # creation of a dataframe
    df = {'task' : [] , 'start_time' : [] , 'end_time' : [] , 'legend' : []}
    curr_time = 0

    for i in range(len(N)) :
        curr_task = schedule[i]
        curr_name = "Job "+str(curr_task)
        


        # waiting period
        df['task'].append(curr_name)
        df['legend'].append("waiting_time")
        df['start_time'].append(0)
        df['end_time'].append(a[curr_task])

        curr_time = max(curr_time , a[curr_task])

        # processing period
        df['task'].append(curr_name)
        df['legend'].append('processing_time')
        df['start_time'].append(curr_time)
        df['end_time'].append(curr_time+d[curr_task])

        


        # queuing period
        df['task'].append(curr_name)
        df['legend'].append('queuing_time')
        df['start_time'].append(curr_time+d[curr_task])
        df['end_time'].append(curr_time+d[curr_task]+q[curr_task])

        curr_time += d[curr_task]

    
    df = pd.DataFrame(df)
    df['color'] = df.apply(color, axis=1)


    # graphic part

    fig, (ax, ax1) = plt.subplots(2, figsize=(16,6), gridspec_kw={'height_ratios':[6, 1]}, facecolor='#36454F')
    ax.set_facecolor('#36454F')
    ax1.set_facecolor('#36454F')


    ax.barh(df.task, df['end_time'] - df['start_time'], left=df.start_time, color=df.color)
    ax.xaxis.grid(color='k', linestyle='dashed', alpha=1, which='both')
    
    ax.set_axisbelow(True)
    ax.xaxis.grid(color='k', linestyle='dashed', alpha=0.4, which='both')

    plt.setp([ax.get_xticklines()], color='w')

    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['left'].set_position(('outward', 10))
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_color('w')

    

    ##### LEGENDS #####
    c_dict = {'waiting_time':'#E64646', 'processing_time':'#E69646', 'queuing_time':'#34D05C'}

    legend_elements = [Patch(facecolor=c_dict[i], label=i)  for i in c_dict]
    legend = ax1.legend(handles=legend_elements, loc='upper center', ncol=5, frameon=False)
    plt.setp(legend.get_texts(), color='w')

    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.set_xticks([])
    ax1.set_yticks([])

    return fig



if __name__ == "__main__" :
    pass