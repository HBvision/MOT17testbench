## Intro

This is a python module which does all of the file io for the CAM2 object
trackers. It also retrieves all of the relevant ground truth information stored
with the dataset, allowing it to also run any necessary benchmark metrics, given
the performance of the tracker.

This is compatible with any MOT dataset due to their shared file structure formats.

## Dependencies

opencv-python

motmetrics

numpy

## Getting Started

The module was designed to be incredibly easy to use. Because of this, the
only necessary input information is optionally set as the path to the dataset
directory. This path could be absolute, or relative from where you are running
the script. If no path is specified, the module will try to operate assuming
the dataset is in the current directory. Note that the dataset should be stored
exactly as it is downloaded, and your path should lead to wherever the train and test
folders are.

## Example Usage
```python
import benchmark
loader = benchmark.DataLoader(filepath='./', midpoints=True)
for sequence in loader:
    for frame, gt_data in sequence:
        # Tracker code for the current sequence
        my_midpoints = []
        dists = sequence.update_metrics(my_midpoints)
    sequence.display_metrics()
    # Resetting tracker for the next sequence
```
