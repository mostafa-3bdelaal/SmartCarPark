# ParkVision 🅿️

**ParkVision** is a smart parking lot monitoring system using Python, OpenCV, and CVZone.  
It automatically detects free and occupied parking spots from images or video, making parking management easier and more efficient.

---

## 🔹 Project Idea

**ParkVision** helps manage parking lots by tracking which spots are free or occupied in real-time.

### How it works:
1. **Mark parking spots**  
   - Load an image of the parking lot.  
   - Left-click to add a spot, right-click to remove a spot.  
   - Spot positions are saved in `CarParkPos.pkl` for future use.  

2. **Process parking lot video**  
   - Converts video frames to grayscale, applies blur, thresholding, and dilation to highlight vehicles.  
   - Checks each marked spot to determine occupancy by counting pixels.  

3. **Display results**  
   - **Green rectangles** = empty spots  
   - **Red rectangles** = occupied spots  
   - Each spot is numbered inside the rectangle  
   - Total free spots are displayed at the top-left corner  

4. **Output video**  
   - Saves a processed video with visual indicators for later review.

---

## 🔹 Features

- Automated detection of parking spot occupancy  
- Manual spot marking with visual feedback  
- Real-time visualization with color-coded rectangles  
- Numbered spots and total free spot counter  
- Sorts spots into columns and rows for clarity  
- Saves output video for sharing or record-keeping  

### Future Enhancements
- Notifications when parking lot is full  
- Integration with a web dashboard for live monitoring  
- Vehicle detection using deep learning models for more accuracy  

---



