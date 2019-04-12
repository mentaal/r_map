import pickle

def test_pickle(data):
    p = pickle.dumps(data)
    print(type(p))

    up = pickle.loads(p)

    print(type(up))
    print(dir(up))

    #print("Up: {}".format(up.name))
    count = 0
    for n in up._walk(levels=-1):
        count += 1
    print(f"{count} nodes in count")


