import benchmark

# Example gt filename
root = "../HB/HB04/"
seq_filename = root + "seqinfo.ini"
gt_filename = root + "gt/gt.txt"
extra_gt_filename = root + "gt/speed_truth.txt"

sequence_info = benchmark.SequenceLoader(root)
fid = open(gt_filename, "w")

img_width = int(sequence_info.imWidth) # 1920 for this dataset
img_height = int(sequence_info.imHeight) # 1080 for this dataset

starting_frame = 1
x_pos = (img_width) / 2 + 30
x_speed = 0
y_pos = float(img_height / 2 + 130)
y_speed = 0.1
height = float(1080 * 2 / 5) - 25
height_speed = 0
width = 120

extra_fid = open(extra_gt_filename, "w")

for x in range(starting_frame, int(sequence_info.seqLength), 1):
    if y_pos + height < img_height:
        fid.write(f"{x},1,{int(x_pos)},{int(y_pos)},{width},{int(height)},-1,-1,-1,-1,-1\n")
    else:
        print(x)
    if x == 55:
        x_speed = 7
    if x == 80:
        x_speed = 9
    if x == 90:
        x_speed = 11

    if x_pos + width > img_width or x_pos < 0:
        print(x)
        break;
    if y_pos < 0:
        print(x)
        break;

    x_pos += x_speed
    y_pos -= y_speed
    height += height_speed

starting_frame = 1
x_pos = (img_width) / 2 - 130
x_speed = -3
y_pos = float(img_height / 2 + 130)
y_speed = 0.1
height = float(1080 * 2 / 5) - 25
height_speed = 0
width = 120

for x in range(starting_frame, int(sequence_info.seqLength), 1):
    if y_pos + height < img_height:
        fid.write(f"{x},2,{int(x_pos)},{int(y_pos)},{width},{int(height)},-1,-1,-1,-1,-1\n")
    else:
        print(x)
    if x == 30:
        x_speed = -4
    if x == 50:
        x_speed = -7
    if x == 115:
        x_speed = -9

    if x_pos + width > img_width or x_pos < 0:
        print(x)
        break;
    if y_pos < 0:
        print(x)
        break;

    x_pos += x_speed
    y_pos -= y_speed
    height += height_speed

fid.close()