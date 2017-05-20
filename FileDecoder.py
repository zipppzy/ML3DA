import bpy

class Point():
        def __init__(self,x,y,z):
                self.x=x
                self.y=y
                self.z=z
        def distance(self,B):
                return math.sqrt(((B.x-self.x)**2)+((B.y-self.y)**2)+((B.z-self.z)**2))

def visualize(startPos,goalPos,movePos):
    global currentFrame
    start=bpy.data.objects["Start"]
    goal=bpy.data.objects["Goal"]
    start.location=(startPos.x,startPos.y,startPos.z)
    goal.location=(goalPos.x,goalPos.y,goalPos.z)
    goal.keyframe_insert(data_path="location",frame=currentFrame)
    start.keyframe_insert(data_path="location",frame=currentFrame)
    start.location=(movePos.x,movePos.y,movePos.z)
    currentFrame+=10
    start.keyframe_insert(data_path="location",frame=currentFrame)
    goal.keyframe_insert(data_path="location",frame=currentFrame)
    currentFrame+=1
def reset():
    bpy.data.objects["Start"].animation_data_clear()

currentFrame=1
file=open("animationEncoding.txt","r")
reset()
x=file.read().split(",")
i=0
while i<len(x):
    startPointX=float(x[i])
    i+=1
    startPointY=float(x[i])
    i+=1
    startPointZ=float(x[i])
    i+=1
    pointBX=float(x[i])
    i+=1
    pointBY=float(x[i])
    i+=1
    pointBZ=float(x[i])
    i+=1
    pointAX=float(x[i])
    i+=1
    pointAY=float(x[i])
    i+=1
    pointAZ=float(x[i])
    i+=1
    visualize(Point(startPointX,startPointY,startPointZ),Point(pointBX,pointBY,pointBZ),Point(pointAX,pointAY,pointAZ))
