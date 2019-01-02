import pickle

def test_pickle(data):
    p = pickle.dumps(data)
    print(type(p))

    up = pickle.loads(p)

    print(type(up))
    print(dir(up))

    #print("Up: {}".format(up.name))


