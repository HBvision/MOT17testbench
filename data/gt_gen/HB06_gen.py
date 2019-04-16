import benchmark

# Example gt filename
root = "../HB/HB06/"
seq_filename = root + "seqinfo.ini"
gt_filename = root + "gt/gt.txt"
extra_gt_filename = root + "gt/speed_truth.txt"

sequence_info = benchmark.SequenceLoader(root)
fid = open(gt_filename, "w")

img_width = int(sequence_info.imWidth) # 1920 for this dataset
img_height = int(sequence_info.imHeight) # 1080 for this dataset

starting_frame = 1
x_pos = (img_width / 2) + 30
x_speed = 0
y_pos = float(img_height / 2) + 50
y_speed = 0
height = y_pos - 100
height_speed = 0
width = 150

extra_fid = open(extra_gt_filename, "w")

for x in range(starting_frame, int(sequence_info.seqLength), 1):
    fid.write(f"{x},1,{int(x_pos)},{int(y_pos)},{width},{int(height)},-1,-1,-1,-1,-1\n")
    extra_fid.write(f"{x},1,{int(x_pos)},{int(y_pos)},{width},{int(height)},-1,-1,-1,-1,-1,0,0\n")

    if x == 170:
        x_speed = 1
        y_speed = 0.3
        height_speed = 0.3

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
x_pos = img_width - 235
x_speed = 0
y_pos = float(img_height / 2) + 60
y_speed = 0
height = float(img_height / 2) - 100
height_speed = 0
width = 150

for x in range(starting_frame, int(sequence_info.seqLength), 1):
    fid.write(f"{x},2,{int(x_pos)},{int(y_pos)},{width},{int(height)},-1,-1,-1,-1,-1\n")
    extra_fid.write(f"{x},1,{int(x_pos)},{int(y_pos)},{width},{int(height)},-1,-1,-1,-1,-1,-3.1,-0.01\n")

    if x == 15:
        x_speed = -2
    if x == 30:
        x_speed = -10
    if x == 50:
        x_speed = -12
        y_speed = -0.4
        height_speed = -0.2
    if x == 130:
        x_speed = -13
    if x == 150:
        x_speed = -10

    if x_pos + width > img_width or x_pos < 0:
        print(x)
        break;
    if y_pos < 0 or y_pos + height > img_height:
        print(x)
        break;
    # Note: sequence length is 202
    x_pos += x_speed
    y_pos -= y_speed
    height += height_speed


fid.close()