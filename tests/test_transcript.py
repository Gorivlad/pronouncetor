import os
import pytest
from transcript import save_transcript_to_txt


@pytest.fixture
def sample_result():
    return {
        'text': 'This is a sample transcription.',
        'segments': [
            {
                'id': 0,
                'start': 0.0,
                'end': 2.5,
                'text': 'This is a sample',
                'words': [
                    {'word': 'This',
                     'start': 0.0, 'end': 0.5, 'probability': 0.98
                     },
                    {'word': 'is',
                     'start': 0.5, 'end': 1.0, 'probability': 0.97
                     },
                    {'word': 'a',
                     'start': 1.0, 'end': 1.5, 'probability': 0.96
                     },
                    {'word': 'sample',
                     'start': 1.5, 'end': 2.5, 'probability': 0.95
                     },
                ]
            }
        ]
    }


@pytest.fixture
def output_file():
    return 'test_transcript.txt'


@pytest.fixture(autouse=True)
def cleanup_output_file(output_file):
    yield
    if os.path.exists(output_file):
        os.remove(output_file)


def test_save_transcript_to_txt(sample_result, output_file):
    save_transcript_to_txt(sample_result, output_file)

    with open(output_file, 'r') as file:
        content = file.read()

    expected_content = (
        "Full Transcription:\n"
        "This is a sample transcription.\n\n"
        "Segment 0:\n"
        "Start: 0.00s, End: 2.50s\n"
        "This is a sample\n\n"
    )

    assert content.strip() == expected_content.strip()


def test_save_transcript_to_txt_empty_segments(output_file):
    result_empty_segments = {
        'text': 'This is a sample transcription.',
        'segments': []
    }
    save_transcript_to_txt(result_empty_segments, output_file)

    with open(output_file, 'r') as file:
        content = file.read()

    expected_content = (
        "Full Transcription:\n"
        "This is a sample transcription.\n\n"
    )

    assert content.strip() == expected_content.strip()


def test_save_transcript_to_txt_empty_result(output_file):
    result_empty = {
        'text': '',
        'segments': []
    }
    save_transcript_to_txt(result_empty, output_file)

    with open(output_file, 'r') as file:
        content = file.read()

    expected_content = (
        "Full Transcription:\n\n"
    )

    assert content.strip() == expected_content.strip()


# Test filter_transcript
# TODO
