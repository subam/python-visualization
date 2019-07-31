# python-visualization

## Dependencies
* python3
* python pacakages
    * [matplotlib](https://matplotlib.org)
    * [pandas](https://pandas.pydata.org)
    * [folium](https://python-visualization.github.io/folium/#)
    * [geopy](https://geopy.readthedocs.io/en/stable/) - optional
        * needed if coordinates needs to be generated

## Required Changes when running in local

Replace the values of path variables in **core.py** in with your local absolute path for the directory.

## Creating map visualisation for a single agent

### Generating Coordinates (Optional)

*All the commads are run from the root project folder in terminal.*

```bash
python3 -m Visualisation.coordinates
```
This generates the required csv file with the geo coordinates for different locations present in **mali_localhost_16/input_csv/locations.csv** which is stored in the **output** directory.

>This is not required to run again as the file has already been included in the repo

> Running this to many time in short interval will result in timeout exception due to the limitation of openstreetmaps. Coordinates are retrived using geopy package

### Generating the single agent movement on the map

```bash
python3 -m Visualisation.visualise
```
Executing the above command will prompt you to enter the agent number. The result will be generated as a html file in output directory. A sample html output can be seen by opening **output/mali_single_agent.html** in your local machine.

> Note: Ad Blockers might prevent the map and points from being displayed. Disable them if you cannot see the points.