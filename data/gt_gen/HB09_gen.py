import benchmark

# Example gt filename
root = "../HB/HB09/"
seq_filename = root + "seqinfo.ini"
gt_filename = root + "/gt/gt.txt"

sequence_info = benchmark.SequenceLoader(root)
fid = open(gt_filename, "w")

img_width = int(sequence_info.imWidth) # 1920 for this dataset
img_height = int(sequence_info.imHeight) # 1080 for this dataset

# First bounding box (Sumati)
starting_frame = 1
x_pos = img_width / 2 - 340
x_speed = 0
y_pos = float(img_height / 4 + 50)
y_speed = 0.5
height = float(img_height / 2)
height_speed = 1
width = 220
width_speed = 0

# Sequence gets way too close at frame 190
ending_frame = 190

for x in range(starting_frame, ending_frame, 1):
    fid.write(f"{x},1,{int(x_pos)},{int(y_pos)},{width},{int(height)},-1,-1,-1,-1,-1\n")
    if x == 40:
        x_speed = -2
        width_speed = 2
        y_speed = 0.8
        height_speed = 4
    if x == 80:
        x_speed = -4
        width_speed = 3
        y_speed = 1.4
        height_speed = 8
    if x == 120:
        x_speed = -4
        width_speed = -1
        y_speed = 3
    if x == 150:
        x_speed = -8
        width_speed = 4

    if y_pos - 10 < 0:
        y_speed = 0

    if y_pos + height > img_height:
        height_speed = y_speed

    x_pos += x_speed
    y_pos -= y_speed
    height += height_speed
    width += width_speed

# Second bounding box (Rohan)
starting_frame = 1
x_pos = img_width / 2 - 100
x_speed = 0
y_pos = float(img_height / 4 + 30)
y_speed = 0.5
height = float(img_height / 2) - 50
height_speed = 1
width = 160
width_speed = 0

for x in range(starting_frame, int(sequence_info.seqLength), 1):
    fid.write(f"{x},1,{int(x_pos)},{int(y_pos)},{width},{int(height)},-1,-1,-1,-1,-1\n")
    if x == 30:
        y_speed = 0.6
        height_speed = 3
        x_speed = -0.3
        width_speed = 1
    if x == 60:
        width_speed = 2
    if x == 90:
        x_speed = -1
        height_speed = 5
    if x == 120:
        y_speed = 2
    if x == 180:
        x_speed = 2
        y_speed = 4
        width_speed = 4
    if x == 200:
        x_speed = 12
        width_speed = 0
        y_speed = 0

    if y_pos - 10 < 0:
        y_speed = 0

    if y_pos + height > img_height:
        height_speed = y_speed

    x_pos += x_speed
    y_pos -= y_speed
    height += height_speed
    width += width_speed

# Third bounding box ()
starting_frame = 1
ending_frame = 220
x_pos = img_width / 2 + 100
x_speed = 0
y_pos = float(img_height / 4) - 35
y_speed = 0.5
height = float(img_height / 2) + 80
height_speed = 1
width = 160
width_speed = 0

for x in range(starting_frame, ending_frame, 1):
    fid.write(f"{x},1,{int(x_pos)},{int(y_pos)},{width},{int(height)},-1,-1,-1,-1,-1\n")
    if x == 30:
        y_speed = 1
        height_speed = 2
        width_speed = 1
    if x == 60:
        y_speed = 2
        height_speed = 5
    if x == 80:
        height_speed = 7
    if x == 90:
        width_speed = 3
    if x == 120:
        y_speed = 3
    if x == 160:
        x_speed = 12
        width_speed = 5
    if x == 180:
        break
    if x == 200:
        x_speed = 9

    if x_pos + width > img_width:
        break
    if y_pos - 10 < 0:
        y_speed = 0
    check = y_pos + height
    if y_pos + height > img_height - 10:
        height_speed = y_speed

    x_pos += x_speed
    y_pos -= y_speed
    height += height_speed
    width += width_speed



fid.close()