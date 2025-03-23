#!/bin/bash

set -e  # Exit on error

# === Paths ===
CONFIG_PATH="/home/sim-runner/adith/ttl_generation/spline-trajectory-optimization/traj_opt_double_track.yaml"
OUTPUT_DIR="/home/sim-runner/adith/ttl_generation/generated_ttls/Atlanta_Motor_Speedway/Atlanta_Motor_Speedway_TTL/"
OUTPUT_PATH="/home/sim-runner/adith/ttl_generation/generated_ttls/Atlanta_Motor_Speedway/Atlanta_Motor_Speedway_TTL/Atlanta_Motor_Speedway_TTL.csv"


# Original input files
left_csv="/home/sim-runner/adith/ttl_generation/spline-trajectory-optimization/tracks/inner_outer_tracks/Atlanta_Motor_Speedway_raceway_nodes_interpolated_main_track_inner_track.csv"
right_csv="/home/sim-runner/adith/ttl_generation/spline-trajectory-optimization/tracks/inner_outer_tracks/Atlanta_Motor_Speedway_raceway_nodes_interpolated_main_track_outer_track.csv"
center_csv="/home/sim-runner/adith/ttl_generation/spline-trajectory-optimization/tracks/inner_outer_tracks/Atlanta_Motor_Speedway_raceway_nodes_interpolated_main_track.csv"

# Output ENU CSVs
left_csv_enu="/home/sim-runner/adith/ttl_generation/spline-trajectory-optimization/tracks_enu/inner_outer_tracks/Atlanta_Motor_Speedway_raceway_nodes_interpolated_main_track_inner_track.csv"
right_csv_enu="/home/sim-runner/adith/ttl_generation/spline-trajectory-optimization/tracks_enu/inner_outer_tracks/Atlanta_Motor_Speedway_raceway_nodes_interpolated_main_track_outer_track.csv"
center_csv_enu="/home/sim-runner/adith/ttl_generation/spline-trajectory-optimization/tracks_enu/inner_outer_tracks/Atlanta_Motor_Speedway_raceway_nodes_interpolated_main_track.csv"

# Cleaned intermediate files (in tracks_enu folder for inspection)
clean_left_csv="/home/sim-runner/adith/ttl_generation/spline-trajectory-optimization/tracks_enu/inner_outer_tracks/cleaned_left.csv"
clean_right_csv="/home/sim-runner/adith/ttl_generation/spline-trajectory-optimization/tracks_enu/inner_outer_tracks/cleaned_right.csv"
clean_center_csv="/home/sim-runner/adith/ttl_generation/spline-trajectory-optimization/tracks_enu/inner_outer_tracks/cleaned_center.csv"

# === Origin and Filtering Parameters ===
LAT=33.3822085
LON=-84.321063
ALT=0.0
THRESH=100.0

# === Make sure output directory exists ===
mkdir -p "$(dirname "$left_csv_enu")"
mkdir -p "$OUTPUT_DIR"

# === Preprocess: remove header and first column, add alt = 0.0, ensure valid rows ===
awk -F',' 'NR > 1 && NF >= 3 && $2 != "" && $3 != "" {gsub(/[\r\n]+/, "", $2); gsub(/[\r\n]+/, "", $3); print $2 "," $3 ",0.0"}' "$left_csv" > "$clean_left_csv"
awk -F',' 'NR > 1 && NF >= 3 && $2 != "" && $3 != "" {gsub(/[\r\n]+/, "", $2); gsub(/[\r\n]+/, "", $3); print $2 "," $3 ",0.0"}' "$right_csv" > "$clean_right_csv"
awk -F',' 'NR > 1 && NF >= 3 && $2 != "" && $3 != "" {gsub(/[\r\n]+/, "", $2); gsub(/[\r\n]+/, "", $3); print $2 "," $3 ",0.0"}' "$center_csv" > "$clean_center_csv"

# === Process cleaned CSVs into ENU coordinates ===
python3 /home/sim-runner/adith/ttl_generation/spline-trajectory-optimization/helper_scripts.py/process_track.py \
    --input_file "$clean_left_csv" --output_file "$left_csv_enu" \
    --origin_lat $LAT --origin_lon $LON --origin_alt $ALT --threshold $THRESH

python3 /home/sim-runner/adith/ttl_generation/spline-trajectory-optimization/helper_scripts.py/process_track.py \
    --input_file "$clean_right_csv" --output_file "$right_csv_enu" \
    --origin_lat $LAT --origin_lon $LON --origin_alt $ALT --threshold $THRESH

python3 /home/sim-runner/adith/ttl_generation/spline-trajectory-optimization/helper_scripts.py/process_track.py \
    --input_file "$clean_center_csv" --output_file "$center_csv_enu" \
    --origin_lat $LAT --origin_lon $LON --origin_alt $ALT --threshold $THRESH

# === Update YAML config with new paths ===
python3 -c "
import yaml
with open('$CONFIG_PATH') as f:
    data = yaml.safe_load(f)
data['left_boundary'] = '$left_csv_enu'
data['right_boundary'] = '$right_csv_enu'
data['centerline'] = '$center_csv_enu'
data['output'] = '$OUTPUT_PATH'
with open('$CONFIG_PATH', 'w') as f:
    yaml.safe_dump(data, f)
"



# === Run the tool ===
traj_opt_double_track 

# === Append origin (lat, lon, alt) to only the first line of the final TTL CSV ===
echo "📄 Appending origin to first line of: $OUTPUT_PATH"

if [ -f "$OUTPUT_PATH" ]; then
    tmp_output="${OUTPUT_PATH}.tmp"
    awk -v lat="$LAT" -v lon="$LON" -v alt="$ALT" 'BEGIN{FS=OFS=","}
        NR==1 {print $0, lat, lon, alt; next}
        {print}
    ' "$OUTPUT_PATH" > "$tmp_output"
    mv "$tmp_output" "$OUTPUT_PATH"
    echo "✅ First row updated with origin: $LAT, $LON, $ALT"
else
    echo "❌ Output file not found: $OUTPUT_FILE"
    exit 1
fi

python3 /path/to/add_normals.py -i "$OUTPUT_DIR"


echo "Added Normals
