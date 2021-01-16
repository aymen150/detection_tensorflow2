from object_detection.protos.string_int_label_map_pb2 import StringIntLabelMap, StringIntLabelMapItem
from google.protobuf import text_format

def convert_classes(classes, start=1):
    msg = StringIntLabelMap()
    for id, name in enumerate(classes, start=start):
        msg.item.append(StringIntLabelMapItem(id=id, name=name))

    text = str(text_format.MessageToBytes(msg, as_utf8=True), 'utf-8')
    return text


txt = convert_classes(['Stop sign', 'Car', 'Traffic sign', 'Traffic light'])
print(txt)
with open('training/label_map.pbtxt', 'w') as f:
    f.write(txt)