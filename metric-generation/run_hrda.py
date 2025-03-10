import geopandas as gpd
import os
import warnings

warnings.filterwarnings("ignore")

BUFFER_SIZES = [0.5, 1.0, 2.0]
GSD = 1.0  # Ground Sampling Distance


def compute_acc_with_gsd(gt_shp, pred_shp, buffer_size=0.5, gsd=1.0):
    gt_gdf = gpd.read_file(gt_shp)
    pred_gdf = gpd.read_file(pred_shp)

    gt_gdf = gt_gdf[gt_gdf.geometry.type == "LineString"]
    pred_gdf = pred_gdf[pred_gdf.geometry.type == "LineString"]

    pred_buffer = pred_gdf.geometry.buffer(buffer_size)

    total_gt_points = 0
    points_inside_buffer = 0

    for line in gt_gdf.geometry:
        line_length = line.length
        num_points = int(line_length / gsd)
        sampled_points = [line.interpolate(i * gsd) for i in range(num_points)]

        for pt in sampled_points:
            if any(pred_buffer.contains(pt)):
                points_inside_buffer += 1

        total_gt_points += len(sampled_points)

    acc = points_inside_buffer / total_gt_points if total_gt_points > 0 else 0
    return round(acc, 4)

def compute_metrics(gt_path, pred_path, label):
    print(f"\nMetrics for {label}:")
    for buffer in BUFFER_SIZES:
        acc = compute_acc_with_gsd(gt_path, pred_path, buffer_size=buffer, gsd=GSD)
        print(f"  Accuracy @{buffer}m buffer: {acc}")