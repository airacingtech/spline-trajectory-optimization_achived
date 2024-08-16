from pathlib import Path
from argparse import ArgumentParser
from zipfile import ZipFile
import pandas as pd
from pymap3d import enu2geodetic
from io import StringIO
from datetime import datetime

def convert_enu_to_gps(enu_fp : str) -> pd.DataFrame:
    enu_df = pd.read_csv(enu_fp, header=None, skiprows=1)
    header = ''
    with open(enu_fp, 'r') as f:
        header = f.readline().strip().split(',')
    lat, lon, alt = enu2geodetic(enu_df[0], enu_df[1], enu_df[2], float(header[-3]), float(header[-2]), float(header[-1]))
    gps_df = pd.DataFrame({'latitude': lat, 'longitude': lon, 'altitude': alt})
    return gps_df

def main(input_fp: Path, glob_pattern : str):
    # Get all csv files in input folder
    csv_files = list(input_fp.glob(glob_pattern))
    parents = set([fp.relative_to(input_fp).parent for fp in csv_files])
    timestamp = datetime.now().strftime("%m-%d_%H:%M:%S")
    for parent in parents:
        with ZipFile(f'{parent}ttls_ky_{timestamp}.zip', 'w') as zip:
            for fp in list(filter(lambda x: x.relative_to(input_fp).parent == parent, csv_files)):
                df = convert_enu_to_gps(fp)
                zip.writestr(fp.name, StringIO(df.to_csv(index=False)).getvalue())

if __name__ == "__main__":
    parser = ArgumentParser(description='Generate GPS Visualizer Zip Files')
    parser.add_argument('-i', '--input_fp', type=Path, help='Input folder to look at', default=Path("ttls"))
    parser.add_argument('-g', '--glob_str', type=str, help='Glob string to use', default='**/*.csv')
    args = parser.parse_args()
    main(args.input_fp, args.glob_str)