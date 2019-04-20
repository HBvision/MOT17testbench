import benchmark

root = './data/' + "HB/"
sequence_path = root + "HB03"
det_loader = benchmark.SequenceLoader(sequence_path, detections=True, midpoints=False, id=True)
gt_loader = benchmark.SequenceLoader(sequence_path, detections=False, midpoints=False, id=True)

