print('######### PREPARE BLENDER SCENE (ANIMATIONS) #########')
import bpy
import os
from pathlib import Path

# Récupérer le dossier de sortie depuis la variable d'environnement
output_folder_env = os.environ.get('BLENDER_EXPORT_OUTPUT_FOLDER')
if output_folder_env:
    new_folder = Path(output_folder_env)
    print(f"Using output folder from environment: {new_folder}")
else:
    # Fallback si pas de variable d'environnement
    raise ValueError("Environment variable 'BLENDER_EXPORT_OUTPUT_FOLDER' not set.")

#bpy.ops.object.prepare_scene_for_export() #@TODO: Uncomment this line when bbpl is fixed!
bpy.context.scene.bfu_use_static_export = False
bpy.context.scene.bfu_use_static_collection_export = False
bpy.context.scene.bfu_use_skeletal_export = False
bpy.context.scene.bfu_use_animation_export = True
bpy.context.scene.bfu_use_alembic_export = False
bpy.context.scene.bfu_use_groom_simulation_export = False
bpy.context.scene.bfu_use_camera_export = False
bpy.context.scene.bfu_use_spline_export = False

bpy.context.scene.bfu_use_text_export_log = True
bpy.context.scene.bfu_use_text_import_asset_script = True
bpy.context.scene.bfu_use_text_import_sequence_script = True
bpy.context.scene.bfu_use_text_additional_data = True

bpy.context.scene.bfu_export_static_mesh_file_path = str(new_folder / "StaticMesh")
bpy.context.scene.bfu_export_skeletal_mesh_file_path = str(new_folder / "SkeletalMesh")
bpy.context.scene.bfu_export_skeletal_animation_file_path = str(new_folder / "SkeletalAnimation")
bpy.context.scene.bfu_export_alembic_file_path = str(new_folder / "Alembic")
bpy.context.scene.bfu_export_groom_file_path = str(new_folder / "Groom")
bpy.context.scene.bfu_export_camera_file_path = str(new_folder / "Sequencer")
bpy.context.scene.bfu_export_spline_file_path = str(new_folder / "Spline")
bpy.context.scene.bfu_export_other_file_path = str(new_folder)

bpy.context.scene.bfu_file_import_asset_script_name = "import_asset_script.py"
bpy.context.scene.bfu_export_selection_filter = "default"

print('######### START EXPORT #########')
bpy.ops.object.exportforunreal()
print('######### END EXPORT #########')