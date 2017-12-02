_enable_debug = True


def _debug(str):
    if _enable_debug:
        print('%s\n' % str)


def get_image_max_index(fid, folder_name):
    data_label_name = folder_name.join('_max_index')
    _debug('Get \033[0;32m%s\033[0m' % data_label_name)
    if fid.get(data_label_name):
        _debug('Max image index is \033[0;32m%s\033[0m' %
               fid[data_label_name].value)
        return int(fid[data_label_name].value)
    else:
        return 0


def save_image_max_index(fid, folder_name, max_index):
    data_label_name = folder_name.join('_max_index')
    save_data(fid, data_label_name, max_index)


def save_data(fid, data_label_name, data_value):
    if fid.get(data_label_name):
        fid[data_label_name] = data_value
        _debug('\033[0;32m%s\033[0m was updated.' % data_label_name)
    else:
        fid.create_dataset(data_label_name, data=data_value)
        _debug('\033[0;32m%s\033[0m was saved.' % data_label_name)
