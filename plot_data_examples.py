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
id_hale = np.load('data/id_hale.npy', allow_pickle=True) #ID code of Hale classes in each HARP e.g. A (alpha), BG (beta-gamma), etc.
phase_durs = np.load('data/phase_durs.npy', allow_pickle=True).item() #total durations each phase type is observed for across all HARPs

#CMEs per phase type in simple, complex, and no class regions
phase_CMEs = {'II':[4,17,0],'DI':[3,3,0],'ID':[1,13,0],'DD':[2,8,0],'IF':[0,0,0],'DF':[0,0,0],
              'FI':[0,0,0],'FD':[0,0,0],'FF':[0,0,0],'All':[10,41,0],'NA':[0,0,0]}

print('All regions:')
for k, cmes in phase_CMEs.items():
    phases = phase_durs[k][0]
    durs = phase_durs[k][1:]
    durs_tot, cmes_tot = sum(durs,timedelta()).total_seconds()/(3600), sum(cmes)
    if durs_tot != 0.0:
        cme_rate = cmes_tot / (durs_tot/100)
        dur_avg = durs_tot/phases
    else:
        cme_rate = np.nan
        dur_avg = np.nan
    print(f'{k}: {phases} phases, {cmes_tot} CMEs, {durs_tot} hours = {cme_rate} CMEs per 100 hours, {dur_avg} hours per phase.')

#Rates of CMEs when flux is Increasing or Decreasing, and hc is Increasing or Decreasing
def cme_rate_combined (ids=['II','ID','IF']):
    dur_total = (sum(phase_durs[ids[0]][1:],timedelta())+sum(phase_durs[ids[1]][1:],timedelta())+sum(phase_durs[ids[2]][1:],timedelta())).total_seconds()/(3600)
    cmes_total = sum(phase_CMEs[ids[0]])+sum(phase_CMEs[ids[1]])+sum(phase_CMEs[ids[2]])
    cme_rate = cmes_total/(dur_total/100)
    return cme_rate
print(f"CME rate during increasing flux vs decreasing flux = {cme_rate_combined(['II','ID','IF'])} vs {cme_rate_combined(['DI','DD','DF'])}")
print(f"CME rate during increasing flux vs decreasing flux = {cme_rate_combined(['II','DI','FI'])} vs {cme_rate_combined(['ID','DD','FD'])}")

labels = ['Simple Regions:', 'Complex Regions:', 'No class Regions:']
for r, label in enumerate(labels):
    print(label)
    for k, cmes in phase_CMEs.items():
        dur = phase_durs[k][r+1].total_seconds()/3600
        cme = cmes[r]
        if dur != 0.0:
            cme_rate = cme / (dur/100)
        else:
            cme_rate = np.nan
        print(f'{k}: {cme} CMEs, {dur} hours = {cme_rate} CMEs per 100 hours')

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

harp = '3999' #specify which HARP to plot for
h = np.where(harps==harp)[0][0] #get index of desired HARP

fluxes_h = [flux[2] for flux in fluxes[h]] #0 for -ve, 1 for +ve, 2 for unsigned
cmap = cm.get_cmap('plasma') #for colouring phases
colours = {'II':[cmap(0.1)], 'DI':[cmap(0.4)], 'ID':[cmap(0.7)], 'DD':[cmap(1.0)],
           'IF':['black'], 'DF':['black'],'FI':['black'], 'FD':['black'], 'FF':['black'],'NA':['none']}
fig, ax1 = plt.subplots()
ax1.plot(times[h], fluxes_h, c='k')
[ax1.axvspan(t_phases[h][i], t_phases[h][i+1], alpha=0.2, color=colours[id_phases[h][i]][-1],zorder=-1,lw=0) for i in range(len(t_phases[h])-1)] #colour times of phases
for t_cme in t_cmes[h]:
    if t_cme!='': #if cme time is not blank i.e. there were CMEs
        ax1.axvline(datetime.strptime(t_cme,'%Y.%m.%dT%H:%M'), linestyle='-', color='k') #draw vertical lines at CME times
start_year = times[h][0].strftime('%Y') #year of first data point for chosen HARP
ax1.set_xlabel(f'Time ({start_year})')
ax1.set_ylabel('Magnetic Flux (Mx)')
ax1b = ax1.twinx()
ax1b.plot(times[h], heights[h], zorder=3, linestyle='dashed') #critical height vs time
ax1b.yaxis.set_label_position("right")
ax1b.yaxis.tick_right()
ax1b.set_ylabel('Critical Height (Mm)',color='C0')
plt.title(f'HARP {harps[h]}')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b')) #major ticks labelled day-month
plt.gca().xaxis.set_major_locator(mdates.DayLocator())  #major ticks at new days
plt.show()

fig, ax1 = plt.subplots()
ax1.plot(times[h], heights[h], linestyle='dashed') #critical height vs time
start_year = times[h][0].strftime('%Y') #year of first data point for chosen HARP
ax1.set_xlabel(f'Time ({start_year})')
ax1.set_ylabel('Critical Height (Mm)',color='C0')
ax1b = ax1.twinx()
ax1b.plot(times[h], seps[h], c='orange', linestyle='dotted') #half polarity separation vs time
ax1b.yaxis.set_label_position("right")
ax1b.yaxis.tick_right()
ax1b.set_ylabel(r'$\frac{1}{2}$ Polarity Separation (Mm)', color='orange')
sepmin, hmin = np.nanmin(seps[h]), np.nanmin(heights[h]) #minimum value between d and hc
sepmax, hmax = np.nanmax(seps[h]), np.nanmax(heights[h]) #maximum value between d and hc
ymin, ymax = np.nanmin([sepmin,hmin]), np.nanmax([sepmax,hmax]) #take min and max of separations and heights
ax1.set_ylim(ymin*0.95,ymax*1.05)  #y axes have same limits. add 5% whitespace
ax1b.set_ylim(ymin*0.95,ymax*1.05) #y axes have same limits. add 5% whitespace
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

bin_width = 10 #width of bins in Mm
bin_min, bin_max = round_down(min(cme_hc),bin_width), round_up(max(cme_hc),bin_width) #define bins from min/max of data and bin width
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
