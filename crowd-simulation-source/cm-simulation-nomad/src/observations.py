'''
Created on 1 Mar 2015

@author: quangv
'''

import matplotlib.pyplot as plt
import numpy as np
import constants


class ObservationPlots:

#http://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
# for observation legend plotting techniques

    def __init__(self, sampling_frequency, parameters):
        self.sampling_frequency = sampling_frequency
        self.parameters = parameters
        self.t_values = list()
        
        self.flowrates = list()
        self.total_escaped = list() #list by time the number of people escaped

    def add_sample(self, t, flowrate=None, total_escaped =None):
        
        self.t_values.append(t)
        self.flowrates.append(flowrate)
        self.total_escaped.append(total_escaped)

    def _create_plot(self, title, xlabel, ylabel):
        fig = plt.figure()
        fig.set_size_inches(8,4)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        return fig
    
    def _annotate_plot(self, fig):

        ax = fig.gca()
        param_text = []

        param_text.append("$Children_velocity=%.2f$" % self.parameters['young_velocity_mean'])
        param_text.append("$Adult_velocity=%.2f$" % self.parameters['adult_velocity_mean'])
        param_text.append("$Elderly_velocity=%.2f$" % self.parameters['elderly_velocity_mean'])
      
        ax.text(0.98, 0.85, "\n".join(param_text),
                transform=ax.transAxes,
                verticalalignment='top',
                horizontalalignment='right',
                fontdict={'family': 'serif'},
                bbox = {'facecolor': 'w', 'edgecolor': 'w', 'alpha': 0.5},
                )
        
    def _total_escaped_time_plot(self):
        fig = self._create_plot("Number of pedestrians escaped by time", 
                "t", "pedestrians")
        plt.plot(self.t_values, self.total_escaped, label='pedestrian_number_escaped')
        self._annotate_plot(fig)
        return fig
  
    def _flowrate_plot(self):
        # Convert flowrate graph into a moving average
        average_count = int(round(constants.flowrate_moving_avg / constants.plot_sample_frequency))
        fig = self._create_plot("Flow rate (%.1f second average)" % constants.flowrate_moving_avg, "t", "pedestrians/second/metre")
        for i in range(len(self.parameters["flowrate_lines"])):
            rates = [x[i] for x in self.flowrates]
            flowrates = []
            name = "flowline %d" % i

            for i in range(len(self.flowrates)):
                start = max(0, i-average_count)
                flowrates.append(np.average(rates[start:i+1]))
            plt.plot(self.t_values, flowrates, label=name )

        self._annotate_plot(fig)
        return fig
    
    def save(self, prefix,currentTime):
        flowrate_plot = self._flowrate_plot()
        
        flowrate_plot.savefig("%s-%s-%s.pdf" % (prefix, "flowrate",currentTime),
                bbox_inches='tight')
        
        escape_number_plot = self._total_escaped_time_plot()
        escape_number_plot.savefig("%s-%s-%s.pdf" % (prefix, "escaped",currentTime),
                bbox_inches='tight')