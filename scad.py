import copy
import opsc
import oobb
import oobb_base
import yaml
import os
import scad_help

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    parts = []

    typ = kwargs.get("typ", "")

    if typ == "":
        #setup    
        typ = "all"
        #typ = "fast"
        #typ = "manual"

    oomp_mode = "project"
    #oomp_mode = "oobb"

    if typ == "all":
        filter = "30_mm_gap_0_mm_flange_ribbed_extra"; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = True
        #filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr", "laser", "true"]
    elif typ == "fast":
        #filter = ""; save_type = "none"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = True
        filter = ""; save_type = "none"; navigation = False; overwrite = True; modes = ["3dpr"]; oomp_run = False
    elif typ == "manual":
    #filter
        filter = ""
        #filter = "test"

    #save_type
        save_type = "none"
        #save_type = "all"
        
    #navigation        
        #navigation = False
        navigation = True    

    #overwrite
        overwrite = True
                
    #modes
        #modes = ["3dpr", "laser", "true"]
        modes = ["3dpr"]
        #modes = ["laser"]    

    #oomp_run
        oomp_run = True
        #oomp_run = False    

    #adding to kwargs
    kwargs["filter"] = filter
    kwargs["save_type"] = save_type
    kwargs["navigation"] = navigation
    kwargs["overwrite"] = overwrite
    kwargs["modes"] = modes
    kwargs["oomp_mode"] = oomp_mode
    kwargs["oomp_run"] = oomp_run
    
       
    # project_variables
    if True:
        pass
    
    # declare parts
    if True:

        directory_name = os.path.dirname(__file__) 
        directory_name = directory_name.replace("/", "\\")
        project_name = directory_name.split("\\")[-1]
        #max 60 characters
        length_max = 40
        if len(project_name) > length_max:
            project_name = project_name[:length_max]
            #if ends with a _ remove it 
            if project_name[-1] == "_":
                project_name = project_name[:-1]
                
        #defaults
        kwargs["size"] = "oobb"
        kwargs["width"] = 1
        kwargs["height"] = 1
        kwargs["thickness"] = 3
        #oomp_bits
        if oomp_mode == "project":
            kwargs["oomp_classification"] = "project"
            kwargs["oomp_type"] = "github"
            kwargs["oomp_size"] = "oomlout"
            kwargs["oomp_color"] = project_name
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""
        elif oomp_mode == "oobb":
            kwargs["oomp_classification"] = "oobb"
            kwargs["oomp_type"] = "part"
            kwargs["oomp_size"] = ""
            kwargs["oomp_color"] = ""
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""

        part_default = {} 
       
        part_default["project_name"] = project_name
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        



        gaps = []
        gaps.append(8)
        gaps.append(10)
        gaps.append(12)
        gaps.append(16)
        gaps.append(20)
        gaps.append(30)
        gaps.append(45)

        flanges = []
        flanges.append(0)
        flanges.append(6)
        
        thicknesses = []
        thicknesses.append(60)
        thicknesses.append(80)
        thicknesses.append(100)
        thicknesses.append(120)

        styles = []
        styles.append("")
        styles.append("ribbed")

        for gap in gaps:
            for flange in flanges:
                for thickness in thicknesses:
                    for style in styles:
                        part = copy.deepcopy(part_default)
                        p3 = copy.deepcopy(kwargs)

                        width_calculated = gap + 28
                        wid = width_calculated // 15 + 1

                        p3["width"] = wid
                        p3["height"] = 1.5
                        #gap = 16
                        p3["gap"] = gap
                        #flange = 0
                        p3["flange"] = flange

                        p3["thickness"] = thickness
                        p3["style"] = style
                        p3["extra"] = f"{gap}_mm_gap_{flange}_mm_flange"
                        if style != "":
                            p3["extra"] += f"_{style}"
                        part["kwargs"] = p3
                        nam = "base"
                        part["name"] = nam
                        if oomp_mode == "oobb":
                            p3["oomp_size"] = nam
                        parts.append(part)


    kwargs["parts"] = parts

    scad_help.make_parts(**kwargs)

    #generate navigation
    if navigation:
        sort = []
        sort.append("name")
        sort.append("gap")

        #sort.append("width")
        #sort.append("height")
        sort.append("thickness")
        sort.append("flange")
        sort.append("style")

        
        scad_help.generate_navigation(sort = sort)


def get_base(thing, **kwargs):
    prepare_print = kwargs.get("prepare_print", True)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    gap = kwargs.get("gap", 16)
    flange = kwargs.get("flange", 0)
    depth_plate = 9
    style = kwargs.get("style", "")

    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth_plate
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = "perimeter"
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    #oobb_base.append_full(thing,**p3)


    #add screw
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_screw_countersunk"
        p3["depth"] = depth
        p3["radius_name"] = "m3_screw_wood"
        p3["holes"] = "perimeter"
        p3["m"] = "#"
        poss = []
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        pos1[1] += 0
        pos1[2] += depth_plate
        poss.append(pos1)
        p3["pos"] = poss
        oobb_base.append_full(thing,**p3)

    #add nuts
    shift_x = gap/2 + 14/2
    if True:
        depth_total = depth + 5
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_nut"        
        p3["radius_name"] = "m6"
        p3["hole"] = True
        p3["overhang"] = True
        p3["m"] = "#"

        poss = []
        pos1 = copy.deepcopy(pos)
            
        pos1[0] += shift_x
        pos1[1] += 0
        pos1[2] += 0
        poss.append(pos1)
        pos1 = copy.deepcopy(pos)
        pos1[0] += - shift_x
        pos1[1] += 0
        pos1[2] += 0
        poss.append(pos1)
        p3["pos"] = poss
        oobb_base.append_full(thing,**p3)    

        p4 = copy.deepcopy(p3)
        shift_z = depth_total
        poss = []     
        pos1 = copy.deepcopy(pos)
        pos1[0] += shift_x
        pos1[1] += 0
        pos1[2] = shift_z
        poss.append(pos1)
        pos1 = copy.deepcopy(pos)
        pos1[0] += - shift_x
        pos1[1] += 0
        pos1[2] = shift_z
        poss.append(pos1)
        p4["pos"] = poss
        p4["zz"] = "top"
        oobb_base.append_full(thing,**p4)

    #add cylinder lifters
    if True:
        if style =="":
            rad = 14/2
            p3 = copy.deepcopy(kwargs)
            p3["type"] = "positive"
            p3["shape"] = f"oobb_cylinder"
            p3["radius"] = rad
            p3["depth"] = depth_total
            poss = []
            pos1 = copy.deepcopy(pos)
            pos1[0] += shift_x
            pos1[1] += 0
            pos1[2] += depth_total/2
            poss.append(pos1)
            pos1 = copy.deepcopy(pos)
            pos1[0] += - shift_x
            pos1[1] += 0
            pos1[2] += depth_total/2
            poss.append(pos1)
            p3["pos"] = poss
            oobb_base.append_full(thing,**p3)
        elif style == "ribbed":
            rad = 18/2
            radius_donut = 10
            p3 = copy.deepcopy(kwargs)
            p3["type"] = "positive"
            p3["shape"] = f"oobb_cylinder"
            p3["radius"] = rad
            p3["depth"] = depth_total
            poss = []
            pos1 = copy.deepcopy(pos)
            pos1[0] += shift_x
            pos1[1] += 0
            pos1[2] += depth_total/2
            poss.append(pos1)
            pos1 = copy.deepcopy(pos)
            pos1[0] += - shift_x
            pos1[1] += 0
            pos1[2] += depth_total/2
            poss.append(pos1)
            p3["pos"] = poss
            #p3["m"] = "#"
            oobb_base.append_full(thing,**p3)
            #add donut cutouts
            if True:
                p3 = copy.deepcopy(kwargs)
                p3["type"] = "negative"
                p3["shape"] = f"oring"
                p3["id"] = 14/2
                p3["depth"] = radius_donut
                #p3["m"] = "#"
                repeats = (depth_total-9-5) /radius_donut
                for i in range(int(repeats)):
                    p4 = copy.deepcopy(p3)
                    pos1 = copy.deepcopy(pos)
                    pos1[0] += shift_x
                    pos1[1] += 0
                    pos1[2] += radius_donut/2 + i * radius_donut + depth_plate
                    p4["pos"] = [pos1]
                    oobb_base.append_full(thing,**p4)
                    p4 = copy.deepcopy(p4)
                    pos1 = copy.deepcopy(pos)
                    pos1[0] += - shift_x
                    pos1[1] += 0
                    pos1[2] += radius_donut/2 + i * radius_donut + depth_plate
                    p4["pos"] = [pos1]
                    oobb_base.append_full(thing,**p4)



            

    #add cylinder toppers
    if True:
        rad = 14/2
        if flange != 0:
            rad = 25/2
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"oobb_cylinder"
        p3["radius"] = rad        
        dep = 6
        p3["depth"] = dep
        poss = []
        pos1 = copy.deepcopy(pos)      
        pos1[0] += shift_x
        pos1[1] += 0
        pos1[2] += depth_total
        poss.append(pos1)
        pos1 = copy.deepcopy(pos)
        pos1[0] += - shift_x
        pos1[1] += 0
        pos1[2] += depth_total
        poss.append(pos1)
        p3["pos"] = poss
        p3["zz"] = "top"
        oobb_base.append_full(thing,**p3)



    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 150
        pos1[2] += depth_plate * 2
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        pos1[1] += 0
        pos1[2] += 9
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)
    
if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)