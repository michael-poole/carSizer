from stl import mesh, Dimension


class Part:
    def __init__(self, p_name, p_model, p_params):
        self.p_name = p_name
        self.p_model = p_model
        self.p_params = p_params
        
        
    def return_data(self):
        return self.p_name + ": " + str(self.p_params)
    

def make_part(my_part_name):
    my_file_name = "burgreen/frog/data/" + my_part_name + ".stl"
    stl_model = make_model_from_stl_file(my_file_name)

    mins_maxs = find_mins_maxs(stl_model)
    width = get_width(mins_maxs)
    length = get_length(mins_maxs)
    height = get_height(mins_maxs)
    params = [width, length, height]
    
    return Part(my_part_name, stl_model, params)
    
    
def parse_data(raw_data):
    all_data = raw_data.split('\'')[1].split("type=Params&")[1]
    data = all_data.split('&')   
    part_names = str(data[0]).split('=')[1].split(",+")
    
    return(part_names)


def make_model_from_stl_file(file_name):
    model = mesh.Mesh.from_file(file_name)
    return model


def find_mins_maxs(obj):
    minx = maxx = miny = maxy = minz = maxz = None
    for p in obj.points:
        # p contains (x, y, z)
        if minx is None:
            minx = p[Dimension.X]
            maxx = p[Dimension.X]
            miny = p[Dimension.Y]
            maxy = p[Dimension.Y]
            minz = p[Dimension.Z]
            maxz = p[Dimension.Z]
        else:
            maxx = max(p[Dimension.X], maxx)
            minx = min(p[Dimension.X], minx)
            maxy = max(p[Dimension.Y], maxy)
            miny = min(p[Dimension.Y], miny)
            maxz = max(p[Dimension.Z], maxz)
            minz = min(p[Dimension.Z], minz)
    dimensions = [minx, maxx, miny, maxy, minz, maxz]
    return dimensions


def get_width(dims):
    w = dims[3] - dims[2]
    return w


def get_length(dims):
    l = dims[1] - dims[0]
    return l


def get_height(dims):
    h = dims[5] - dims[4]
    return h


def main(data):
    # parsed_data = ["brakes", 2, 3, 4, 5]
    parsed_data = parse_data(data)
    stl_files = []
    parts = []
    for datum in parsed_data:
        if datum == "brakes" or datum == "tires" or datum == "wheels":
            datum = datum.rstrip("s").capitalize()
            part_names = ["frontLeft" + datum,
                          "frontRight" + datum,
                          "backLeft" + datum,
                          "backRight" + datum]
            for part_name in part_names:
                parts.append(make_part(part_name))
        else:
            parts.append(make_part(datum))

    return_params = []
    for part in parts:
        return_params.append(part.return_data())

    return return_params
