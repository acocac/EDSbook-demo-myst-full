import sys
sys.path.append('.././src')
import numpy as np
import matplotlib.pyplot as plt
import general.CreateDataName as cn
import general.plotting as rfplt
import xarray as xr
import intake
import s3fs

from general.constants_cloud import *


def load_mitgcm_data():
    """Load original data"""

    cat = intake.open_catalog('.././data/inputs_paper.yml')

    ori = cat.MITGCM_model.to_dask()

    return ori


def mask_data(ds):
    """Land mask"""
    
    land_mask = ds['Mask']

    return land_mask


def get_exp_name(
    run_vars,
    data_prefix,
    exp_prefix ,
    model_prefix 
    
):
    data_name = f"{data_prefix}{cn.create_dataname(run_vars)}"
    model_name = f"{model_prefix}{data_name}"
    exp_name = f"{exp_prefix}{model_name}"
    
    return exp_name


def load_preds(
    pred_path, exp_nam
):
    fs = s3fs.S3FileSystem(
        anon=True,
        client_kwargs={"endpoint_url": "https://pangeo-eosc-minioapi.vm.fedcloud.eu/"},
    )

    filename = f'{pred_path}{exp_nam}_AveragedSinglePredictions.nc'
    preds = xr.open_dataset(fs.open(filename))
    
    return preds

   
def get_av_abs_error(
    pred_path, run_vars
):

    original = load_mitgcm_data()
    mask = mask_data(original)
    exp_nam = get_exp_name(
        run_vars,
        data_prefix,
        exp_prefix ,
        model_prefix 
    )
    preds = load_preds(
        pred_path, 
        exp_nam
    )

    da_Av_AbsError = preds['Av_AbsErrors']
    avg_err = np.where(mask==1, da_Av_AbsError, np.nan)

    return avg_err, preds, exp_nam


def graph_abs_error(
    avg_err,
    preds,
    cbar_label_err, 
    level,
    x_coord,
    exp_nam,
    figs_path
    
):
    fig, ax, im = rfplt.plot_depth_fld(
        avg_err[:,:,:], 
        'Averaged Absolute Errors', 
        level,
        preds['X'].values, 
        preds['Y'].values, 
        preds['Z'].values,
        text='(a)', 
        title=None, 
        min_value=0.0, 
        max_value=0.000306, 
        cmap='Reds',
        Sci=True
    )
    fig.savefig(
        f"{figs_path}fig3a_{exp_nam}_AvAbsErrors_z{str(level)}.png",
        bbox_inches = 'tight', 
        pad_inches = 0.1, 
        format='png'
    )
    plt.show()

    fig, ax, im = rfplt.plot_xconst_crss_sec(
        avg_err[:,:,:], 
        'Averaged Absolute Errors',
        x_coord,
        preds['X'].values, 
        preds['Y'].values, 
        preds['Z'].values,
        text='(b)', 
        title=None, 
        min_value=0.0, 
        max_value=0.000306, 
        cmap='Reds',
        cbar_label=cbar_label_err, 
        Sci=True
    )
    fig.savefig(
        f"{figs_path}fig3b_{exp_nam}_AvAbsErrors_x{str(x_coord)}.png",
        bbox_inches = 'tight', 
        pad_inches = 0.1, 
        format='png'
    )
    plt.show()

def main_pattern_errors(
    run_vars=run_vars,
    pred_path=pred_path,
    cbar_label_err=cbar_label_err,
    level=level,
    x_coord=x_coord,
    figs_path=figs_path,
):
    avg_err, preds, exp_nam = get_av_abs_error(
        pred_path, run_vars
    )
    
    graph_abs_error(
        avg_err,
        preds,
        cbar_label_err,
        level,
        x_coord,
        exp_nam,
        figs_path
    )
    
main_pattern_errors()