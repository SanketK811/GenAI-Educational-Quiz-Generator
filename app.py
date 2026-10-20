"""AI-Powered Educational Quiz Generator.

A small Streamlit application that generates multiple-choice questions from a
topic or an uploaded text file. If an OpenAI API key is available the
questions are generated with AI; otherwise built-in sample questions are used
so the app always works.

Run with:  streamlit run app.py
"""

from __future__ import annotations

import json
import os
import random
import re
from typing import Any, Dict, List, Optional, Tuple

import streamlit as st

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency
    OpenAI = None
    OPENAI_AVAILABLE = False

from sample_questions import SAMPLE_BANKS

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------
DEFAULT_MODEL = "gpt-4o-mini"
LETTERS = ["A", "B", "C", "D"]
MIN_QUESTIONS = 5
MAX_QUESTIONS = 10
MAX_SOURCE_CHARS = 6000

st.set_page_config(
    page_title="AI-Powered Quiz Generator",
    page_icon="🧠",
    layout="centered",
)


# --------------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------------
def get_config_value(name: str, default: str = "") -> str:
    """Read a value from Streamlit secrets or an environment variable."""
    try:
        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass
    return os.getenv(name, default) or default


def read_uploaded_file(uploaded) -> str:
    """Decode an uploaded text file safely."""
    if uploaded is None:
        return ""
    raw = uploaded.read()
    if isinstance(raw, str):
        return raw
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return raw.decode(encoding)
        except (UnicodeDecodeError, AttributeError):
            continue
    return raw.decode("utf-8", errors="ignore")


def pretty_topic_from_filename(filename: str) -> str:
    stem = os.path.splitext(os.path.basename(filename or ""))[0]
    stem = stem.replace("_", " ").replace("-", " ").strip()
    return stem.title() if stem else "Uploaded Notes"


# --------------------------------------------------------------------------
# AI question generation
# --------------------------------------------------------------------------
def build_prompt(topic: str, source_text: str, count: int) -> str:
    topic = topic or "the provided study material"
    prompt = [
        f"Create exactly {count} multiple-choice questions about: {topic}.",
        "",
        "Rules:",
        f"1. Return exactly {count} questions.",
        "2. Each question must have exactly 4 options.",
        "3. Exactly one option must be correct.",
        "4. Include a short explanation (1-2 sentences) for the correct answer.",
        "5. Questions must be clear, factual and suitable for a college student.",
        "",
        "Return ONLY valid JSON in this exact shape:",
        '{',
        '  "questions": [',
        '    {',
        '      "question": "Question text?",',
        '      "options": ["Option A", "Option B", "Option C", "Option D"],',
        '      "answer": "A",',
        '      "explanation": "Why this answer is correct."',
        '    }',
        '  ]',
        '}',
        "",
        '"answer" must be one of "A", "B", "C" or "D".',
    ]
    if source_text:
        prompt.extend(
            [
                "",
                "Base the questions on the following study material:",
                "----- START MATERIAL -----",
                source_text[:MAX_SOURCE_CHARS],
                "----- END MATERIAL -----",
            ]
        )
    return "\n".join(prompt)


def extract_json(text: str) -> Any:
    """Pull a JSON object out of a model response."""
    if not text:
        raise ValueError("The AI returned an empty response.")

    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    for opener, closer in (("{", "}"), ("[", "]")):
        start = cleaned.find(opener)
        end = cleaned.rfind(closer)
        if start != -1 and end > start:
            try:
                return json.loads(cleaned[start:end + 1])
            except json.JSONDecodeError:
                continue

    raise ValueError("Could not find valid JSON in the AI response.")


def parse_answer(value: Any, options: List[str]) -> Optional[int]:
    """Convert an answer in many possible formats into a 0-based index."""
    if value is None or isinstance(value, bool):
        return None

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        number = int(value)
        if 0 <= number <= 3:
            return number
        if 1 <= number <= 4:
            return number - 1
        return None

    text = str(value).strip()
    if not text:
        return None

    match = re.match(r"^(?:OPTION\s*)?\(?([A-Da-d])\)?[\.\):]?\s*$", text)
    if match:
        return LETTERS.index(match.group(1).upper())

    lowered = [option.strip().lower() for option in options]
    if text.lower() in lowered:
        return lowered.index(text.lower())

    digits = re.sub(r"\D", "", text)
    if digits and len(digits) <= 2:
        number = int(digits)
        if 0 <= number <= 3:
            return number
        if 1 <= number <= 4:
            return number - 1
    return None


def normalize_question(raw: Any) -> Optional[Dict[str, Any]]:
    """Validate and normalize a single generated question."""
    if not isinstance(raw, dict):
        return None

    question = str(
        raw.get("question") or raw.get("q") or raw.get("text") or ""
    ).strip()
    if not question:
        return None

    options = raw.get("options") or raw.get("choices") or raw.get("answers") or []
    if isinstance(options, dict):
        keys = sorted(options.keys())
        options = [options[key] for key in keys]

    cleaned_options: List[str] = []
    for option in options:
        option_text = str(option).strip()
        option_text = re.sub(r"^[A-Da-d][\.\):\-]\s*", "", option_text).strip()
        if option_text:
            cleaned_options.append(option_text)

    if len(cleaned_options) < 4:
        return None
    cleaned_options = cleaned_options[:4]

    answer_value = raw.get(
        "answer",
        raw.get("correct_answer", raw.get("correct", raw.get("answer_index"))),
    )
    answer_index = parse_answer(answer_value, cleaned_options)
    if answer_index is None:
        return None

    explanation = str(
        raw.get("explanation") or raw.get("reason") or raw.get("rationale") or ""
    ).strip()
    if not explanation:
        explanation = "The correct option is the right answer for this question."

    return {
        "question": question,
        "options": cleaned_options,
        "answer": answer_index,
        "explanation": explanation,
    }


def validate_questions(payload: Any, count: int) -> List[Dict[str, Any]]:
    """Extract, validate and return at least MIN_QUESTIONS questions."""
    if isinstance(payload, dict):
        raw_questions = payload.get("questions") or payload.get("quiz") or payload.get("data")
    else:
        raw_questions = payload

    if isinstance(raw_questions, dict):
        raw_questions = [raw_questions]
    if not isinstance(raw_questions, list):
        raise ValueError("The AI response did not contain a list of questions.")

    questions: List[Dict[str, Any]] = []
    seen = set()
    for item in raw_questions:
        question = normalize_question(item)
        if question is None:
            continue
        key = question["question"].strip().lower()
        if key in seen:
            continue
        seen.add(key)
        questions.append(question)

    if len(questions) < MIN_QUESTIONS:
        raise ValueError(
            "The AI returned only %d valid question(s); at least %d are required."
            % (len(questions), MIN_QUESTIONS)
        )
    return questions[:count]


def generate_ai_questions(
    topic: str,
    source_text: str,
    api_key: str,
    model: str,
    count: int,
) -> List[Dict[str, Any]]:
    """Call the OpenAI API and return validated questions."""
    if not OPENAI_AVAILABLE or OpenAI is None:
        raise RuntimeError(
            "The 'openai' package is not installed. Run: pip install -r requirements.txt"
        )

    client = OpenAI(api_key=api_key)
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert teacher who writes clear multiple-choice "
                "questions for college students. Always reply with valid JSON only."
            ),
        },
        {"role": "user", "content": build_prompt(topic, source_text, count)},
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            response_format={"type": "json_object"},
        )
    except Exception:
        # Some OpenAI-compatible providers do not support response_format.
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
        )

    content = response.choices[0].message.content
    return validate_questions(extract_json(content), count)


# --------------------------------------------------------------------------
# Sample (offline) question generation
# --------------------------------------------------------------------------
def keyword_score(text: str, keywords: List[str]) -> int:
    score = 0
    for keyword in keywords:
        pattern = r"(?<![a-z0-9])" + re.escape(keyword) + r"(?![a-z0-9])"
        if re.search(pattern, text):
            score += 1
    return score


def pick_sample_bank(topic: str, source_text: str) -> Dict[str, Any]:
    """Choose the most relevant built-in question bank."""
    topic_text = (topic or "").lower()
    source = (source_text or "").lower()[:MAX_SOURCE_CHARS]

    best_bank = None
    best_score = -1
    for bank in SAMPLE_BANKS:
        score = 3 * keyword_score(topic_text, bank["keywords"])
        score += keyword_score(source, bank["keywords"])
        if score > best_score:
            best_bank = bank
            best_score = score

    if best_bank is None or best_score <= 0:
        best_bank = next(
            (bank for bank in SAMPLE_BANKS if bank["name"] == "General Knowledge"),
            SAMPLE_BANKS[-1],
        )
    return best_bank


def generate_sample_questions(
    topic: str,
    source_text: str,
    count: int,
) -> Tuple[List[Dict[str, Any]], str]:
    """Return sample questions and the name of the bank that was used."""
    bank = pick_sample_bank(topic, source_text)

    pool: List[Dict[str, Any]] = list(bank["questions"])
    if count > len(pool):
        # Only needed when the user asks for more than one bank has.
        for other in SAMPLE_BANKS:
            if other is bank:
                continue
            for question in other["questions"]:
                if question not in pool:
                    pool.append(question)
            if len(pool) >= count:
                break

    selected = random.sample(pool, k=min(count, len(pool)))
    return selected, bank["name"]


# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------
def init_state() -> None:
    defaults = {
        "quiz_questions": [],
        "quiz_id": 0,
        "submitted": False,
        "user_answers": {},
        "quiz_source": "",
        "quiz_topic": "",
        "quiz_notice": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_quiz() -> None:
    st.session_state.quiz_questions = []
    st.session_state.submitted = False
    st.session_state.user_answers = {}
    st.session_state.quiz_id += 1
    st.session_state.quiz_source = ""
    st.session_state.quiz_topic = ""
    st.session_state.quiz_notice = ""


init_state()


# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    api_key = st.text_input(
        "OpenAI API key (optional)",
        value=get_config_value("OPENAI_API_KEY"),
        type="password",
        help="Leave empty to use the built-in sample questions.",
    ).strip()

    model = st.text_input(
        "AI model",
        value=get_config_value("OPENAI_MODEL", DEFAULT_MODEL),
        help="Used only when an API key is provided.",
    ).strip() or DEFAULT_MODEL

    num_questions = st.slider(
        "Number of questions",
        min_value=MIN_QUESTIONS,
        max_value=MAX_QUESTIONS,
        value=MIN_QUESTIONS,
        step=1,
    )

    st.divider()
    if api_key:
        if OPENAI_AVAILABLE:
            st.success("AI mode: questions will be generated with AI.")
        else:
            st.warning("API key found, but the 'openai' package is missing.")
    else:
        st.info("Demo mode: built-in sample questions will be used.")

    st.markdown(
        """
        **How it works**
        1. Enter a topic or upload a `.txt` file.
        2. Click **Generate Quiz**.
        3. Answer the questions and click **Submit Answers**.
        4. See your score, percentage and detailed feedback.
        """
    )


# --------------------------------------------------------------------------
# Header and input area
# --------------------------------------------------------------------------
st.title("🧠 AI-Powered Quiz Generator")
st.caption(
    "Create a multiple-choice quiz on any topic and test yourself. "
    "Works with or without an AI API key."
)

col_topic, col_file = st.columns([3, 2])

with col_topic:
    topic_input = st.text_input(
        "🔤 Enter a topic",
        placeholder="e.g. Python functions, DBMS normalization, Photosynthesis",
    ).strip()

with col_file:
    uploaded_file = st.file_uploader(
        "📄 Or upload a text file",
        type=["txt", "md"],
        help="The file content is used as the source material for the quiz.",
    )

generate_clicked = st.button(
    "✨ Generate Quiz",
    type="primary",
    use_container_width=True,
)


# --------------------------------------------------------------------------
# Generate the quiz
# --------------------------------------------------------------------------
if generate_clicked:
    source_text = ""
    file_name = ""
    if uploaded_file is not None:
        source_text = read_uploaded_file(uploaded_file).strip()
        file_name = getattr(uploaded_file, "name", "")
        if not source_text:
            st.error("The uploaded file is empty. Please upload a file with text.")
            st.stop()

    topic = topic_input or (pretty_topic_from_filename(file_name) if file_name else "")

    if not topic and not source_text:
        st.error("Please enter a topic or upload a text file.")
        st.stop()

    if source_text:
        st.caption(
            "📎 Using source file: %s (%d characters read)"
            % (file_name, len(source_text))
        )

    questions: List[Dict[str, Any]] = []
    source_label = ""
    warning_message = ""

    if api_key and OPENAI_AVAILABLE:
        with st.spinner("Generating questions with AI..."):
            try:
                questions = generate_ai_questions(
                    topic=topic,
                    source_text=source_text,
                    api_key=api_key,
                    model=model,
                    count=num_questions,
                )
                source_label = "🤖 Generated with AI (%s)" % model
            except Exception as exc:  # noqa: BLE001 - show any API error to the user
                warning_message = (
                    "AI generation failed (%s). Falling back to built-in sample "
                    "questions." % str(exc)[:200]
                )
    elif api_key and not OPENAI_AVAILABLE:
        warning_message = (
            "The 'openai' package is not installed, so built-in sample questions "
            "were used instead. Run: pip install -r requirements.txt"
        )

    if not questions:
        with st.spinner("Preparing sample questions..."):
            questions, bank_name = generate_sample_questions(
                topic, source_text, num_questions
            )
            source_label = "📚 Built-in sample questions (%s)" % bank_name

    # Store the fresh quiz in the session so it survives reruns.
    st.session_state.quiz_questions = questions
    st.session_state.quiz_id += 1
    st.session_state.submitted = False
    st.session_state.user_answers = {}
    st.session_state.quiz_source = source_label
    st.session_state.quiz_topic = topic or "Uploaded Notes"
    # st.rerun() below discards elements drawn in this run, so keep any notice
    # in the session state and display it after the rerun.
    st.session_state.quiz_notice = warning_message
    st.rerun()


# --------------------------------------------------------------------------
# Quiz rendering
# --------------------------------------------------------------------------
questions = st.session_state.quiz_questions

if not questions:
    st.info("👆 Enter a topic or upload a file, then click **Generate Quiz** to begin.")
else:
    st.divider()
    st.subheader("📝 Quiz: %s" % st.session_state.quiz_topic)
    st.caption(st.session_state.quiz_source)
    if st.session_state.quiz_notice:
        st.warning(st.session_state.quiz_notice)
    st.caption(
        "Choose one answer for each question (%d questions)."
        % len(questions)
    )

    submitted = st.session_state.submitted
    quiz_id = st.session_state.quiz_id

    for index, question in enumerate(questions):
        st.markdown("**Q%d. %s**" % (index + 1, question["question"]))
        option_labels = [
            "%s. %s" % (LETTERS[position], option)
            for position, option in enumerate(question["options"])
        ]

        selected_index = None
        if submitted:
            selected_index = st.session_state.user_answers.get(index)

        st.radio(
            "Select an answer for question %d" % (index + 1),
            options=list(range(len(option_labels))),
            format_func=lambda value, labels=option_labels: labels[value],
            index=selected_index,
            key="answer_%d_%d" % (quiz_id, index),
            label_visibility="collapsed",
            disabled=submitted,
        )
        st.write("")

    if not submitted:
        if st.button("✅ Submit Answers", type="primary", use_container_width=True):
            answers = {
                index: st.session_state.get("answer_%d_%d" % (quiz_id, index))
                for index in range(len(questions))
            }
            st.session_state.user_answers = answers
            st.session_state.submitted = True
            st.rerun()
    else:
        answers = st.session_state.user_answers
        total = len(questions)
        answered = sum(1 for value in answers.values() if value is not None)
        score = sum(
            1
            for index, question in enumerate(questions)
            if answers.get(index) == question["answer"]
        )
        percentage = round((score / total) * 100) if total else 0

        st.divider()
        st.subheader("📊 Your Result")

        unanswered = total - answered
        if unanswered > 0:
            st.warning(
                "%d unanswered question(s) were marked as incorrect." % unanswered
            )

        metric_a, metric_b, metric_c = st.columns(3)
        metric_a.metric("Score", "%d / %d" % (score, total))
        metric_b.metric("Percentage", "%d%%" % percentage)
        metric_c.metric("Status", "Pass ✅" if percentage >= 50 else "Retry 💪")

        st.progress(percentage / 100.0)

        if percentage >= 80:
            st.success(
                "🌟 Excellent! You have a strong understanding of this topic."
            )
        elif percentage >= 60:
            st.info("👍 Good job! Review the explanations to improve further.")
        elif percentage >= 40:
            st.warning(
                "📚 Keep practising. Read the explanations carefully and try again."
            )
        else:
            st.error(
                "❗ Don't give up! Study the material and attempt the quiz again."
            )

        st.markdown("### 🔍 Answer Review")
        for index, question in enumerate(questions):
            selected = answers.get(index)
            correct = question["answer"]
            is_correct = selected == correct
            icon = "✅" if is_correct else "❌"

            with st.expander(
                "%s Q%d. %s" % (icon, index + 1, question["question"])
            ):
                for position, option in enumerate(question["options"]):
                    line = "%s. %s" % (LETTERS[position], option)
                    if position == correct:
                        st.markdown("- **%s** ✅ (correct answer)" % line)
                    elif position == selected:
                        st.markdown("- %s ❌ (your answer)" % line)
                    else:
                        st.markdown("- %s" % line)

                if selected is None:
                    st.error("You did not answer this question.")
                elif is_correct:
                    st.success("Your answer is correct.")
                else:
                    st.error(
                        "Your answer is incorrect. Correct answer: **%s. %s**"
                        % (LETTERS[correct], question["options"][correct])
                    )

                st.info("💡 **Explanation:** %s" % question["explanation"])

        st.divider()
        if st.button("🔄 Start a New Quiz", use_container_width=True):
            reset_quiz()
            st.rerun()


# --------------------------------------------------------------------------
# Footer
# --------------------------------------------------------------------------
st.divider()
st.caption(
    "Built with Python and Streamlit · AI questions are generated only when an "
    "API key is provided; otherwise built-in sample questions are used."
)
