import pytest
from pathlib import Path
from scipy.io.wavfile import read

from detection import has_clap


@pytest.mark.parametrize('path', list(Path('claps').iterdir()))
def test_detection(path: Path):
    _, data = read(path)
    data = data / 2**31
    clap = has_clap(data, 128, 0.1)
    assert clap == path.name.startswith('clap')
