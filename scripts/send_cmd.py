import json, socket, sys
def send(d):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.connect(("127.0.0.1",8765))
    s.sendall(json.dumps(d).encode("utf-8")); print(s.recv(65536).decode("utf-8")); s.close()

if __name__=="__main__":
    m=sys.argv[1]
    if m=="set_pose":
        _,_,path,tx,ty,tz,rx,ry,rz=sys.argv
        send({"cmd":"set_pose","path":path,"t":[float(tx),float(ty),float(tz)],"r":[float(rx),float(ry),float(rz)]})
    elif m=="set_camera":
        _,_,path,tx,ty,tz,rx,ry,rz=sys.argv
        send({"cmd":"set_camera","path":path,"t":[float(tx),float(ty),float(tz)],"r":[float(rx),float(ry),float(rz)]})
    elif m=="add_cube": _,_,path,size=sys.argv; send({"cmd":"add_cube","path":path,"size":float(size)})
    elif m=="rm":       _,_,path=sys.argv;     send({"cmd":"remove_prim","path":path})
    elif m=="vis":      _,_,path,flag=sys.argv;send({"cmd":"set_visibility","path":path,"visible":flag.lower()=="true"})
    elif m=="attr":     _,_,path,attr,val=sys.argv; send({"cmd":"set_attr","path":path,"attr":attr,"value":val})
    elif m=="open":     _,_,f=sys.argv;        send({"cmd":"open_stage","path":f})
    elif m=="save":     send({"cmd":"save"})
    # Animation commands (Character Kitchen project)
    elif m=="import_fbx": _,_,f=sys.argv;      send({"cmd":"import_fbx","path":f})
    elif m=="play":     
        if len(sys.argv) > 2:
            _,_,start,end=sys.argv; send({"cmd":"play","start":int(start),"end":int(end)})
        else:
            send({"cmd":"play"})
    elif m=="stop":     send({"cmd":"stop"})
    elif m=="set_time": _,_,frame=sys.argv;    send({"cmd":"set_time","frame":int(frame)})
    elif m=="get_time": send({"cmd":"get_time"})
    # Color command (Box Color Change project)
    elif m=="set_color": _,_,path,color=sys.argv; send({"cmd":"set_color","path":path,"color":color})
    # List objects command (Warehouse project)
    elif m=="list_objects":
        if len(sys.argv) > 2:
            _,_,obj_type=sys.argv; send({"cmd":"list_objects","type":obj_type})
        else:
            send({"cmd":"list_objects"})
    # Viewport refresh command
    elif m=="refresh": send({"cmd":"refresh"})
