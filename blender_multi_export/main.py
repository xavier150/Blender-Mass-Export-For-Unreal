from . import bpl
from . import bpl
from . import config_user_Input
from . import export_process



def main():
    bpl.advprint.print_simple_title("Blender Multi Export")
    bpl.console_utils.clear_console()
    start_export()

def start_export():

    # export_folders = ["M:/MMVS_ProjectFiles/Other/BlenderMultiExport/test_file"]
    bpl.console_utils.clear_console()
    export_config = config_user_Input.get_export_list()
    print("----")
    export_list = export_process.create_export_tasks(export_config)
    export_list.print_task_list()
    print("----")
    #export_list.debug_export_first_file_only = True
    export_time_str = export_list.perform_exports()
    export_list.print_import_commands()
    total_assets, total_frames = export_list.get_exported_animation_stats()

    print()
    print(f"Total number of files: {str(len(export_list.tasks))}")
    print(f"Total assets in all files: {total_assets}")
    print(f"Total number of frames: {total_frames}")
    print(f"Total export time: " + export_time_str)