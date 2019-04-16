import benchmark

# Example gt filename
root = "../HB/HB01/"
seq_filename = root + "seqinfo.ini"
gt_filename = root + "/gt/gt.txt"
extra_gt_filename = root + "gt/speed_truth.txt"

starting_frame = 1
x_pos = 40
y_pos = float(1080 / 2 - 100) + 10
height = float(1080 * 1 / 5) + 80
width = 90
height_speed = 0

sequence_info = benchmark.SequenceLoader(root)

img_width = int(sequence_info.imWidth) # 1920 for this dataset
img_height = int(sequence_info.imHeight) # 1080 for this dataset

fid = open(gt_filename, "w")
x_speed = 3
y_speed = 0.1
extra_fid = open(extra_gt_filename, "w")

for x in range(starting_frame, int(sequence_info.seqLength), 1):
    fid.write(f"{x},1,{int(x_pos)},{int(y_pos)},{width},{int(height)},-1,-1,-1,-1,-1\n")
    if x == 30:
        x_speed = 5
    if x == 110:
        x_speed = 6
    if x == 200:
        x_speed = 5
    if x == 260:
        x_speed = 4
    if x == 150:
        y_speed = 0.5

    if x_pos + width > img_width or x_pos < 0:
        break;
    if y_pos < 0 or y_pos + height > img_height:
        break;

    x_pos += x_speed
    y_pos -= y_speed
    height += height_speed

fid.close()