from unittest import mock
from pyannote.core import Segment
from speaker_diarization import DiarizationModel


# Test for DiarizationModel.__init__
@mock.patch("speaker_diarization.Pipeline.from_pretrained")
def test_diarization_model_init(mock_from_pretrained):
    model_name = "pyannote/speaker-diarization-3.0"
    model = DiarizationModel(model_name=model_name)

    mock_from_pretrained.assert_called_once_with(model_name)
    assert model.pipeline == mock_from_pretrained.return_value


# Test for DiarizationModel.infer_file
@mock.patch("speaker_diarization.ProgressHook")
@mock.patch("speaker_diarization.Pipeline.from_pretrained")
def test_infer_file(mock_from_pretrained, mock_progress_hook):
    mock_pipeline = mock_from_pretrained.return_value
    mock_diarization_result = mock.MagicMock()

    # Mocking the return value when the pipeline is called
    mock_pipeline.return_value = mock_diarization_result

    # Mock the __enter__ method of ProgressHook
    # to return the mock_progress_hook itself
    mock_progress_hook.return_value.__enter__.return_value = (
        mock_progress_hook.return_value
        )

    model = DiarizationModel()
    file_path = "test_audio.wav"
    num_speakers = 2

    result = model.infer_file(file_path, num_speakers)

    mock_progress_hook.assert_called_once()
    mock_pipeline.assert_called_once_with(
        file_path, hook=mock_progress_hook.return_value,
        num_speakers=num_speakers
    )
    assert result == mock_diarization_result
    print("Diarization performed")


# Test for DiarizationModel.time_extraction_touples
def test_time_extraction_touples():
    mock_diarization_result = mock.MagicMock()
    mock_turn1 = Segment(0, 10)
    mock_turn2 = Segment(15, 20)

    mock_diarization_result.itertracks.return_value = [
        (mock_turn1, None, "SPEAKER_00"),
        (mock_turn2, None, "SPEAKER_00"),
        (Segment(25, 30), None, "SPEAKER_01"),
    ]

    model = DiarizationModel()
    target_speaker = "SPEAKER_00"

    result = model.time_extraction_touples(
        mock_diarization_result, target_speaker
        )

    expected_result = [(mock_turn1.start, mock_turn1.end),
                       (mock_turn2.start, mock_turn2.end)]
    assert result == expected_result
    print(f"Timestamps of {target_speaker} extracted as a list of tuples")


# Test for DiarizationModel.plot_diarization
@mock.patch("speaker_diarization.plt.show")
@mock.patch("speaker_diarization.plt.subplots")
def test_plot_diarization(mock_subplots, mock_show):
    mock_fig = mock.MagicMock()
    mock_ax = mock.MagicMock()
    mock_subplots.return_value = (mock_fig, mock_ax)

    mock_diarization_result = mock.MagicMock()
    mock_diarization_result.itertracks.return_value = [
        (Segment(0, 10), None, "SPEAKER_00"),
        (Segment(15, 20), None, "SPEAKER_01"),
    ]
    mock_diarization_result.labels.return_value = ["SPEAKER_00", "SPEAKER_01"]

    model = DiarizationModel()
    title = "Test Diarization Plot"

    model.plot_diarization(mock_diarization_result, title)

    mock_ax.plot.assert_any_call([0, 10], ["SPEAKER_00", "SPEAKER_00"], lw=6)
    mock_ax.plot.assert_any_call([15, 20], ["SPEAKER_01", "SPEAKER_01"], lw=6)
    mock_ax.set_yticks.assert_called_once_with(["SPEAKER_00", "SPEAKER_01"])
    mock_ax.set_yticklabels.assert_called_once_with(
        ["Speaker SPEAKER_00", "Speaker SPEAKER_01"]
        )
    mock_ax.set_xlabel.assert_called_once_with("Time (s)")
    mock_ax.set_title.assert_called_once_with(title)
    mock_show.assert_called_once()
    print("Diarization plot displayed")
