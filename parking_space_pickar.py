import cv2
import pickle

# Load saved parking positions if available
try:
    with open('CarParkPos.pkl','rb') as f:
        posList=pickle.load(f)
except:
    posList=[]

# Size of each parking spot rectangle
width, height = 105, 49

# Mouse click function to add/remove spots
def MouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:    # left click = add spot
        posList.append((x, y))

    if events == cv2.EVENT_RBUTTONDOWN:    # right click = remove spot
        for i, pos in enumerate(posList):
            x1, y1 = pos

            # check if click is inside a spot
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    # Save updated positions to file
    with open('CarParkPos.pkl','wb') as f:
        pickle.dump(posList,f)

# Setup display window
cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("image", 1280, 720)

# Main loop to display image and handle clicks
while True:
    img = cv2.imread("carParkImg.png")  # load parking lot image
    
    # Draw all saved spots as rectangles
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    # Show image
    cv2.imshow('image', img)

    # Set mouse callback for adding/removing spots
    cv2.setMouseCallback("image", MouseClick)
    
    if cv2.waitKey(1) & 0xFF == 27:      # Exit loop on ESC key

        break

cv2.destroyAllWindows()



