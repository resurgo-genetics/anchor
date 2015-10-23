# -*- coding: utf-8 -*-
"""See log bayes factors which led to modality categorization"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


darkblue, green, red, purple, yellow, lightblue = sns.color_palette('deep')
MODALITY_ORDER = ['~0', 'middle', '~1', 'bimodal', 'multimodal']
MODALITY_TO_COLOR = {'~0': lightblue, 'middle': yellow, '~1': red,
                     'bimodal': purple, 'multimodal': 'lightgrey'}
MODALITY_PALETTE = [MODALITY_TO_COLOR[m] for m in MODALITY_ORDER]


class _ModalityEstimatorPlotter(object):
    def __init__(self):
        self.fig = plt.figure(figsize=(5 * 2, 3 * 2))
        self.ax_violin = plt.subplot2grid((3, 5), (0, 0), rowspan=3, colspan=1)
        self.ax_loglik = plt.subplot2grid((3, 5), (0, 1), rowspan=3, colspan=3)
        self.ax_bayesfactor = plt.subplot2grid((3, 5), (0, 4), rowspan=3,
                                               colspan=1)

    def plot(self, event, logliks, logsumexps, modality_to_color,
             renamed=''):
        modality = logsumexps.idxmax()

        sns.violinplot(event.dropna(), bw=0.2, ax=self.ax_violin,
                       color=modality_to_color[modality])

        self.ax_violin.set_ylim(0, 1)
        self.ax_violin.set_title('Guess: {}'.format(modality))
        self.ax_violin.set_xticks([])
        self.ax_violin.set_yticks([0, 0.5, 1])

        for name, loglik in logliks.iteritems():
            # print name,
            self.ax_loglik.plot(loglik, 'o-', label=name,
                                color=modality_to_color[name])
            self.ax_loglik.legend(loc='best')
        self.ax_loglik.set_title('Log likelihoods at different '
                                 'parameterizations')
        self.ax_loglik.grid()
        self.ax_loglik.set_xlabel('phantom', color='white')

        for i, (name, height) in enumerate(logsumexps.iteritems()):
            self.ax_bayesfactor.bar(i, height, label=name,
                                    color=modality_to_color[name])
        self.ax_bayesfactor.set_title('$\log$ Bayes factors')
        self.ax_bayesfactor.set_xticks([])
        self.ax_bayesfactor.grid()
        self.fig.tight_layout()
        self.fig.text(0.5, .025, '{} ({})'.format(event.name, renamed),
                      fontsize=10, ha='center', va='bottom')
        sns.despine()
        return self


class ModalitiesViz(object):
    """Visualize results of modality assignments"""

    modality_order = MODALITY_ORDER
    modality_to_color = MODALITY_TO_COLOR
    modality_palette = MODALITY_PALETTE

    def bar(self, counts, phenotype_to_color=None, ax=None, percentages=True):
        """Draw barplots grouped by modality of modality percentage per group

        Parameters
        ----------


        Returns
        -------


        Raises
        ------

        """
        if percentages:
            counts = 100 * (counts.T / counts.T.sum()).T

        # with sns.set(style='whitegrid'):
        if ax is None:
            ax = plt.gca()

        full_width = 0.8
        width = full_width / counts.shape[0]
        for i, (group, series) in enumerate(counts.iterrows()):
            left = np.arange(len(self.modality_order)) + i * width
            height = [series[i] if i in series else 0
                      for i in self.modality_order]
            color = phenotype_to_color[group]
            ax.bar(left, height, width=width, color=color, label=group,
                   linewidth=.5, edgecolor='k')
        ylabel = 'Percentage of events' if percentages else 'Number of events'
        ax.set_ylabel(ylabel)
        ax.set_xticks(np.arange(len(self.modality_order)) + full_width / 2)
        ax.set_xticklabels(self.modality_order)
        ax.set_xlabel('Splicing modality')
        ax.set_xlim(0, len(self.modality_order))
        ax.legend(loc='best')
        ax.grid(axis='y', linestyle='-', linewidth=0.5)
        sns.despine()

    def event_estimation(self, event, logliks, logsumexps, renamed=''):
        """Show the values underlying bayesian modality estimations of an event

        Parameters
        ----------


        Returns
        -------


        Raises
        ------
        """
        plotter = _ModalityEstimatorPlotter()
        plotter.plot(event, logliks, logsumexps, self.modality_to_color,
                     renamed=renamed)
        return plotter