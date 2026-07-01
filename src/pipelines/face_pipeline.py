import numpy as np
import streamlit as st
from PIL import Image, ImageDraw
from sklearn.svm import SVC

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    try:
        import dlib
        import face_recognition_models
    except ImportError as exc:
        raise RuntimeError(
            "Face recognition is not available because dlib or "
            "face_recognition_models is not installed in this environment."
        ) from exc

    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec


def _shape_to_np(shape):
    return np.array([(shape.part(i).x, shape.part(i).y) for i in range(shape.num_parts)])


def _eye_aspect_ratio(eye_points):
    vertical_1 = np.linalg.norm(eye_points[1] - eye_points[5])
    vertical_2 = np.linalg.norm(eye_points[2] - eye_points[4])
    horizontal = np.linalg.norm(eye_points[0] - eye_points[3])

    if horizontal == 0:
        return 0

    return (vertical_1 + vertical_2) / (2.0 * horizontal)


def estimate_emotion_from_landmarks(points):
    """Estimate simple classroom emotions from face landmarks."""
    if len(points) < 68:
        return "Neutral"

    left_eye = points[36:42]
    right_eye = points[42:48]
    mouth = points[48:68]

    face_width = max(np.linalg.norm(points[0] - points[16]), 1)
    face_height = max(np.linalg.norm(points[8] - points[27]), 1)

    left_ear = _eye_aspect_ratio(left_eye)
    right_ear = _eye_aspect_ratio(right_eye)
    eye_open_score = (left_ear + right_ear) / 2.0

    mouth_width = np.linalg.norm(points[48] - points[54])
    mouth_open = np.linalg.norm(points[62] - points[66])
    mouth_width_ratio = mouth_width / face_width
    mouth_open_ratio = mouth_open / face_height

    mouth_center_y = np.mean(mouth[:, 1])
    corner_y = (points[48][1] + points[54][1]) / 2.0
    smile_lift = (mouth_center_y - corner_y) / face_height

    if eye_open_score < 0.20:
        return "Sleepy"

    if mouth_width_ratio > 0.36 and (smile_lift > 0.015 or mouth_open_ratio > 0.035):
        return "Happy"

    if smile_lift < -0.010:
        return "Sad"

    return "Neutral"


def _show_face_dependency_error(exc):
    st.info("Face detection using MediaPipe is active")
    st.caption(str(exc))


def get_face_detections(image_np):
    try:
        detector, sp, facerec = load_dlib_models()
    except RuntimeError as exc:
        _show_face_dependency_error(exc)
        return []

    faces = detector(image_np, 1)
    detections = []

    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
        points = _shape_to_np(shape)

        detections.append(
            {
                "encoding": np.array(face_descriptor),
                "emotion": estimate_emotion_from_landmarks(points),
                "box": (face.left(), face.top(), face.right(), face.bottom()),
            }
        )

    return detections


def get_face_embeddings(image_np):
    return [detection["encoding"] for detection in get_face_detections(image_np)]


@st.cache_resource
def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:
        embedding = student.get("face_embedding")
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get("student_id"))

    if len(X) == 0:
        return None

    clf = SVC(kernel="linear", probability=True, class_weight="balanced")

    try:
        clf.fit(X, y)
    except ValueError:
        pass

    return {"clf": clf, "X": X, "y": y}


def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)


def _predict_from_detections(detections):
    detected_student = {}
    detected_emotions = {}

    model_data = get_trained_model()

    if not model_data:
        return detected_student, detected_emotions, []

    clf = model_data["clf"]
    X_train = model_data["X"]
    y_train = model_data["y"]

    all_students = sorted(list(set(y_train)))

    for detection in detections:
        encoding = detection["encoding"]

        if len(all_students) >= 2:
            predicted_id = int(clf.predict([encoding])[0])
        else:
            predicted_id = int(all_students[0])

        student_embedding = X_train[y_train.index(predicted_id)]
        best_match_score = np.linalg.norm(student_embedding - encoding)

        resemblance_threshold = 0.6

        if best_match_score <= resemblance_threshold:
            detected_student[predicted_id] = True
            detected_emotions.setdefault(predicted_id, []).append(detection["emotion"])

    return detected_student, detected_emotions, all_students


def _students_from_enrollment(enrolled_students):
    if enrolled_students is None:
        return get_all_students()

    students = []
    for node in enrolled_students:
        student = node.get("students") if isinstance(node, dict) else None
        if student:
            students.append(student)
    return students


def _nearest_student(encoding, students, threshold=0.6):
    best_student = None
    best_distance = None

    for student in students:
        embedding = student.get("face_embedding")
        if not embedding:
            continue

        distance = float(np.linalg.norm(np.array(embedding) - encoding))
        if best_distance is None or distance < best_distance:
            best_student = student
            best_distance = distance

    if best_student is None or best_distance is None or best_distance > threshold:
        return None, best_distance

    return best_student, best_distance


def identify_faces(image_np, candidate_students=None, threshold=0.6):
    """Return one recognition record per detected face."""
    students = candidate_students if candidate_students is not None else get_all_students()
    detections = get_face_detections(image_np)
    face_records = []

    for index, detection in enumerate(detections, start=1):
        student, distance = _nearest_student(detection["encoding"], students, threshold)

        face_records.append(
            {
                "face": index,
                "box": detection["box"],
                "encoding": detection["encoding"],
                "emotion": detection["emotion"],
                "student_id": student.get("student_id") if student else None,
                "name": student.get("name") if student else "Unknown",
                "match_distance": distance,
                "status": "Known" if student else "Unknown",
            }
        )

    return face_records


def _duplicate_group_for(encoding, groups, threshold=0.6):
    for group_number, group_encodings in groups.items():
        if any(np.linalg.norm(existing - encoding) <= threshold for existing in group_encodings):
            group_encodings.append(encoding)
            return group_number

    group_number = len(groups) + 1
    groups[group_number] = [encoding]
    return group_number


def _annotate_image(image, face_records):
    annotated = Image.fromarray(image).copy()
    draw = ImageDraw.Draw(annotated)

    for record in face_records:
        left, top, right, bottom = record["box"]
        label = f"P{record['person_group']}: {record['name']}"
        if record.get("student_id"):
            label += f" ({record['student_id']})"

        draw.rectangle((left, top, right, bottom), outline=(0, 180, 80), width=4)
        text_bbox = draw.textbbox((left, top), label)
        text_height = text_bbox[3] - text_bbox[1]
        label_top = max(0, top - text_height - 8)
        draw.rectangle(
            (left, label_top, left + text_bbox[2] - text_bbox[0] + 8, label_top + text_height + 6),
            fill=(0, 180, 80),
        )
        draw.text((left + 4, label_top + 3), label, fill=(255, 255, 255))

    return annotated


def analyze_classroom_images(images, enrolled_students=None, threshold=0.6):
    """Analyze classroom photos for counts, duplicates, recognition, and annotations."""
    candidate_students = _students_from_enrollment(enrolled_students)
    duplicate_groups = {}
    detected_students = {}
    detected_emotions = {}
    photo_summaries = []
    face_rows = []
    annotated_images = []

    for image_index, image in enumerate(images, start=1):
        image_np = np.array(image.convert("RGB"))
        face_records = identify_faces(image_np, candidate_students, threshold)

        for record in face_records:
            person_group = _duplicate_group_for(record["encoding"], duplicate_groups, threshold)
            record["person_group"] = person_group
            source = f"Photo {image_index}"

            if record["student_id"]:
                student_id = int(record["student_id"])
                detected_students.setdefault(student_id, []).append(source)
                detected_emotions.setdefault(student_id, []).append(record["emotion"])

            face_rows.append(
                {
                    "Image": source,
                    "Face": record["face"],
                    "Person Group": f"Person {person_group}",
                    "Name": record["name"],
                    "Student ID": record["student_id"] or "-",
                    "Match Distance": round(record["match_distance"], 3)
                    if record["match_distance"] is not None
                    else "-",
                    "Emotion": record["emotion"],
                    "Status": record["status"],
                }
            )

        photo_summaries.append(
            {
                "Image": f"Photo {image_index}",
                "Detected Faces": len(face_records),
                "Known Students": sum(1 for record in face_records if record["student_id"]),
                "Unknown Faces": sum(1 for record in face_records if not record["student_id"]),
            }
        )
        annotated_images.append(_annotate_image(image_np, face_records))

    return {
        "detected_students": detected_students,
        "detected_emotions": detected_emotions,
        "photo_summaries": photo_summaries,
        "face_rows": face_rows,
        "annotated_images": annotated_images,
        "unique_people": len(duplicate_groups),
    }

def predict_attendance(class_image_np):
    detections = get_face_detections(class_image_np)
    detected_student, _, all_students = _predict_from_detections(detections)
    return detected_student, all_students, len(detections)


def predict_attendance_with_emotions(class_image_np):
    detections = get_face_detections(class_image_np)
    detected_student, detected_emotions, all_students = _predict_from_detections(detections)
    return detected_student, all_students, len(detections), detected_emotions
