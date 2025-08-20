# streamlit_app.py
# --------------------------------------------
# A2 Cambridge-style Exam (Reading + Listening)
# Run: streamlit run streamlit_app.py
# Optional deps: pip install streamlit gTTS
# --------------------------------------------

import io
import json
import textwrap
from typing import List, Dict
import streamlit as st

# Optional text-to-speech
TTS_AVAILABLE = False
try:
    from gtts import gTTS
    TTS_AVAILABLE = True
except Exception:
    TTS_AVAILABLE = False

# -----------------------------
# Exam content (ENGLISH, A2 CEFR)
# -----------------------------

READING: List[Dict] = [
    {
        "title": "Text 1 – Short Message",
        "text": ("Hi Tom, the football match is at 4:30 p.m. today. "
                 "Let’s meet at the bus stop at 4:00 so we can go together. "
                 "See you! – Ben"),
        "qa": [
            {
                "q": "What time is the match?",
                "options": ["4:00 p.m.", "4:15 p.m.", "4:30 p.m.", "5:00 p.m.", "5:30 p.m."],
                "answer": "C"
            },
            {
                "q": "Where will they meet?",
                "options": ["At school", "At the bus stop", "At the football field", "At Ben’s house", "At the train station"],
                "answer": "B"
            },
            {
                "q": "Who wrote the message?",
                "options": ["Tom", "Ben", "The bus driver", "The football coach", "Tom’s brother"],
                "answer": "B"
            },
            {
                "q": "Why do they meet at 4:00?",
                "options": ["To buy tickets", "To have lunch", "To go together", "To practise football", "To wait for another friend"],
                "answer": "C"
            },
            {
                "q": "What is this text?",
                "options": ["An email", "A letter", "A text message", "A newspaper article", "A poster"],
                "answer": "C"
            },
        ]
    },
    {
        "title": "Text 2 – Notice",
        "text": ("SWIMMING POOL CLOSED\n"
                 "We are cleaning the pool this weekend. "
                 "It will open again on Monday morning. Thank you for your understanding."),
        "qa": [
            {
                "q": "Why is the pool closed?",
                "options": ["There is a party", "There is a competition", "For cleaning", "For repairs", "For painting"],
                "answer": "C"
            },
            {
                "q": "When will it open again?",
                "options": ["Saturday afternoon", "Sunday evening", "Monday morning", "Tuesday morning", "Friday morning"],
                "answer": "C"
            },
            {
                "q": "Who is this notice for?",
                "options": ["Only children", "Swimming teachers", "People who use the pool", "The cleaning staff", "Lifeguards"],
                "answer": "C"
            },
            {
                "q": "How long will it stay closed?",
                "options": ["1 day", "2 days", "3 days", "4 days", "5 days"],
                "answer": "B"   # Weekend (Sat+Sun): 2 days
            },
            {
                "q": "Where would you see this notice?",
                "options": ["In a cinema", "In a restaurant", "In a swimming centre", "In a shop", "At the airport"],
                "answer": "C"
            },
        ]
    },
    {
        "title": "Text 3 – Email",
        "text": ("Dear Anna,\n"
                 "Thanks for your email. I’m excited you’re coming to London next month! "
                 "The weather is usually cold in November, so bring warm clothes. "
                 "We can visit the museums and maybe go to the theatre.\n"
                 "See you soon!\nBest wishes,\nClara"),
        "qa": [
            {
                "q": "Who is visiting London?",
                "options": ["Clara", "Anna", "Both of them", "Clara’s family", "Clara’s friends"],
                "answer": "B"
            },
            {
                "q": "When is Anna coming?",
                "options": ["This week", "Next month", "In summer", "Next year", "In two weeks"],
                "answer": "B"
            },
            {
                "q": "What will the weather be like?",
                "options": ["Warm", "Hot", "Cold", "Rainy every day", "Very sunny"],
                "answer": "C"
            },
            {
                "q": "What does Clara suggest?",
                "options": ["Going shopping", "Visiting museums", "Playing football", "Going to the park", "Taking photos at the zoo"],
                "answer": "B"
            },
            {
                "q": "What is the purpose of this email?",
                "options": ["To invite Anna to a wedding", "To ask Anna to bring food", "To welcome Anna and give advice", "To tell Anna not to come", "To complain about the weather"],
                "answer": "C"
            },
        ]
    },
    {
        "title": "Text 4 – Short Article",
        "text": ("A Day at the Zoo\n"
                 "Last Saturday, my family and I went to the zoo. We saw lions, elephants and monkeys. "
                 "The penguins were my favourite because they were swimming and playing in the water. "
                 "We had lunch at the zoo café and then watched a bird show. It was amazing!"),
        "qa": [
            {
                "q": "Where did the family go?",
                "options": ["To the park", "To the zoo", "To the beach", "To the mountains", "To a farm"],
                "answer": "B"
            },
            {
                "q": "Which animals did they see?",
                "options": ["Tigers, elephants, penguins", "Lions, elephants, monkeys, penguins", "Bears, lions, penguins", "Only penguins", "Lions and giraffes"],
                "answer": "B"
            },
            {
                "q": "Why were the penguins the favourite?",
                "options": ["They were eating", "They were swimming and playing", "They were big", "They were making noise", "They were dancing"],
                "answer": "B"
            },
            {
                "q": "Where did they eat?",
                "options": ["At home", "In a restaurant outside the zoo", "In the zoo café", "In the park", "They didn’t eat"],
                "answer": "C"
            },
            {
                "q": "What did they do after lunch?",
                "options": ["Saw a bird show", "Went home", "Fed the animals", "Took a train ride", "Saw the penguins again"],
                "answer": "A"
            },
        ]
    },
    {
        "title": "Text 5 – Story",
        "text": ("Last summer, Lucas travelled to Spain with his friends. They stayed in a small hotel near the beach. "
                 "Every morning, they went swimming in the sea, and in the afternoons, they visited different towns. "
                 "One day, they took a boat trip to an island, where they had a picnic. "
                 "It was one of the best holidays of Lucas’s life."),
        "qa": [
            {
                "q": "Where did Lucas go on holiday?",
                "options": ["Italy", "Spain", "Portugal", "France", "Greece"],
                "answer": "B"
            },
            {
                "q": "Who went with Lucas?",
                "options": ["His family", "His classmates", "His friends", "His work colleagues", "His neighbours"],
                "answer": "C"
            },
            {
                "q": "What did they do every morning?",
                "options": ["Went shopping", "Went swimming", "Took a boat trip", "Went to towns", "Played football"],
                "answer": "B"
            },
            {
                "q": "What did they do on the island?",
                "options": ["Went swimming", "Had a picnic", "Took photos only", "Visited a castle", "Watched a show"],
                "answer": "B"
            },
            {
                "q": "How did Lucas feel about the holiday?",
                "options": ["It was boring", "It was okay", "It was one of the best", "It was too expensive", "It was a bad experience"],
                "answer": "C"
            },
        ]
    },
]

LISTENING: List[Dict] = [
    {
        "title": "Audio 1 – Message",
        "script": "Hi, this is a message for Laura. Your guitar lesson tomorrow is at 3 p.m. instead of 4 p.m. Please bring your music book.",
        "question": "What time is Laura’s guitar lesson tomorrow?",
        "options": ["2 p.m.", "3 p.m.", "4 p.m.", "5 p.m.", "6 p.m."],
        "answer": "B"
    },
    {
        "title": "Audio 2 – Café Announcement",
        "script": "Welcome to Sunny Café! Today’s special is chicken soup with bread for only five dollars. We also have fresh salads and sandwiches.",
        "question": "What is today’s special?",
        "options": ["Salad", "Chicken soup with bread", "Sandwich", "Pasta", "Pizza"],
        "answer": "B"
    },
    {
        "title": "Audio 3 – Travel Plan",
        "script": "Hi Sam, it’s Jenny. The train leaves at nine fifteen, so let’s meet at the station at nine o’clock near the ticket office.",
        "question": "Where will they meet?",
        "options": ["On the train", "At the bus stop", "Near the ticket office", "In a café", "At Sam’s house"],
        "answer": "C"
    },
    {
        "title": "Audio 4 – Weather Report",
        "script": "Good afternoon! This is a weather report. Tomorrow will be sunny in the morning, but there will be rain in the afternoon. Temperatures will be around eighteen degrees.",
        "question": "What will the weather be like tomorrow afternoon?",
        "options": ["Snowy", "Sunny", "Rainy", "Windy", "Cloudy"],
        "answer": "C"
    },
    {
        "title": "Audio 5 – Sports Programme",
        "script": "Hello, and welcome to our sports programme. Today, we talk to Alex, a young swimmer who won a gold medal last week in the national competition.",
        "question": "What sport does Alex do?",
        "options": ["Running", "Swimming", "Cycling", "Football", "Tennis"],
        "answer": "B"
    },
]

# -----------------------------------
# Helpers
# -----------------------------------
LETTERS = "ABCDE"

def letter_from_index(idx: int) -> str:
    return LETTERS[idx]

def index_from_letter(letter: str) -> int:
    return LETTERS.index(letter)

def answer_key_reading() -> Dict[str, List[str]]:
    key = {}
    for i, block in enumerate(READING, start=1):
        key[f"Text {i}"] = [qa["answer"] for qa in block["qa"]]
    return key

def answer_key_listening() -> Dict[str, str]:
    return {blk["title"]: blk["answer"] for blk in LISTENING}

def tts_bytes(text: str) -> bytes:
    if not TTS_AVAILABLE:
        raise RuntimeError("gTTS not available")
    tts = gTTS(text=text)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()

# -----------------------------------
# UI / App
# -----------------------------------
st.set_page_config(page_title="A2 Cambridge-style Exam", page_icon="📝", layout="wide")

# Minimal styling
st.markdown("""
<style>
.small {font-size:0.9rem;}
.question {padding:0.5rem 0; margin:0.25rem 0; border-bottom:1px dashed #ddd;}
.codebox {background:#f8f9fa; padding:0.5rem 0.75rem; border-radius:6px; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;}
</style>
""", unsafe_allow_html=True)

st.title("A2 Cambridge-style Exam (Reading + Listening)")

if "responses" not in st.session_state:
    st.session_state.responses = {"reading": {}, "listening": {}}
if "submitted" not in st.session_state:
    st.session_state.submitted = False

tabs = st.tabs(["📖 Reading", "🎧 Listening", "✅ Finish & Score"])

# ---------------- Reading Tab ----------------
with tabs[0]:
    st.subheader("Part 1 – Reading")
    st.caption("Instructions: Read each text and select the correct answer A–E for each question.")

    total_reading_q = 0
    answered_reading = 0

    for t_idx, block in enumerate(READING, start=1):
        with st.expander(f"{block['title']}", expanded=True if t_idx == 1 else False):
            st.write(block["text"])
            # init storage
            if t_idx not in st.session_state.responses["reading"]:
                st.session_state.responses["reading"][t_idx] = [None]*len(block["qa"])
            # questions
            for q_idx, qa in enumerate(block["qa"], start=1):
                total_reading_q += 1
                user_choice = st.session_state.responses["reading"][t_idx][q_idx-1]
                label = f"Q{q_idx}. {qa['q']}"
                opts = [f"{LETTERS[i]}) {opt}" for i, opt in enumerate(qa["options"])]
                selection = st.radio(
                    label,
                    options=["(no answer)"] + opts,
                    index=(0 if user_choice is None else user_choice+1),
                    key=f"r-{t_idx}-{q_idx}",
                    label_visibility="visible",
                )
                if selection != "(no answer)":
                    chosen_idx = opts.index(selection)
                    st.session_state.responses["reading"][t_idx][q_idx-1] = chosen_idx
                    answered_reading += 1

    col_a, col_b = st.columns([1,3])
    with col_a:
        st.progress(answered_reading / max(1, total_reading_q), text=f"Answered {answered_reading}/{total_reading_q}")
    with col_b:
        st.info("Answer all questions you can. You can return here before submitting on the **Finish & Score** tab.")

# ---------------- Listening Tab ----------------
with tabs[1]:
    st.subheader("Part 2 – Listening")
    st.caption("Instructions: Listen (or read) each audio and select the correct answer A–E.")

    total_listening_q = len(LISTENING)
    answered_listening = 0

    for a_idx, blk in enumerate(LISTENING, start=1):
        with st.expander(f"{blk['title']}", expanded=True if a_idx == 1 else False):
            st.markdown("**Script (for teacher or TTS):**")
            st.markdown(f"<div class='codebox small'>{blk['script']}</div>", unsafe_allow_html=True)

            # optional TTS
            c1, c2 = st.columns([1,3])
            with c1:
                if TTS_AVAILABLE and st.button(f"🔊 Generate audio {a_idx}", key=f"tts-btn-{a_idx}"):
                    try:
                        audio_bytes = tts_bytes(blk["script"])
                        st.session_state[f"audio_{a_idx}"] = audio_bytes
                        st.success("Audio generated.")
                    except Exception as e:
                        st.error(f"Could not generate audio: {e}")

            with c2:
                if f"audio_{a_idx}" in st.session_state:
                    st.audio(st.session_state[f"audio_{a_idx}"], format="audio/mp3")

            # init response
            if a_idx not in st.session_state.responses["listening"]:
                st.session_state.responses["listening"][a_idx] = None

            st.write(f"**Question:** {blk['question']}")
            opts = [f"{LETTERS[i]}) {opt}" for i, opt in enumerate(blk["options"])]
            current = st.session_state.responses["listening"][a_idx]
            selection = st.radio(
                "Choose one:",
                options=["(no answer)"] + opts,
                index=(0 if current is None else current+1),
                key=f"l-{a_idx}",
            )
            if selection != "(no answer)":
                chosen_idx = opts.index(selection)
                st.session_state.responses["listening"][a_idx] = chosen_idx
                answered_listening += 1

    st.progress(answered_listening / max(1, total_listening_q), text=f"Answered {answered_listening}/{total_listening_q}")
    st.info("You may generate TTS audio (if available) or simply read the script aloud.")

# ---------------- Finish & Score Tab ----------------
with tabs[2]:
    st.subheader("Finish & Score")

    def compute_score():
        reading_points = 0
        reading_total = 0
        reading_detail = []

        for t_idx, block in enumerate(READING, start=1):
            for q_idx, qa in enumerate(block["qa"], start=1):
                reading_total += 1
                correct_letter = qa["answer"]
                correct_idx = index_from_letter(correct_letter)
                user_idx = st.session_state.responses["reading"].get(t_idx, [None]*5)[q_idx-1]
                is_correct = (user_idx == correct_idx)
                if is_correct:
                    reading_points += 1
                reading_detail.append({
                    "text": t_idx,
                    "q": q_idx,
                    "correct": correct_letter,
                    "user": None if user_idx is None else letter_from_index(user_idx),
                    "is_correct": is_correct
                })

        listening_points = 0
        listening_total = len(LISTENING)
        listening_detail = []

        for a_idx, blk in enumerate(LISTENING, start=1):
            correct_letter = blk["answer"]
            correct_idx = index_from_letter(correct_letter)
            user_idx = st.session_state.responses["listening"].get(a_idx, None)
            is_correct = (user_idx == correct_idx)
            if is_correct:
                listening_points += 1
            listening_detail.append({
                "audio": a_idx,
                "correct": correct_letter,
                "user": None if user_idx is None else letter_from_index(user_idx),
                "is_correct": is_correct
            })

        return (reading_points, reading_total, reading_detail,
                listening_points, listening_total, listening_detail)

    col1, col2 = st.columns([1,1])
    with col1:
        submit = st.button("✅ Submit all & Grade", type="primary")
    with col2:
        if st.button("♻️ Reset all answers"):
            st.session_state.responses = {"reading": {}, "listening": {}}
            for k in list(st.session_state.keys()):
                if k.startswith("r-") or k.startswith("l-") or k.startswith("audio_"):
                    del st.session_state[k]
            st.session_state.submitted = False
            st.experimental_rerun()

    if submit:
        st.session_state.submitted = True

    if st.session_state.submitted:
        (r_pts, r_tot, r_det,
         l_pts, l_tot, l_det) = compute_score()

        st.success(f"Your score: Reading {r_pts}/{r_tot}  |  Listening {l_pts}/{l_tot}  |  Total {r_pts + l_pts}/{r_tot + l_tot}")

        with st.expander("📊 Reading – details"):
            for row in r_det:
                icon = "✅" if row["is_correct"] else "❌"
                st.write(f"{icon} Text {row['text']} – Q{row['q']}: Your answer = {row['user']}, Correct = {row['correct']}")

        with st.expander("🎧 Listening – details"):
            for row in l_det:
                icon = "✅" if row["is_correct"] else "❌"
                st.write(f"{icon} Audio {row['audio']}: Your answer = {row['user']}, Correct = {row['correct']}")

        # Downloadable answer key
        key_r = answer_key_reading()
        key_l = answer_key_listening()
        key_all = {
            "reading": key_r,
            "listening": key_l
        }
        key_text = [
            "ANSWER KEY",
            "",
            "Reading:"
        ]
        for k, v in key_r.items():
            key_text.append(f"{k}: " + ", ".join(v))
        key_text.append("")
        key_text.append("Listening:")
        for k, v in key_l.items():
            key_text.append(f"{k}: {v}")
        key_blob = "\n".join(key_text)

        st.download_button(
            "⬇️ Download answer key (TXT)",
            data=key_blob.encode("utf-8"),
            file_name="A2_answer_key.txt",
            mime="text/plain"
        )

        # Export user answers
        user_json = json.dumps(st.session_state.responses, indent=2)
        st.download_button(
            "⬇️ Download my answers (JSON)",
            data=user_json.encode("utf-8"),
            file_name="A2_my_answers.json",
            mime="application/json"
        )

st.markdown("---")
st.caption("Tip: You can add your own MP3 files with st.file_uploader and replace the TTS scripts if you prefer recorded audio.")
