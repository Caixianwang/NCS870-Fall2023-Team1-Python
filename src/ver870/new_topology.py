import numpy as np

import new_utils


def topo_calc(file_path):
    dict_path_1min = dict()
    list_path_1min_linenum = []

    linenum = 0
    substr = "AS_PATH"  # Substring to search for.
    with open(file_path, 'rt') as updateMessage:
        for line in updateMessage:
            linenum += 1

            # break when in line 1201
            #         if linenum == as_path_pre_end[0]:  # last cell, 'line 1201'
            #             break

            if line.find(substr) != -1:  # if case-insensitive match
                # dict format = {int: str}
                dict_path_1min[linenum] = line.rstrip(
                    '\n')  # removes any trailing characters (characters at the end a string)
                list_path_1min_linenum.append(linenum)

    len(list_path_1min_linenum)  # how many lines of as path in that minutes

    edge_list_np_all = np.array([])
    for i_linenum in range(
            len(list_path_1min_linenum)):  # list_path_1min_linenum, list of all paths of lines in the update message
        #     p = dict_path_1min.get(list_path_1min_linenum[i_linenum])  #  get value
        p = dict_path_1min.pop(list_path_1min_linenum[i_linenum])  # pop key, get value, save memory
        p_nodes = p[8:]  # skip "AS_PATH: ", output is sitll str

        # Need this step if has "{}" -begin
        p_nodes_list = p_nodes.split()
        if len(p_nodes_list) <= 1:
            continue
        # print(len(p_nodes_list))
        #     print('list before removing {}:', p_nodes_list)  # list
        # need to remove "{" or "}"
        for i in range(len(p_nodes_list)):
            p_nodes_list[i] = p_nodes_list[i].strip('{}')
            p_nodes_list[i] = p_nodes_list[i].replace(':', ' ')
            p_nodes_list[i] = p_nodes_list[i]

        #     print('list after removing {}:', p_nodes_list)  # list
        #     print(p_nodes_list)

        p_nodes_list = ' '.join(p_nodes_list)  # may be used if there exists "{}"

        p_nodes = p_nodes_list
        # Need this step if has "{}" -end

        p_nodes_np = np.fromstring(p_nodes, dtype=int, sep=' ')  # numpy.ndarray

        edge_list_np = np.array([])
        for i in range(len(p_nodes_np) - 1):
            edge_list_np_i = np.array([p_nodes_np[i], p_nodes_np[i + 1]])
            if i != 0:
                edge_list_np = np.append(edge_list_np, [edge_list_np_i], axis=0)  # np.concatenate may be slower
            else:
                edge_list_np = [edge_list_np_i]
        # print(edge_list_np)
        if i_linenum == 0:
            edge_list_np_all = edge_list_np
        else:
            edge_list_np_all = np.append(edge_list_np_all, edge_list_np, axis=0)  # np.concatenate may be slower
    #     print(edge_list_np)

    json_req = {
        'topo': edge_list_np_all.tolist()
    }
    new_utils.pushOutput(json_req)
