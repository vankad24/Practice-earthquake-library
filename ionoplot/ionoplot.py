import datetime
from collections import defaultdict
from datetime import (datetime)

import cartopy.crs as ccrs
import h5py
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from cartopy import feature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from dateutil import tz

from numpy import pi, sin, cos, arccos
from enum import Enum

# TECu - Total Electron Content Unit
# ROTI Maps
# tnpgn - Turkish National Permanent GNSS Network
# Global Navigation Satellite System (GNSS)
# DTEC (Differential Total Electron Content)
# VTEC (Vertical Total Electron Content)

"""# Define some constants"""
DEFAULT_PARAMS = {'font.size': 20,
                  'figure.dpi': 300,
                  'font.family': 'sans-serif',
                  'font.style': 'normal',
                  'font.weight': 'light',
                  'legend.frameon': True,
                  'font.variant' : 'small-caps',
                  'axes.titlesize' : 20,
                  'axes.labelsize' : 20,
                  'xtick.labelsize' : 18,
                  'xtick.major.pad': 5,
                  'ytick.major.pad': 5,
                  'xtick.major.width' : 2.5,
                  'ytick.major.width' : 2.5,
                  'xtick.minor.width' : 2.5,
                  'ytick.minor.width' : 2.5,
                  'ytick.labelsize' : 20}

TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
_UTC = tz.gettz('UTC')
RE_meters = 6371000

"""# Retrieve and plot methods"""

def _prepare_layout(ax,
                    lon_limits,
                    lat_limits):
    """Настраивает отображение"""
    plt.rcParams.update(DEFAULT_PARAMS)
    gl = ax.gridlines(linewidth=2, color='gray', alpha=0.5, draw_labels=True, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    ax.set_xlim(*lon_limits)
    ax.set_ylim(*lat_limits)
    #put some features on the map
    ax.add_feature(feature.COASTLINE, linewidth=2.5)
    ax.add_feature(feature.BORDERS, linestyle=':', linewidth=2)
    ax.add_feature(feature.LAKES, alpha=0.5)
    ax.add_feature(feature.RIVERS)

#Plot data for one time moment
def plot_map(plot_times, data, type_d,
             lon_limits=(-180, 180),
             lat_limits=(-90, 90),
             nrows=1,
             ncols=3,
             markers=[],
             sort=False,
             use_alpha=False,
             c_limits=None,
             save_path=None):
    """
    Plotting data
    input - <time> string type time from SIMuRG map file
            <lats> list of latitudes
            <lons> list of longitudes
            <values> list of values
            <type_d> string type of data going to be plotted
    output - figure
    """
    if not c_limits:
        c_limits = {
            'ROTI': [-0,0.5,'TECu/min'],
            '2-10 minute TEC variations': [-0.2,0.2,'TECu'],
            '10-20 minute TEC variations': [-0.4,0.4,'TECu'],
            '20-60 minute TEC variations': [-0.6,0.6,'TECu'],
            'tec': [0,50,'TECu/min'],
            'tec_adjusted': [0,50,'TECu'],
        }

    assert len(plot_times) == ncols
    if isinstance(type_d, list):
        assert len(type_d) == nrows
    else:
        type_d = [type_d]
    fig, axs = plt.subplots(nrows=nrows,ncols=ncols,
                            subplot_kw={'projection': ccrs.PlateCarree()},
                            figsize=(6.7*ncols, 5.5*nrows))
    if nrows * ncols > 1:
        axs=axs.flatten()
    else:
        axs=[axs]

    #fig = plt.figure(figsize=(20, 8))
    #ax1 = plt.axes(projection=ccrs.PlateCarree())

    for iprod in range(nrows):
        for itime in range(ncols):
            ax1 = axs[itime + ncols * iprod]
            time = plot_times[itime]
            prod = type_d[iprod]
            if sort:
                arr = np.sort(data[prod][time], order='vals')
            else:
                arr = data[prod][time]
            lats = arr['lat']
            lons = arr['lon']
            values = arr['vals']

            _prepare_layout(ax1, lon_limits, lat_limits)
            if use_alpha: #Использовать прозрачность у точек или нет
                m = max(np.max(values), -np.min(values))
                alphas = [(v+m/4)/(m+m/4) for v in values]
                alphas = [abs(a) for a in alphas]
            else:
                alphas = [1 for _ in values]

            sctr = ax1.scatter(lons, lats, c=values,
                               alpha = alphas,
                               marker = 's', s =15, zorder=3,
                               vmin = c_limits[prod][0],
                               vmax = c_limits[prod][1],
                               cmap = 'jet')
            for marker in markers: #расстановка звёздочек
                ax1.scatter(marker['lon'], marker['lat'],
                            marker='*', color="black", s=400,
                            zorder=5)
            if iprod == 0: #заголовок, если строк с картинками несколько
                ax1.set_title(time.strftime(TIME_FORMAT)[:-7]+'\n'+prod)
            else:
                ax1.set_title('\n'+prod)
            if itime % ncols == ncols - 1:
                cax = fig.add_axes([ax1.get_position().x1+0.01,
                                    ax1.get_position().y0,
                                    0.02,
                                    ax1.get_position().height])
                cbar = ax1.figure.colorbar(sctr, cax=cax) #color bar
                cbar_label = c_limits[prod][2] + "\n" if type_d == "ROTI" else c_limits[prod][2]
                cbar.ax.set_ylabel(cbar_label, rotation=-90, va="bottom")

            ax1.xaxis.set_ticks_position('none')

            if save_path:
                plt.savefig(save_path)

    if not save_path:
        plt.show()
    plt.close()
    plt.rcdefaults()


#Read data from h5 file to python dict
def retrieve_data(file, type_d, times=[]):
    """
    Plotting data from map file
    input - <file> string type name of file
            <type_d> string type of data going to be plotted
    output - figures
    """
    with h5py.File(file, 'r') as f_in:
        lats = []
        lons = []
        values = []
        data = {}
        for str_time in list(f_in['data'])[:]:
            time = datetime.strptime(str_time, TIME_FORMAT)
            time = time.replace(tzinfo=time.tzinfo or _UTC)
            if times and time not in times:
                continue
            data[time] = f_in['data'][str_time][:]
    return data

def retrieve_data_multiple_source(files, type_d, times=[]):
    datas = defaultdict(list)
    for file in files:
        file_data = retrieve_data(file, type_d, times=times)
        for time, data in file_data.items():
            datas[time].append(data)
    for time in datas:
        datas[time] = np.concatenate(datas[time])
    return datas



class MapType(Enum):
    ROTI = 'ROTI'
    TEC_2_10 = '2-10 minute TEC variations'
    TEC_10_20 = '10-20 minute TEC variations'
    TEC_20_60 = '20-60 minute TEC variations'
    TEC = 'tec'
    TEC_ADJUSTED = 'tec_adjusted'

# times - array with time need to be select from the files
# epicenter - dict with lat, lon
def plot_maps(files_path, map_type: MapType, times, epicenters, c_limits=None, scale=1, use_alpha=True, save_path=None):
    if not c_limits:
        c_limits={
            'ROTI': [0,0.5*scale,'TECu/min'],
            '2-10 minute TEC variations': [-0.4*scale,0.4*scale,'TECu'],
            '10-20 minute TEC variations': [-0.6*scale,0.6*scale,'TECu'],
            '20-60 minute TEC variations': [-1*scale,1*scale,'TECu'],
            'tec': [0,50*scale,'TECu/min'],
            'tec_adjusted': [0,50*scale,'TECu'],
        }
    type_d = map_type.value
    if not isinstance(files_path, list):
        files_path = [files_path]
    if not isinstance(epicenters, list):
        epicenters = [epicenters]

    times = [t.replace(tzinfo=t.tzinfo or _UTC) for t in times]

    data_from_files = retrieve_data_multiple_source(files_path, type_d, times)
    data = {type_d: data_from_files}
    plot_map(times, data, type_d,
             use_alpha=use_alpha,
             lat_limits=(25, 50),
             lon_limits=(25, 50),
             sort=True,
             markers=epicenters,
             c_limits=c_limits, save_path=save_path)

"""# Distance time"""

def get_dist_time(data, eq_location, direction='all'):
    x, y, c = [], [], []
    for time, map_data in data.items():
        lats = np.radians(map_data["lat"][:])
        lons = np.radians(map_data["lon"][:])
        vals = map_data["vals"][:]
        _eq_location = {}
        _eq_location["lat"] = np.radians(eq_location["lat"])
        _eq_location["lon"] = np.radians(eq_location["lon"])
        if direction == "all":
            inds = np.isreal(lats)
        elif direction == "north":
            inds = lats >= _eq_location["lat"]
        elif direction == "south":
            inds = lats <= _eq_location["lat"]
        elif direction == "east":
            inds = lats >= _eq_location["lon"]
        elif direction == "west":
            inds = lats <= _eq_location["lon"]
        else:
            inds = np.isreal(lats)
        lats = lats[inds]
        lons = lons[inds]
        vals = vals[inds]
        plats = np.zeros_like(lats)
        plons = np.zeros_like(lons)
        plats[:] = _eq_location["lat"]
        plons[:] = _eq_location["lon"]

        dists = great_circle_distance_numpy(lats,lons,
                                            plats, plons)


        x.extend([time] * len(vals))
        y.extend(dists / 1000)
        c.extend(vals)
    return x, y, c


def plot_distance_time(file_path, map_type: MapType, epicenter, sort = True, line=dict(), c_limits=None, dmax=1750, save_path=None):
    if not c_limits:
        c_limits = {
            'ROTI': [-0, 0.5, 'TECu/min\n'],
            '2-10 minute TEC variations': [-0.6, 0.6, 'TECu'],
            '10-20 minute TEC variations': [-0.8, 0.8, 'TECu'],
            '20-60 minute TEC variations': [-1.0, 1.0, 'TECu'],
            'tec': [0, 50, 'TECu/min'],
            'tec_adjusted': [0, 50, 'TECu'],
        }

    ptype = map_type.value
    data = retrieve_data(file_path, ptype)
    x, y, c = get_dist_time(data, epicenter)

    c_abs = [abs(_c) for _c in c]
    if sort:
        x = [i for _, i in sorted(zip(c_abs, x))]
        y = [i for _, i in sorted(zip(c_abs, y))]
        c = [i for _, i in sorted(zip(c_abs, c))]

    times = [t for t in data]
    times.sort()
    plt.figure(figsize=(18, 5))
    plt.rcParams.update(DEFAULT_PARAMS)
    plot_ax = plt.axes()
    plt.scatter(x, y, c=c, cmap='jet')
    cbar = plt.colorbar()
    plt.clim(c_limits[ptype][0], c_limits[ptype][1])
    plt.ylabel('Distance, km')

    dt_utc = times[-1].astimezone()
    formatted_string = dt_utc.strftime("UTC for %B %d, %Y") #'UTC for February 6, 2023'
    plt.title(formatted_string)

    plt.xlim(times[0], times[-1])
    plt.ylim(0, dmax)
    # plot vertical lines for earthquake times
    plt.axvline(x=epicenter['time'], color='black', linewidth=3)
    cbar.ax.set_ylabel(c_limits[ptype][2], rotation=-90, va="bottom")
    plot_ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()


def great_circle_distance_numpy(late, lone, latp, lonp, R=RE_meters):
    """
    Calculates arc length. Uses numpy arrays
    late, latp: double
        latitude in radians
    lone, lonp: double
        longitudes in radians
    R: double
        radius
    """
    lone[np.where(lone < 0)] = lone[np.where(lone < 0)] + 2*pi
    lonp[np.where(lonp < 0)] = lonp[np.where(lonp < 0)] + 2*pi
    dlon = lonp - lone
    inds = np.where((dlon > 0) & (dlon > pi))
    dlon[inds] = 2 * pi - dlon[inds]
    dlon[np.where((dlon < 0) & (dlon < -pi))] += 2 * pi
    dlon[np.where((dlon < 0) & (dlon < -pi))] = -dlon[np.where((dlon < 0) & (dlon < -pi))]
    cosgamma = sin(late) * sin(latp) + cos(late) * cos(latp) * cos(dlon)
    return R * arccos(cosgamma)