import benchmark
import cv2

dataset_path = './data/' + "HB"
# dataset_path = './data/' + input("Please input name of the dataset: ")
# dataset_path = root + '/' + input("Please input the name of the dataset: ")

sequence = benchmark.SequenceLoader(dataset_path + '/HB03', detections=True)

frame_num = 1
count = 1
# for frame, gt_data in sequence:

for frame, gt_data in sequence:
    for box in gt_data:
        int_box = [int(x) for x in box]
        if count == 1:
            cv2.rectangle(frame, (int_box[0], int_box[1]), (int_box[0] + int_box[2], int_box[1] + int_box[3]),
                          (0, 255, 0), 3)
            count += 1
        elif count == 2:
            cv2.rectangle(frame, (int_box[0], int_box[1]), (int_box[0] + int_box[2], int_box[1] + int_box[3]),
                          (0, 0, 255), 3)
            count += 1
        elif count == 3:
            cv2.rectangle(frame, (int_box[0], int_box[1]), (int_box[0] + int_box[2], int_box[1] + int_box[3]),
                          (255, 0, 0), 3)

    new_frame = cv2.resize(frame, (int(1366 / 2), int(768 / 2)))
    # new_frame = frame
    cv2.putText(new_frame, f'{frame_num}', (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255))
    cv2.imshow('image', new_frame)
    cv2.waitKey(1)
    frame_num += 1
    count = 1

# loader = benchmark.DataLoader(dataset_path)
#
# for sequence in loader:
#     for frame, gt_data in sequence:
#         for box in gt_data:
#             int_box = [int(x) for x in box]
#             cv2.rectangle(frame, (int_box[0], int_box[1]), (int_box[0] + int_box[2], int_box[1] + int_box[3]), (0, 255, 0), 3)
#         cv2.imshow('image', frame)
#         cv2.waitKey(1)

cv2.destroyAllWindows()