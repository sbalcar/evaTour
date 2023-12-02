from bs4 import BeautifulSoup

def test01():
    print("test01")

    # Reading the data inside the xml
    # file to a variable under the name
    # data
    with open('../../../data/rows.xml', 'r') as f:
        data = f.read()

    # Passing the stored data inside
    # the beautifulsoup parser, storing
    # the returned object
    Bs_data = BeautifulSoup(data, "xml")

    # Finding all instances of tag
    # `unique`
    b_row = Bs_data.find_all('row')
    #print(len(b_row))
    count = 0;
    for rowI in b_row:
        idI = rowI.get('_id')
        boroughI = rowI.select('borough')
        latitudeI = rowI.select('latitude')
        longitudeI = rowI.select('longitude')
        if len(latitudeI) == 1 and len(longitudeI) == 1 and len(boroughI) == 1:
            if boroughI[0].get_text() == "MANHATTAN":
                count = count +1
                print(idI)
                print(latitudeI[0].get_text())
                print(longitudeI[0].get_text())

    print("")
    print("count: " + str(count))
#    print(b_unique)

    # Using find() to extract attributes
    # of the first instance of the tag
#    b_name = Bs_data.find('child', {'name': 'Frank'})

#    print(b_name)

    # Extracting the data stored in a
    # specific attribute of the
    # `child` tag
#    value = b_name.get('test')

#    print(value)



if __name__ == "__main__":
    test01()