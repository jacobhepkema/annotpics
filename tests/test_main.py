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
    mock_ui = mocker.patch('annotpics.__main__.AnnotationUI')
    mock_data = mocker.patch('annotpics.__main__.AnnotationData')
    mock_image = mocker.patch('annotpics.__main__.ImageManager')
    mocker.patch('annotpics.__main__.Tk')

    args = [
        setup_test_files["image_dir"],
        setup_test_files["bindings_path"],
        '--o', setup_test_files["output_csv"],
        '--resize_w', '100',
        '--resize_h', '200',
    ]
    result = runner.invoke(main, args)

    assert result.exit_code == 0
    mock_data.assert_called_once()
    mock_image.assert_called_once_with(resize_w=100, resize_h=200)
    mock_ui.assert_called_once()

def test_main_with_csv(runner, setup_test_files, mocker):
    mock_ui = mocker.patch('annotpics.__main__.AnnotationUI')
    mock_data = mocker.patch('annotpics.__main__.AnnotationData')
    mock_image = mocker.patch('annotpics.__main__.ImageManager')
    mocker.patch('annotpics.__main__.Tk')

    csv_path = setup_test_files["output_csv"]
    # Create a dummy csv to avoid FileNotFoundError
    with open(csv_path, 'w') as f:
        f.write("image,jeans,shirt\n")
        f.write("test.jpg,1,0\n")

    args = [
        setup_test_files["image_dir"],
        setup_test_files["bindings_path"],
        '--csv', csv_path,
        '--o', setup_test_files["output_csv"],
    ]
    result = runner.invoke(main, args)

    assert result.exit_code == 0
    mock_data.assert_called_once()
    # Check that csv argument was passed to AnnotationData
    assert mock_data.call_args[1]['csv'] == csv_path
    mock_image.assert_called_once()
    mock_ui.assert_called_once()
