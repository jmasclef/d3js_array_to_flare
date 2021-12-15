# d3js_array_to_flare
Python script to convert array of nested data to d3js json flare<br/><br/>
<code>array=[['00001', '00004'], ['00001', '00004'], ['00002', '00008'], ['00002', '00008'], ['00002', '00008'], ['00002', '00014'], ['00002', '00014'], ['00003', '00092'], ['00003', '00092'], ['00003', '01004']]</code>
<br/><br/>
<code>value_is_count=True </code><br/>
<code>value_is_lastColumn=False </code><br/>
<br/>
* Either array contains values in its last column, set value_is_lastColumn=True<br/>
* Either array has no provided values but has duplicates to count, set value_is_count=True<br/>
* Either array has single lines, values bill be set to 1<br/>
<br/>
<code>dict=asr_array_to_d3js_flare(array=array, value_is_count=value_is_count, value_is_lastColumn=value_is_lastColumn)</code><br/>
<br/>Will give a python dict like this:<br/><br/>
<code>{'name': 'flare', 'children': [{'name': '00001', 'children': [{'name': '00004', 'value': 2}]},  {'name': '00002', 'children': [{'name': '00008', 'value': 3}, {'name': '00014', 'value': 2}]}, {'name': '00003','children': [{'name': '00092', 'value': 2}, {'name': '01004', 'value': 1}]}]}</code><br/>
<br/>
To obtain JSON string: <br/>
<code>import json</code><br/>
<code>json.dumps(d)</code><br/><br/>
Will give this string:<br/>
<code>{"name": "flare", "children": [{"name": "00001", "children": [{"name": "00004", "value": 2}]}, {"name": "00002", "children": [{"name": "00008", "value": 3}, {"name": "00014", "value": 2}]}, {"name": "00003", "children": [{"name": "00092", "value": 2}, {"name": "01004", "value": 1}]}]}</code>
<br/>
<br/>
Et voilà !
