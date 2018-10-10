from stl import mesh


def csv_to_tuples(csv):
    csv_data = open(csv, 'r')
    csv_tuples = []
    for line in csv_data:
        line = line.rstrip("\n")
        line_parts = line.split(", ")

        part_name = line_parts[0]
        x_factor = int(line_parts[1])
        y_factor = int(line_parts[2])
        z_factor = int(line_parts[3])
        factor_list = [x_factor, y_factor, z_factor]

        csv_tuple = (part_name, factor_list)
        csv_tuples.append(csv_tuple)
    csv_data.close()
    return csv_tuples


def make_model_from_stl_file(file_name):
    model = mesh.Mesh.from_file(file_name)
    return model


def scale_model(model, scale_factors_xyz):
    print(scale_factors_xyz)
    model.x, model.y, model.z = model.x*scale_factors_xyz[0], model.y*scale_factors_xyz[1], model.z*scale_factors_xyz[2]


def set_distance_model(model, name, distance_factors_xyz):
    print(distance_factors_xyz)
    if("Left" in name):
        model.x, model.y, model.z = model.x - float(distance_factors_xyz[0]), model.y - float(distance_factors_xyz[1]), model.z - float(distance_factors_xyz[2])
    else:
        model.x, model.y, model.z = model.x + float(distance_factors_xyz[0]), model.y + float(distance_factors_xyz[1]), model.z + float(distance_factors_xyz[2])


def generate_new_file_name(file_name):
    new_file_name = "modified_" + file_name
    return new_file_name


def save_new_stl_file(model, new_file_name):
    model.save(new_file_name)


def parse_data(raw_data):
    all_data = raw_data.split('"type": "Scale", ')[1]
    data = all_data.split(', ')
    new_data = []
    for item in data:
        item = item.replace('\"', '').rstrip('}')
        new_data.append(item)
    tuple_data = []
    for datum in new_data:
        part_name = datum.split(': ')[0]
        scale_string = datum.split(': ')[1]
        if("," in scale_string):
            scale_string_list = scale_string.lstrip('[').rstrip(']').split(',')
            scale_number_list = []
            for num in scale_string_list:
                scale_number_list.append(float(num))
            tuple_data.append( (part_name, scale_number_list) )
        else:
            tuple_data.append( (part_name, scale_string) )
    return(tuple_data)


def get_original_cog(model):
    volume, cog, inertia = model.get_mass_properties()

    xyz_cog = str(cog).lstrip("[").rstrip("]").split()
    return(xyz_cog)

    
def set_to_center(model, xyz_cog):
    pos_list = [model.x, model.y, model.z]
    i = 0
    while i <= 2:
        pos_list[i] -= float(xyz_cog[i])
        i += 1

def set_to_original(model, xyz_cog):
    pos_list = [model.x, model.y, model.z]
    i = 0
    while i <= 2:
        pos_list[i] += float(xyz_cog[i])
        i += 1

def main(data):
    stl_scale_factor_tuples = parse_data(data)
    mode = ""
    for stl_scale_factor_tuple in stl_scale_factor_tuples:

        stl_file = stl_scale_factor_tuple[0]

        if(stl_file == "mode"):
            mode = stl_scale_factor_tuple[1]
        else:
            stl_model = make_model_from_stl_file(stl_file)

            scale_xyz = stl_scale_factor_tuple[1]
            print(scale_xyz)
            if(mode == "Scale"):
                original_cog = get_original_cog(stl_model)

                set_to_center(stl_model, original_cog)
                scale_model(stl_model, scale_xyz)
                set_to_original(stl_model, original_cog)
            elif(mode == "Distance"):
                set_distance_model(stl_model, stl_file, scale_xyz)

            # new_stl_file = generate_new_file_name(stl_file)
            save_new_stl_file(stl_model, stl_file)
