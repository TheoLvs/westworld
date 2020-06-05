

from collections import defaultdict

import datetime
import pandas as pd
import json
import matplotlib.pyplot as plt
import plotly.io as pio
import visdom
import webbrowser

plt.style.use("bmh")
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.grid'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False



class Logger:

    def __init__(self,use_visdom = False,graphs = None,freq_update = 1):
        
        self.data = defaultdict(list)
        self.use_visdom = use_visdom
        self.graphs = graphs
        self._clock_ref = None
        self._clock = 0
        self._freq_update = freq_update

        if use_visdom:
            self.init_visdom_server()


    @property
    def df(self):
        return pd.DataFrame(self.data)


    def init_visdom_server(self):
        self.visdom_server = visdom.Visdom()

    def __getitem__(self,key):
        return self.data[key]

    @staticmethod
    def open_visdom_interface():
        webbrowser.open('http://localhost:8097')


    def log_metric(self,name,value = None):

        if isinstance(name,dict):
            for k,v in name.items():
                self.log_value(k,v)
        else:

            if self.use_visdom:

                if self._clock_ref is None:
                    self._clock_ref = name

                if name == self._clock_ref:
                    self._clock += 1

                if self._clock % self._freq_update == 0:
                    self.send_visdom_server()

            
            self.data[name].append(value)


    # def make_data_plotly(self,cols = None,data = None):
    #     if cols is None: cols = list(self.data.keys())
    #     if not isinstance(cols,list): cols = [cols]
    #     if data is None:
    #         data = pd.DataFrame.from_dict(self.data,orient = "index").T.dropna()
    #     return data[cols].melt()


    # def show_plotly(self,cols,data = None,kind = "line",return_fig = False,return_dict = False):
    #     if not isinstance(cols,list): cols = [cols]

    #     if kind == "line":
    #         data = self.make_data_plotly(cols,data)
    #         fig = px.line(data,y = "value",color = "variable")
    #         if return_fig:
    #             return fig
    #         elif return_dict:
    #             return json.loads(fig.to_json())
    #         else:
    #             fig.show()

    @staticmethod
    def _make_line_trace(y,name = "trace"):
        if len(y) == 0:
            raise Exception("Empty sequence to plot, you are probably request the wrong key from the data defaultdict")
        x = list(range(len(y)))
        y = list(y)
        trace = dict(
            x=x, 
            y=y,
            mode="lines", 
            name=name,
            type="scatter",
        )
        return trace

    @staticmethod
    def _make_layout_dict(title,xaxis = "x",yaxis = "y"):
        layout = dict(title=title, xaxis={'title': xaxis}, yaxis={'title': yaxis})
        return layout


    def make_line_chart(self,cols = None,title = None,return_dict = False,return_visdom = False):
        # Remark, plotly express is too slow we have to use the original API 

        if cols is None: cols = list(self.data.keys())
        if not isinstance(cols,list): cols = [cols]

        if title is None:
            title = f"Evolution of metrics: {', '.join(cols)}"

        traces = [self._make_line_trace(self.data[col],col) for col in cols]
        layout = self._make_layout_dict(title,"Step","Value")
        data = {"data":traces,"layout":layout,"win":title}


        if return_visdom:
            self.send_visdom_data(data)
        elif return_dict:
            return data
        else:
            return pio.show(data)


    def send_visdom_data(self,data):
        self.visdom_server._send(data)



    def send_visdom_server(self):

        if self.graphs is None:
            for name in self.data:
                self.make_line_chart(name,return_visdom = True)





    def save(self):
        pass


    def show(self,key):

        pd.Series(self[key]).plot(figsize = (15,4),title = f"Westworld logging for metric {key}")
        plt.show()


