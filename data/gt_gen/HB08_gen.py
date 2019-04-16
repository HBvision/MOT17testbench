import benchmark

# Example gt filename
root = "../HB/HB08/"
seq_filename = root + "seqinfo.ini"
gt_filename = root + "/gt/gt.txt"

sequence_info = benchmark.SequenceLoader(root)
fid = open(gt_filename, "w")

img_width = int(sequence_info.imWidth) # 1920 for this dataset
img_height = int(sequence_info.imHeight) # 1080 for this dataset

starting_frame = 1
x_pos = float(img_width * 1 / 2) - 150
x_speed = 0
y_pos = float(img_height * 1 / 4) - 100
y_speed = 0.2
height = float(img_height / 2) - 50
height_speed = 0
width = 180
width_speed = 0


for x in range(starting_frame, int(sequence_info.seqLength), 1):
    fid.write(f"{int(x)},1,{int(x_pos)},{int(y_pos)},{int(width)},{int(height)},-1,-1,-1,-1,-1\n")
    if x == 30:
        x_speed = -0.6
        width_speed = 1
        height_speed = 1
    if x == 70:
        height_speed = 3
    if x == 95:
        y_speed = 1
        height_speed = 5
    if x == 105:
        height_speed = 9
        x_speed = -3
        width_speed = 6
    if x == 115:
        x_speed = -5
        width_speed = 8
        height_speed = 12
    if x == 130:
        y_speed = 3
        height_speed = 6
        x_speed = -5
        width_speed = 5
    if x == 140:
        width_speed = 5.5
    if x ==170:
        x_speed = -3
        width_speed = -4
    if x == 190:
        x_speed = -7
        width_speed = 3
    # if x == 180:
    #     x_speed = -8
    #     width_speed = 6
    if y_pos < 10:
        y_speed = 0
        height = img_height - 20
    if y_pos + height > img_height - 10:
        height_speed = y_speed
    x_pos += x_speed
    y_pos -= y_speed
    height += height_speed
    width += width_speed

fid.close()