cmd = ''


fd = open("./video_fifo", 'w')
while(cmd != 'quit'):
    cmd = input("Type a command: ")
    if cmd == "pause":
        print("pause the video")
        fd.write('pause\n')
    elif cmd == "progress":
        fd.write('osd_show_progression\n')    
    elif cmd == "seek":
        fd.write('seek 10 0\n')
    elif cmd == "stop":
        fd.write('stop\n')
 
    fd.flush()

fd.close()
