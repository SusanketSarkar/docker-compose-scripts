import yaml
import os
import tqdm
import random
import warnings
import subprocess

warnings.filterwarnings("ignore")

class DockerComposeMapper:
    def __init__(self, compose_file_path: str):
        self.compose_file_path = compose_file_path
        self.compose_data = self._load_compose_file()

    def _load_compose_file(self) -> dict:
        with open(self.compose_file_path, 'r') as file:
            return yaml.safe_load(file)

    def save_compose_file(self, output_path: str):
        """Saves the updated docker-compose.yml file."""
        with open(output_path, 'w') as file:
            yaml.dump(self.compose_data, file, default_flow_style=False)

    def run_compose(self, compose_file_path: str, log_file_path: str):
        """Runs the docker-compose file."""
        with open(log_file_path, "w") as log_file:
            subprocess.run(["docker-compose", "-f", compose_file_path, "up", "--build"], stdout=log_file)

if __name__ == "__main__":
    mapper = DockerComposeMapper("docker-compose-scripts/docker-compose-haul-road.yml")
    
    for hlr_number in tqdm.tqdm(range(18, 35)):
        if os.path.exists(f"D:/INPUT-1-1/Nigahi/HLR-{hlr_number}/INPUT.shp"):
            input_shapefile_folder = f"D:/INPUT-1-1/Nigahi/HLR-{hlr_number}/"
            smartline_output_path = f"D:/OUTPUT_HRA/Nigahi/hrda-test-nigahi-{hlr_number}-smartline"
            centerline_output_path = f"D:/OUTPUT_HRA/Nigahi/hrda-test-nigahi-{hlr_number}-centerline"
            edges_nm_output_path = f"D:/OUTPUT_HRA/Nigahi/hrda-test-nigahi-{hlr_number}-edges-no_median"
            edges_wm_output_path = f"D:/OUTPUT_HRA/Nigahi/hrda-test-nigahi-{hlr_number}-edges-with_median"
            os.environ['ENV'] = "platform"
            os.environ['CHAINAGE_DISTANCE'] = str(random.randint(5, 25))
            os.environ['VEHICLE_WIDTH'] = str(random.randint(5, 15))
            os.environ['INPUT_DTM_PATH'] = "D:/INPUT_HRA/Nigahi/Nigahi_dtm.tif"
            os.environ['SHAPEFILE_DIRECTORY'] = input_shapefile_folder
            os.environ['SMARTLINE_OUTPUT_DIRECTORY'] = smartline_output_path
            os.environ['CENTERLINE_OUTPUT_DIRECTORY'] = centerline_output_path
            os.environ['CENTERLINE_SHAPEFILE_DIRECTORY'] = smartline_output_path
            os.environ['EDGES_SHAPEFILE_DIRECTORY'] = smartline_output_path
            os.environ['EDGES_NM_OUTPUT_DIRECTORY'] = edges_nm_output_path
            os.environ['EDGES_WM_OUTPUT_DIRECTORY'] = edges_wm_output_path

            os.makedirs(smartline_output_path, exist_ok=True)
            os.makedirs(centerline_output_path, exist_ok=True)
            os.makedirs(edges_nm_output_path, exist_ok=True)
            os.makedirs(edges_wm_output_path, exist_ok=True)

            log_file_path = os.path.join(smartline_output_path, f"logs_hlr_{hlr_number}.txt")

            mapper.run_compose("docker-compose-scripts/docker-compose-haul-road.yml", log_file_path)

       