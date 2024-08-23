import pytest
from speaker_diarization import DiarizationModel  # type: ignore


test_model = DiarizationModel()


def test_infer_file_invalid_path():
    invalid_file_path = "non_existent_file.wav"

    # Use pytest to check that an appropriate exception is raised
    with pytest.raises(Exception) as exc_info:
        test_model.infer_file(invalid_file_path)

    # Check if the exception message contains specific text
    assert (f"{invalid_file_path} does not exist" in str(exc_info.value))
