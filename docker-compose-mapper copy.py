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

    def run_compose(self, compose_file_path: str = "docker-compose-scripts/docker-compose-bctd.yml"):
        """Runs the docker-compose file."""
        subprocess.run(["docker-compose", "-f", compose_file_path, "up", "--build"])

if __name__ == "__main__":
    mapper = DockerComposeMapper("docker-compose-scripts/docker-compose-bctd.yml")
    
    for dataset in ["Jayant", "Khadia", "Dudhichua", "AMPL", "SMIORE"]:
        # Get list of HLR folders for current dataset
        
        print("#" * 25)
        print(f"### Started Processing for {dataset} ###")
        print("#" * 25)
        dtm_path = "" #Enter path to dtm

        for param1 in [0.5, 0.6, 0.7, 0.8, 1]:
            for param2 in [20, 30, 40]:
                for param3 in [1, 2, 3]:
                    output_path = f"D:/Jay/bctd_docker/{str(param1)}_{str(param2)}_{str(param2)}"
                    os.makedirs(output_path, exist_ok=True)
                    os.environ['ENV'] = "platform"
                    os.environ['param1'] = str(param1)
                    os.environ['param2'] = str(param2)
                    os.environ['param3'] = str(param3)

                    mapper.run_compose()