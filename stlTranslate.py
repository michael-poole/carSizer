from stl import mesh


def make_model_from_stl_file(file_name):
    model = mesh.Mesh.from_file(file_name)
    return model


def save_new_stl_file(model, new_file_name):
    model.save(new_file_name)


def main():
    stl_file = "burgreen/frog/data/frontRightBrake.stl"
    stl_model = make_model_from_stl_file(stl_file)
    
    stl_model.z -= 31

    save_new_stl_file(stl_model, stl_file)

main()