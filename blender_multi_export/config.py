import os
import platform
import tempfile
from typing import Dict, Tuple, Optional, List

blender_executable = "chemin_vers_blender_executable"  # Remplacez par le chemin vers l'exécutable Blender sur votre système
export_folder = os.path.join(tempfile.gettempdir(), "ExportFolder")

default_source_content_paths = {
    "Windows": "M:/MMVS_ProjectFiles_v2/SourceAssets/",
    "Linux": "/media/bleuraven/Macro Micro VR Service/MMVS_ProjectFiles_v2/SourceAssets/"
}

def get_content_folder():
    config_folder = os.getenv("MMVS_SOURCE_CONTENT_FOLDER")
    if not config_folder:
        current_system = platform.system()
        config_folder = default_source_content_paths.get(current_system, "")
    return config_folder

def get_content_path(relatif_path: str) -> str:
    source_content = get_content_folder()
    full_path = os.path.abspath(os.path.join(source_content, relatif_path))
    return full_path

export_list: Dict[str, Dict[str, Tuple[str, str]]] = {
    "Export test": {
        # Character
        #"Talas_StandUpStomp": ("M:/MMVS_ProjectFiles_v2/SourceAssets/Talas_StandUpStomp/Actions/stompagain", "ANIMATIONS"),

    },
    "Character Meshs": {
        "Cobble_MESHS": (get_content_path("Characters/Cobble_Character/Rig/v4"), "SKELETAL_MESH"),
        "Talas_MESHS": (get_content_path("Characters/Talas_Character/Rig/v4"), "SKELETAL_MESH"),
        "MMVS_Character_MESHS": (get_content_path("Characters/MMVS_Character/Rig/v4"), "SKELETAL_MESH"),
        "Tesy_MESHS": (get_content_path("Characters/Tesy_Character/Rig/v4"), "SKELETAL_MESH"),
    },   
    "Talas Shoes Skeletal Meshs": {
        "Talas_WinterShoes_MESHS": (get_content_path("Characters/Talas_WinterShoes/Rig/v4"), "SKELETAL_MESH"),
    },
    "Talas Shoes Static Meshs": {
        "Talas_WinterShoes_MESHS": (get_content_path("Characters/Talas_WinterShoes/Meshes"), "STATIC_MESH"),
    },
    "Other Meshs": {
        "TagDigestiveSystem_MESHS": (get_content_path("TagDigestiveSystem/Rig/v3"), "SKELETAL_MESH"),
        "CozyHouseDynamicDoor_MESHS": (get_content_path("Talas_CozyHouseDoor/CozyHouseDynamicDoor/Rig/v3"), "SKELETAL_MESH"),
        "ToyCar_MESHS": (get_content_path("Vehicles/CobbleToyCar"), "SKELETAL_MESH"),
    },
    "Character Animations": {
        "CharactersSituations": (get_content_path("CharactersSituations"), "ANIMATIONS"),
        "Cobble": (get_content_path("Characters/Cobble_Character/Animation"), "ANIMATIONS"),
        "Talas": (get_content_path("Characters/Talas_Character/Animation"), "ANIMATIONS"),
    },
    "Talas StandUp Actions": {
        "Talas_StandUpVore": (get_content_path("Talas_StandUpVore"), "ANIMATIONS"),
        "Talas_MawExhibition": (get_content_path("Talas_MawExhibition"), "ANIMATIONS"),
        "Talas_StandUpStomp": (get_content_path("Talas_StandUpStomp"), "ANIMATIONS"),
        "Talas_StandUpGrab": (get_content_path("Talas_StandUpGrab"), "ANIMATIONS"),
        "Talas_StandAgaintWall": (get_content_path("Talas_StandAgaintWall"), "ANIMATIONS"),
        "Talas_CheckSole": (get_content_path("Talas_CheckSole"), "ANIMATIONS"),
        "Talas_Reacts": (get_content_path("Talas_Reacts"), "ANIMATIONS"),
        "Talas_BodyReacts": (get_content_path("Talas_BodyReacts"), "ANIMATIONS"),
    },
    "Talas Indoor Scenes": {
        "Talas_SofaTable": (get_content_path("Talas_SofaTable"), "ANIMATIONS"),
        "Talas_RoomBed": (get_content_path("Talas_RoomBed"), "ANIMATIONS"),
        "Talas_SitOnFloor": (get_content_path("Talas_SitOnFloor"), "ANIMATIONS"),
        "Talas_Armchair": (get_content_path("Talas_Armchair"), "ANIMATIONS"),
        "Talas_WoodenChair": (get_content_path("Talas_WoodenChair"), "ANIMATIONS"),
    },
    "Cobble Items": {
        "Cobble_CageBed": (get_content_path("Cobble_CageBed"), "ANIMATIONS"),
        "Cobble_ToyCar": (get_content_path("Vehicles/CobbleToyCar/CobbleAnimations"), "ANIMATIONS"),
    },
    "Talas Items": {
        "TalasWinterShoe": (get_content_path("Items/TalasWinterShoe"), "ANIMATIONS"),
        "Talas_CozyHouseDoor": (get_content_path("Talas_CozyHouseDoor/Animations"), "ANIMATIONS"),
    }
}

def get_export_items() -> Dict[str, List[Tuple[str, str]]]:

    comput_export_dict: Dict[str, List[Tuple[str, str]]] = {}

    # - Create item with all links.
    def get_all_item(filter_type: Optional[str] = None) -> List[Tuple[str, str]]:
        all_found_item: List[Tuple[str, str]] = []
        for export_list_key in export_list:
            export_group = export_list[export_list_key]

            if len(export_group) > 1:           
                for item_key in export_group:
                    folder_path = export_group[item_key][0]
                    export_type = export_group[item_key][1]
                    if filter_type:
                        if filter_type == export_type:
                            all_found_item.append((folder_path, export_type))
                    else:
                        all_found_item.append((folder_path, export_type))
        return all_found_item
    
    comput_export_dict["ALL"] = get_all_item()
    comput_export_dict["ALL - ANIMATIONS"] = get_all_item("ANIMATIONS")
    comput_export_dict["ALL - SKELETAL_MESH"] = get_all_item("SKELETAL_MESH")


    for export_list_key in export_list:
        export_group = export_list[export_list_key]
        if len(export_group) > 1:
            # - Create item with all links per group.
            all_found_group_item: List[Tuple[str, str]] = []
            for item_key in export_group:
                folder_path = export_group[item_key][0]
                export_type = export_group[item_key][1]
                all_found_group_item.append((folder_path, export_type))
            group_name = "[" + export_list_key + "] - ALL"
            comput_export_dict[group_name] = all_found_group_item
        
        # - Create item with individual links.
        for item_key in export_group:
            folder_path = export_group[item_key][0]
            export_type = export_group[item_key][1]
            item_name = "[" + export_list_key + "] - " + item_key + " -> " + export_type
            comput_export_dict[item_name] = [(folder_path, export_type)]

    return comput_export_dict