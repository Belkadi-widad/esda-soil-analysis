
import os


def interactiveMap(mx, column="DOMSOI", schema=None, k=5,   tooltip="DOMSOI", color_palette="viridis_r", path='./data/DOM_choro.html'):
    if os.path.exists(f".{path}") == False:
        if schema is None:
            fig = mx.explore(column=column,
                             tooltip=tooltip,
                             popup=True,
                             tiles="CartoDB positron",
                             k=k,
                             cmap=color_palette,
                             style_kwds=dict(color="black")
                             )
        else:
            fig = mx.explore(column=column,
                             scheme=schema,
                             tooltip=tooltip,
                             popup=True,
                             k=k,
                             tiles="CartoDB positron",
                             cmap=color_palette,
                             style_kwds=dict(color="black")
                             )

        fig.save(f".{path}")
    return f".{path}"
