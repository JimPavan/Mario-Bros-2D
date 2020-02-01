from Constants import *


def level_0():
    decors = [
##        [0, 0, 32, 436, Bush_one_img],
##        [0, 0, 128, 436, Bush_one_img],
        
        [0, 0, 64, 32, cloud_tree_img],
        [0, 0, 200, 96, cloud_tree_img],
        [0, 0, 700, 40, cloud_tree_img],
        [0, 0, 1500, 36, cloud_tree_img],
        [0, 0, 2000, 88, cloud_tree_img],
        [0, 0, 900, 55, cloud_tree_img],
        [0, 0, 1300, 77, cloud_tree_img],
        [0, 0, 2200, 25, cloud_tree_img],
        [0, 0, 2500, 50, cloud_tree_img],
        [0, 0, 500, 95, cloud_tow_img],
        [0, 0, 1700, 96, cloud_tow_img],
        [0, 0, 1100, 130, cloud_tow_img],
        [0, 0, 880, 90, cloud_tow_img],
        [0, 0, 2240, 100, cloud_tow_img],
        [0, 0, 16, 85, cloud_tow_img],
        [0, 0, 810, 100, cloud_tow_img],
        [0, 0, 16, 398, large_hill],
        [0, 0, 224, 378, large_tree],
        [0, 0, 404, 436, Bush_two_img]

    ]

    blocks = [
        [32, 32, 960, 436, block_img],
        [32, 32, 928, 436, block_img],
        [32, 32, 960, 404, block_img],
        [32, 32, 2080, 404, block_img],
        [32, 32, 2112, 436, block_img],
        [32, 32, 2080, 436, block_img],
    ]

    pltf_moving = [

        [32, 32, 436, 436, move_pltf],
        #[32, 32, 960, 436, move_pltf],
    ]

    for index_ground in range(0, 93):
        if index_ground > 7 and index_ground < 11:
            pass
        
        elif index_ground > 30 and index_ground < 65:
            blocks.append([16, 16, index_ground*32, 388, bridge_bottom])
            decors.append([16, 16, index_ground*32, 372, bridge_top])
            decors.append([16, 16, index_ground*32, 484, waves_img])

        elif index_ground * 32 == 2560:
            blocks.append([16, 16, index_ground*32, 468, ground_img])
            decors.append([16, 16, index_ground*32, 372, mush_bottom])
            blocks.append([16, 16, index_ground*32-32, 340, mush_top])
            blocks.append([16, 16, index_ground*32-128, 436, block_img])
                          
        else:
            blocks.append([32, 32, index_ground*32, 468, bricks_img])

    return blocks, decors, pltf_moving



    


