# Drag-o-meter

Hi! This GUI app will allow you to plot data of SUMO simulations in real time. It was developed in the context of [Andrea's bachelor thesis](https://github.com/andreastedile/bachelor-thesis), which deals with aerodynamics of vehicle platoons.

## Installation

Of course, first install [SUMO](https://github.com/AdvancedNetworkingSystems/sumo), remembering to checkout branch `slipstream_device`.

The following tutorial assumes you have a fresh installation of Ubuntu 20.04, where Python 3 is present.

Install `pip`:

```
sudo apt install python3-pip
```

Install [PLEXE APIs for Python](https://github.com/michele-segata/plexe-pyapi).

Add directory `.local/bin` to PATH, appending the following line to `bashrc`:

```
export PATH=$PATH:$HOME/.local/bin
```

Clone the repository and install it:

```
git clone https://github.com/AdvancedNetworkingSystems/dragometer
cd dragometer
pip3 install .
```

## Usage

To understand the operating mode of Drag-o-meter and its API, checkout program `join.py` in the `example` directory.

Navigate to the `example` directory, open the command line and do:

```
dragometer join.py
```

A SUMO simulation about two platooning vehicles appears. The simulation is repeated twice. In the second one, the succeeding vehicle uses the Slipstream device to update its drag coefficient.

At the end of the simulations, Drag-o-meter should look as follows:

![screenshot](https://github.com/AdvancedNetworkingSystems/dragometer/blob/master/screenshot.png)

The relevant parts of `join.py` are:

- `def main(api: Dragometer = None)`: The `main` function takes the Drag-o-meter API as parameter.
- `from dragometer.dragometer import Dragometer` is used to add a type hint to the parameter. This allows to read the documentation inside the `Dragometer` module.

That's it! When writing custom programs, you are only required to have a `main` method formatted as before.

## API methods

To use the API methods, you program must have an instance object of the API, which must be passed as parameter to the `main` function (see previous section). The API methods are callable through the instance object. The following list contains all method signatures.

```
add_plot(ID)
```

- ID: str

Create a plot with the provided ID.

```
set_subplots(ID, count)
```

- ID: str
- count: int

Creates *count* subplots in a plot. This can be useful, for example, to draw different lines in the same plot. Subplots are accessed with a 0-based index.

```
set_title(ID, title)
```

- ID: str
- title: str

Sets a title to the plot.

```
set_x_axis_title(ID, title)
```

- ID: str
- title: str

Sets a title to a plot's x-axis.

```
set_y_axis_title(ID, title)
```

- ID: str
- tile: str

Sets a title to a plot's y-axis.

```
set_x_max(ID, xMax)
```

- ID: str
- xMax: float or int >= 0

Sets a plot's maximum range to *xMax*. This disables automatic rescaling of the plot's x-axis.

```
set_y_min(ID, yMin)
```

- ID: str
- yMin: float or int

Sets a plot's minimum range to *yMin*. Points plotted below *yMin* will not be visible.

```
set_y_max(ID, yMax)
```

- ID: str
- yMax: float or int

Sets a plot's maximum range to *yMax*. Points plotted above *yMax* will not be visible.

```
plot(ID, x, y, subplotIndex = 0)
```

- ID: str
- x: float or int >= 0
- y: float or int
- subplotIndex: int >= 0

Plots a point with coordinates *x* and *y* to a plot. If the plot contains subplots, it is possible to plot the point to a specific subplot by specifying its *subplotIndex*.