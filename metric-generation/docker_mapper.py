import yaml
import subprocess

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

    def run_compose(self, log_file_path: str):
        """Runs the docker-compose file."""
        with open(log_file_path, "w") as log_file:
            subprocess.run(["docker-compose", "-f", self.compose_file_path, "up", "--build"], stdout=log_file)