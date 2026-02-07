import cv2
import pickle
import cvzone
import numpy as np

# Video of the parking lot
cap = cv2.VideoCapture('carpark.mp4')

# Load saved parking spot positions
with open('CarParkPos.pkl', 'rb') as f:
    posList = pickle.load(f)

width, height = 105, 49  # size of each parking spot

# Function to sort spots by columns first
def sortPosListColumns(posList, colTolerance=20):
    """
    Sort parking spots vertically first:
    - First column from top to bottom
    - Then second column, etc.
    colTolerance: allows small deviation in X for spots in the same column
    """

    # Sort initially by X (columns)
    posListSorted = sorted(posList, key=lambda x: x[0])
    cols = []

    for pos in posListSorted:
        placed = False
        for col in cols:
            if abs(pos[0] - col[0][0]) < colTolerance:
                col.append(pos)
                placed = True
                break
                
        if not placed:
            cols.append([pos])

    # Sort each column by Y (top to bottom) and merge all columns
    finalList = []
    for col in cols:
        colSorted = sorted(col, key=lambda x: x[1])
        finalList.extend(colSorted)

    return finalList

# Function to check and draw parking spots
def CheckParkingSpace(imgPro):
    """
    Check each spot:
    - Green and thick if empty
    - Red and thin if occupied
    - Number each spot inside the rectangle
    - Show free spots on top-left
    """
    spaceCounter = 0

    # Sort spots vertically
    posListSorted = sortPosListColumns(posList)

    for i, pos in enumerate(posListSorted):
        x, y = pos

        # Crop the spot area and count white pixels
        imgCrop = imgPro[y:y+height, x:x+width]
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            color = (0, 255, 0)  # empty
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)  # occupied
            thickness = 2

        # Draw rectangle around spot
        cv2.rectangle(img, (x, y), (x + width, y + height), color, thickness)

        # Draw number inside the spot
        cvzone.putTextRect(
            img,
            str(i + 1),
            (x + 5, y + 25),
            scale=1,
            thickness=2,
            offset=5,
            colorR=color
        )

    # Show number of free spots on top-left
    cvzone.putTextRect(
        img,
        f'Free: {spaceCounter}/{len(posList)}',
        (10, 40),
        scale=3,
        thickness=5,
        offset=20,
        colorR=(0, 200, 0)
    )

# Setup display window
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Image", 1280, 720)

# Setup video writer to save output
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

out = cv2.VideoWriter(
    'carpark_output.mp4',                    # output file name
    cv2.VideoWriter_fourcc(*'mp4v'),         # codec
    fps,                                     # frames per second
    (frame_width, frame_height)              # video size
)

# Main loop to process video
while True:
    # Restart video if it ends
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    if not success:
        break

    # Process image to detect parking spots
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 5)
    imgThreshold = cv2.adaptiveThreshold(
        imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 25, 16
    )
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    # Check spots and draw rectangles
    CheckParkingSpace(imgDilate)

    # Save current frame to output video
    out.write(img)

    # Show video
    cv2.imshow('Image', img)

    # Exit on Esc key
    if cv2.waitKey(1) & 0xFF == 27:  # esc
        break

cap.release()
out.release()
cv2.destroyAllWindows()
