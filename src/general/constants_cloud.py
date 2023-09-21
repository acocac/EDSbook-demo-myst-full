# Paths
figs_path = 'outputs/figures/'
data_raw_path = 'data/raw/'
data_interim_path_local = 'data/interim/'
data_interm_path = 's3://acocacastro-edsbook-data/team3/data/interim/'
pred_path = "s3://acocacastro-edsbook-data/team3/outputs/predictions/"
mod_path = "s3://acocacastro-edsbook-data/team3/outputs/models/"
# Averages
start=500
skip=14

# Plots raw data: depth, cross-sections, colorbars
sd_min_value = 0
sd_max_value = 0.00025
time = 2500
point = [2, 8, 6]
level = point[0]
y_coord = point[1]
x_coord = point[2]
lat_arange = [
    0,
    8.36,
    15.5,
    21.67,
    27.25,
    32.46,
    37.5,
    42.54,
    47.75,
    53.32,
    59.5,
    66.64,
    75.5
]

lon_arange = [0, 4.5, 9.5]
diff_min_value = -.001
diff_max_value = .001


lat_label = 'Latitude ('+u'\xb0'+' N)'
lon_label = 'Longitude ('+u'\xb0'+' E)'
depth_label = 'Depth (m)'
cbar_label = 'Temperature ('+u'\xb0'+'C)'
cbar_diff_label = 'Temperature Change ('+u'\xb0'+'C)'
cbar_sd_label = 'Temperature Standard Deviation ('+u'\xb0'+'C)'
cbar_label_err = 'Error ('+u'\xb0'+'C)'
# Plots average trends

vars_avgs = (
    'Av_ADVx_TH', 
    'Av_ADVy_TH', 
    'Av_ADVr_TH', 
    'Av_DFxE_TH',
    'Av_DFyE_TH', 
    'Av_DFrE_TH', 
    'Av_DFrI_TH' 
)

names_avgs = (
    'Zonal Advective Flux of Pot.Temperature\n', 
    'Meridional Advective Flux of Pot.Temperature\n',
    'Vertical Advective Flux of Pot.Temperature\n',
    'Zonal Diffusive Flux of Pot.Temperature\n',
    'Meridional Diffusive Flux of Pot.Temperature\n',
    'Explicit Vertical Diffusive Flux of Pot.Temperature\n',
    'Implicit Vertical Diffusive Flux of Pot.Temperature\n'
)

text_avgs = (
    '(a)',
    '(b)',
    '(c)',
    '(a)',
    '(b)',
    '(c)',
    '(d)'
)

label_avgs = 'Flux $(Cm^3 s^{-1})$'

# Predictions

run_vars = {
    'dimension':3,
    'lat':True ,
    'lon':True,
    'dep':True ,
    'current':True , 
    'bolus_vel':True , 
    'sal':True ,
    'eta':True , 
    'density':True ,
    'poly_degree':2,
    'StepSize':1,
    'predict':'DelT'
}

data_prefix = ''
exp_prefix = ''
model_prefix = 'alpha.001_'


coe_nam = [
    'Above NW', 
    'Above N', 
    'Above NE', 
    'Above W', 
    'Above', 
    'Above E', 
    'Above SW', 
    'Above S', 
    'Above SE',  
    'NW', 
    'N',
    'NE',
    'W', 
    'Centre point',
    'E', 
    'SW', 
    'S', 
    'SE', 
    'Below NW', 
    'Below N', 
    'Below NE',
    'Below W', 
    'Below', 
    'Below E',
    'Below SW',
    'Below S',
    'Below SE'
]


line_ligh = [0,3,6,9,12,15,18,21,24,27]
line_bold = [0,9,18,27]

temp_no_inputs = 27
