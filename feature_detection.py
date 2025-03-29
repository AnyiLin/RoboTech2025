import cv2
import numpy as np

def get_bounding_boxes(image, debug=False):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(nfeatures=6000)

    keypoints, _ = orb.detectAndCompute(gray, None)
    vicinity_threshold = 5
    min_neighbors = 8 

    filtered_keypoints = []
    for i, kp in enumerate(keypoints):
        (x1, y1) = kp.pt
        neighbor_count = 0
        for j, other_kp in enumerate(keypoints):
            if i == j:
                continue
            (x2, y2) = other_kp.pt
            distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            if distance < vicinity_threshold:
                neighbor_count += 1
        if neighbor_count >= min_neighbors:
            filtered_keypoints.append(kp)

    mask = np.zeros_like(gray, dtype=np.uint8)

    circle_radius = 0
    for kp in filtered_keypoints:
        x, y = int(kp.pt[0]), int(kp.pt[1])
        cv2.circle(mask, (x, y), circle_radius, 255, -1)

    dilation_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    mask_dilated = cv2.dilate(mask, dilation_kernel, iterations=1)

    closing_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask_closed = cv2.morphologyEx(mask_dilated, cv2.MORPH_CLOSE, closing_kernel)

    contours, _ = cv2.findContours(mask_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
    areas = []
    kp_counts = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        boxes.append((x, y, w, h))
        areas.append(w * h)
        
        count = 0
        for kp in keypoints:
            # The test returns >= 0 if the point is inside or on the contour.
            if cv2.pointPolygonTest(cnt, kp.pt, False) >= 0:
                count += 1
        kp_counts.append(count)

    if len(areas) == 0 or len(kp_counts) == 0:
        print("No blobs to filter.")
        exit()

    max_area = max(areas)
    max_kp = max(kp_counts)

    alpha = 0.2  # Weight for area
    beta = 0.8   # Weight for keypoint count

    combined_scores = []
    for area, count in zip(areas, kp_counts):
        normalized_area = area / max_area
        normalized_kp = count / max_kp if max_kp != 0 else 0
        score = alpha * normalized_area + beta * normalized_kp
        combined_scores.append(score)

    combined_threshold = 0.1
    filtered_boxes = [box for box, score in zip(boxes, combined_scores) if score >= combined_threshold]


    # --- Step 7: Draw the Bounding Boxes ---
    filtered_annotated_image = image.copy()
    for (x, y, w, h) in filtered_boxes:
        cv2.rectangle(filtered_annotated_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    for idx, (x, y, w, h) in enumerate(filtered_boxes):
        # Put a number at the top-left corner of the bounding box.
        cv2.putText(
            filtered_annotated_image,
            str(idx), 
            (x, y - 10), 
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7, 
            (0, 0, 255), 
            2,
            cv2.LINE_AA
        )
    
    if debug:
        image_all = cv2.drawKeypoints(image, keypoints, None, color=(0, 255, 0), flags=0)
        image_filtered = cv2.drawKeypoints(image, filtered_keypoints, None, color=(0, 0, 255), flags=0)
        annotated_image = image.copy()
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(annotated_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.drawContours(annotated_image, [cnt], -1, (255, 0, 0), 1)

        # output_filename = 'output.mp4'
        # fps = 60  # Frames per second
        # frame_size = (mask_closed.shape[1], mask_closed.shape[0])
        # fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # FourCC for MP4 (other options: 'X264', 'avc1', etc.)

        # # Create the VideoWriter object
        # video_writer = cv2.VideoWriter(output_filename, fourcc, fps, frame_size)
        # base_image = np.zeros_like(gray, dtype=np.uint8)
        # dilation_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
        # closing_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

        # for i in range(600):
        #     keypoints_slice = filtered_keypoints[i*10:i*10+10]
        #     for kp in keypoints_slice:
        #         x, y = int(kp.pt[0]), int(kp.pt[1])
        #         cv2.circle(base_image, (x, y), 0, 255, -1)
        #     temp = cv2.dilate(base_image, dilation_kernel, iterations=1)
        #     temp2 = cv2.morphologyEx(temp, cv2.MORPH_CLOSE, closing_kernel)
        #     video_writer.write(temp2)
        # video_writer.release()
        
        cv2.imshow("All Keypoints (Green)", image_all)
        cv2.imshow("Filtered Keypoints (Red)", image_filtered)
        cv2.imshow("Grouped Keypoint Mask", mask_closed)
        cv2.imshow("Annotated Image with Bounding Boxes", annotated_image)
        cv2.imshow("Annotated Image with Filtered Bounding Boxes", filtered_annotated_image)
        cv2.imwrite("all_keypoints.png", image_all)
        cv2.imwrite("filtered_keypoints.png", image_filtered)
        cv2.imwrite("grouped_keypoint_mask.png", mask_closed)
        cv2.imwrite("annotated_image.png", annotated_image)
        cv2.imwrite("filtered_annotated_image.png", filtered_annotated_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return filtered_boxes, filtered_annotated_image

if __name__ == "__main__":
    number = 2
    file_type = "png"
    image_path = f"./images/pipe_{number}.{file_type}"
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image '{image_path}'")
        exit()
    boxes, annotated = get_bounding_boxes(image, True)
    cv2.imwrite(f"./images/pipe_{number}_annotated.{file_type}", annotated)

