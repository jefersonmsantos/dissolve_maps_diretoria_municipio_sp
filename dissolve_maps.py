import geopandas as gpd

gp = gpd.read_file('dir_json.json')
gp['geometry']=gp['geometry'].buffer(0)

diretorias = gp.dissolve(by='diretoria')

diretorias.reset_index(level=0,inplace=True)

def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        if str(type(row['geometry']))=="<class 'shapely.geometry.polygon.Polygon'>":
            t = 'Polygon'
        elif str(type(row['geometry']))=="<class 'shapely.geometry.multipolygon.MultiPolygon'>":
            t = 'MultiPolygon'
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':t,
                               'coordinates':[]}}
        geo_aux=gpd.GeoSeries(row['geometry']).to_json()
        parsed = json.loads(geo_aux)
        feature['geometry']['coordinates'] = parsed['features'][0]['geometry']['coordinates']
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson



cols = ['diretoria', 'name','description']
geojson = df_to_geojson(diretorias, cols)

with open('dashapp/diretorias_v6.json', 'w') as json_file:
    json.dump(geojson, json_file)
