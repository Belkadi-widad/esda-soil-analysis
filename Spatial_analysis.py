#!/usr/bin/env python
# coding: utf-8

# In[2]:


from pysal.lib import weights
import seaborn
import numpy
import matplotlib.pyplot as plt
import mapclassify
import folium
import base64
from io import BytesIO
import os
# Graphics
import matplotlib.pyplot as plt
from splot.esda import plot_moran

# Analysis
from pysal.explore import esda
from pysal.lib import weights
from numpy.random import seed
from data import getDataset, soil_properties

soil_props_names = ['sand %',
                    'silt %',
                    'clay %',
                    'pH water',
                    'OC %',
                    'N %',
                    'BS %',
                    'CEC',
                    'CEC clay',
                    'CaCO3 %',
                    'BD',
                    'C/N']
countries_fao = ['TUNISIA', 'MOROCCO', 'ALGERIA', 'LIBYA', 'MAURITANIA']


# In[4]:


soil_properties = ['sand % topsoil',
                   'sand % subsoil',
                   'silt % topsoil',
                   'silt% subsoil',
                   'clay % topsoil',
                   'clay % subsoil',
                   'pH water topsoil',
                   'pH water subsoil',
                   'OC % topsoil',
                   'OC % subsoil',
                   'N % topsoil',
                   'N % subsoil',
                   'BS % topsoil',
                   'BS % subsoil',
                   'CEC topsoil',
                   'CEC subsoil',
                   'CEC clay topsoil',
                   'CEC Clay subsoil',
                   'CaCO3 % topsoil',
                   'CaCO3 % subsoil',
                   'BD topsoil',
                   'BD subsoil',
                   'C/N topsoil',
                   'C/N subsoil']

cp_union = getDataset()


def spatial_weights():
    wr = weights.contiguity.Rook.from_dataframe(cp_union)
    return wr


wr = spatial_weights()


#  In[8]: # Map Classifications

# ### Equal intervals

def equal_intervals(k=5, prop="OC % topsoil"):
    return mapclassify.EqualInterval(cp_union[prop], k=k)


# ### Quantiles
#


def quantiles(k=5, prop="OC % topsoil"):

    q5 = {}
    q5['quantiles'] = mapclassify.Quantiles(cp_union[prop], k=k)
    q5['width'] = q5['quantiles'].bins[1:] - q5['quantiles'].bins[:-1]

    return q5


def mean_standard_dev(prop="OC % topsoil"):

    return mapclassify.StdMean(cp_union[prop])


# ### Maximum Breaks


def maximum_breaks(k=5, prop="OC % topsoil"):
    return mapclassify.MaximumBreaks(cp_union[prop], k=k)


def BoxPlot(prop="OC % topsoil"):

    return mapclassify.BoxPlot(cp_union[prop])


# ### Head-Tail Breaks

def head_tail_breaks(prop="OC % topsoil"):

    return mapclassify.HeadTailBreaks(cp_union[prop])


# ### Jenks Caspall

def Jenks_Caspall(k=5, prop="OC % topsoil"):

    numpy.random.seed(12345)
    return mapclassify.JenksCaspall(cp_union[prop], k=k)


# ### Fisher Jenks

def fisher_jenks(k=5, prop="OC % topsoil"):
    numpy.random.seed(12345)
    return mapclassify.FisherJenks(cp_union[prop], k=k)


# Append class values as a separate column
def all_classifiers(soil_prop, k):
    mx = cp_union
    mx["Quantiles"] = quantiles(k=k, prop=soil_prop)['quantiles'].yb
    mx["Equal Interval"] = equal_intervals(k=k, prop=soil_prop).yb
    mx["Head-Tail Breaks"] = head_tail_breaks(prop=soil_prop).yb
    mx["Maximum Breaks"] = maximum_breaks(k=k, prop=soil_prop).yb
    mx["Mean-Standard Deviation"] = mean_standard_dev(prop=soil_prop).yb
    mx["Fisher-Jenks"] = fisher_jenks(k=k, prop=soil_prop).yb
    mx["Jenks Caspall"] = Jenks_Caspall(k=k,  prop=soil_prop).yb
    mx["BoxPlot"] = BoxPlot(prop=soil_prop).yb
    return mx


def heatmap(mx):
    f, ax = plt.subplots(1, figsize=(9, 3))
    seaborn.heatmap(
        mx.set_index("CNT_FULLNAME")
        .sort_values(soil_properties[0])[
            [
                "Head-Tail Breaks",
                "Fisher-Jenks",
                "Maximum Breaks",
                "Equal Interval",
                "MaxP",
                "Quantiles",
                "Jenks Caspall",
                "Mean-Standard Deviation",
                "User Defined",
                "BoxPlot"
            ]
        ]
        .T,
        cmap="YlGn",
        cbar=False,
        ax=ax,
    )
    ax.set_xlabel("Country")
    return f

# In[9] #Plot functions


def plot_scheme(mx, schema, soil_prop, color_palette="YlGn"):
    ax = mx.plot(
        column=soil_prop,  # Data to plot
        scheme=schema,  # Classification scheme
        cmap=color_palette,  # Color palette
        legend=True,  # Add legend
        # Remove decimals in legend
        legend_kwds={"fmt": "{:.0f}", 'loc': 'lower left'},
    )

    ax.set_axis_off()
    return ax


def BoxMap(mx, soil_prop, path='assets/boxmap.html'):

    if os.path.exists(f".{path}") == False:
        bp = BoxPlot(prop=soil_prop)
        if len(bp.bins) == 5:
            legends = [f'Lower outlier : ({bp.counts[0]}) (-inf , {bp.bins[0]:.2f}]', f'< 25% : ({bp.counts[1]}) ({bp.bins[0]:.2f} , {bp.bins[1]:.2f}]', f'25 % - 50% ({bp.counts[2]}) ({bp.bins[1]:.2f} , {bp.bins[2]:.2f}]',
                       f' 50% - 75% ({bp.counts[3]}) ({bp.bins[2]:.2f}, {bp.bins[3]:.2f}]', f' >75% ({bp.counts[4]}) ({bp.bins[3]:.2f} , {bp.bins[4]:.2f}]', f'Upper outlier (0) ({bp.bins[4]:.2f} , +inf)']
        else:
            legends = [f'Lower outlier : ({bp.counts[0]}) (-inf , {bp.bins[0]:.2f}]', f'< 25% : ({bp.counts[1]}) ({bp.bins[0]:.2f} , {bp.bins[1]:.2f}]', f'25 % - 50% ({bp.counts[2]}) ({bp.bins[1]:.2f} , {bp.bins[2]:.2f}]',
                       f' 50% - 75% ({bp.counts[3]}) ({bp.bins[2]:.2f}, {bp.bins[3]:.2f}]', f' >75% ({bp.counts[4]}) ({bp.bins[3]:.2f} , {bp.bins[4]:.2f}]', f'Upper outlier ({bp.counts[5]}) ({bp.bins[4]:.2f} , {bp.bins[5]:.2f}]']

        m = mx.explore(
            column=soil_prop,  # make choropleth based on "BoroName" column
            scheme='BoxPlot',  # use mapclassify's natural breaks scheme
            legend=True,  # show legend
            tooltip=soil_properties,
            k=6,  # use 10 bins
            cmap='viridis_r',
            # do not use colorbar
            legend_kwds=dict(colorbar=False, labels=legends),
            name="CNT_FULLNAME"  # name of the layer in the map
        )
        # folium.TileLayer('Stamen Toner', control=True).add_to(
        #     m)  # use folium to add alternative tiles
        # folium.LayerControl().add_to(m)  # use folium to add layer control
        m.save(path)
    return f'./{path}'


# In[] #Global spatial autocorrelation


def calculateMoranSI(db, prop,  k=8):
    #db = copy.deepcopy(soil_data)
    # Generate W from the GeoDataFrame
    w = weights.KNN.from_dataframe(db, k=k)
    # Row-standardization
    w.transform = "R"
    moran = esda.moran.Moran(db[prop], w)
    moransI = moran.I
    p_sim = moran.p_sim

    return moran, moransI, p_sim


def plotMoran(moranObjct, path="global-scatter.html"):

    if os.path.exists(f".{path}") == False:
        plot = plot_moran(moranObjct)
        # plot[0].save(path)
        # plt.savefig(f".{path}")
        #fig = plt.figure()
        tmpfile = BytesIO()
        plt.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        print(path)
        f = open(f".{path}", "x+")

        html = f'''<html>
            <head>
            <title>HTML File</title>
            </head> 
            <body>
            <img src='data:image/png;base64,{encoded}' style="width: 100%;">
            </body>
            </html>'''
        print(html)
        # writing the code in   to the file
        # f.write(html)

        # close the file
        # f.close()
        with open(f".{path}", 'w') as f:
            print(path)
            f.write(html)

    return path


def calculateLISA(db, k, soil_prop):
    w = weights.KNN.from_dataframe(db, k=k)
    lisa = esda.moran.Moran_Local(db[soil_prop], w)
    lisaIs = lisa.Is
    return lisa, lisaIs
