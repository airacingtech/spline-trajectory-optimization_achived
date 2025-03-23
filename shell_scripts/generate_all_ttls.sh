#!/bin/bash

set -e

# === Paths ===
BASE_DIR="/home/sim-runner/adith/ttl_generation/spline-trajectory-optimization"
INPUT_DIR="$BASE_DIR/tracks/inner_outer_tracks"
CONFIG_PATH="$BASE_DIR/traj_opt_double_track.yaml"
OUTPUT_BASE="/home/sim-runner/adith/ttl_generation/generated_ttls"
ENU_DIR="$BASE_DIR/tracks_enu/inner_outer_tracks"

mkdir -p "$ENU_DIR"

for inner_file in "$INPUT_DIR"/*_inner_track.csv; do
    filename=$(basename -- "$inner_file")
    track_name="${filename%%_raceway_nodes_interpolated_centerline_main_track_inner_track.csv}"

    echo "Processing track: $track_name"

    outer_file="$INPUT_DIR/${track_name}_raceway_nodes_interpolated_centerline_main_track_outer_track.csv"
    center_file="$INPUT_DIR/${track_name}_raceway_nodes_interpolated_centerline_main_track.csv"

    left_enu="$ENU_DIR/${track_name}_raceway_nodes_interpolated_centerline_main_track_inner_track.csv"
    right_enu="$ENU_DIR/${track_name}_raceway_nodes_interpolated_centerline_main_track_outer_track.csv"
    center_enu="$ENU_DIR/${track_name}_raceway_nodes_interpolated_centerline_main_track.csv"

    clean_left="$ENU_DIR/cleaned_left.csv"
    clean_right="$ENU_DIR/cleaned_right.csv"
    clean_center="$ENU_DIR/cleaned_center.csv"

    TRACK_OUTPUT_DIR="$OUTPUT_BASE/$track_name/${track_name}_TTL"
    OUTPUT_CSV="$TRACK_OUTPUT_DIR/${track_name}_TTL.csv"

    mkdir -p "$TRACK_OUTPUT_DIR"

    # === Clean input CSVs ===
    awk -F',' 'NR > 1 && NF >= 3 && $2 != "" && $3 != "" {gsub(/[\r\n]+/, "", $2); gsub(/[\r\n]+/, "", $3); print $2 "," $3 ",0.0"}' "$inner_file" > "$clean_left"
    awk -F',' 'NR > 1 && NF >= 3 && $2 != "" && $3 != "" {gsub(/[\r\n]+/, "", $2); gsub(/[\r\n]+/, "", $3); print $2 "," $3 ",0.0"}' "$outer_file" > "$clean_right"
    awk -F',' 'NR > 1 && NF >= 3 && $2 != "" && $3 != "" {gsub(/[\r\n]+/, "", $2); gsub(/[\r\n]+/, "", $3); print $2 "," $3 ",0.0"}' "$center_file" > "$clean_center"

    # === Extract origin ===
    read LAT LON <<< $(head -n 1 "$clean_center" | awk -F',' '{print $1, $2}')
    ALT=0.0
    THRESH=100.0
    echo "Origin set to: LAT=$LAT, LON=$LON"

    # === Convert to ENU ===
    python3 "$BASE_DIR/helper_scripts.py/process_track.py" \
        --input_file "$clean_left" --output_file "$left_enu" \
        --origin_lat "$LAT" --origin_lon "$LON" --origin_alt "$ALT" --threshold "$THRESH"

    python3 "$BASE_DIR/helper_scripts.py/process_track.py" \
        --input_file "$clean_right" --output_file "$right_enu" \
        --origin_lat "$LAT" --origin_lon "$LON" --origin_alt "$ALT" --threshold "$THRESH"

    python3 "$BASE_DIR/helper_scripts.py/process_track.py" \
        --input_file "$clean_center" --output_file "$center_enu" \
        --origin_lat "$LAT" --origin_lon "$LON" --origin_alt "$ALT" --threshold "$THRESH"


    # === Update YAML config ===
    
    python3 -c "
import yaml
with open('$CONFIG_PATH') as f:
    data = yaml.safe_load(f)
data['left_boundary'] = '$left_enu'
data['right_boundary'] = '$right_enu'
data['centerline'] = '$center_enu'
data['output'] = '$OUTPUT_CSV'
with open('$CONFIG_PATH', 'w') as f:
    yaml.safe_dump(data, f)
"




    # === Run trajectory optimization tool ===
    traj_opt_double_track

    # === Add origin to first row of TTL CSV ===
    if [ -f "$OUTPUT_CSV" ]; then
        tmp_output="${OUTPUT_CSV}.tmp"
        awk -v lat="$LAT" -v lon="$LON" -v alt="$ALT" 'BEGIN{FS=OFS=","}
            NR==1 {print $0, lat, lon, alt; next}
            {print}
        ' "$OUTPUT_CSV" > "$tmp_output"
        mv "$tmp_output" "$OUTPUT_CSV"
        echo "First row updated with origin: $LAT, $LON, $ALT"
    else
        echo "Output file not found: $OUTPUT_CSV"
        exit 1
    fi

    # === Add normals ===
    python3 "$BASE_DIR/helper_scripts.py/add_normals.py" -i "$TRACK_OUTPUT_DIR"
    echo "Normals added for $track_name"

    if [ -f "ttl_optm.txt" ]; then
        mv ttl_optm.txt "$TRACK_OUTPUT_DIR/"
        echo "Moved ttl_optm.txt to $TRACK_OUTPUT_DIR/"
    else
        echo "Warning: ttl_optm.txt not found after optimization."
    fi

done

echo "All tracks processed."
