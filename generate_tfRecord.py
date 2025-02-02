"""
Usage:
  # Create train data:
 python generate_tfRecord.py --csv_input=Dataset/train/Label/train_labels.csv  --output_path=Label/train.record --image_dir="Dataset/train/"

  # Create test data:
  python generate_tfRecord.py --csv_input=Dataset/test/Label/test_labels.csv  --output_path=Label/test.record  --image_dir=Dataset/test/
  
# From /Tensorflow
  python models/research/object_detection/model_main.py     --pipeline_config_path=/home/aymen/Documents/OIDv4_ToolKit-master/OID/training/faster_rcnn_inception_v2_coco.config     --model_dir=/home/aymen/Documents/OIDv4_ToolKit-master/OID/training/    --num_train_steps=50000     --sample_1_of_n_eval_examples=1     --alsologtostderr
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow as tf
import tensorflow.compat.v1 as tf
import sys


from PIL import Image
import dataset_util
from collections import namedtuple, OrderedDict

flags = tf.app.flags
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('image_dir', '', 'Path to images')
FLAGS = flags.FLAGS


# TO-DO replace this with label map
def class_text_to_int(row_label):
    if row_label == 'Stop sign':
        return 1
    if row_label == 'Car':
        return 2
    if row_label == 'Traffic sign':
        return 3
    if row_label == 'Traffic light':
        return 4
    else:
        None


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]

def reconize_path(path,file):
    for p in ["Car/","Stop sign/","Traffic sign/","Traffic light/"]:
        pathF = path +  p
        if os.path.isfile(pathF+file) :
            return pathF
        
    print(file)    
def create_tf_example(group, pathF):
    
    path = reconize_path(pathF,group.filename)
    print("path ->",path)
    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
            'image/height': dataset_util.int64_feature(height),
            'image/width': dataset_util.int64_feature(width),
            'image/filename': dataset_util.bytes_feature(filename),
            'image/source_id': dataset_util.bytes_feature(filename),
            'image/encoded': dataset_util.bytes_feature(encoded_jpg),
            'image/format': dataset_util.bytes_feature(image_format),
            'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
            'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
            'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
            'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
            'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
            'image/object/class/label': dataset_util.int64_list_feature(classes),
        }))
    return tf_example


def main(_):
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
    path = os.path.join(FLAGS.image_dir)
    examples = pd.read_csv(FLAGS.csv_input)
    grouped = split(examples, 'filename')
    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords: {}'.format(output_path))


if __name__ == '__main__':
    tf.app.run()

