"""
Plots fields from MITgcm dataset
multiple cross sections
"""
import os
import sys
sys.path.append('.././src')

import general.plotting as rfplt
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import intake

from general.constants_cloud import *

os.makedirs(figs_path, exist_ok=True)

def load_data(
):
    """Read in netcdf file and get shape
    """
    
    print('Reading in MITGCM dataset ...')

    cat = intake.open_catalog('.././data/inputs_paper.yml')

    da = cat.MITGCM_model.to_dask()

    dam = da['Ttave'].isel(T=slice(time, time + 2)).where(da['Mask'] == 1)

    print(f'Shape of dataset: {dam.shape}\n')

    return dam, da


def plot_depth_fields(
    select,
    min_value, 
    max_value, 
    x_label, 
    y_label, 
    lon_arange, 
    lat_arange,
    da_x, 
    da_y,
    name_o,
    lab,
    cmap,
    figs_path
):

    plt = rfplt.plot_parms()
    fig = plt.figure(figsize=(2.2, 2), dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    im = ax.pcolormesh(
        select, 
        vmin=min_value, 
        vmax=max_value, 
        edgecolors='face', 
        snap=True,
        cmap=cmap
    )
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xticks(lon_arange)
    ax.set_xticklabels(
        np.round(da_x.values[np.array(lon_arange).astype(int)], decimals=-1).astype(int)
    ) 
    ax.set_yticks(lat_arange)
    ax.set_yticklabels(
        np.round(da_y.values[np.array(lat_arange).astype(int)], decimals=-1).astype(int)
    ) 
    plt.text(-0.1, 0.86, lab, transform=fig.transFigure)
    plt.savefig(
        f"{figs_path}{name_o}", 
        format='png', 
        bbox_inches = 'tight', 
        pad_inches = 0.1
    )
    plt.show()
    return plt, im, ax
    
    
    
def plot_cross_sections(
    select,
    min_value, 
    max_value,
    lat_label,
    depth_label,
    lat_arange,
    depth_arange,
    da_y,
    da_z,
    name_o,
    lab,
    cmap,
    figs_path
):
    plt = rfplt.plot_parms()
    fig = plt.figure(figsize=(2.2, 2), dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    ax.pcolormesh(
        select,
        vmin=min_value, 
        vmax=max_value, 
        edgecolors='face', 
        snap=True,
        cmap=cmap
    )
    ax.invert_yaxis()
    ax.set_xlabel(lat_label)
    ax.set_ylabel(depth_label)
    ax.set_xticks(lat_arange)
    ax.set_xticklabels(
        np.round(da_y.values[np.array(lat_arange).astype(int)], decimals=-1).astype(int)
    ) 
    ax.set_yticks(depth_arange)
    ax.set_yticklabels(da_z.values[np.array(depth_arange)].astype(int))
    plt.text(-0.055, 0.86, lab, transform=fig.transFigure)
    plt.savefig(
        f"{figs_path}{name_o}", 
        format='png',
        bbox_inches = 'tight', 
        pad_inches = 0.1
    )
    plt.show()

    return plt


def ocean_dynamics_plots(
    figs_path
):
    
    print("================================================")

    print("\n LOADING MITGCM DATASET \n")

    print("================================================\n")
    
    dam, da = load_data()
    
    da_x, da_y, da_z = da['X'], da['Y'], da['Z']
    
    depth_arange = [0, 7, 15, 21, 28, 37, da_z.values.shape[0]-1]
    
    min_value = min(
        np.nanmin(dam[0:,:,x_coord]), 
        np.nanmin(dam[1:,:,x_coord]),
        np.nanmin(dam[0,level,:,:]),
        np.nanmin(dam[1,level,:,:]),
        np.nanmin(dam[0,:,y_coord,:]), 
        np.nanmin(dam[0,:,y_coord,:]) 
    )

    max_value = max( 
        np.nanmax(dam[0:,:,x_coord]), 
        np.amax(dam[1:,:,x_coord]),
        np.nanmax(dam[0,level,:,:]), 
        np.amax(dam[1,level,:,:]),
        np.nanmax(dam[0,:,y_coord,:]), 
        np.amax(dam[0,:,y_coord,:]) 
    )
    
    print("\n\n\n\n\n\n\n\n")
    
    print("================================================")

    print("\n 25 M BELOW THE SURFACE FOR ONE PARTICULAR DAY \n")

    print("================================================\n")
 
    print("Temperature (°C) at 25 m below the surface for one particular day.")
    
    plt, im, ax = plot_depth_fields(
        dam[0,level,:,:],
        min_value, 
        max_value, 
        lon_label, 
        lat_label, 
        lon_arange, 
        lat_arange,
        da_x, 
        da_y,
        "fig1a.png",
        "(a)",
        None,
        figs_path
    )

    fig = plt.figure( figsize=(5.5, .2), dpi=300 )
    cbaxes = fig.add_axes([0.05, 0.05, 0.9, 0.9 ]) 
    cb = plt.colorbar(im, ax=ax, orientation='horizontal', cax=cbaxes)
    cb.set_label(cbar_label)
    plt.savefig(f"{figs_path}fig1a_color.png", format='png', bbox_inches = 'tight', pad_inches = 0.1)
    plt.show()

    print("Change in temperature between over 1 day at 25 m below the surface.")

    plt, im, ax = plot_depth_fields(
        dam[0,level,:,:]-dam[1,level,:,:], 
        diff_min_value, 
        diff_max_value, 
        lon_label, 
        lat_label, 
        lon_arange, 
        lat_arange,
        da_x, 
        da_y,
        "fig1b.png",
        "(b)",
        'bwr',
        figs_path


    )

    fig = plt.figure(figsize=(5.5, .2), dpi=300 )
    cbaxes = fig.add_axes([0.05, 0.05, 0.9, 0.9 ]) 
    cb = plt.colorbar(im, ax=ax, orientation='horizontal', cax=cbaxes, extend='both')
    cb.set_label(cbar_diff_label)    
    cb.formatter.set_powerlimits((-2, 2))
    cb.update_ticks()
    plt.savefig(f"{figs_path}fig1b_color.png", format='png', bbox_inches = 'tight', pad_inches = 0.1)
    plt.show()

    print("Standard deviation in temperature at 25 m below the surface.")

    plt, im, ax = plot_depth_fields(
        np.std(dam[:,level,:,:], axis=0), 
        sd_min_value, 
        sd_max_value, 
        lon_label, 
        lat_label, 
        lon_arange, 
        lat_arange,
        da_x, 
        da_y,
        "fig1c.png",
        "(c)",
        None,
        figs_path


    )   
    fig = plt.figure(figsize=(5.5, .2), dpi=300)
    cbaxes = fig.add_axes([0.05, 0.05, 0.9, 0.9 ]) 
    cb = plt.colorbar(im, ax=ax, orientation='horizontal', cax=cbaxes, extend='both')
    cb.set_label(cbar_sd_label)    
    plt.savefig(f"{figs_path}fig1c_color.png", format='png', bbox_inches = 'tight', pad_inches = 0.1)
    plt.show()

    print("\n\n\n\n\n\n\n\n")
   
    print("================================================")

    print("\n 25 M BELOW THE SURFACE & AT at 13° E FOR ONE PARTICULAR DAY \n")

    print("================================================\n")
    
    print("Temperature (°C) at 25 m below the surface & at 13° E for one particular day.")

    plot_cross_sections(
        dam[0,:,:,x_coord],
        min_value, 
        max_value,
        lat_label,
        depth_label,
        lat_arange,
        depth_arange,
        da_y,
        da_z,
        "fig1d.png",
        "(d)",
        None,
        figs_path

    )
    
    print("Change in temperature between over 1 day in temperature at 25 m below the surface & at 13° E.")

    plot_cross_sections(
        dam[0,:,:,x_coord]-dam[1,:,:,x_coord],
        diff_min_value, 
        diff_max_value,
        lat_label,
        depth_label,
        lat_arange,
        depth_arange,
        da_y,
        da_z,
        "fig1e.png",
        "(e)",
        'bwr',
        figs_path

    )
    
    print("Standard deviation in temperature at 25 m below the surface & at 13° E.")

    plot_cross_sections(
        np.std(dam[:,:,:,x_coord], axis=0),
        sd_min_value, 
        sd_max_value,
        lat_label,
        depth_label,
        lat_arange,
        depth_arange,
        da_y,
        da_z,
        "fig1f.png",
        "(f)",
        None,
        figs_path

    )
    
    print("\n\n\n\n\n\n\n\n")
           
    print("================================================")

    print("\n  TIME SERIES AT 57° N, 17° E, and −25 m \n")

    print("================================================\n")
    
    daa = da.sel(X=17, Y=57, Z=-25, method='nearest')
    
    # Set figure's height and width
    fig = plt.figure()
    fig.set_figwidth(15)
    fig.set_figheight(2)
    
    # Plot the first 20 years
    daa['Ttave'].head(7200).plot()
    plt.xticks([])
    plt.xlabel("Years")
    plt.ylabel("Temp (°C)")
    plt.savefig(
        f"{figs_path}fig1g.png",
        bbox_inches = 'tight',
        pad_inches = 0.1,
        format='png'
    )
    plt.show()
    plt.close()

    print("\n\n\n\n\n\n\n\n")
       
    print("================================================")

    print("\n  TIME SERIES AT 55° S, 9° E, and −25 m \n")

    print("================================================\n")
    
    dab = da.sel(X=9, Y=-55, Z=-25, method='nearest')

    # Set figure's height and width
    fig = plt.figure()
    fig.set_figwidth(15)
    fig.set_figheight(2)
    
    # Plot the first 20 years
    dab['Ttave'].head(7200).plot()
    plt.xticks([])
    plt.xlabel("Years")
    plt.ylabel("Temp (°C)")
    plt.savefig(
        f"{figs_path}fig1i.png",
        bbox_inches = 'tight',
        pad_inches = 0.1,
        format='png'
    )
    plt.show()
    plt.close()


ocean_dynamics_plots(
    figs_path
)
