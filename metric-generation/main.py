import os
import tqdm
import random
import warnings

from docker_mapper import *

warnings.filterwarnings("ignore")

ITERATION_NAME = "testing-first"
BASE_DIR = "D://Mines//"
RESULT_DIR = f"D://Susanket//Haul_Road_Detection//Results//{ITERATION_NAME}"

def run_docker_mapper(input_dtm_path: str, input_smartline_path: str, output_path:str, dockerfile_path: str = "docker-compose-scripts/metric-generation/docker-compose.yml", log_file_path: str = "log.txt"):
    mapper = DockerComposeMapper(compose_file_path=dockerfile_path)

    os.environ['ENV'] = "platform"
    os.environ['CHAINAGE_DISTANCE'] = str(random.randint(5, 10))
    os.environ['VEHICLE_WIDTH'] = str(random.randint(5, 8))
    os.environ['INPUT_DTM_PATH'] = input_dtm_path
    os.environ['SHAPEFILE_DIRECTORY'] = input_smartline_path
    os.environ['SMARTLINE_OUTPUT_DIRECTORY'] = output_path

    # mapper.run_compose("docker-compose-scripts/docker-compose-hra-grad-poly-start.yml", log_file_path)



def process_files(dockerfile_path: str = "docker-compose-scripts/metric-generation/docker-compose.yml", dataset = "CIL"):
    dataset_path = os.path.join(os.path.join(BASE_DIR, dataset))

    if not os.path.exists(dataset_path):
        print(f"The dataset {dataset} doesn't exist.")

    sites = [site for site in os.listdir(dataset_path)]

    for site in sites:
        site_path = os.path.join(dataset_path, site)

        subfolders = [f for f in os.listdir(site_path) if os.path.isdir(os.path.join(site_path, f))]

        if subfolders:
            for subfolder in subfolders:
                subfolder_path = os.path.join(site_path, subfolder)
                dtm_path = os.path.join(subfolder_path, "dtm.tif")

                log_file_path = os.path.join(subfolder_path, "log.txt")

                run_docker_mapper(input_dtm_path=dtm_path, input_smartline_path="", dockerfile_path=dockerfile_path, log_file_path=log_file_path)

                
        else:
            dtm_path = os.path.join(site_path, "dtm.tif")

            log_file_path = os.path.join(subfolder_path, "log.txt")

            run_docker_mapper(dockerfile_path, log_file_path=log_file_path)


        


def get_metrics():
    process_files()


get_metrics()