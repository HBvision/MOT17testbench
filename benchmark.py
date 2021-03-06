import cv2
import glob
import motmetrics as mm
import numpy as np
import csv

# The maintainer of this codebase is Ian Haggerty,
# a student at Purdue University. To contact him,
# email ihaggert@purdue.edu

# Instructions relating to the format of the dataset
# https://motchallenge.net/instructions
# left, top, width, height


class DataLoader:
    def __init__(self, filepath='./', midpoints=False):
        """
        Initializes a DataLoader object

        :param filepath: Defaults to assuming that you're using the current directory, but can be specified as a
        separate directory within the file system.
        """
        self.filepath = filepath
        self.choose_midpoints = midpoints

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

        #TODO: Rewrite this like in the SequenceLoader class
        #TODO: Make the sequence loader class check for IOError
        error_check = False
        while not error_check:
            try:
                current_sequence = self.load_sequence(self.sequence)
                self.sequence += 1
                yield current_sequence
            except IOError:
                error_check = True
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

        if 'HB' in self.filepath:
            sequence_filepath = self.filepath + '*/HB' + sequence_string
        elif 'MOT16' in self.filepath:
            sequence_filepath = self.filepath + '*/MOT16' + sequence_string
        elif 'MOT15' in self.filepath:
            sequence_filepath = self.filepath + '*/MOT15' + sequence_string

        data_path = ''.join(glob.glob(sequence_filepath, recursive=True))
        if len(data_path) == 0:
            raise IOError  # Raise an error if the sequence cannot be found

        return SequenceLoader(filepath=data_path, midpoints=self.choose_midpoints)


class SequenceLoader:
    def __init__(self, filepath='./', midpoints=False, detections=False, id=False):
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
        self.midpoints = []
        self.choose_midpoints = midpoints
        self.detections = detections
        self.id = id
        self.frame = 1

        self.detection_generator = self.load_detections()

    def __iter__(self):
        """
        Defines the functionality for SequenceLoader's use in a for loop, returning images and ground truth bounding
        boxes for each frame in the sequence.
        :return: img, gt_data are the image array and the bounding boxs for that frame
        """
        for frame in range(1, int(self.seqLength) + 1):
            frame_string = str(frame).zfill(6)
            img_filename = self.filepath + '/' + self.imDir + '/' + frame_string + self.imExt
            img = cv2.imread(img_filename, 1)
            if img is None:
                break
            yield img, next(self.detection_generator)
            del img

    def __next__(self):
        """
        Defines generator functionality to the SequenceLoader object by returning the next frame in the sequnece as well
        as information about its ground truth bounding boxes

        :return: A numpy array of the image followed by a list of ground truth detections for a given frame in the
        correct format
        """

        if self.frame <= int(self.seqLength):
            frame_string = str(self.frame).zfill(6)
            img = cv2.imread(self.filepath + '/' + self.imDir + '/' + frame_string + self.imExt)
        else:
            raise GeneratorExit
        if img is None:
            raise GeneratorExit
        # Note:
        return img, next(self.detection_generator)

    def load_detections(self):
        """
        Loads the ground truth file
        :return:
        """
        if self.detections:
            fix_gt(self.filepath + '/det/det.txt')
            gt_filepath = self.filepath + '/det/det.txt'
        else:
            fix_gt(self.filepath + '/gt/gt.txt')
            gt_filepath = self.filepath + '/gt/gt_corrected.txt'  # If we are dealing with the training set, we should use the ground truth file

        # If we are dealing with the testing set, there is no ground truth file
        with open(gt_filepath, 'r') as fid:
            boxes = []  # A list to store the data on each bounding box
            midpoints = []
            lines = fid.readlines()
            line_num = 0
            frame_match = False
            while self.frame <= int(self.seqLength) and line_num < len(lines):
                line = lines[line_num]
                box = line.split(',')
                if line != '\n':
                    # box[0] is the current bounding box
                    # self.frame is the actual frame of the sequence we should be on
                    if int(box[0]) > self.frame and frame_match:
                        self.frame += 1
                        self.midpoints = midpoints
                        if self.choose_midpoints is True:
                            yield (midpoints)
                        else:
                            yield (boxes)
                        del (boxes[:])
                        del(midpoints[:])
                        del(self.midpoints[:])
                        frame_match = False
                    elif int(box[0]) > self.frame:
                        self.frame += 1
                        yield ([])
                    else:
                        if self.id is True:
                            boxes.append([float(box[x]) for x in range(2, 6)].append(box[1]))
                            midpoints.append([float(box[2]) + float(box[4]) / 2, float(box[3]) + float(box[5]) / 2, box[1]])
                        else:
                            boxes.append([float(box[x]) for x in range(2, 6)])  # Add the relevant parts of the box info
                            midpoints.append([float(box[2]) + float(box[4]) / 2, float(box[3]) + float(box[5]) / 2])

                        line_num += 1
                        frame_match = True
                else:
                    line_num += 1

        yield (boxes)  # Returns the final frame of boxes
        while 1:
            self.frame += 1
            yield []

    def update_metrics(self, predictions):
        """
        :param predictions: A 1x2 numpy array of the midpoint of your prediction
        :param gt: The provided ground truth object
        :return: A numpy array of the distances between each prediction and each ground truth box
        """

        p_coords = np.array(predictions)
        g_coords = np.array(self.midpoints)
        dists = mm.distances.norm2squared_matrix(p_coords, g_coords)
        self.accumulator.update(
            list(range(len(self.midpoints))),
            list(range(len(predictions))),
            dists
        )

        return dists

    def display_metrics(self):
        mh = mm.metrics.create()
        print(mh.compute(self.accumulator, metrics=['num_frames', 'mota', 'motp']))


def fix_gt(filename):
    with open(filename, 'r') as fid:
        reader = csv.reader(fid)
        sorted_list = sorted(reader, key=lambda row: int(row[0]), reverse=False)

    out_filename = filename[0:-4] + '_corrected.txt'
    with open(out_filename, 'w', newline='') as fid:
        writer = csv.writer(fid, delimiter=',')
        writer.writerows(sorted_list)

if __name__ == '__main__':
    loader = DataLoader(filepath='./data/', midpoints=True)
    for sequence in loader:
        for frame, gt_data in sequence:
            sequence.update_metrics(gt_data)
        sequence.display_metrics()
