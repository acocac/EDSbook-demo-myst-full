import pickle
import os
import AssessModel as am
import numpy as np
import sys

sys.path.append('.././src')
from general.constants_cloud import *
import glob as glob
import gzip
import s3fs


# define denormalising function
def denormalise_data(norm_data, mean, std):
    denorm_data = norm_data * std + mean
    return denorm_data


def make_scatter_plots(run_vars, data_name, model_name, norm_inputs_tr, norm_inputs_val, lim=None, plot_val=True, fig_prefix='fig'):
    fs = s3fs.S3FileSystem(
        anon=True,
        client_kwargs={"endpoint_url": "https://pangeo-eosc-minioapi.vm.fedcloud.eu/"},
    )

    lr = pickle.load(fs.open(mod_path + model_name + '_pickle.pkl'))

    # loading input arrays - These are the processed input vectors with all the
    # polynomial input features
    outputs_tr_DelT_filename = fs.open(data_interm_path + 'SinglePoint_' + data_name + '_OutputsDelTTr.npy')
    outputs_val_DelT_filename = fs.open(data_interm_path + 'SinglePoint_' + data_name + '_OutputsDelTVal.npy')
    outputs_te_DelT_filename = data_interm_path + 'SinglePoint_' + data_name + '_OutputsDelTTe.npy.gz'
    outputs_tr_Temp_filename = fs.open(data_interm_path + 'SinglePoint_' + data_name + '_OutputsTempTr.npy')
    outputs_val_Temp_filename = fs.open(data_interm_path + 'SinglePoint_' + data_name + '_OutputsTempVal.npy')

    if lim is not None:
        # Loading Output Arrays
        norm_outputs_tr_DelT = np.load(outputs_tr_DelT_filename)[:lim]
        norm_outputs_val_DelT = np.load(outputs_val_DelT_filename)[:lim]

        norm_outputs_tr_Temp = np.load(outputs_tr_Temp_filename)[:lim]
        norm_outputs_val_Temp = np.load(outputs_val_Temp_filename)[:lim]

    else:
        # Loading Output Arrays
        norm_outputs_tr_DelT = np.load(outputs_tr_DelT_filename)
        norm_outputs_val_DelT = np.load(outputs_val_DelT_filename)
        with fs.open(outputs_te_DelT_filename, 'rb') as f:
            g = gzip.GzipFile(fileobj=f)  # Decompress data with gzip
            norm_outputs_te_DelT = np.load(g)

        norm_outputs_tr_Temp = np.load(outputs_tr_Temp_filename)
        norm_outputs_val_Temp = np.load(outputs_val_Temp_filename)

    if run_vars['predict'] == 'DelT':
        norm_outputs_tr = norm_outputs_tr_DelT
        norm_outputs_val = norm_outputs_val_DelT

    elif run_vars['predict'] == 'Temp':
        norm_outputs_tr = norm_outputs_tr_Temp
        norm_outputs_val = norm_outputs_val_Temp

        # predict values
    print('predict values')
    norm_lr_predicted_tr = lr.predict(norm_inputs_tr).reshape(-1, 1).astype('float64')
    norm_lr_predicted_val = lr.predict(norm_inputs_val).reshape(-1, 1).astype('float64')

    # Read in mean and std
    mean_std_file = data_interm_path + 'SinglePoint_' + data_name + '_MeanStd.npz'
    zip_mean_std_file = mean_std_file + '.gz'
    if fs.exists(data_interm_path + 'SinglePoint_' + data_name + '_MeanStd.npz'):
        mean_std_data = np.load(fs.open(mean_std_file))
    elif os.path.isfile(zip_mean_std_file):
        os.system("gunzip %s" % (zip_mean_std_file))
        mean_std_data = np.load(mean_std_file)
        os.system("gunzip %s" % (mean_std_file))
    output_DelT_mean = mean_std_data['arr_2']
    output_DelT_std = mean_std_data['arr_3']
    output_Temp_mean = mean_std_data['arr_4']
    output_Temp_std = mean_std_data['arr_5']

    if run_vars['predict'] == 'DelT':
        output_mean = output_DelT_mean
        output_std = output_DelT_std
    elif run_vars['predict'] == 'Temp':
        output_mean = output_Temp_mean
        output_std = output_Temp_std

    # denormalise the predictions and true outputs
    denorm_lr_predicted_tr = denormalise_data(norm_lr_predicted_tr, output_mean, output_std)
    denorm_lr_predicted_val = denormalise_data(norm_lr_predicted_val, output_mean, output_std)
    denorm_outputs_tr = denormalise_data(norm_outputs_tr, output_mean, output_std)
    denorm_outputs_val = denormalise_data(norm_outputs_val, output_mean, output_std)

    # ------------------
    # Assess the model
    # ------------------
    # Calculate 'persistance' score - persistence prediction is just zero everywhere as we're predicting the trend
    top = max(max(denorm_outputs_tr), max(denorm_lr_predicted_tr), max(denorm_outputs_val),
              max(denorm_lr_predicted_val))
    top = top + 0.1 * abs(top)
    bottom = min(min(denorm_outputs_tr), min(denorm_lr_predicted_tr), min(denorm_outputs_val),
                 min(denorm_lr_predicted_val))
    bottom = bottom - 0.1 * abs(top)

    print("================================================")

    print("\n  Predictions against truth for Training datasets for the control regressor \n")

    print("================================================\n")
    am.plot_scatter(model_name, denorm_outputs_tr, denorm_lr_predicted_tr, name='train', top=top, bottom=bottom,
                    text='(a)', save=True, fig_prefix=f'{fig_prefix}a')

    if plot_val == True:
        print("================================================")

        print("\n  Predictions against truth for Validation datasets for the control regressor \n")

        print("================================================\n")
        am.plot_scatter(model_name, denorm_outputs_val, denorm_lr_predicted_val, name='Validation', top=top,
                        bottom=bottom, text='(b)', save=True, fig_prefix=f'{fig_prefix}b')