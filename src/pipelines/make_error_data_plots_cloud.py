import pickle
import os
import numpy as np
import sys
sys.path.append('.././src')
from general.constants_cloud import *
import plotting as rfplt
import xarray as xr
import time as tt
import matplotlib.pyplot as plt
import intake
import s3fs


def make_error_plots(mitgcm_filename, exp_name, cntrl_name, fig_prefix='fig'):
    #-------------------
    # Read in land mask 
    #-------------------
    mitgcm_ds = mitgcm_filename.to_dask()
    land_mask = mitgcm_ds['Mask']

    fs = s3fs.S3FileSystem(
        anon=True,
        client_kwargs={"endpoint_url": "https://pangeo-eosc-minioapi.vm.fedcloud.eu/"},
    )

    data_filename=pred_path+exp_name+'_AveragedSinglePredictions.nc'
    with fs.open(data_filename) as fileObj:
        ds = xr.open_dataset(fileObj, engine='h5netcdf')
        da_Av_AbsError=ds['Av_AbsErrors'].values

    cntrl_filename=pred_path+cntrl_name+'_AveragedSinglePredictions.nc'
    with fs.open(cntrl_filename) as fileObj:
        cntrl_ds = xr.open_dataset(fileObj, engine='h5netcdf')
        da_cntrl_Av_AbsError=cntrl_ds['Av_AbsErrors'].values

    #Plotting Cross-section at 13 degrees East
    point = [ 2, 8, 6]
    x_coord = point[2]

    # mask data
    Av_AbsError = np.where(land_mask==1, da_Av_AbsError, np.nan)
    Cntrl_Av_AbsError = np.where(land_mask==1, da_cntrl_Av_AbsError, np.nan)

    print("\n ================================================")
    print("\n Plotting the absolute error from predictions across the grid at 500 different times averaged to give a spatial pattern of errors. \n")
    print("================================================\n")

    
    fig, ax, im = rfplt.plot_xconst_crss_sec(Av_AbsError[:,:,:], 'Averaged Absolute Errors', x_coord,
                                         mitgcm_ds['X'].values, mitgcm_ds['Y'].values, mitgcm_ds['Z'].values,
                                         text='(a)', title=None, min_value=0.0, max_value=0.000306, cmap='Reds',
                                         cbar_label=cbar_label, Sci=True)
    fig.savefig(
        f"{figs_path}{fig_prefix}a_{exp_name}_coeffs.png",
        bbox_inches='tight',
        pad_inches=0.1,
        format='png'
    )
    plt.show()

    
    
    #Plot x cross section of difference between cntrl and exp
    print("\n ================================================")

    print("\n Plotting the difference between this and the control run, with areas shaded in red indicating where the error has increased as a consequence of withholding information about the vertical structure, and blue indicating areas where the predictions are improved. \n")

    print("================================================\n")

    
    fig, ax, im = rfplt.plot_xconst_crss_sec(
    Av_AbsError[:,:,:]-Cntrl_Av_AbsError, 
    'Diff in Averaged Absolute Errors with Control Run', 
    x_coord,
    mitgcm_ds['X'].values, mitgcm_ds['Y'].values, mitgcm_ds['Z'].values,
    text='(b)', title=None, min_value=None, max_value=None, diff=True,
    cbar_label=cbar_label, Sci=True)
    fig.savefig(
        f"{figs_path}{fig_prefix}b_{exp_name}_coeffs.png",
        bbox_inches='tight',
        pad_inches=0.1,
        format='png'
    )
    plt.show()
    
    
  