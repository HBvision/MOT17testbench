import benchmark
import cv2

loader = benchmark.DataLoader(filepath='./data/')

for sequence in loader:
    for frame, gt_data in sequence:
        for box in gt_data:
            int_box = [int(x) for x in box]
            cv2.rectangle(frame, (int_box[0], int_box[1]), (int_box[0] + int_box[2], int_box[1] + int_box[3]), (0, 255, 0), 3)
        cv2.imshow('image', frame)
        cv2.waitKey(1)

cv2.destroyAllWindows()