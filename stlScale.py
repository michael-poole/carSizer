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
    model.x, model.y, model.z = model.x*scale_factors_xyz[0], model.y*scale_factors_xyz[1], model.z*scale_factors_xyz[2]


def generate_new_file_name(file_name):
    new_file_name = "modified_" + file_name
    return new_file_name


def save_new_stl_file(model, new_file_name):
    model.save(new_file_name)

def parse_data(raw_data):
    all_data = raw_data.split('\'')[1]
    data = all_data.split('&')
    tuple_data = []
    for datum in data:
        part_name = datum.split('=')[0]
        scale_string = datum.split('=')[1]
        scale_string_list = scale_string.lstrip('[').rstrip(']').split(',')
        scale_int_list = []
        for num in scale_string_list:
            scale_int_list.append(int(num))
        tuple_data.append( (part_name, scale_int_list) )
    return(tuple_data)


def main(data):
    stl_scale_factor_tuples = parse_data(data)
    for stl_scale_factor_tuple in stl_scale_factor_tuples:

        stl_file = stl_scale_factor_tuple[0]
        stl_model = make_model_from_stl_file(stl_file)

        scale_xyz = stl_scale_factor_tuple[1]
        scale_model(stl_model, scale_xyz)

        # new_stl_file = generate_new_file_name(stl_file)
        save_new_stl_file(stl_model, stl_file)
