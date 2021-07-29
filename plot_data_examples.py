import numpy as np
from datetime import timedelta
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from datetime import datetime
import matplotlib.dates as mdates

#--------------

harps = np.load('data/harps.npy', allow_pickle=True) #HARP numbers
t_phases = np.load('data/t_phases.npy', allow_pickle=True) #boundary times of phases in each HARP
id_phases = np.load('data/id_phases.npy', allow_pickle=True) #ID code of phases in each HARP e.g. II, ID, DD, etc.
id_hale = np.load('data/id_hale.npy', allow_pickle=True) #

#For each type of phase, we will count the number of phases, and their durations seen in simple, complex, and N/A Hale class regions
phase_durs_all = {'II':[0,timedelta(hours=0),timedelta(hours=0),timedelta(hours=0)],
                  'DI':[0,timedelta(hours=0),timedelta(hours=0),timedelta(hours=0)],
                  'ID':[0,timedelta(hours=0),timedelta(hours=0),timedelta(hours=0)],
                  'DD':[0,timedelta(hours=0),timedelta(hours=0),timedelta(hours=0)],
                  'IF':[0,timedelta(hours=0),timedelta(hours=0),timedelta(hours=0)],
                  'DF':[0,timedelta(hours=0),timedelta(hours=0),timedelta(hours=0)],
                  'FI':[0,timedelta(hours=0),timedelta(hours=0),timedelta(hours=0)],
                  'FD':[0,timedelta(hours=0),timedelta(hours=0),timedelta(hours=0)],
                  'FF':[0,timedelta(hours=0),timedelta(hours=0),timedelta(hours=0)],
                  'NA':[0,timedelta(hours=0),timedelta(hours=0),timedelta(hours=0)],
                  'All':[0,timedelta(hours=0),timedelta(hours=0),timedelta(hours=0)]}

#Loop over the HARPs and total up the phase information
for h, harp in enumerate(harps):
    durs = [t_phases[h][i+1]-t_phases[h][i] for i in range(len(t_phases[h])-1)] #durations of each phase in each HARP

    for i, id in enumerate(id_phases[h]): #for each phase:
        if i==0 or (i>0 and id != id_phases[i-1]): #count number of phases. Take the first and then increase the count when subsequent phase IDs don't match
            phase_durs_all[id][0] += 1
            phase_durs_all['All'][0] += 1
        if id_hale[h][i] == 'A' or id_hale[h][i] == 'B': #simple region: alpha or beta
            phase_durs_all[id][1] += durs[i]
            phase_durs_all['All'][1] += durs[i]
        elif 'G' in id_hale[h][i] or 'D' in id_hale[h][i]: #complex region: gamma or delta
            phase_durs_all[id][2] += durs[i]
            phase_durs_all['All'][2] += durs[i]
        else:                                           #other e.g. no class
            phase_durs_all[id][3] += durs[i]
            phase_durs_all['All'][3] += durs[i]

print('Phase Type, Number of Phases, Duration in Simple Regions (Hours), Duration in Complex Regions (Hours), Duration Regions with no Hale class (Hours)')
for k, v in phase_durs_all.items():
    print(k, v[0], (v[1]).total_seconds()/3600, (v[2]).total_seconds()/3600, (v[3]).total_seconds()/3600)
print('Note: I do not include "NA" data in the paper. These correspond to data gaps.')

#--------------
#Flux, critical height, and polarity separation vs time

harps = np.load('data/harps.npy', allow_pickle=True) #HARP numbers
times = np.load('data/times.npy', allow_pickle=True) #times for each HARP
fluxes = np.load('data/fluxes.npy', allow_pickle=True) #-ve, +ve, and us fluxes for each HARP
heights = np.load('data/heights.npy', allow_pickle=True) #critical heights for each HARP
seps = np.load('data/seps.npy', allow_pickle=True) #polarity separations for each HARP
t_cmes = np.load('data/t_cmes.npy', allow_pickle=True) #times of CMEs in each HARP
t_phases = np.load('data/t_phases.npy', allow_pickle=True) #boundary times of phases in each HARP
id_phases = np.load('data/id_phases.npy', allow_pickle=True) #ID code of phases in each HARP e.g. II, ID, DD, etc.

harp = '3999'
h = np.where(harps==harp)[0][0] #get index of desired HARP
start_year = times[h][0].strftime('%Y') #year of first data point for chosen HARP

fluxes_h = [flux[2] for flux in fluxes[h]] #0 for -ve, 1 for +ve, 2 for unsigned
cmap = cm.get_cmap('plasma') #for colouring phases
colours = {'II':[cmap(0.1)], 'DI':[cmap(0.5)], 'ID':[cmap(0.8)], 'DD':['black'],
           'IF':['none'], 'DF':['none'],'FI':['none'], 'FD':['none'], 'FF':['none'],'NA':['none']}
#
fig, ax = plt.subplots()
ax.plot(times[h], fluxes_h)
[ax.axvspan(t_phases[h][i], t_phases[h][i+1], alpha=0.2, color=colours[id_phases[h][i]][-1],zorder=-1,lw=0) for i in range(len(t_phases[h])-1)] #colour times of phases
for t_cme in t_cmes[h]:
    if t_cme!='': #if cme time is not blank i.e. there were CMEs
        ax.axvline(datetime.strptime(t_cme,'%Y.%m.%dT%H:%M'), linestyle='-', color='k') #draw vertical lines at CME times
plt.xlabel(f'Time ({start_year})')
plt.ylabel('Magnetic Flux (Mm)')
plt.title(f'HARP {harps[h]}')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b')) #major ticks labelled day-month
plt.gca().xaxis.set_major_locator(mdates.DayLocator())  #major ticks at new days
plt.show()

plt.plot(times[h], heights[h])
plt.xlabel(f'Time ({start_year})')
plt.ylabel('Critical Height (Mm)')
plt.title(f'HARP {harps[h]}')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b')) #major ticks labelled day-month
plt.gca().xaxis.set_major_locator(mdates.DayLocator())  #major ticks at new days
plt.show()

plt.plot(times[h], seps[h])
plt.xlabel(f'Time ({start_year})')
plt.ylabel('Polarity Separation (Mm)')
plt.title(f'HARP {harps[h]}')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b')) #major ticks labelled day-month
plt.gca().xaxis.set_major_locator(mdates.DayLocator())  #major ticks at new days
plt.show()

#--------------
#Histogram of critical heights at CME onset

cme_hc = np.load('data/cme_hc.npy', allow_pickle=True) #polarity separations for each HARP

def round_down(num, divisor):
    return num - (num%divisor)
def round_up(num, divisor):
    return num + (divisor-(num%divisor))

bin_width = 10
bin_min, bin_max = round_down(min(cme_hc),bin_width), round_up(max(cme_hc),bin_width)
bins = np.arange(bin_min,bin_max+bin_width, bin_width)
hist = plt.hist(cme_hc, bins, histtype='bar', rwidth=0.8)
plt.xticks(bins)
plt.xlabel('Critical Height (Mm)')
plt.ylabel('Number of CMEs')
plt.title('Critical Height at CME Onset')
plt.show()

#--------------
#Mean critical height vs polarity separation

hc_means = np.load('data/mean_hc.npy', allow_pickle=True) #mean critical height for each HARP
sep_means = np.load('data/mean_sep.npy', allow_pickle=True) #mean polarity separation for each HARP
bipolar = np.load('data/bipolar.npy', allow_pickle=True) #indices of bipolar HARPs
multipolar = np.load('data/multipolar.npy', allow_pickle=True) #indices of multipolar HARPs

x_bp, y_bp = [sep_means[i]*2 for i in bipolar], [hc_means[i] for i in bipolar] #data for x and y axes in bipolar HARPs
x_mp, y_mp = [sep_means[i]*2 for i in multipolar], [hc_means[i] for i in multipolar] #data for x and y axes in multipolar HARPs
x_all, y_all = [sep_mean*2 for sep_mean in sep_means], [hc_mean for hc_mean in hc_means] #data for x and y axes in all HARPs

fig, ax = plt.subplots()
ax.scatter(x_bp, y_bp, c='b', marker='o')
ax.scatter(x_mp, y_mp, c='r', marker='x')
#
p_bp, V_bp = np.polyfit(x_bp, y_bp, 1, cov=True) #linear fit to bipolar HARP data
err_bp = [np.sqrt(V_bp[0][0]), np.sqrt(V_bp[1][1])] #error in slope and offset
fit_slope_bp = f'slope = {round(p_bp[0],2):.2f} $\pm$ {round(err_bp[0],2):.2f}' #slope and error
ax.plot(np.unique(x_bp), np.poly1d(np.polyfit(x_bp, y_bp, 1))(np.unique(x_bp)), c='k', label=fit_slope_bp) #plot fit
#
p_all, V_all = np.polyfit(x_all, y_all, 1, cov=True) #linear fit to all HARP data
err_all = [np.sqrt(V_all[0][0]), np.sqrt(V_all[1][1])] #error in slope and offset
fit_slope_all = f'slope = {round(p_all[0],2):.2f} $\pm$ {round(err_all[0],2):.2f}' #slope and error
ax.plot(np.unique(x_all), np.poly1d(np.polyfit(x_all, y_all, 1))(np.unique(x_all)), c='k', linestyle='--', label=fit_slope_all) #plot fit
#
ax.set_xlabel('d (Mm)')
ax.set_ylabel('$\mathdefault{h_c}$ (Mm)')
ax.legend()
plt.show()
print(f'{fit_slope_bp}, offset = {round(p_bp[1],2)} $\pm$ {round(err_bp[1],2)}') #slope and error, y-offset and error
print(f'{fit_slope_all}, offset = {round(p_all[1],2)} $\pm$ {round(err_all[1],2)}') #slope and error, y-offset and error
