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
    _debug(fid.attrs.keys())
    _debug(fid.attrs.values())


def print_all_data_name(fid):
    _debug(fid.attrs.keys())
