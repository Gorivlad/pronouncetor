import pytest
from unittest.mock import patch, MagicMock
from feedback_generator import Feedback, system_query


@pytest.fixture
def mock_openai():
    with patch('feedback_generator.OpenAI') as MockOpenAI:
        mock_openai = MockOpenAI.return_value
        mock_openai.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(
                content="This is a mock response"
                ))]
        )
        yield mock_openai


@pytest.fixture
def transcription():
    return "This is a test transcription"


@pytest.fixture
def system_query_example():
    return system_query["short_funny"]


def test_feedback_initialization(transcription, system_query_example):
    feedback = Feedback(transcription, system_query_example)

    assert feedback.transcription == transcription
    assert feedback.system_query == system_query_example
    assert feedback.conversation_history == [
        {"role": "system", "content": system_query_example}
    ]


def test_first_message(mock_openai, transcription, system_query_example):
    feedback = Feedback(transcription, system_query_example)
    response = feedback.first_message()

    assert response == (
        "Here is feedback on your Grammar\nThis is a mock response"
        )
    assert len(feedback.conversation_history) == 2
    assert feedback.conversation_history[-1] == {
        "role": "assistant",
        "content": "This is a mock response"
    }


def test_continuous_chat(mock_openai, transcription, system_query_example):
    feedback = Feedback(transcription, system_query_example)
    feedback.first_message()  # Initialize conversation

    user_input = "This is another input"
    response = feedback.continuous_chat(user_input)

    assert response == "This is a mock response"
    assert len(feedback.conversation_history) == 4
    # Initial system + transcription + user + assistant
    assert feedback.conversation_history[-2] == {
        "role": "user",
        "content": user_input
    }
    assert feedback.conversation_history[-1] == {
        "role": "assistant",
        "content": "This is a mock response"
    }
