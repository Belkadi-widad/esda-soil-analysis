# Improtant note: This data file would ordinarily be used to connect with a proper database server
# more likely PostgreSQL, but thats me. I do plan on rewritting this in the future for such implementations.
# With that said, this file will be be very slow to run and only to demonstrate data processing using
# functions and pandas along with providing a central file for data references
#
# Import Pandas
import pandas as pd
import geopandas as gpd
import json


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

DOM_mapping_all = {
    "A": "ACRISOLS",
    "Ao": "Orthic Acrisols",
    "Af": "Ferric Acrisols",
    "Ah": "Humic Acrisols",
    "Ap": "Plinthic Acrisols",
    "Ag": "Gleyic Acrisols",
    "B": "CAMBISOLS",
    "Be": "Eutric Cambisols",
    "Bd": "Dystric Cambisols",
    "Bh": "Humic Cambisols",
    "Bg": "Gleyic Cambisols",
    "Bx": "Gelic Cambisols",
    "Bk": "Calcic Cambisols",
    "Bc": "Chromic Cambisols",
    "Bv": "Vertic Cambisols",
    "Bf": "Ferralic Cambisols",
    "C": "CHERNOZEMS",
    "Ch": "Haplic Chernozems",
    "Ck": "Calcic Chernozems",
    "Cl": "Luvic Chernozems",
    "Cg": "Glossic Chernozems",
    "D": "PODZOLUVISOLS",
    "De": "Eutric Podzoluvisols",
    "Dd": "Dystric Podzoluvisols",
    "Dg": "Gleyic Podzoluvisols",
    "E": "RENDZINAS",
    "F":  "FERRALSOLS",
    "Fo": "Orthic Ferralsols",
    "Fx": "Xanthic Ferralsols",
    "Fr": "Rhodic Ferralsols",
    "Fh": "Humic Ferralsols",
    "Fa": "Acric Ferralsols",
    "Fp": "Plinthic Ferralsols",
    "G": "GLEYSOLS",
    "Ge": "Eutric Gleysols",
    "Gc": "Calcaric Gleysols",
    "Gd": "Dystric Gleysols",
    "Gm": "Mollic Gleysols",
    "Gh": "Humic Gleysols",
    "Gp": "Plinthic Gleysols",
    "Gx": "Gelic Gleysols",
    "H": "PHAEOZEMS",
    "Hh": "Haplic Phaeozems",
    "Hc": "Calcaric Phaeozems",
    "Hl": "Luvic Phaeozems",
    "Hg": "Gleyic Phaeozems",
    "I": "LITHOSOLS",
    "J": "FLUVISOLS",
    "Je": "Eutric Fluvisols",
    "Jc": "Calcaric Fluvisols",
    "Jd": "Dystric Fluvisols",
    "Jt": "Thionic Fluvisols",
    "K": "KASTANOZEMS",
    "Kh": "Haplic Kastanozems",
    "Kk": "Calcic Kastanozems",
    "Kl": "Luvic Kastanozems",
    "L": "LUVISOLS",
    "Lo": "Orthic Luvisols",
    "Lc": "Chromic Luvisols",
    "Lk": "Calcic Luvisols",
    "Lv": "Vertic Luvisols",
    "Lf": "Ferric Luvisols",
    "La": "Albic Luvisols",
    "Lp": "Plinthic Luvisols",
    "Lg": "Gleyic Luvisols",
    "M": "GREYZEMS",
    "Mo": "Orthic Greyzems",
    "Mg": "Gleyic Greyzems",
    "N": "NITOSOLS",
    "Ne": "Eutric Nitosols",
    "Nd": "Dystric Nitosols",
    "Nh": "Humic Nitosols",
    "O": "HISTOSOLS",
    "Oe": "Eutric Histosols",
    "Od": "Dystric Histosols",
    "Ox": "Gelic Histosols",
    "P": "PODZOLS",
    "Po": "Orthic Podzols",
    "Pl": "Leptic Podzols",
    "Pf": "Ferric Podzols",
    "Ph": "Humic Podzols",
    "Pp": "Placic Podzols",
    "Pg": "Gleyic Podzols",
    "Q": "ARENOSOLS",
    "Qc": "Cambic Arenosols",
    "Ql": "Luvic Arenosols",
    "Qf": "Ferralic Arenosols",
    "Qa": "Albic Arenosols",

    "R": "REGOSOLS",
    "Re": "Eutric Gleysols",
    "Rc": "Calcaric Regosols",
    "Rd": "Dystric Regosols",
    "Rx": "Gelic Regosols",

    "S": "SOLONETZ",
    "So": "Orthic Solonetz",
    "Sm": "Mollic Solonetz",
    "Sg": "Gleyic Solonetz",

    "T": "ANDOSOLS",
    "To": "Ochric Andosols",
    "Tm": "Mollic Andosols",
    "Th": "Humic Andosols",
    "Tv": "Vitric Andosols",

    "U": "RANKERS",

    "V": "VERTISOLS",
    "Vp": "Pellic Vertisols",
    "Vc": "Chromic Vertisols",

    "W": "PLANOSOLS",
    "We": "Eutric Planosols",
    "Wd": "Dystric Planosols",
    "Wm": "Mollic Planosols",
    "Wh": "Humic Planosols",
    "Ws": "Solodic Planosols",
    "Wx": "Gelic Planosols",
    "X": "XEROSOLS",
    "Xk": "Calcic Xerosols",
    "Xh": "Haplic Xerosols",
    "Xy": "Gypsic Xerosols",
    "Xl": "Luvic Xerosols",
    "Y": "YERMOSOLS",
    "Yh": "Haplic Yermosols",
    "Yk": "Calcic Yermosols",
    "Yy": "Gypsic Yermosols",
    "Yl": "Luvic Yermosols",
    "Yt": "Takyric Yermosols",
    "Z": "SOLONCHAKS",
    "Zo": "Orthic Solonchaks",
    "Zm": "Mollic Solonchaks",
    "Zt": "Takyric Solonchaks",
    "Zg": "Gleyic Solonchaks",
    "WR": 'Water',
    "DS": 'Dunes or shifting sands',
    'ST': 'Salt flats',
    'RK': 'Rock'
}


DOM_existan = ['RK', 'WR', 'DS', 'ST', 'Bk', 'Lg',  'Vp', 'So', 'K', 'La', 'Jc', 'Bc', 'Rd', 'Vc', 'Lo', 'E',
               'X', 'Ne', 'I', 'Lc', 'Xk', 'Xh', 'Zo', 'Be', 'Yk', 'Yh', 'Kk', 'Zt', 'Yy', 'Zg',
               'Je', 'Rc', 'V', 'Kl', 'We',  'Y', 'Hl', 'Re', 'Xy', 'Yt', 'R', 'Jt', 'Qc', 'Ql', 'Lf',
               'Bv']
DOM_mapping = {dom: DOM_mapping_all[dom] for dom in DOM_existan}


description_visualizations = {
    # ditrubution page
    "histo_soil_prop": "Histogram to show the distribution of the selected soil property. You can vary the number of bins",
    "boxplot_soil_property": "Box plot to show the distribution of one soil property. You can also group the box plot  by country or dominant soil unit.",
    "boxplot_soil_properties": "Box plot to show the distribution of miltiple soil properties so that we can compare their distribution. You can also group the boxplots by country.",
    "correlation-heatmap": "",
    "scatter-plot": "",
    # choropleth page
    "boxplot_boxmap": "A box map (Anselin 1994) is the mapping counterpart of the idea behind a box plot. The point of departure is a quartile map. But the four categories are extended to six bins, to separately identify the lower and upper outliers.",
    "map-classifier-choro": "Select the classifier algorithm to classify the study area by the selected soil property. You need to fix the number of neighbors. You can also change the color palette.",
    "global-spatial-corr": """By examining the global spatial autocorrelation, a statement can be made about the degree of clustering within the data set. The first choice
                            for estimating global autocorrelation is a well-known statistic called Moran’s I.
                            In the left, the empirical distribution generated by simulating 999
                            random maps using the values of the soil property variable and computing
                            Moran’s I for each of these maps is shown in gray. A blue line marks the mean value and the red line shows Moran’s I. 
                            In the right, the Moran scatter plot, first outlined in Anselin (1996), consists of a plot with the spatially lagged variable on the y-axis and the original variable on the x-axis. 
                            The slope of the linear fit to the scatter plot equals Moran’s I.
                            """,
    "local-corr": """Local autocorrelation aims to identify the clusters in order to provide a more
                    detailed picture. It is offered by the Local Indicators of Spatial Association (LISA). The values of LISA are represented in a choropleth map. The Scatter quadrant shows the location of quadrants of the Moran's scatterplot.
                    The Statistical significance map shows the significance of LISA values, you can fix the significance percent. The Moran cluster map shows the quadrants including the non-significant cluster according the fixed significance threshold.
"""

}


def get_domsoi_items():
    items = map(lambda x: f"{x[0]}: {x[1]}" if type(
        x) is tuple else x, list(['All']) + list(DOM_mapping.items()))

    return list(items)


def getDataset(path='./data/spatial_dataset_all_maghreb.csv', countries=countries_fao, domSoils=list(DOM_mapping.keys())):
    df_maghreb_prop = pd.read_csv(path)
    cp_union = gpd.GeoDataFrame(
        df_maghreb_prop.loc[:, [
            c for c in df_maghreb_prop.columns if c not in ["geometry", "centroid"]]],
        geometry=gpd.GeoSeries.from_wkt(df_maghreb_prop["geometry"]),
        crs="EPSG:4326",
    )

    cp_union = cp_union[(cp_union['CNT_FULLNAME'].isin(
        countries)) & (cp_union['DOMSOI'].isin(domSoils))]
    return cp_union


def from_json_togeopd(data):
    study_area = json.loads(data)
    soil_data = gpd.GeoDataFrame.from_features(study_area["features"])
    soil_data.crs = "EPSG:4326"
    return soil_data
