import pytest
from click.testing import CliRunner
from annotpics.__main__ import main
import os
import json
import pandas as pd
from PIL import Image

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def setup_test_files(tmpdir):
    image_dir = tmpdir.mkdir("images")
    dummy_image = Image.new('RGB', (100, 100), color='blue')
    dummy_image_path = os.path.join(image_dir, "test.jpg")
    dummy_image.save(dummy_image_path)

    bindings = {"j": "jeans", "s": "shirt"}
    bindings_path = tmpdir.join("bindings.json")
    with open(bindings_path, "w") as f:
        json.dump({"bindings": bindings}, f)

    return {
        "image_dir": str(image_dir),
        "bindings_path": str(bindings_path),
        "output_csv": str(tmpdir.join("output.csv"))
    }

def test_main_help(runner):
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert 'Picture annotation tool' in result.output

def test_main_no_csv(runner, setup_test_files, mocker):
    mocker.patch('annotpics.__main__.AnnotationInterface')
    mocker.patch('annotpics.__main__.Tk')

    args = [
        setup_test_files["image_dir"],
        setup_test_files["bindings_path"],
        '--o', setup_test_files["output_csv"],
    ]
    result = runner.invoke(main, args)

    assert result.exit_code == 0
    # Check that AnnotationInterface was called with the correct arguments
    # This part is a bit tricky because we can't directly inspect the `ai` object.
    # A better approach would be to have main() return the dataframe for inspection.
    # For now, we just check that the command runs without error.
    # A more advanced test could patch `pd.DataFrame.to_csv` and check its inputs.

def test_main_with_csv(runner, setup_test_files, mocker):
    mocker.patch('annotpics.__main__.AnnotationInterface')
    mocker.patch('annotpics.__main__.Tk')

    csv_path = setup_test_files["output_csv"]
    data = {"image": ["test.jpg"], "jeans": [1], "shirt": [0]}
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)

    args = [
        setup_test_files["image_dir"],
        setup_test_files["bindings_path"],
        '--csv', csv_path,
        '--o', setup_test_files["output_csv"],
    ]
    result = runner.invoke(main, args)

    assert result.exit_code == 0
