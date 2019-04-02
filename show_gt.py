import benchmark
import cv2

dataset_path = './data/' + "HB"
#dataset_path = './data/' + input("Please input name of the dataset: ")
#dataset_path = root + '/' + input("Please input the name of the dataset: ")

loader = benchmark.DataLoader(dataset_path)

for sequence in loader:
    for frame, gt_data in sequence:
        for box in gt_data:
            int_box = [int(x) for x in box]
            cv2.rectangle(frame, (int_box[0], int_box[1]), (int_box[0] + int_box[2], int_box[1] + int_box[3]), (0, 255, 0), 3)
        cv2.imshow('image', frame)
        cv2.waitKey(1)

cv2.destroyAllWindows()