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
    mapper = DockerComposeMapper("docker-compose-scripts/docker-compose-bctd.yml")
    
    for dataset in ["Jayant", "Khadia", "Dudhichua", "AMPL", "SMIORE"]:
        # Get list of HLR folders for current dataset
        
        print("#" * 25)
        print(f"### Started Processing for {dataset} ###")
        print("#" * 25)
        dataset_path = 
                
        # Process each HLR folder
        for hlr_number in tqdm.tqdm(hlr_numbers):
            if os.path.exists(f"D:/INPUT-1-1/{dataset}/HLR-{hlr_number}/INPUT.shp"):
                output_path = f"D:/OUTPUT_HRA/{dataset}/hrda-test-{dataset}-{hlr_number}"

                os.environ['ENV'] = "platform"

                os.makedirs(smartline_output_path, exist_ok=True)
                # os.makedirs(centerline_output_path, exist_ok=True)
                # os.makedirs(edges_nm_output_path, exist_ok=True)
                # os.makedirs(edges_wm_output_path, exist_ok=True) 

                # Log environment variables
                log_file_path = os.path.join(smartline_output_path, f"logs_hlr_{hlr_number}.txt")
                env_var_file_path = os.path.join(smartline_output_path, f"env_variables_hlr_{hlr_number}.txt")
                    
                with open(env_var_file_path, "w") as env_file:
                    env_file.write("Environment Variables:\n")
                    env_file.write(f"ENV: {os.environ['ENV']}\n")
                    env_file.write(f"CHAINAGE_DISTANCE: {os.environ['CHAINAGE_DISTANCE']}\n") 
                    env_file.write(f"VEHICLE_WIDTH: {os.environ['VEHICLE_WIDTH']}\n")
                    env_file.write(f"INPUT_DTM_PATH: {os.environ['INPUT_DTM_PATH']}\n")
                    env_file.write(f"SHAPEFILE_DIRECTORY: {os.environ['SHAPEFILE_DIRECTORY']}\n")
                   
                 

                mapper.run_compose("docker-compose-scripts/docker-compose-hra-grad-poly-start.yml", log_file_path)

       