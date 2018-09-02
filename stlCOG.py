from stl import mesh

# Using an existing closed stl file:
your_mesh = mesh.Mesh.from_file('burgreen/frog/data/backLeftTire.stl')

volume, cog, inertia = your_mesh.get_mass_properties()
print("Position of the center of gravity (COG) = {0}".format(cog))

xyz_cog = str(cog).lstrip("[").rstrip("]").split()
print(xyz_cog)

pos_list = [your_mesh.x, your_mesh.y, your_mesh.z]
i = 0
while i <= 2:
    pos_list[i] -= float(xyz_cog[i])
    i += 1

i = 0
while i <= 2:
    pos_list[i] += float(xyz_cog[i])
    i += 1

your_mesh.save('burgreen/frog/data/backLeftTire.stl')