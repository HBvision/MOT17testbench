# Example gt filename
seq_filename = "../HB/HB02/seqinfo.ini"
gt_filename = "../HB/HB02/gt/gt.txt"

starting_frame = 80
x_pos = 0
y_pos = float(1080 / 2 + 100)
height = float(1080 * 3 / 10) + 35
width = 130
height_speed = 1

fid = open(gt_filename, "w")
x_speed = 8
y_speed = 0.5

x_speed = 8
for x in range(starting_frame, 255, 1):
    fid.write(f"{x},1,{int(x_pos)},{int(y_pos)},{width},{int(height)},-1,-1,-1,-1,-1\n")
    # fid.write("%d,1,%d,%d,%d,%d,-1,-1,-1,-1,-1\n".format(x, x_pos, y_pos, width, height))
    if x == 180:
        x_speed = 14

    x_pos += x_speed
    y_pos -= y_speed
    height += height_speed

height = float(1080 * 2 / 5) + 20
x_speed = 12
x_pos = 1650
y_pos = 1080 / 2
y_speed = 0.4
height_speed = -0.45
for x in range(starting_frame, 300, 1):
    if x == 120:
        x_speed = 8
    if x == 180:
        x_speed = 7
        height_speed = -0.6
    fid.write(f"{x},2,{x_pos},{y_pos},{width},{int(height)},-1,-1,-1,-1,-1\n")
    # fid.write("%d,2,%d,%d,%d,%d,-1,-1,-1,-1,-1\n".format(x, x_pos, y_pos, width, height))
    x_pos -= x_speed
    y_pos += y_speed
    height += height_speed

fid.close()