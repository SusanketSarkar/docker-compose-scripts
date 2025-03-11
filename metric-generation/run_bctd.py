import geopandas as gpd
import os
import warnings

warnings.filterwarnings("ignore")

BUFFER_SIZES = [0.5, 1.0, 2.0]
GSD = 1.0  # Ground Sampling Distance

def compute_acc_with_gsd(gt_shp, pred_shp, buffer_size=0.5, gsd=1.0):
    gt_gdf = gpd.read_file(gt_shp)
    pred_gdf = gpd.read_file(pred_shp)

    print(f"gt: {gt_gdf.crs}, pred: {pred_gdf.crs}")

    if gt_gdf.crs != pred_gdf.crs:
        gt_gdf = gt_gdf.to_crs(pred_gdf.crs)

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

def process_dataset(main_folder):
    datasets = [d for d in os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, d))]

    for dataset in datasets:
        dataset_path = os.path.join(main_folder, dataset)
        gt_folder = os.path.join(dataset_path, "Ground_Truth")
        result_folder = os.path.join(dataset_path, "Results", "test_bctd")

        gt_toes = os.path.join(gt_folder, "GT_Toes.shp")
        gt_crests = os.path.join(gt_folder, "GT_Crests.shp")

        pred_toes = os.path.join(result_folder, "Toes.shp")
        pred_crests = os.path.join(result_folder, "Crests.shp")

        print(f"\n===== Dataset: {dataset} =====")

        if os.path.exists(gt_toes) and os.path.exists(pred_toes):
            compute_metrics(gt_toes, pred_toes, "Toes")
        else:
            print(os.path.exists(gt_toes))
            print(os.path.exists(pred_toes))
            print("  Toe shapefiles missing."+gt_toes+pred_toes)

        if os.path.exists(gt_crests) and os.path.exists(pred_crests):
            compute_metrics(gt_crests, pred_crests, "Crests")
        else:
            print("  Crest shapefiles missing.")

if __name__ == "__main__":
    main_folder_path = "D:/Jay/bench-analytics-generation/files/"
    process_dataset(main_folder_path)
