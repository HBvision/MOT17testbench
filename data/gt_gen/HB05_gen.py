import benchmark

# Example gt filename
root = "../HB/HB05/"
seq_filename = root + "seqinfo.ini"
gt_filename = root + "gt/gt.txt"
extra_gt_filename = root + "gt/speed_truth.txt"

sequence_info = benchmark.SequenceLoader(root)
fid = open(gt_filename, "w")

img_width = int(sequence_info.imWidth) # 1920 for this dataset
img_height = int(sequence_info.imHeight) # 1080 for this dataset

starting_frame = 1
x_pos = 40
x_speed = 3
y_pos = float(1080 / 2) - 55
y_speed = 0
height = float(img_height / 2) + 33
height_speed = 0
width =180

extra_fid = open(extra_gt_filename, "w")

for x in range(starting_frame, int(sequence_info.seqLength), 1):
    if x_pos + width > img_width or x_pos < 0:
        print(x)
        break;
    if y_pos < 0 or y_pos + height > img_height:
        print(x)
        break;
    fid.write(f"{x},1,{int(x_pos)},{int(y_pos)},{width},{int(height)},-1,-1,-1,-1,-1\n")
    extra_fid.write(f"{x},1,{int(x_pos)},{int(y_pos)},{width},{int(height)},-1,-1,-1,-1,-1,3.2,0\n")
    if x == 15:
        x_speed = 12
    if x == 70:
        x_speed = 0
    if x == 100:
        x_speed = 3
    if x == 110:
        x_speed = 12
        y_speed = 0.6
    if x == 150:
        x_speed = 13
    if x == 160:
        x_speed = 14


    x_pos += x_speed
    y_pos -= y_speed
    height += height_speed

starting_frame = 1
x_pos = img_width - 100
x_speed = -3
y_pos = float(img_height / 2) - 55
y_speed = 0
height = float(img_height / 2) + 36
height_speed = 0
width = 180

# Sequence length is 212
for x in range(starting_frame, int(sequence_info.seqLength), 1):
    if x_pos < 0:
        print(x)
        break;
    if y_pos < 0 or y_pos + height > img_height:
        print(x)
        break;

    if x_pos + width < img_width:
        fid.write(f"{x},2,{int(x_pos)},{int(y_pos)},{width},{int(height)},-1,-1,-1,-1,-1\n")
        extra_fid.write(f"{x},2,{int(x_pos)},{int(y_pos)},{width},{int(height)},-1,-1,-1,-1,-1,-3.4,0\n")
    else:
        print(x)
    if x == 15:
        x_speed = -15
    if x == 67:
        x_speed = 0
    if x == 120:
        x_speed = 2
    if x == 130:
        x_speed = 12
        y_speed = 0.3
    if x == 145:
        x_speed = 10
    if x == 160:
        x_speed = 13

    x_pos += x_speed
    y_pos -= y_speed
    height += height_speed

fid.close()