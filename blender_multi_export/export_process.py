import os
import platform
import time
import subprocess
import shutil
import json
from typing import List, Tuple
from . import bpl
from . import config
from enum import Enum
from pathlib import Path

class TaskExportResult(Enum):
    NOT_STARTED = 1
    SUCCESS = 2
    FAIL = 3
    MISSING_DATA = 4
    SUCCESS_WITH_MULTI_ATTEMPTS = 5


class ExportTask():

    def __init__(self, blend_file: str, export_type: str):
        self.blend_file = blend_file
        self.export_type = export_type

        self.export_sucess: bool = False
        self.export_attempts: int = 0
        self.last_export_folder: Path = Path()
        self.export_result: TaskExportResult = TaskExportResult.NOT_STARTED

    def print_task(self, index: int = -1):
        if index == -1:
            string_start = "- "
        else:
            string_start = f"- ({str(index)}) - "

        print(f"{string_start}{self.export_type}, {self.blend_file}")

    def export_blend_file(self):
        # Clean
        self.export_sucess = False
        self.export_attempts = 0
        self.last_export_folder = Path()
        self.export_result = TaskExportResult.NOT_STARTED

        blend_file = os.path.basename(self.blend_file)
        print("Start export " + blend_file)
        start_time = time.time()  # Heure de début de l'export

        new_folder: Path = create_unique_folder(config.export_folder, "export_anim")
        self.last_export_folder = new_folder

        # Relative script path
        test_file_path = Path(__file__).parent / "python_scripts/test_blender_script.py"
        skeletal_mesh_file_path = Path(__file__).parent / "python_scripts/skeletal_mesh_blender_script.py"
        static_mesh_file_path = Path(__file__).parent / "python_scripts/static_mesh_blender_script.py"
        animation_file_path = Path(__file__).parent / "python_scripts/animation_blender_script.py"


        if self.export_type == "TEST":
            result, attempts = open_blend_file_and_execute_command(self.blend_file, test_file_path, new_folder)
        elif self.export_type == "SKELETAL_MESH":
            result, attempts = open_blend_file_and_execute_command(self.blend_file, skeletal_mesh_file_path, new_folder)
        elif self.export_type == "STATIC_MESH":
            result, attempts = open_blend_file_and_execute_command(self.blend_file, static_mesh_file_path, new_folder)
        elif self.export_type == "ANIMATIONS":
            result, attempts = open_blend_file_and_execute_command(self.blend_file, animation_file_path, new_folder)
        else:
            print("Unknown export type: " + self.export_type)
            result = False
            attempts = 0
        self.export_attempts = attempts
        
        end_time = time.time()  # Heure de fin de l'export
        elapsed_time = end_time - start_time  # Durée écoulée en secondes
        print(f"Export finished in {elapsed_time:.2f}s")

        info_file_path = os.path.abspath(os.path.join(new_folder, "ImportAssetData.json"))
        print("->", blend_file, info_file_path)

        # Vérifier si le fichier existe
        if result:
            if os.path.isfile(info_file_path):  # Vérification stricte pour un fichier
                if attempts == 1:
                    self.export_sucess = True
                    self.export_result = TaskExportResult.SUCCESS
                else:
                    self.export_sucess = True
                    self.export_result = TaskExportResult.SUCCESS_WITH_MULTI_ATTEMPTS
            else:
                self.export_sucess = False
                self.export_result = TaskExportResult.MISSING_DATA
        else:
            self.export_sucess = False
            self.export_result = TaskExportResult.FAIL



class ExportTasks():

    def __init__(self):
        self.tasks: List[ExportTask]  = []
        self.debug_export_first_file_only = False

    def add_task(self, blend_file: str, export_type: str):
        self.tasks.append(ExportTask(blend_file, export_type))

    def print_task_list(self):
        if len(self.tasks) > 0:
            for x, task in enumerate(self.tasks):
                task.print_task(x)
        else:
            print("No tasks found!")
        

    def perform_exports(self):
        clear_export_folder()
        timer = bpl.utils.CounterTimer()
        for task in self.tasks:
            task.export_blend_file()
            if self.debug_export_first_file_only:
                return timer.get_str_time()
        return timer.get_str_time()

    def print_import_commands(self):
        for task in self.tasks:
            if task.export_sucess:
                import_command = os.path.abspath(os.path.join(task.last_export_folder, "import_asset_script.py"))
                print('py "{0}"'.format(import_command))

    def get_exported_animation_stats(self):
        total_assets = 0
        total_frames = 0

        for x, task in enumerate(self.tasks):
            asset_count = 0
            frames_count = 0

            info_file_path = os.path.abspath(os.path.join(task.last_export_folder, "ImportAssetData.json"))
            if os.path.exists(info_file_path):
                with open(info_file_path, 'r') as json_file:
                    data = json.load(json_file)
                    assets = data.get("assets", [])
                    info = data.get("info", {})

                    asset_count = len(assets)
                    total_assets += asset_count

                    for asset in assets:
                        start_frame = asset.get("animation_start_frame", 0)
                        end_frame = asset.get("animation_end_frame", 0)
                        frames_count += (end_frame - start_frame)
                        total_frames += frames_count
            
            if task.export_result == TaskExportResult.SUCCESS:
                export_result = "SUCCESS"
            elif task.export_result == TaskExportResult.SUCCESS_WITH_MULTI_ATTEMPTS:
                export_result = f"SUCCESS With multiple {str(task.export_attempts)} attempt(s)"
            elif task.export_result == TaskExportResult.MISSING_DATA:
                export_result = "MISSING_DATA"
            elif task.export_result == TaskExportResult.FAIL:
                export_result = "FAIL"
            else: 
                export_result = "Unknow: " + str(task.export_result)

            animation_stat = f"-> {task.blend_file} - {export_result} \n Source: {task.last_export_folder} - {asset_count} assets, {frames_count} frames total"
            
            if task.export_result == TaskExportResult.SUCCESS:
                print(bpl.color_set.green(animation_stat))
            elif task.export_result == TaskExportResult.SUCCESS_WITH_MULTI_ATTEMPTS:
                print(bpl.color_set.yellow(animation_stat))
            elif task.export_result == TaskExportResult.MISSING_DATA:
                print(bpl.color_set.yellow(animation_stat))
            else:
                print(bpl.color_set.red(animation_stat))

        return total_assets, total_frames

def create_export_tasks(export_config: List[Tuple[str, str]]) -> ExportTasks:
    export_tasks = ExportTasks()

    for export_folder, export_type in export_config:
        if not os.path.isdir(export_folder):
            print(f"Le dossier spécifié n'existe pas : {export_folder}")

        for root, _, files in os.walk(export_folder):  # dirs non utilisé ici
            for file in files:
                print(file)
                if file.endswith('.blend'):
                    blend_file = os.path.abspath(os.path.join(root, file))
                    export_tasks.add_task(blend_file, export_type)
                    print(f"Tâche ajoutée pour : {blend_file}")
    return export_tasks

def clear_export_folder():
    export_folder = config.export_folder
    if os.path.exists(export_folder):
        shutil.rmtree(export_folder)
    os.makedirs(export_folder)

def create_unique_folder(base_folder: str, prefix: str) -> Path:
    folder_exists = True
    folder_number = 1
    folder_path: Path = Path()
    while folder_exists:
        folder_name = f"{prefix}_{folder_number}"
        folder_path = Path(base_folder) / folder_name
        if not folder_path.exists():
            folder_path.mkdir(parents=True)
            folder_exists = False
        else:
            folder_number += 1
    return folder_path

def get_blender_executable() -> str:
    current_system = platform.system()
    if current_system == "Windows":
        return "D:/SteamLibrary/steamapps/common/Blender/blender.exe"
    elif current_system == "Linux":
        return "/media/bleuraven/Game & Data ALT (SSD)/SteamLibrary/steamapps/common/Blender/blender-launcher"
    else:
        return "blender"

def open_blend_file_and_execute_command(blend_file_path: str, script_path: Path, output_folder: Path) -> Tuple[bool, int]:
    blender_executable = get_blender_executable()
 
    # Définir une variable d'environnement pour passer le dossier de sortie
    env = os.environ.copy()
    env['BLENDER_EXPORT_OUTPUT_FOLDER'] = str(output_folder.resolve())
    
    # Construire la commande pour ouvrir le fichier Blender et exécuter le script
    blender_command: List[str] = [
        blender_executable,
        "--background",
        blend_file_path,
        "--python",
        str(script_path.resolve())
    ]
    print("Running command:", " ".join(blender_command))
    print("Output folder:", str(output_folder.resolve()))

    max_attempts: int = 10
    attempts: int = 0

    while attempts < max_attempts:
        attempts += 1
        # Exécuter la commande Blender en tant que processus externe
        print(f"Attempt {attempts}/{max_attempts}...")
        result = subprocess.run(blender_command, capture_output=True, text=True, env=env)

        # Vérifier s'il y a des erreurs Python même si le code de retour est 0
        has_python_error = (
            "SyntaxError:" in result.stderr or 
            "SyntaxError:" in result.stdout or
            "Traceback (most recent call last):" in result.stderr or
            "Traceback (most recent call last):" in result.stdout or
            "Error:" in result.stderr or
            "Exception:" in result.stderr
        )

        if result.returncode == 0 and not has_python_error:
            print("Script executed successfully")
            return True, attempts
        else:
            # Afficher les logs détaillés uniquement en cas d'erreur
            print("=" * 50)
            print(f"Return code: {result.returncode}")
            print("STDOUT:")
            print(result.stdout)
            print("STDERR:")
            print(result.stderr)
            print("=" * 50)
            
            if has_python_error:
                print("Python error detected in Blender output!")
            if result.returncode != 0:
                print(f"Blender failed with return code {result.returncode}")
            print("Script execution failed")
            
    print("All attempts failed.")
    return False, attempts
    

