import benchmark

# Example gt filename
root = "../HB/HB02/"
seq_filename = "../HB/HB02/seqinfo.ini"
gt_filename = "../HB/HB02/gt/gt.txt"
extra_gt_filename = root + "gt/speed_truth.txt"
sequence_info = benchmark.SequenceLoader(root)

img_width = int(sequence_info.imWidth) # 1920 for this dataset
img_height = int(sequence_info.imHeight) # 1080 for this dataset
starting_frame = 80
x_pos = 0
y_pos = float(1080 / 2 + 100)
height = float(1080 * 3 / 10) + 35
width = 130
height_speed = 1

fid = open(gt_filename, "w")
x_speed = 8
y_speed = 0.5
extra_fid = open(extra_gt_filename, "w")

x_speed = 8
for x in range(starting_frame, 255, 1):
    fid.write(f"{x},1,{int(x_pos)},{int(y_pos)},{width},{int(height)},-1,-1,-1,-1,-1\n")
    if x == 180:
        x_speed = 14

    if x_pos + width > img_width or x_pos < 0:
        break;
    if y_pos < 0 or y_pos + height > img_height:
        break;

    x_pos += x_speed
    y_pos -= y_speed
    height += height_speed

starting_frame = 60
height = float(1080 * 2 / 5) + 20
x_speed = 12
x_pos = 1850
y_pos = 1080 / 2
y_speed = 0.4
height_speed = -0.45
for x in range(starting_frame, 300, 1):
    fid.write(f"{x},2,{x_pos},{y_pos},{width},{int(height)},-1,-1,-1,-1,-1\n")
    if x == 80:
        height = float(1080 * 2 / 5) + 20
        x_speed = 12
        x_pos = 1650
        y_pos = 1080 / 2
        y_speed = 0.4
        height_speed = -0.45
    if x == 120:
        x_speed = 8
    if x == 180:
        x_speed = 7
        height_speed = -0.6

    if x_pos + width > img_width or x_pos < 0:
        break;
    if y_pos < 0 or y_pos + height > img_height:
        break;

    x_pos -= x_speed
    y_pos += y_speed
    height += height_speed

fid.close()