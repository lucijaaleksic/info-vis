import folium

def main():
    croatia_map = folium.Map(location=[45.1, 15.2], zoom_start=7)

    folium.GeoJson(
        'croatia.geojson',
        name='Croatia',
        style_function=lambda feature: {
            'fillColor': 'lightblue',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.4
        }
    ).add_to(croatia_map)

    croatia_map.save('map_croatia.html')


if __name__ == '__main__':
    main()
