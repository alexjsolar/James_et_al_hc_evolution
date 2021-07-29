import numpy as np
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

#--------------
#Flux, critical height, and polarity separation vs time

harps = np.load('data/harps.npy', allow_pickle=True) #HARP numbers
times = np.load('data/times.npy', allow_pickle=True) #times for each HARP
fluxes = np.load('data/fluxes.npy', allow_pickle=True) #-ve, +ve, and us fluxes for each HARP
heights = np.load('data/heights.npy', allow_pickle=True) #critical heights for each HARP
seps = np.load('data/seps.npy', allow_pickle=True) #polarity separations for each HARP

harp = '3999'
h = np.where(harps==harp)[0][0] #get index of desired HARP
start_year = times[h][0].strftime('%Y') #year of first data point for chosen HARP

fluxes_h = [flux[2] for flux in fluxes[h]] #0 for -ve, 1 for +ve, 2 for unsigned
plt.plot(times[h], fluxes_h)
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
