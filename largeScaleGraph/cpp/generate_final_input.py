"""
the python version of "generate final input"
which takes the filtered file and output the edges computation
or it can read the final output of large vis and output the author point split
and paper embedding split
"""

import os
import sys
import json
import sets

# the 
input_dir_1 = "/home/wuzhuofeng/intermediate_files/lines_belong_toconf_smaller.txt";

output_file = "/home/wuzhuofeng/intermediate_files/non_bias_edges_withauthors.txt";

largeVis_output = "./citation_qiaozhu.txt";

split_location = "/home/wuzhuofeng/domainShiftVisualization/largeScaleGraph/cpp/final_visulization/";

conf_info = {}

index_count = 0

id_to_ref = {}
id_to_index = {}
year_to_indexlist = {}
year_counter = {}   # count the sigir paper in each year
author_to_index = {}
conf_pool = set()
sigir_pool = set()
conf_to_index = {}
index_to_conf = {}
index_to_loc = {}

tmp_counter = 0

split_points = ['1994', '2007']


def read_and_parse():
    global index_count
    global tmp_counter
    conf_lines_file = open(input_dir_1)
    for line in conf_lines_file:
        tmp_obj = json.loads(line)
        if "id" not in tmp_obj:
            continue
        if "venue" not in tmp_obj:
            continue
        if "year" not in tmp_obj:
            continue
        venue_string = tmp_obj["venue"]
        conf_pool.add(venue_string)
        id_string = tmp_obj["id"]
        year_string = tmp_obj["year"]
        if year_string not in year_to_indexlist:
            year_to_indexlist[year_string] = []

        id_to_index[id_string] = index_count
        index_to_conf[index_count] = venue_string

        # if venue_string not in conf_to_index:
        #     conf_to_index[venue_string] = []
        # conf_to_index.append(index_count)

        if id_string not in id_to_ref:
            id_to_ref[index_count] = []

        if venue_string == "SIGIR" or venue_string == "SIGIR Forum":
            if year_string not in year_counter:
                year_counter[year_string] = 0
            year_counter[year_string] += 1
            tmp_counter += 1

        if "authors" in tmp_obj:
            author_list = tmp_obj["authors"]
            for tmp in author_list:
                if "name" in tmp:
                    if tmp["name"] not in author_to_index:
                        author_to_index[tmp["name"]] = []
                    author_to_index[tmp["name"]].append(index_count)

        if "references" in tmp_obj:
            for ref in tmp_obj["references"]:
                id_to_ref[index_count].append(ref)

        year_to_indexlist[year_string].append(index_count)
        index_count += 1
    conf_lines_file.close()



def generate_index_to_loc():
    tmp_file = open(largeVis_output)
    for line in tmp_file:
        vec = line.split()
        index_to_loc[vec[0]] = line
    tmp_file.close()


def generate_conf_index():
    global index_count
    for conf in conf_pool:
        conf_to_index[conf] = index_count
        index_count += 1


def generate_edges():
    out_edges_file = open(output_file, "w")
    for k, v in id_to_ref.items():
        for tmp in v:
            if tmp not in id_to_index:
                continue
            out_edges_file.write(str(k) + " " + str(id_to_index[tmp]) + " 1\n")
    for k, v in index_to_conf.items():
        out_edges_file.write(str(k) + " " + str(conf_to_index[v]) + " 2\n");
    out_edges_file.close()


def generate_files():
    year_counter_list = sorted(year_counter.items(), key=lambda x:x[0])
    # print(year_counter_list)
    # print(tmp_counter)
    cur_layer = 0
    layer_list = {}
    for k, v in sorted(year_to_indexlist.items(), key=lambda x:x[0]):
        if cur_layer not in layer_list:
            layer_list[cur_layer] = []
        for tmp in v:
            if tmp not in index_to_loc:
                continue
            layer_list[cur_layer].append(tmp)
        if k in split_points:
            cur_layer += 1
    
    for k, v in sorted(layer_list.items(), key=lambda x:x[0]):
        point_file = open(split_location + str(k) + "_points.txt", 'w')
        label_file = open(split_location + str(k) + "_labels.txt", 'w')
        
        point_file.write(str(len(v)) + "\n")
        for tmp in v:
            if tmp in sigir_pool:
                point_file.write(index_to_loc[tmp] + "\n")
                label_file.wrtei("10\n")
            else:
                point_file.write(index_to_loc[tmp] + "\n")
                label_file.wrtei("0\n")
        
        point_file.close()
        label_file.close()



def main():
    read_and_parse()
    generate_conf_index()
    generate_edges()
    generate_index_to_loc()
    generate_files()

    
    


if __name__ == "__main__":
    main()


