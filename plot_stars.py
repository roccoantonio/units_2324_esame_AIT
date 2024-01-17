#!/usr/bin/env python



################################################################################
#  After downloading the file   
#      https://github.com/MilenaValentini/TRM_Dati/blob/main/Nemo_6670.dat
#  we scatter plot the stars' colour vs magnitude. Then, we colour code the
#  scatter plot by assigning a colour to stars in each age group. 
################################################################################





import sys
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors
from matplotlib import lines as mlines
import numpy as np



# First we read the file name of the downloaded file given as an argument to 
# launch this script
data_filename = sys.argv[1]



# We read the file and use columns 5, 9, 13, 1, 2, then assign the columns to 5 
# arrays named after the columns (each col in the file has a #header label).
data = np.loadtxt(data_filename, delimiter=' ', usecols=(4, 8, 12, 0, 1), unpack=True)
M_ass = data[0]
b_y = data[1]
age_parent = data[2]
MsuH = data[3]
m_ini = data[4]



# We create the arrays age_bins_edges to colormap the plot. Each dot in the 
# scatter plot will be coloured according to its age. We have 35 age bins.
# Note: since there are 35 bins, then the bins delimiters have to be 
# 35 + 1, thus the array has a  len()  equal to 36.
age_bins_edges = [0, 0.05, 0.11, 0.18, 0.25, 0.33, 
                  0.41, 0.51, 0.61, 0.73, 0.85, 0.99, 
                  1.14, 1.3, 1.48, 1.68, 1.89, 2.13, 
                  2.39, 2.67, 2.99, 3.33, 3.7, 4.12, 
                  4.57, 5.06, 5.60, 6.20, 6.85, 7.57, 
                  8.35, 9.21, 10.15, 11.19, 12.32, 13.56]



# We used MS Paint's "color picker" tool to read the RGB values of the 35 colors
# in the legend of the image. We saved the 35 RGB values in a file:
rgb_colors_filename = 'colors.txt'

# We read the file and use columns 1, 2, 3, which contain RGB values of the 35 
# colors, stored as int values ranging from 0 to 255.
colors_from_paint = np.loadtxt(rgb_colors_filename, delimiter=',', 
                               usecols=(0, 1, 2), unpack=True)

# Here we create a 2D array which will have the shape 35 x 3.
col_rgb = np.vstack((colors_from_paint)).T

# Here we divide all the RGB values by 255 to create Matplotlib RGB values in 
# the interval [0, 1] .
col_rgb = col_rgb/255.

# We use the helper routine  from_levels_and_colors()  to:
#  * to convert data values (floats) from the interval [0, 1] to the RGB color 
#    that the Colormap represents,
#  * linearly normalize data into the [0.0, 1.0] interval.
custom_colormap, norm = mcolors.from_levels_and_colors(age_bins_edges, col_rgb)



# We initialise the subplots
fig1, ax1 = plt.subplots(figsize=(14,11))

# set axes' limits
plt.ylim(8.5, -4.1)
plt.xlim(-0.1, 1.0)

# set axes' labels
fig1.subplots_adjust(top=0.935)
fig1.suptitle("Colour coded scatter plot: stars' Colour vs. Magnitude.", fontsize=16)
ax1.set_title('Colours codify the age of the stars.')
ax1.set_xlabel(r'$b-y$')
ax1.set_ylabel(r'$M_V$')

# set ticks parameters along the edges (axes)
ax1.tick_params(direction='in', 
                labelbottom=True, labeltop=False, 
                labelleft=True, labelright=False, 
                bottom=True, top=True, left=True, right=True)



# Scatter plot. We set: 
# c - color each dot according to the star's age and the color mapping, 
# ec - edge color (white), 
# lw - line width of each dot's edge, 
# s - size of the dots, 
# cmap and norm - parameters for the color mapping
ax1.scatter(b_y, M_ass, c=age_parent, ec='k', lw=0, s=10, 
            cmap=custom_colormap, norm=norm)



# Here we add the elements to the legend of the plot. 
# Firste we create an array to store legend handles to be used in  legend() . 
legend_dots = []

# Here we append the legend handles to the array. 
# Each handle contains a Line2D Artist, where only the markers will be used to 
# represent the colors in the plot, and a legend string. 
for i in range( len(age_bins_edges) -1 ):
    legend_label_text = "{} Gyr - {} Gyr".format( 
        str( f'{age_bins_edges[i]:.2f}' ), str( f'{age_bins_edges[i+1]:.2f}' ) 
    )
    legend_dots.append( 
        mlines.Line2D( [0], [0], marker='o', markersize=7, color='w', 
                      markerfacecolor=custom_colormap.colors[i], 
                      label=legend_label_text 
                     ) 
    )

# We call legend()
ax1.legend(loc='upper right', handles=legend_dots)

plt.savefig('image_1.png', bbox_inches='tight')
plt.show()




################################################################################
#  Here we're going to plot three overlapping histograms showing the number of
#  stars per metallicity value, each histogram refers to stars in an age group.
#  The age groups delimiters can be modified in the array defined below, see:
#     age_bins_separator
################################################################################

import matplotlib.patheffects as pe
from matplotlib.patches import Rectangle

fig2, ax2 = plt.subplots(figsize=(14,9))

# We create a 2D array containing both metallicities and ages of all the stars
stars_metallicity_age = np.vstack((MsuH, age_parent)).T

# We find metallicity min and max values first, and round them
stars_metallicity_min = np.floor(np.min(stars_metallicity_age[:,0])*10)/10.
stars_metallicity_max = np.ceil(np.max(stars_metallicity_age[:,0])*10)/10.

# We create three 1D arrays containing metallicity values for stars grouped 
# together by age.
age_bins_separator = [1, 3]
#  1) We create a 1D array containing the metallicities of the stars younger 
#     than 1 Gyr
array_stars_metallicity_young = stars_metallicity_age[:,0][stars_metallicity_age[:,1]<age_bins_separator[0]]

#  2) We create a temproary 2D array containing the metallicities of the stars 
#     older than or equal to 1 Gyr...
temp_array_metallicity_by_age = stars_metallicity_age[:][stars_metallicity_age[:,1]>=age_bins_separator[0]]

#    ...then we create a 1D array from the array above, containing the 
#       metallicities of stars both older than 1 Gyr and younger than 3 Gyr
array_stars_metallicity_middleaged = temp_array_metallicity_by_age[:,0][temp_array_metallicity_by_age[:,1]<age_bins_separator[1]]

#  3) We create a 1D array containing the metallicities of the stars older than 
#     or equal to 3 Gyr
array_stars_metallicity_old = stars_metallicity_age[:,0][stars_metallicity_age[:,1]>=age_bins_separator[1]]

# We collect the three arrays above in one dictionary for iteration purposes
dict_stars_metallicity_by_age = {
  0: array_stars_metallicity_young,
  1: array_stars_metallicity_middleaged,
  2: array_stars_metallicity_old
}

# We create a dictionary of labels for iteration purposes
dict_stars_metallicity_by_age_labels = {
    0: ' $ t < {} $ '.format(age_bins_separator[0]),
    1: ' $ {} \leq t < {} $ '.format(age_bins_separator[0],age_bins_separator[1]),
    2: ' $ t \geq {} $ '.format(age_bins_separator[1])
}

# We create a dictionary of colors for iteration purposes
dict_stars_metallicity_by_age_colors = {
    0: 'red',
    1: 'green',
    2: 'blue'
}

# We set the number of bins.
# Experimentation showed that starting from 100 bins, and halfing down the value
# twice we don't lose detail. In fact, some of the bins had 0 frequencies.
# The histogram somehow shows that metallicities values are close to 27 distinct 
# values.
num_of_bins = 27
stars_metallicity_histogram_bins = np.linspace(stars_metallicity_min, 
                                               stars_metallicity_max, 
                                               num_of_bins+1)

# We set the ticks on the x axis to match the number of bins
ax2.set_xticks(np.linspace(stars_metallicity_min, 
                           stars_metallicity_max, 
                           num_of_bins+1))

# We set the histogram title and labels
fig2.subplots_adjust(top=0.935)
fig2.suptitle("Histograms: Number of stars (relative freq.) vs Metallicity of stars, grouped by age $t$.", fontsize=16)
ax2.set_xlabel(r'$M / H$')
ax2.tick_params(axis='x', labelsize=9)
ax2.set_ylabel(r'$f$')

# We set the grid and the ylim
plt.grid(ls=':', lw=0.5, c='gray')
#ax5.set_ylim(0., 1.)
ax2.set_xlim(-2.1, 0.8)



# We loop over the three age categories to plot three overlapping histograms.
stars_histogram = []
for i in range(3):
    stars_histogram.append( 
        ax2.hist(dict_stars_metallicity_by_age[i], 
                 stars_metallicity_histogram_bins, 
                 weights=np.zeros_like(dict_stars_metallicity_by_age[i]) + 1. / dict_stars_metallicity_by_age[i].size, 
                 color=dict_stars_metallicity_by_age_colors[i], 
                 alpha=0.25, fill=True, histtype='step',linewidth=1.5 )
    )



# We compute the mean and the median values for each of the three subpopulations 
# and plot them.
mean_lines = []
median_lines = []
mean_labels = []
median_labels = []

for i in range(3):
    mean = np.mean(dict_stars_metallicity_by_age[i])
    median = np.median(dict_stars_metallicity_by_age[i])
    mean_lines.append( ax2.vlines(mean, 0, 1, transform=ax2.get_xaxis_transform(), 
                                  linestyles='solid', lw=3, 
                                  colors=dict_stars_metallicity_by_age_colors[i] ) )
    median_lines.append( ax2.vlines(median, 0, 1, transform=ax2.get_xaxis_transform(), 
                                    linestyles='dashed', lw=3, 
                                    colors=dict_stars_metallicity_by_age_colors[i] ) )
    ax2.text(mean, 0.2-i*0.0175, '{:0.2f} '.format(mean), 
             c=dict_stars_metallicity_by_age_colors[i], fontsize='x-large', 
             horizontalalignment='right', 
             path_effects=[pe.withStroke(linewidth=2.5, foreground='w' )])
    ax2.text(median, 0.2-i*0.0175, ' {:0.2f}'.format(median), 
             c=dict_stars_metallicity_by_age_colors[i], fontsize='x-large', 
             horizontalalignment='left', 
             path_effects=[pe.withStroke(linewidth=2.5, foreground='w' )])


# Mean and median lines legend
title_proxy_1 = Rectangle((0,0), 0, 0, color='w')
legend_hndl_1 = [Rectangle((0,0),1,1,color=c,alpha=0.33,ec="k") for c in 
            [dict_stars_metallicity_by_age_colors[0], 
             dict_stars_metallicity_by_age_colors[1], 
             dict_stars_metallicity_by_age_colors[2]]]

mean_line = ax2.vlines(0, 0, 0, linestyles='solid', lw=3, colors='k' )
median_line = ax2.vlines(0, 0, 0, linestyles='dashed', lw=3, colors='k' )

# Final legend
legend_handle_1 = ax2.legend([legend_hndl_1[0], legend_hndl_1[1], legend_hndl_1[2], 
                              title_proxy_1, mean_line, median_line], 
                             [dict_stars_metallicity_by_age_labels[0], 
                              dict_stars_metallicity_by_age_labels[1], 
                              dict_stars_metallicity_by_age_labels[2], 
                              ' ', 'mean valule', 'median value'], 
                             title='Metallicity frequency \n by stars age $t$ (Gyr):', 
                             handlelength=4, fancybox=True, shadow=True, loc='upper left' )

plt.savefig('image_2.png', bbox_inches='tight')
plt.show()




################################################################################
#  Here we scatter plot mmetallicity vs initial mass of stars. Also, we use
#  three colours and markers with different shapes to differentiate stars 
#  belonging to each age group.
################################################################################

stars_mass_metallicity_age = np.vstack((m_ini, MsuH, age_parent)).T

stars_mass_min = np.floor(np.min(stars_mass_metallicity_age[:,0])*10)/10.
stars_mass_max = np.ceil(np.max(stars_mass_metallicity_age[:,0])*10)/10.

# We create three 1D arrays containing metallicity values for stars grouped 
# together by age.
#  1) We create a 1D array containing the metallicities of the stars younger 
#     than 1 Gyr
array_stars_mass_young = stars_mass_metallicity_age[:,0][stars_mass_metallicity_age[:,2]<age_bins_separator[0]]

#  2) We create a temproary 2D array containing the metallicities of the stars 
#     older than or equal to 1 Gyr...
temp_array_mass_by_age = stars_mass_metallicity_age[:][stars_mass_metallicity_age[:,2]>=age_bins_separator[0]]

#    ...then we create a 1D array from the array above by slicing, containing  
#       the metallicities of stars both older than 1 Gyr and younger than 3 Gyr
array_stars_mass_middleaged = temp_array_mass_by_age[:,0][temp_array_mass_by_age[:,2]<age_bins_separator[1]]

#  3) We create a 1D array containing the metallicities of the stars older than 
#     or equal to 3 Gyr
array_stars_mass_old = stars_mass_metallicity_age[:,0][stars_mass_metallicity_age[:,2]>=age_bins_separator[1]]

# We collect the three arrays above in one dictionary for possible iteration 
# purposes
dict_stars_mass_by_age = {
  0: array_stars_mass_young,
  1: array_stars_mass_middleaged,
  2: array_stars_mass_old
}

# We compute the boundaries for all the subsequent plots
stars_mass_young_min = np.floor(np.min(array_stars_mass_young)*10)/10.
stars_mass_young_max = np.ceil(np.max(array_stars_mass_young)*10)/10.
stars_mass_middleaged_min = np.floor(np.min(array_stars_mass_middleaged)*10)/10.
stars_mass_middleaged_max = np.ceil(np.max(array_stars_mass_middleaged)*10)/10.
stars_mass_old_min = np.floor(np.min(array_stars_mass_old)*10)/10.
stars_mass_old_max = np.ceil(np.max(array_stars_mass_old)*10)/10.



# We initialise the plot.
fig3, ax3 = plt.subplots(figsize=(10,10))

# We plot stars in the three age groups.
ax3.scatter(array_stars_mass_young, array_stars_metallicity_young, 
            s=45, c='r', alpha=0.15, marker='s',
            label=dict_stars_metallicity_by_age_labels[0])

ax3.scatter(array_stars_mass_middleaged, array_stars_metallicity_middleaged, 
            s=30, c='g', alpha=0.20, marker='o',
            label=dict_stars_metallicity_by_age_labels[1])

ax3.scatter(array_stars_mass_old, array_stars_metallicity_old, 
            s=15, c='b', alpha=0.25, marker='^',
            label=dict_stars_metallicity_by_age_labels[2])

fig3.subplots_adjust(top=0.925)
fig3.suptitle('Scatter plot: Metallicity vs. Initial Mass of stars, grouped by age $t$.', fontsize=16)
ax3.set_xlabel('$m_{ini}$')
ax3.set_ylabel('$M / H$')

ax3.legend(loc="lower right", title="Stars by age $t$ (Gyr):")

plt.xscale('log')

plt.savefig('image_3.png', bbox_inches='tight')
plt.show()




################################################################################
#  Here we create three 2D histograms for comparison.
#  Each hist2d shows mmetallicity vs initial mass of stars in an age group.
###############################################################################

fig4, ax4 = plt.subplots(1,3, figsize=(14,4))

hist_1 = ax4[0].hist2d(array_stars_mass_young, array_stars_metallicity_young, 
                    range=[[stars_mass_young_min-0.1, stars_mass_young_max+0.1], 
                           [stars_metallicity_min-0.1, stars_metallicity_max+0.1]], 
                    bins=22, cmin=0.5, cmap='Wistia', alpha=0.7)

hist_2 = ax4[1].hist2d(array_stars_mass_middleaged, array_stars_metallicity_middleaged, 
                    range=[[stars_mass_middleaged_min-0.1, stars_mass_middleaged_max+0.1], 
                           [stars_metallicity_min-0.1, stars_metallicity_max+0.1]], 
                    bins=22, cmin=0.5, cmap='Wistia', alpha=0.7)

hist_3 = ax4[2].hist2d(array_stars_mass_old, array_stars_metallicity_old, 
                    range=[[stars_mass_old_min-0.1, stars_mass_old_max+0.1], 
                           [stars_metallicity_min-0.1, stars_metallicity_max+0.1]], 
                    bins=22, cmin=0.5, cmap='Wistia', alpha=0.7)


fig4.colorbar(hist_1[3])
fig4.colorbar(hist_2[3])
fig4.colorbar(hist_3[3])

fig4.subplots_adjust(top=0.825)
fig4.suptitle('2D histogram comparison: Metallicity vs. Initial Mass of stars, grouped by age $t$ (Gyr)', fontsize=16)

ax4[0].set_title(dict_stars_metallicity_by_age_labels[0])
ax4[0].set_xlabel('$m_{ini}$')
ax4[0].set_ylabel('$M / H$')

ax4[1].set_title(dict_stars_metallicity_by_age_labels[1])
ax4[1].set_xlabel('$m_{ini}$')

ax4[2].set_title(dict_stars_metallicity_by_age_labels[2])
ax4[2].set_xlabel('$m_{ini}$')

plt.savefig('image_4.png', bbox_inches='tight')
plt.show()




################################################################################
#  Here we iterate the plot above in a different fashion. 
#  We plot three contour plots over a 2D histogram to show how stars' 
#  metallicities are related to their initial mass for the three different
#  age groups.
################################################################################

fig5, ax5 = plt.subplots(figsize=(8,7))

plt.xscale('log')

hist_all = ax5.hist2d(stars_mass_metallicity_age[:,0], stars_mass_metallicity_age[:,1], 
                      range=[[stars_mass_min-0.1, stars_mass_max+0.1], 
                             [stars_metallicity_min-0.1, stars_metallicity_max+0.1]], 
                      bins=22, cmin=0.5, cmap='Wistia', alpha=0.7)

hist_young_1 = np.histogram2d(array_stars_mass_young, array_stars_metallicity_young, 
                            range=[[stars_mass_min-0.1, stars_mass_max+0.1], 
                                   [stars_metallicity_min-0.1, stars_metallicity_max+0.1]], 
                            bins=22)

hist_mid_1 = np.histogram2d(array_stars_mass_middleaged, array_stars_metallicity_middleaged, 
                          range=[[stars_mass_min-0.1, stars_mass_max+0.1], 
                                 [stars_metallicity_min-0.1, stars_metallicity_max+0.1]], 
                          bins=22)

hist_old_1 = np.histogram2d(array_stars_mass_old, array_stars_metallicity_old, 
                          range=[[stars_mass_min-0.1, stars_mass_max+0.1], 
                                 [stars_metallicity_min-0.1, stars_metallicity_max+0.1]], 
                          bins=22)

hist_young_2 = np.where(hist_young_1[0] > 0, hist_young_1[0], np.nan)
hist_mid_2 = np.where(hist_mid_1[0] > 0, hist_mid_1[0], np.nan)
ist_old_2 = np.where(hist_old_1[0] > 0, hist_old_1[0], np.nan)


conts=[None]*3

conts[0] = ax5.contour(np.linspace(stars_mass_min-0.1, stars_mass_max+0.1, num=22), 
                       np.linspace(stars_metallicity_min-0.1, stars_metallicity_max+0.1, num=22), 
                       hist_young_2.T, [70], colors='r', alpha=0.6)

conts[1] = ax5.contour(np.linspace(stars_mass_min-0.1, stars_mass_max+0.1, num=22), 
                       np.linspace(stars_metallicity_min-0.1, stars_metallicity_max+0.1, num=22), 
                       hist_mid_2.T, [100], colors='g', alpha=0.6)

conts[2] = ax5.contour(np.linspace(stars_mass_min-0.1, stars_mass_max+0.1, num=22), 
                       np.linspace(stars_metallicity_min-0.1, stars_metallicity_max+0.1, num=22), 
                       ist_old_2.T, [100], colors='b', alpha=0.6)


for i in range(3):
    ax5.clabel(conts[i], inline=True, fontsize=10)

fig5.colorbar(hist_all[3])

fig5.subplots_adjust(top=0.85)
fig5.suptitle('Metallicity vs. Initial Mass of stars', fontsize=16, x=0.45)
ax5.set_title('The histogram refers to all stars. Each contour refers to an age group.\n A contour contains only bins with at least the indicated number\n of stars. Bins outside the contours have less stars than indicated.')
ax5.set_xlabel('$m_{ini}$')
ax5.set_ylabel('$M / H$')


# Mean and median lines legend
title_proxy2 = Rectangle((0,0), 0, 0, color='w')
handless2 = [Rectangle((0,0),1,1,color=c,alpha=0.6,ec="w") for c in 
            [dict_stars_metallicity_by_age_colors[0], 
             dict_stars_metallicity_by_age_colors[1], 
             dict_stars_metallicity_by_age_colors[2]]]

# Legend
legend_handle_2 = ax5.legend([handless2[0], handless2[1], handless2[2], title_proxy2], 
                             [dict_stars_metallicity_by_age_labels[0], 
                              dict_stars_metallicity_by_age_labels[1], 
                              dict_stars_metallicity_by_age_labels[2]], 
                             title='Age group colour:', 
                             handlelength=4, fancybox=True, shadow=True, loc='lower right' )

plt.savefig('image_5.png', bbox_inches='tight')
plt.show()