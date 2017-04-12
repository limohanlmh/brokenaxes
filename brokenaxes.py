import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


class BrokenAxes:
    def __init__(self, xlims=None, ylims=None, d=.015, tilt=None, subplot_spec=None, fig=None, *args, **kwargs):

        if fig is None:
            fig = plt.figure()

        if xlims:
            width_ratios = [i[1] - i[0] for i in xlims]
        else:
            width_ratios = [1]

        if ylims:
            height_ratios = [i[1] - i[0] for i in ylims[::-1]]
        else:
            height_ratios = [1]

        ncols, nrows = len(width_ratios), len(height_ratios)

        kwargs.update(ncols=ncols, nrows=nrows, height_ratios=height_ratios, width_ratios=width_ratios)
        if subplot_spec:
            gs = gridspec.GridSpecFromSubplotSpec(subplot_spec=subplot_spec, *args, **kwargs)
            self.big_ax = plt.Subplot(fig, subplot_spec)
        else:
            gs = gridspec.GridSpec(*args, **kwargs)
            self.big_ax = plt.Subplot(fig, gridspec.GridSpec(1,1)[0])

        [sp.set_visible(False) for sp in self.big_ax.spines.values()]
        self.big_ax.set_xticks([])
        self.big_ax.set_yticks([])
        self.big_ax.patch.set_facecolor('none')

        self.axs = []
        for igs in gs:
            ax = plt.Subplot(fig, igs)
            fig.add_subplot(ax)
            self.axs.append(ax)
        fig.add_subplot(self.big_ax)

        d_kwargs = dict(transform=fig.transFigure, color='k', clip_on=False)

        bounds = self.big_ax.get_position().bounds
        if tilt is None:
            tilt = bounds[2] / bounds[3]

        for i, ax in enumerate(self.axs):
            if ylims is not None:
                ax.set_ylim(ylims[::-1][i//ncols])
            if xlims is not None:
                ax.set_xlim(xlims[i % ncols])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            if not ax.is_last_row():
                ax.spines['bottom'].set_visible(False)
                ax.set_xticks([])
            elif d:
                if not ax.is_last_col():
                    xpos = ax.get_position().bounds[0] + ax.get_position().bounds[2]
                    ypos = ax.get_position().bounds[1]

                    ax.plot((xpos - d, xpos + d), (ypos - tilt * d,  ypos + tilt * d), **d_kwargs)

                if not ax.is_first_col():
                    xpos = ax.get_position().bounds[0]
                    ypos = ax.get_position().bounds[1]
                    ax.plot((xpos - d, xpos + d), (ypos - tilt * d, ypos + tilt * d), **d_kwargs)

            if not ax.is_first_col():
                ax.spines['left'].set_visible(False)
                ax.set_yticks([])

            elif d:
                if not ax.is_first_row():
                    xpos = ax.get_position().bounds[0]
                    ypos = ax.get_position().bounds[1] + ax.get_position().bounds[3]
                    ax.plot((xpos - d, xpos + d), (ypos - tilt * d, ypos + tilt * d), **d_kwargs)

                if not ax.is_last_row():
                    xpos = ax.get_position().bounds[0]
                    ypos = ax.get_position().bounds[1]
                    ax.plot((xpos - d, xpos + d), (ypos - tilt * d, ypos + tilt * d), **d_kwargs)

    def plot(self, *args, **kwargs):
        [ax.plot(*args, **kwargs) for ax in self.axs]

    def set_xlabel(self, *args, labelpad=20, **kwargs):
        self.big_ax.set_xlabel(*args, labelpad=labelpad, **kwargs)

    def set_ylabel(self, *args, labelpad=30, **kwargs):
        self.big_ax.xaxis.labelpad = labelpad
        self.big_ax.set_ylabel(*args, labelpad=labelpad, **kwargs)

    def set_title(self, *args, **kwargs):
        self.big_ax.set_title(*args, **kwargs)

    def legend(self, *args, **kwargs):
        h, l = self.axs[0].get_legend_handles_labels()
        self.big_ax.legend(h, l, *args, **kwargs)

    def axis(self, *args, **kwargs):
        [ax.axis(*args, **kwargs) for ax in self.axs]


def brokenaxes(*args, **kwargs):
    return BrokenAxes(*args, **kwargs)