import os

import overpy

def test01():
    api = overpy.Overpass()

    # fetch all ways and nodes
    result = api.query("""
        way(50.746,7.154,50.748,7.157) ["highway"];
        (._;>;);
        out body;
        """)

#   result = api.query("""
#       is_in(40.748579, -73.985605);
#       (._; >;);
#       out body;
#       """)

    for way in result.ways:
        print("Name: %s" % way.tags.get("name", "n/a"))
        print("  Highway: %s" % way.tags.get("highway", "n/a"))

    print("  Nodes:")
    for node in way.nodes:
        print("    Lat: %f, Lon: %f" % (node.lat, node.lon))


if __name__ == "__main__":
    os.chdir('../../../')
    print("")
    test01()