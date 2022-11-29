import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff


def get_random_colors(N):
    c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]
    return c


def Histogram(df, x="CNT_FULLNAME",  nbins=20,  order_labels=[], sorted="", hover_name="", hover_data={}):

    fig = px.histogram(df, x=x, nbins=nbins,
                       category_orders=dict(x=order_labels))
    if sorted in ['total descending', 'total ascending']:
        fig = fig.update_xaxes(categoryorder=sorted)
    return fig

# points can be all or outliers


def BoxPlot(df,  y, x="", color="", points='all'):
    fig = px.box(df, y=y,  points=points)
    if x is not None:
        fig.update_traces(x=x)
    # if color is not None:
    #     fig.update_traces(color=color)
    return fig


def ScatterPlot(df, x, y, color="", size="", hover_data=[]):

    fig = px.scatter(df, x=x, y=y)
    # if color is not None:
    #     fig.update_traces(color=color)
    # if size is not None:
    #     fig.update_traces(size=size)
    # if hover_data is not None:
    #     fig.update_traces(hover_data=hover_data)
    return fig


def BoxPlotMultipleY(df, y_columns=[], x=None):
    fig = go.Figure()
    colors = get_random_colors(len(y_columns))
    i = 0
    for y in y_columns:
        data = df[y]
        fig.add_trace(go.Box(y=data, name=y,  marker_color=colors[i], x=x
                             ))
        i = i+1
    fig.update_traces(boxpoints='all', jitter=0)
    if x is not None:
        fig.update_layout(boxmode='group')
    return fig


def CorrelationHeatMap(df, target_col, cols):
    df_corr_round = df.corr(numeric_only=True)[[target_col]].T[cols].T.round(2)
    fig_cor = ff.create_annotated_heatmap(
        z=df_corr_round.to_numpy(),
        x=df_corr_round.columns.tolist(),
        y=df_corr_round.index.tolist(),
        zmax=1,
        zmin=-1,
        showscale=True,
        hoverongaps=True,
        ygap=3,
    )
    fig_cor.update_layout(
        yaxis=dict(showgrid=False),
        xaxis=dict(showgrid=False),
        legend=dict(orientation="h", yanchor="bottom",
                    y=1.02, xanchor="right", x=1),
    )
    # fig_cor.update_layout(yaxis_tickangle=-45)
    fig_cor.update_layout(xaxis_tickangle=0)
    fig_cor.update_layout(title_text="", height=550)  #
    return fig_cor
