import cv2
import glob
import motmetrics as mm
import numpy as np


# Instructions relating to the format of the dataset
# https://motchallenge.net/instructions
# left, top, width, height

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
        error_check = False
        while not error_check:
            try:
                current_sequence = self.load_sequence(self.sequence)
                self.sequence += 1
                yield current_sequence
            except IOError:
                error_check = True
        # return self

    def __next__(self):
        error_check = False
        while not error_check:
            try:
                current_sequence = self.load_sequence(self.sequence)
                self.sequence += 1
                yield current_sequence
            except IOError:
                error_check = False
                raise StopIteration

    def load_sequence(self, sequence_number):
        """
        Finds the pathname for the relevant data and ground truth files of the sequence currently being trained on

        :param sequence_number: An integer or string representing the sequence number
        :return: A SequenceLoader object specific to the io of the specific sequence currently being worked on
        """

        if len(str(sequence_number)) == 1:
            sequence_string = '0' + str(sequence_number)
        else:
            sequence_string = str(sequence_number)
        sequence_filepath = self.filepath + 'data/*/MOT16-' + sequence_string
        data_path = ''.join(glob.glob(sequence_filepath, recursive=False))
        if len(data_path) == 0:
            raise IOError  # Raise an error if the sequence cannot be found

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
        self.name =          info[1].split('=')[1][:-1]
        self.imDir =         info[2].split('=')[1][:-1]
        self.frameRate =     info[3].split('=')[1][:-1]
        self.seqLength =     info[4].split('=')[1][:-1]
        self.imWidth =       info[5].split('=')[1][:-1]
        self.imHeight =      info[6].split('=')[1][:-1]
        self.imExt =         info[7].split('=')[1][:-1]

        self.accumulator = mm.metrics.MOTAccumulator(auto_id=True)


    def __iter__(self):
        # return self
        generator = self.load_gt()
        self.frame = 1
        for frame in range(1, int(self.seqLength) + 1):
            frame_string = str(frame).zfill(6)
            img_filename = self.filepath + '/' + self.imDir + '/' + frame_string + self.imExt
            img = cv2.imread(img_filename)
            if img is None:
                break
            yield img, next(generator)

    def __next__(self):
        """
        Defines generator functionality to the SequenceLoader object by returning the next frame in the sequnece as well
        as information about its ground truth bounding boxes

        :return: A numpy array of the image followed by a list of ground truth detections for a given frame in the
        correct format
        """
        generator = self.load_gt()
        for frame in range(1, int(self.seqLength) + 1):
            frame_string = str(frame).zfill(6)
            img = cv2.imread(self.filepath + '/' + self.imDir + '/' + frame_string + self.imExt)
            if img is None:
                break
            yield img, next(generator)

    def load_gt(self):
        if 'train' in self.filepath:
            gt_filepath = self.filepath + '/gt/gt.txt'  # If we are dealing with the training set, we should use the ground truth file
        else:
            gt_filepath = self.filepath + '/det/det.txt'  # If we are dealing with the testing set, there is no ground truth file
        with open(gt_filepath, 'r') as fid:
            boxes = []  # A list to store the data on each bounding box
            midpoints = []
            for line in fid:
                box = line.split(',')
                if int(line[0]) != self.frame:
                    self.frame += 1
                    yield (midpoints)
                    del (boxes[:])
                    del(midpoints[:])
                boxes.append([float(box[x]) for x in range(2, 6)])  # Add the relevant parts of the box info
                midpoints.append([float(box[2]) + float(box[4]) / 2, float(box[3]) - float(box[5]) / 2])

        yield (boxes)  # Returns the final frame of boxes

    def update_metrics(self, predictions, gt):
        """

        :param predictions: A 1x2 numpy array of the midpoint of your prediction
        :param gt: The provided ground truth object
        :return: A numpy array of the distances between each prediction and each ground truth box
        """

        p_coords = np.array(predictions)
        g_coords = np.array(gt)
        dists = mm.distances.norm2squared_matrix(p_coords, g_coords)
        self.accumulator.update(
            list(range(len(gt))),
            list(range(len(predictions))),
            dists
        )

        return dists

    def display_metrics(self):
        mh = mm.metrics.create()
        print(mh.compute(self.accumulator, metrics=['num_frames', 'mota', 'motp']))


if __name__ == '__main__':
    loader = DataLoader()
    acc = mm.MOTAccumulator(auto_id=True)
    for sequence in loader:
        for frame, gt_data in sequence:
            sequence.update_metrics(gt_data, gt_data)
        sequence.display_metrics()
    # Now that the accumulator has been sufficiently updated on all relevant information, metrics are computed
    mh = mm.metrics.create()
    summary = mh.compute(acc, metrics=['num_frames', 'mota', 'motp'])
    print(summary)