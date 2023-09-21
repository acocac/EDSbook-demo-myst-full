# Script written by Rachel Furner
# Plots the coefficients from linear regression model (which were
# outputted as an array into an npz file, which is read in here) 
# rearranged and padded with NaNs to form a grid of interactions
# and then plotted.

import sys
sys.path.append('.././src')
import general.CreateDataName as cn
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import s3fs

from general.constants_cloud import *

data_name = data_prefix+cn.create_dataname(run_vars)
model_name = model_prefix+data_name
exp_name = exp_prefix+model_name

tick_labels, tick_locations, grid_lines = [], [], []    
subgroup_grid_lines_light = []  
subgroup_grid_lines_bold  = [] 
no_inputs, no_variables = 0, 0
tick_labels.append('Temperature')   
tick_locations.append(temp_no_inputs/2)
grid_lines.append(temp_no_inputs)
subgroup_grid_lines_light.append(line_ligh)
subgroup_grid_lines_bold.append(line_bold)
no_inputs = no_inputs + temp_no_inputs
no_variables = no_variables + 1
tick_labels.append('Salinity')   
tick_locations.append(grid_lines[-1]+(temp_no_inputs/2)+.5)
grid_lines.append(grid_lines[-1]+temp_no_inputs)
subgroup_grid_lines_light.append(line_ligh)
subgroup_grid_lines_bold.append(line_bold)
no_inputs = no_inputs + temp_no_inputs
no_variables = no_variables + 1
tick_labels.append('U Current')
tick_locations.append(grid_lines[-1]+(temp_no_inputs/2)+.5)
grid_lines.append(grid_lines[-1]+temp_no_inputs)
subgroup_grid_lines_light.append(line_ligh)
subgroup_grid_lines_bold.append(line_bold)
no_inputs = no_inputs + temp_no_inputs
no_variables = no_variables + 1
tick_labels.append('V Current')   
tick_locations.append(grid_lines[-1]+(temp_no_inputs/2)+.5)
grid_lines.append(grid_lines[-1]+temp_no_inputs)
subgroup_grid_lines_light.append(line_ligh)
subgroup_grid_lines_bold.append(line_bold)
no_inputs = no_inputs + temp_no_inputs
no_variables = no_variables + 1
tick_labels.append('U Bolus Velocities')
tick_locations.append(grid_lines[-1]+(temp_no_inputs/2)+.5)
grid_lines.append(grid_lines[-1]+temp_no_inputs)
subgroup_grid_lines_light.append(line_ligh)
subgroup_grid_lines_bold.append(line_bold)
no_inputs = no_inputs + temp_no_inputs
no_variables = no_variables + 1
tick_labels.append('V Bolus Velocities')
tick_locations.append(grid_lines[-1]+(temp_no_inputs/2)+.5)
grid_lines.append(grid_lines[-1]+temp_no_inputs)
subgroup_grid_lines_light.append(line_ligh)
subgroup_grid_lines_bold.append(line_bold)
no_inputs = no_inputs + temp_no_inputs
no_variables = no_variables + 1
tick_labels.append('W Bolus Velocities')
tick_locations.append(grid_lines[-1]+(temp_no_inputs/2)+.5)
grid_lines.append(grid_lines[-1]+temp_no_inputs)
subgroup_grid_lines_light.append(line_ligh)
subgroup_grid_lines_bold.append(line_bold)
no_inputs = no_inputs + temp_no_inputs
no_variables = no_variables + 1
tick_labels.append('Density')   
tick_locations.append(grid_lines[-1]+(temp_no_inputs/2)+.5)
grid_lines.append(grid_lines[-1]+temp_no_inputs)
subgroup_grid_lines_light.append(line_ligh)
subgroup_grid_lines_bold.append(line_bold)
no_inputs = no_inputs + temp_no_inputs
no_variables = no_variables + 1
tick_labels.append('SSH')   
temp_no_inputs = 9
tick_locations.append(grid_lines[-1]+(temp_no_inputs/2)+.5)
grid_lines.append(grid_lines[-1]+temp_no_inputs)
subgroup_grid_lines_light.append([0,3,6,9])
subgroup_grid_lines_bold.append([0,9])
no_inputs = no_inputs + temp_no_inputs
no_variables = no_variables + 1
no_location_vars = 0
tick_labels.append('Location Info')   
temp_no_inputs = 0
temp_no_inputs = temp_no_inputs + 1
no_location_vars = no_location_vars + 1
temp_no_inputs = temp_no_inputs + 1
no_location_vars = no_location_vars + 1
temp_no_inputs = temp_no_inputs + 1
no_location_vars = no_location_vars + 1
tick_locations.append(grid_lines[-1]+(temp_no_inputs/2)+.5)
grid_lines.append(grid_lines[-1]+temp_no_inputs)
subgroup_grid_lines_light.append([0])
subgroup_grid_lines_bold.append([0])
no_inputs = no_inputs + temp_no_inputs
no_variables = no_variables + 1

fs = s3fs.S3FileSystem(
    anon=True,
    client_kwargs={"endpoint_url": "https://pangeo-eosc-minioapi.vm.fedcloud.eu/"},
)

coef_filename = mod_path+exp_name+'_coefs.npz'
#print(coef_filename)
coeff_data = np.load(fs.open(coef_filename))
raw_coeffs = coeff_data['arr_1']
print('raw_coeffs.shape')
print(raw_coeffs.shape)
raw_coeffs=raw_coeffs.reshape(1,-1)
print('raw_coeffs.shape')
print(raw_coeffs.shape)

# Reshape and pad with NaNs to get as array of polynomial interactions
# and convert to abs value
coeffs = np.empty((no_inputs+2,no_inputs))
coeffs[:, :] = np.nan     
start = 0   # start of data for each row. Should be one on from diagonal term
# force second and third row to repeat 1x info, to emphasise this.
coeffs[0,:] = np.absolute(raw_coeffs[0,:no_inputs])
coeffs[1,:] = np.absolute(raw_coeffs[0,:no_inputs])
coeffs[2,:] = np.absolute(raw_coeffs[0,:no_inputs])
for row in range(0, no_inputs):
    no_terms = no_inputs-row
    coeffs[row+2,-no_terms:] = np.absolute(raw_coeffs[0,start:start+no_terms])
    start = start + no_terms    # update start term, sgain one on from diag term


# Replace points which are exactly zero with NaNs
coeffs=np.where(coeffs == 0.0, np.nan, coeffs)

xlabels = tick_labels
xlabel_ticks = list(np.array(tick_locations).astype(float))
xgrid_lines = [0]+list(np.array(grid_lines).astype(float))


ylabels = ['Linear Terms']+tick_labels[:] 
ylabel_ticks = [1.5]+list(np.array(tick_locations[:])+3.)  # three rows representing coeffs x 1 
ygrid_lines = [0, 3]+list(np.array(grid_lines[:])+3.)      # three rows representing coeffs x 1 

vmax = np.nanmax(coeffs)

av_coeffs=np.empty((no_variables+1, no_variables))
for i in range(no_variables+1):
    i_group_start = int(ygrid_lines[i])
    i_group_end   = int(ygrid_lines[i+1])
    for j in range((no_variables)):
        j_group_start = int(xgrid_lines[j])
        j_group_end   = int(xgrid_lines[j+1])
        av_coeffs[i,j] = np.nanmean(coeffs[i_group_start:i_group_end, j_group_start:j_group_end])
fig = plt.figure(figsize=(4.5, 4.5), dpi=300 )
ax = fig.add_subplot(111, aspect='equal')
im = ax.pcolormesh(av_coeffs, edgecolor='face', snap=True )

# Create colorbar
cbar = ax.figure.colorbar(im, ax=ax, shrink=0.6)#, extend='min')
cbar.ax.set_ylabel('coefficient magnitude',rotation=-90, va="bottom")
      
# Set tick labels
ax.set_xticks(np.arange(0.5,10.5,1))
ax.set_yticks(np.arange(0.5,11.5,1))
ax.set_xticklabels(xlabels)
ax.set_yticklabels(ylabels)
# Let the horizontal axes labeling appear on top.
ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)
# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=-60, ha="right", rotation_mode="anchor")
## remove ticks, so only labels show
ax.tick_params(
    which="major", 
    bottom=False, 
    left=False,
    top=False,
    right=False
)
ax.invert_yaxis()
plt.text(0.03, 0.88, '(a)', transform=fig.transFigure)  
fig.tight_layout()
fig.savefig(
    f"{figs_path}fig4a_{exp_name}.png",
    bbox_inches='tight',
    pad_inches=0.1, 
    format='png'
)
plt.show()

for i in range(no_variables):
    i_group_start = int(xgrid_lines[i])
    i_group_end = int(xgrid_lines[i+1])
    for j in range(min(i+2, no_variables)):
        if (ylabels[j]=='Temperature') & (xlabels[i]=='Temperature'):
            j_group_start = int(ygrid_lines[j])
            j_group_end = int(ygrid_lines[j+1])
            fig = plt.figure(figsize=(6.5, 4.5), dpi=300)
            ax = fig.add_subplot(111, aspect='equal')

            im = ax.pcolormesh(
                coeffs[j_group_start:j_group_end, i_group_start:i_group_end], 
                edgecolors='face', 
                snap=False, 
                vmin=0, 
                vmax=vmax
            )

            # Create colorbar
            cbar = ax.figure.colorbar(im, ax=ax, shrink=0.6)
            cbar.ax.set_ylabel('coefficient magnitude',rotation=-90, va="bottom")

            ## Set tick labels
            ax.set_xticks(np.arange(0.2,27.2,1))
            ax.set_yticks(np.arange(0.5,27.5,1))
            ax.set_xticklabels(
                coe_nam
            )
            ax.set_yticklabels(
                coe_nam
            )

            ## Let the horizontal axes labeling appear on top.
            ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)
            ## Rotate the tick labels and set their alignment.
            plt.setp(ax.get_xticklabels(), rotation=-60, ha="right", rotation_mode="anchor")
            ## remove ticks, so only labels show
            ax.tick_params(which="major", bottom=False, left=False, top=False, right=False)

            ## Create white grid.
            ax.set_xticks(np.array(subgroup_grid_lines_light[i]),minor=True)
            ax.set_yticks(np.array(subgroup_grid_lines_light[j]),minor=True)
            ax.grid(which="minor", color="w", linewidth=0.3)

            ax.set_xticks(np.array(subgroup_grid_lines_bold[i]), minor=True)
            ax.set_yticks(np.array(subgroup_grid_lines_bold[j]), minor=True)
            ax.grid(which="minor", color="w", linewidth=1. )

            ax.invert_yaxis()

            plt.text(
                0.03, 
                0.88, 
                '(b)', 
                transform=fig.transFigure
            )  

            fig.tight_layout()
            plt.savefig(
                f"{figs_path}fig4b_{exp_name}_{ylabels[j]}_{xlabels[i]}_coeffs.png",
                bbox_inches = 'tight', 
                pad_inches = 0.1, 
                format='png'
            )
            plt.show()
            plt.close()