def __asr_array_to_d3js_flare_keys(array:list,value_is_lastColumn:False,value_is_count:False)->dict:
    """
    Do NOT call this function
    Build d3js Flare from keys array, used for recursion only 
    Returned values will be:
    * Filled with 1 if value_is_lastColumn is false and value_is_count is False
    * Filled with a second column if value_is_lastColumn is True (keys must be unique!)
    * Filled with count if value_is_count is True, in that case duplicate keys will be count here
    :param array: 2D sorted array [[key,value],...] if value_is_lastColumn else [ [key1], [key2],....]
    :param value_is_lastColumn: array has second column with value [[key,value],...]
    :param value_is_count: array is [ [key1], [key2],....] duplicate keys will be counted as value
    :return: dict with included children to slice for the future recursion and so on
    """
    if value_is_lastColumn and value_is_count:
        raise "Values are either counted or provided, both is not possible. Fix both bools to False for arbitrary 1 values."
    width=len(array[0])
    expected_width=2 if value_is_lastColumn else 1
    if width!= expected_width:
        raise NameError("Bad array width: expected {} got {}".format(expected_width,width))
    columns=list('ABCDEFGH')[:width]
    df = pandas.DataFrame(array,columns=columns)
    parent_list=[]
    old_key_name=None

    if value_is_count:
        counter = df.value_counts()
        for _, row in df.iterrows():
            key_name = row[0]
            if key_name != old_key_name:
                flare = dict()
                flare['name'] = key_name
                flare['value'] = int(counter[key_name])
                parent_list.append(flare)
                old_key_name=key_name
    else:
        for _, row in df.iterrows():
            key_name = row[0]
            flare = dict()
            flare['name'] = key_name
            flare['value'] = row[1] if value_is_lastColumn else 1
            parent_list.append(flare)

    d = {'name': 'flare', 'children': parent_list}

    return d

def asr_array_to_d3js_flare(array:list,value_is_lastColumn:False,value_is_count:False)->dict:
    """
    Build a d3js flare dict from sorted array
    * Either array contains values in its last column, set value_is_lastColumn=True
    * Either array has no provided values but has duplicates to count, set value_is_count=True
    * Either array has single lines, values bill be set to 1
    :param array: sorted array [[root, node, key,value],...] if value_is_lastColumn else [ [root, node, key], [root, node, key],...]
    :param value_is_lastColumn: array has last column with value [[...,...,key, value],...]
    :param value_is_count: array is [ [...,...,key1], [...,...,key2],....] duplicate keys will be counted as value
    :return: structured dict for hierarchical d3js json flare
    """
    if value_is_lastColumn and value_is_count:
        raise "Values are either counted or provided, both is not possible. Fix both bools to False for arbitrary 1 values."
    array_width=len(array[0])
    first_width = 2 if value_is_lastColumn else 1
    parent_column=array_width-3 if value_is_lastColumn else array_width-2
    first_flare_array=[[line[-2], line[-1]] for line in array] if value_is_lastColumn else [[line[-1]] for line in array]
    first_flare=__asr_array_to_d3js_flare_keys(array=first_flare_array,value_is_lastColumn=value_is_lastColumn,value_is_count=value_is_count)
    current_flare=first_flare

    while parent_column>=0:
        old_parent=None
        new_flare=dict()
        new_flare['name']='flare'
        new_flare['children'] = []
        for line in array:
            parent = line[parent_column]
            child = line[parent_column+1]

            if parent!=old_parent:
                if old_parent is not None:
                    flare=dict()
                    flare['name']=old_parent
                    flare['children']=[flare for flare in current_flare['children'] if flare['name'] in children_set]
                    new_flare['children'].append(flare)
                children_set=set()
                old_parent=parent
            children_set.add(child)

        else:
            flare = dict()
            flare['name'] = old_parent
            flare['children'] = [flare for flare in current_flare['children'] if flare['name'] in children_set]
            new_flare['children'].append(flare)

        current_flare=new_flare
        parent_column -= 1

    return current_flare
