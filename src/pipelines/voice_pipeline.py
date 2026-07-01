import io

import librosa
import numpy as np
import streamlit as st


VOICE_SAMPLE_RATE = 16000
VOICE_EMBEDDING_SIZE = 80


def _normalize(vector):
    vector = np.asarray(vector, dtype=np.float32)
    norm = np.linalg.norm(vector)
    return vector / norm if norm > 0 else vector


def _embedding_from_audio(audio):
    """Create a small, deployment-friendly MFCC speaker embedding."""
    audio = np.asarray(audio, dtype=np.float32)
    audio, _ = librosa.effects.trim(audio, top_db=30)
    if len(audio) < VOICE_SAMPLE_RATE // 2:
        return None

    mfcc = librosa.feature.mfcc(
        y=audio,
        sr=VOICE_SAMPLE_RATE,
        n_mfcc=40,
        n_fft=512,
        hop_length=160,
    )
    embedding = np.concatenate((mfcc.mean(axis=1), mfcc.std(axis=1)))
    return _normalize(embedding)


def get_voice_embedding(audio_bytes):
    try:
        audio, _ = librosa.load(io.BytesIO(audio_bytes), sr=VOICE_SAMPLE_RATE, mono=True)
        embedding = _embedding_from_audio(audio)
        if embedding is None:
            st.error("Please record at least half a second of clear speech.")
            return None
        return embedding.tolist()
    except Exception as exc:
        st.error(f"Voice recognition error: {exc}")
        return None


def identify_speaker(new_embedding, candidates_dict, threshold=0.82):
    if new_embedding is None or not candidates_dict:
        return None, 0.0

    new_embedding = _normalize(new_embedding)
    best_sid = None
    best_score = -1.0

    for sid, stored_embedding in candidates_dict.items():
        if not stored_embedding:
            continue
        stored_embedding = np.asarray(stored_embedding, dtype=np.float32)
        # Ignore embeddings created by an older, incompatible voice model.
        if stored_embedding.shape != new_embedding.shape:
            continue
        score = float(np.dot(new_embedding, _normalize(stored_embedding)))
        if score > best_score:
            best_score = score
            best_sid = sid

    if best_score >= threshold:
        return best_sid, best_score
    return None, best_score


def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.82):
    try:
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=VOICE_SAMPLE_RATE, mono=True)
        segments = librosa.effects.split(audio, top_db=30)
        identified_results = {}

        for start, end in segments:
            if end - start < sr * 0.5:
                continue
            embedding = _embedding_from_audio(audio[start:end])
            if embedding is None:
                continue
            sid, score = identify_speaker(embedding, candidates_dict, threshold)
            if sid is not None and score > identified_results.get(sid, -1.0):
                identified_results[sid] = score

        return identified_results
    except Exception as exc:
        st.error(f"Bulk voice processing error: {exc}")
        return {}