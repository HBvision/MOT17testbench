import benchmark

# Example gt filename
root = "../HB/HB03/"
gt_filename = root + "gt/gt.txt"

sequence_info = benchmark.SequenceLoader(root)
fid = open(gt_filename, "w")

img_width = int(sequence_info.imWidth) # 1920 for this dataset
img_height = int(sequence_info.imHeight) # 1080 for this dataset

starting_frame = 45
x_pos = 0
x_speed = 6
y_pos = float(img_height / 2) + 100
y_speed = 0
height = float(img_height * 1 / 5) + 160
width = 120
height_speed = 0.3


for x in range(starting_frame, int(sequence_info.seqLength), 1):
    fid.write(f"{x},1,{int(x_pos)},{int(y_pos)},{width},{int(height)},-1,-1,-1,-1,-1\n")
    if x == 80:
        x_speed = 6
    if x == 120:
        x_speed = 7
        y_speed = 0.4
        height_speed = 0.5
    if x == 150:
        x_speed = 9
        height_speed = 0.6
    if x == 200:
        x_speed = 11
    if x == 230:
        x_speed = 10
    if x == 260:
        x_speed = 3
    x_pos += x_speed
    y_pos -= y_speed
    height += height_speed

starting_frame = 0
x_pos = img_width - 200
y_pos = float(img_height / 2) + 100
x_speed = -8
y_speed = -0.1
height = float(img_height * 1 / 5) + 160
height_speed = -0.4

for x in range(starting_frame, int(sequence_info.seqLength), 1):
    fid.write(f"{x},1,{int(x_pos)},{int(y_pos)},{width},{int(height)},-1,-1,-1,-1,-1\n")
    if x == 40:
        x_speed = -9
    if x == 80:
        x_speed = -10
    if x == 110:
        x_speed = -9
    if x == 130:
        x_speed = -7
    if x == 170:
        x_speed = -8
    if x == 200:
        x_speed = -7

    x_pos += x_speed
    y_pos -= y_speed
    height += height_speed

fid.close()
