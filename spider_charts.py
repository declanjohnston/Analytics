

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
import seaborn as sns
import pandas as pd
from functools import reduce

def radar_factory(num_vars, frame='circle'):
    """
    Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle', 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarTransform(PolarAxes.PolarTransform):

        def transform_path_non_affine(self, path):
            # Paths with non-unit interpolation steps correspond to gridlines,
            # in which case we force interpolation (to defeat PolarTransform's
            # autoconversion to circular arcs).
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)

    class RadarAxes(PolarAxes):

        name = 'radar'
        PolarTransform = RadarTransform

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            #self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)
        
        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.25).rotate(np.pi/6).translate(.5, .5)
                                    + self.transAxes)
                
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


def load_data():
    data = pd.read_excel("Org Value.xlsx", sheet_name = ["Draft Picks", "Prospects", "Cap Space", "F", "D", "G", "Colors"], keep_default_na=True)
    draft_picks = data["Draft Picks"]
    prospects = data["Prospects"]
    cap_space = data["Cap Space"]
    forwards = data["F"]
    defencemen = data["D"]
    goalies = data["G"]
    colors = data["Colors"]
    return draft_picks, prospects, cap_space, forwards, defencemen, goalies, colors

def clean_to_z_scores(draft_picks, prospects, cap_space, forwards, defencemen, goalies):
    # clean data
    draft_picks_z = draft_picks[["Team", "Z-score"]].rename(columns={"Z-score" : "Draft Picks"})
    prospects_z = prospects[["Team", "Z-score"]].rename(columns={"Z-score" : "Prospects"})
    cap_space_z = cap_space[["Team", "Z-score"]].rename(columns={"Z-score" : "Cap Space"})
    forwards_z = forwards[["Team", "Z-score"]].rename(columns={"Z-score" : "Forwards"})
    defencemen_z = defencemen[["Team", "Z-score"]].rename(columns={"Z-score" : "Defencemen"})
    goalies_z = goalies[["Team", "Z-score"]].rename(columns={"Z-score" : "Goalies"})
    data_frames = [defencemen_z, forwards_z, draft_picks_z, prospects_z, cap_space_z, goalies_z]
    z_scores = reduce(lambda left,right: pd.merge(left,right,on=["Team"], how='outer'), data_frames).head(32)
    
    return z_scores

def normalize_z_scores(data):
    for column in data[1:]:
        if column != "Team":
            z_scores = data[column].tolist()
            z_scores = pd.Series(map(lambda x:  x/max(map(abs,z_scores)), z_scores))
            data[column] = z_scores
    return data


if __name__ == '__main__':
    
    draft_picks, prospects, cap_space, forwards, defencemen, goalies, colors = load_data()
    z_scores = clean_to_z_scores(draft_picks, prospects, cap_space, forwards, defencemen, goalies)
    z_scores = normalize_z_scores(z_scores)
    spoke_labels = ["Defencemen", "Forwards", "Draft Picks", "Prospects", "Cap Space", "Goalies"]
    N = len(spoke_labels)
    theta = radar_factory(N, frame='polygon')
    
    for i in range(0, len(z_scores["Team"].to_list())):
        fig, axs = plt.subplots(figsize=(9, 9), nrows=1, ncols=1,
                                subplot_kw=dict(projection='radar'))
        fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

        axs.set_rgrids([-1,1], labels = ["", ""])
        axs.set_ylim(-1.5,1.5)
        axs.set_title(z_scores["Team"][i], weight='bold', size='medium', position=(0.5, 0.5),
                        horizontalalignment='center', verticalalignment='center')
        axs.plot(theta, z_scores.iloc[i].tolist()[1:],colors.iloc[i][-1])
        axs.fill(theta, z_scores.iloc[i].tolist()[1:], facecolor=colors.iloc[i][-1], alpha=0.25, label='_nolegend_')
        axs.set_varlabels(spoke_labels)

        plt.show()