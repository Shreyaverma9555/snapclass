import io

import librosa
import numpy as np
import streamlit as st


@st.cache_resource
def load_voice_encoder():
    try:
        from resemblyzer import VoiceEncoder
    except ModuleNotFoundError:
        st.error("Voice attendance requires the 'resemblyzer' package. Install it with: pip install resemblyzer")
        return None
    return VoiceEncoder()


def _preprocess_wav(audio):
    try:
        from resemblyzer import preprocess_wav
    except ModuleNotFoundError:
        st.error("Voice attendance requires the 'resemblyzer' package. Install it with: pip install resemblyzer")
        return None
    return preprocess_wav(audio)


def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()
        if encoder is None:
            return None

        audio, _ = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        wav = _preprocess_wav(audio)
        if wav is None:
            return None

        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception as e:
        st.error(f"Voice recognition error: {e}")
        return None


def identify_speaker(new_embedding, candidates_dict, threshold=0.65):
    if new_embedding is None or not candidates_dict:
        return None, 0.0

    new_embedding = np.asarray(new_embedding, dtype=float)
    best_sid = None
    best_score = -1.0

    for sid, stored_embedding in candidates_dict.items():
        if stored_embedding:
            stored_embedding = np.asarray(stored_embedding, dtype=float)
            similarity = float(np.dot(new_embedding, stored_embedding))
            if similarity > best_score:
                best_score = similarity
                best_sid = sid

    if best_score >= threshold:
        return best_sid, best_score

    return None, best_score


def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65):
    try:
        encoder = load_voice_encoder()
        if encoder is None:
            return {}

        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segments = librosa.effects.split(audio, top_db=30)
        identified_results = {}

        for start, end in segments:
            if (end - start) < sr * 0.5:
                continue

            segment_audio = audio[start:end]
            wav = _preprocess_wav(segment_audio)
            if wav is None:
                return {}

            embedding = encoder.embed_utterance(wav)
            sid, score = identify_speaker(embedding, candidates_dict, threshold)

            if sid and (sid not in identified_results or score > identified_results[sid]):
                identified_results[sid] = score

        return identified_results
    except Exception as e:
        st.error(f"Bulk voice processing error: {e}")
        return {}