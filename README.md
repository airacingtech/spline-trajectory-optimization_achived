# spline-trajectory-optimization

**Please head over to `devel` branch for the code in the paper "Spline-Based Minimum-Curvature Trajectory Optimization for Autonomous Racing".**

Spline-based Trajectory Optimization tool for Autonomous Racing (Indy Autonomous Challenge)

## Install

1. Install `SciPy`, `matplotlib`, `shapely`, `casadi`, `bezier`.
2. For min curvature problem, install Julia 1.8.5+.
3. Clone this repository and install with `pip install -e .`.

## Run

- For min curvature problem, run `julia/spline_traj_opt.ipynb`.
- For min time problem, copy `traj_opt_double_track.yaml` in `spline_traj_optm/min_time_otpm/example` to your workspace, and execute `traj_opt_double_track`.



## Boundary generation 

if taking from emlid

original file will be all boundary in one file, in gps coordinates

1. Run emlid_to_geodetic.py to create sperate csvs for each boundary (pit, outside, etc) -> will create a csv file with latitude, longitude, and height in that order

2. Run geodetic_to_enu on the output files of 1. -> will output a file for each boundary in x y z coordinates in enu frame. make sure to set a single origin point that you use for all boundary - good practice is to just pick the first data point from the outside boundary (in gps coordinates) and use that for all the lanes

3. Run plot_track_edges.py on the output of 2. to verify that your boundaries look good. plot_track_edges.py will also generate a automatic centerline based on your inside and output boundaries, in case you dont have an existing centerline guess

4. run traj_opt_double_track.py, set the file names for your inside, outside and centerline boundaries in traj_opt_double_track.yaml
 - important take a look at safety_margin_r and safety_margin_l. If you want to make an optimal ttl, keep these equal and low (around 1 m ish) if you want to make a left lane ttl, keep safety_margin_r higher (ive used 4.5m for right and 1m for left here before), and reverse for right lane ttls - (or you can use your centerline as your new boundary and generate a new centerline from that and then use those)
 
 5. the output ot traj_opt_double_track.py will be a csv represeting tyour ttl (used in race common) and a text file also represeting your ttl (used w mpc), make sure to number them correctly - 27 is pit, 2 is left, 9 is right, 15 is optimal 
 
 
 NOTE: if the boundaries you have generated have 
 - repeated points
 - non sequential points
 - v far spaced points
 

 it will not work
 what you need to do is - use the manual spline fitting tool:https://github.com/HaoruXue/offline-trajectory-tools
 
or kunals autofit tool

NOTE: bank angle is represented in centerline csv, if there is a bank angle centerline csv should be 4 columns (w bank as last column) otherwise should j be 3 columns as usual


if taking from google earth:
first - google earth will give you a ,kml file. convert that to csv and get rid ov everything but the actual data

1. run raw_to_formatted_remove_spaces.py on the input files, and this will put them into a nice lat long z format (the kml uses lat long and seperates coordinates with space instead of new line)

2. run steps 2-4 from above



 
 
 
## Repository Organization

- `spline_traj_optm/examples`: Example inputs for the trajectory optimization (Monza)
- `spline_traj_optm/models`: Data classes for holding optimization information (race track, vehicle, and trajectory information)
- `spline_traj_optm/optimization`: Optimization functions
- `spline_traj_optm/simulator`: Quasi-Steady State (QSS) simulation of a given trajectory for optimal speed
- `spline_traj_optm/tests`: Tests for the package
- `spline_traj_optm/visualization`: Functions for visualization the optimization and simulation results
- `julia/spline_traj_opt.ipynb`: Julia notebook of the optimization notebook
