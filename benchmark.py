import pandas as pd
import cv2
import motmetrics as mm
import glob
import numpy as np


# Instructions relating to the format of the dataset
# https://motchallenge.net/instructions


class DataLoader:
    def __init__(self, filepath='./'):
        """
        Initializes a DataLoader object

        :param filepath: Defaults to assuming that you're using the current directory, but can be specified as a
        separate directory within the file system.
        """
        self.filepath = filepath

    def __iter__(self):
        """
        Defines the behavior of the iterator function for the DataLoader object. This would be used to loop through
        each sequence without worrying about any input parameters

        :return: This object as an iterator, allowing the user to iterate through each sequence's data
        """

        self.sequence = 1
        return self

    def __next__(self):
        try:
            sequence = self.load_sequence(self.sequence)
            self.sequence += 1
            return sequence
        except IOError:
            raise StopIteration

    def load_sequence(self, sequence_number):
        """
        Finds the pathname for the relevant data and ground truth files of the sequence currently being trained on

        :param sequence_number: An integer or string representing the sequence number
        :return: A SequenceLoader object specific to the io of the specific sequence currently being worked on
        """

        if len(str(sequence_number)) == 1:
            sequence_string = '0' + str(sequence_number)
        data_path = ''.join(glob.glob(self.filepath + 'data/*/MOT16-' + sequence_string, recursive=True))
        if len(data_path) == 0:
            raise IOError  # Raise an error if the sequence cannot be found
        if 'train' in data_path:
            data_path += '/gt/gt.txt'  # If we are dealing with the training set, we should use the ground truth file
        else:
            data_path += '/det/det.txt'  # If we are dealing with the testing set, there is no ground truth file

        return SequenceLoader(filepath=data_path)


class SequenceLoader():
    def __init__(self, filepath='./'):
        """
        A class for doing the io of a specific sequence

        :param filepath: The file path for the current sequence being worked on
        """
        self.filepath = filepath
        with open(self.filepath + '/seqinfo.ini') as fid:
            info = fid.readlines()
        self.name =          info[1].split('=')[1]
        self.imDir =         info[2].split('=')[1]
        self.frameRate =     info[3].split('=')[1]
        self.seqLength =     info[4].split('=')[1]
        self.imWidth =       info[5].split('=')[1]
        self.imHeight =      info[6].split('=')[1]
        self.imExt =         info[7].split('=')[1]


    def __iter__(self):
        """
        Defines the behavior of the iterator function for this object

        :return: This object as an iterator, allowing the user to iterate through each frame's data
        """

        self.frame = 1
        self.generator = self.load_gt()
        return self

    def __next__(self):
        '''
        Defines generator functionality to the SequenceLoader object by returning the next frame in the sequnece as well
        as information about its ground truth bounding boxes

        :return: A numpy array of the image followed by a list of ground truth detections for a given frame in the
        correct format
        '''
        frame_string = str(self.frame).zfill(6)
        img = cv2.imread(self.filepath + '/' + self.imDir + '/' + frame_string + self.imExt)
        if img is None:
            raise StopIteration # Terminates the generator
        return img, next(generator)

    def load_gt(self):
        with open(fname, 'r') as fid:
            boxes = []  # A list to store the data on each bounding box
            for line in fid:
                box = line.split(',')
                if int(line[0]) != self.frame:
                    yield (boxes)
                    del (boxes[:])
                boxes.append([float(box[x]) for x in range(2, 7)])  # Add the relevant parts of the box info

        yield (boxes)  # Returns the final frame of boxes


if __name__ == '__main__':
    # fname = load_sequence(1)
    # generator = load_frame(fname)
    # acc = mm.MOTAccumulator(auto_id=True)
    # for frame in range(600):
    #     boxes = next(generator)
    #     coords = np.array(boxes)
    #     dists = mm.distances.norm2squared_matrix(coords, coords)
    #     # Simply testing that the distance metric recognizes the GT boxes as zero distance from themselves

    loader = DataLoader()
    acc = mm.MOTAccumulator(auto_id=True)
    for sequence in loader:
        for frame, data in sequence:
            coords = np.array(data)
            dists = mm.distances.norm2squared_matrix(coords, coords)
            acc.update(
                list(range(len(frame))),
                list(range(len(frame))),
                dists
            )


    # Now that the accumulator has been sufficiently
    mh = mm.metrics.create()
    summary = mh.compute(acc, metrics=['num_frames', 'mota', 'motp'])
    print(summary)
