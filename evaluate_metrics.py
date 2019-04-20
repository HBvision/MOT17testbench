import benchmark
import motmetrics as mm
import numpy as np

root = './data/' + "HB/"
sequence_path = root + "HB03"
det_loader = benchmark.SequenceLoader(sequence_path, detections=True, midpoints=True, id=False)
gt_loader = benchmark.SequenceLoader(sequence_path, detections=False, midpoints=True, id=False)

frame_num = 1

acc = mm.MOTAccumulator(auto_id=True)

while frame_num < 183:
    frame, det_info = next(det_loader)
    frame, gt_info = next(gt_loader)

    gt_midpoints = np.array(gt_info)
    det_midpoints = np.array(det_info)

    try:
        dists = mm.distances.norm2squared_matrix(gt_midpoints, det_midpoints, max_d2=100.)
    except:
        break

    acc.update(range(len(gt_info)),
               range(len(det_info)),
               dists
    )

    # print(acc.mot_events.loc[frame_num - 1])

mh = mm.metrics.create()
summary = mh.compute(acc, metrics=['num_frames', 'mota', 'motp'], name='HB03')
print(summary)