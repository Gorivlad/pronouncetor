from unittest import mock
from utils import (
    convert_to_wav, extract_first_30_seconds,
    display_txt_file, validate_audio_file
)
from pydub import AudioSegment


# Test for convert_to_wav function
@mock.patch("subprocess.run")
def test_convert_to_wav(mock_subprocess_run):
    input_file = "input.mp3"
    output_file = "output.wav"

    convert_to_wav(input_file, output_file)

    expected_command = [
        'ffmpeg', '-y', '-loglevel', 'error', '-i', input_file,
        '-c:a', 'pcm_s16le', output_file
    ]
    mock_subprocess_run.assert_called_once_with(expected_command)
    mock_subprocess_run.assert_called_once()


# Test for extract_and_save_clips function
# TODO

# Test for extract_first_30_seconds function
@mock.patch.object(AudioSegment, "from_file")
@mock.patch.object(AudioSegment, "export")
def test_extract_first_30_seconds(mock_export, mock_from_file):
    mock_audio = mock.MagicMock(spec=AudioSegment)
    mock_audio.channels = 2
    mock_audio.frame_rate = 44100
    mock_audio.sample_width = 2
    mock_from_file.return_value = mock_audio
    mock_audio.__getitem__.return_value = mock_audio

    input_path = "input.mp3"
    output_path = "output.wav"

    extract_first_30_seconds(input_path, output_path)

    # Check that the first 30 seconds were sliced
    mock_audio.__getitem__.assert_called_once_with(slice(None, 30000))

    # Check that the export method was called
    mock_audio.export.assert_called_once_with(output_path, format="wav")


# Test for display_txt_file function
@mock.patch("tkinter.scrolledtext.ScrolledText.insert")
@mock.patch("tkinter.Tk.mainloop")
@mock.patch("tkinter.scrolledtext.ScrolledText.pack")
@mock.patch("tkinter.Tk")
@mock.patch(
    "builtins.open", new_callable=mock.mock_open, read_data="Sample text"
    )
def test_display_txt_file(
    mock_open, mock_tk, mock_pack, mock_mainloop, mock_insert
        ):
    file_path = "sample.txt"

    mock_root = mock_tk.return_value

    display_txt_file(file_path)

    mock_open.assert_called_once_with(file_path, 'r')

    # Check that the text was inserted correctly in the ScrolledText widget
    mock_insert.assert_any_call("end", "Sample text")

    # Ensure that mainloop was indeed called
    mock_root.mainloop.assert_called_once()


# Test for validate_audio_file function
@mock.patch.object(AudioSegment, "from_file")
@mock.patch("os.path.isfile")
def test_validate_audio_file(mock_isfile, mock_from_file):
    mock_isfile.return_value = True
    mock_audio = mock.MagicMock(spec=AudioSegment)
    mock_audio.channels = 2
    mock_audio.frame_rate = 44100
    mock_audio.sample_width = 2
    mock_from_file.return_value = mock_audio
    mock_audio.__len__.return_value = 5 * 60 * 1000  # 5 minutes

    valid_file = "valid_audio.mp3"
    invalid_file = "invalid_audio.txt"
    too_short_audio = "short_audio.mp3"
    too_long_audio = "long_audio.mp3"

    # Test valid file
    assert validate_audio_file(valid_file) is True

    # Test invalid file extension
    assert validate_audio_file(invalid_file) == (
        "Error: The file is not an audio file."
        )

    # Test too short audio
    mock_audio.__len__.return_value = 30 * 1000  # 30 seconds
    assert validate_audio_file(too_short_audio) == (
        "Error: The audio is too short."
        )

    # Test too long audio
    mock_audio.__len__.return_value = 16 * 60 * 1000  # 16 minutes
    assert validate_audio_file(too_long_audio) == (
        "Error: The audio is too long."
        )

    # Test invalid file path
    mock_isfile.return_value = False
    assert validate_audio_file("non_existent_file.mp3") == (
        "Error: Invalid file path."
        )
