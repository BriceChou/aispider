__author__ = 'Brice Chou'

_enable_debug = True


def _debug(str):
    if _enable_debug:
        print('%s\n' % str)


def save_data(fid, data_label_name, data_value):
    if fid.get(data_label_name):
        fid.attrs.modify(data_label_name, data_value)
        _debug('\033[0;32m%s\033[0m was updated.' % data_label_name)
    else:
        fid.create_dataset(data_label_name, data=data_value)
        _debug('\033[0;32m%s\033[0m was saved.' % data_label_name)


def delete_dataset_with_name(fid, dataset_name):
    fid.attrs.__delitem__(dataset_name)


def clear_all_data(fid):
    for key in fid.attrs.keys():
        delete_dataset_with_name(fid, key)


def print_all_data(fid):
    value_list = []
    key_list = []
    for key in fid.keys():
        key_list.append(fid[key].name.split('/')[-1])
        value_list.append(fid[key].value)

    _debug('{}, {}'.format(key_id, value)
           for key_id, value in zip(key_list, value_list))


def print_all_data_name(fid):
    temp_list = []
    for key in fid.keys():
        temp_list.append(fid[key].name.split('/')[-1])
    _debug(temp_list)
