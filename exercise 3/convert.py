import json

def generate_geojson_with_coordinates(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    topology = data['arcs']
    objects = data['objects']['croatia']['geometries']

    features = []
    for obj in objects:
        arcs = obj['arcs']
        coordinates = []

        for arc in arcs:
            if isinstance(arc[0], int):
                # Single-arc case
                arc_indices = [arc]
            else:
                # Multi-arc case
                arc_indices = arc

            for index in arc_indices:
                coordinates.append(get_coordinates(topology, index))

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Polygon',
                'coordinates': [coordinates]
            },
            'properties': {
                'name': obj['properties']['NAME_1'],
                'color': 'red'  # Set the desired color here
            }
        }
        features.append(feature)

    feature_collection = {
        'type': 'FeatureCollection',
        'features': features
    }

    with open(output_file, 'w') as f:
        json.dump(feature_collection, f)

def get_coordinates(topology, index):
    coordinates = []
    for idx in index:
        if idx < 0:
            arc = topology[abs(idx) - 1][::-1]
        else:
            arc = topology[idx]
        coordinates.extend(arc)
    return coordinates

if __name__ == '__main__':
    input_file = 'croatia.geojson'  # Replace with the path to your original file
    output_file = 'output.geojson'  # Replace with the desired output file path
    generate_geojson_with_coordinates(input_file, output_file)
