import pandas as pd
import motmetrics as mm
import glob
import numpy as np

# Instructions relating to the format of the dataset
# https://motchallenge.net/instructions

def load_sequence(sequence):
    '''
    Finds the pathname for the ground truth file of the sequence currently being trained on

    :param sequence: An integer or string representing the sequence number
    :return: fname: the path to the ground truth file of the sequence currently being trained on
    '''
    if len(str(sequence)) == 1:
        sequence = '0' + str(sequence)
    fname = ''.join(glob.glob('./*/MOT16-' + sequence, recursive=True))
    if len(fname) == 0:
        raise IOError
    if fname[2:7] == 'train':
        fname += '/gt/gt.txt'  # If we are dealing with the training set, we should use the ground truth file
    else:
        fname += '/det/det.txt'  # If we are dealing with the testing set, there is no ground truth file

    return fname

def load_frame(fname):
    '''
    A generator function to return ground truth bounding boxes one frame at a time

    :param fname: The file path to the ground truth data
    :return: A list of ground truth detections for a given frame in the correct format
    '''
    with open(fname, 'r') as fid:
        old_frame = 1 # Always start on the first frame
        boxes = [] # A list to store the data on each bounding box
        for line in fid:
            box = line.split(',')
            if int(line[0]) != old_frame:
                yield(boxes)
                del(boxes[:])
            boxes.append([float(box[x]) for x in range(2, 7)]) # Add the relevant parts of the box info
        yield(boxes)

if __name__ == '__main__':
    fname = load_sequence(1)
    generator = load_frame(fname)
    acc = mm.MOTAccumulator(auto_id=True)
    for frame in range(600):
        boxes = next(generator)
        coords = np.array(boxes)
        dists = mm.distances.norm2squared_matrix(coords, coords)
        # Simply testing that the distance metric recognizes the GT boxes as zero distance from themselves
        acc.update(
            list(range(len(boxes))),
            list(range(len(boxes))),
            dists
        )

    # Now that the accumulator has been sufficiently
    mh = mm.metrics.create()
    summary = mh.compute(acc, metrics=['num_frames', 'mota', 'motp'])
    print(summary)
