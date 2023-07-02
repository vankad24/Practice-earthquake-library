import h5py
filename = "dtec_2_10_01_17.h5"

with h5py.File(filename, "r") as f:
    # Print all root level object names (aka keys)
    # these can be group or dataset names
    keys = list(f.keys())
    print(list(f))
    # get first object name/key; may or may NOT be a group
    # print(list(f[keys[1]]))
    f_time = list(f['data'])[0]
    print(f['data'][f_time][:])


    # # get the object type for a_group_key: usually group or dataset
    # print(type(f[a_group_key]))
    #
    # # If a_group_key is a group name,
    # # this gets the object names in the group and returns as a list
    # data = list(f[a_group_key])
    #
    # # If a_group_key is a dataset name,
    # # this gets the dataset values and returns as a list
    # data = list(f[a_group_key])
    # # preferred methods to get dataset values:
    # ds_obj = f[a_group_key]      # returns as a h5py dataset object
    # ds_arr = f[a_group_key][()]  # returns as a numpy array