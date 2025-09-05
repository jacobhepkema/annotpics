import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
import numpy as np
from PIL import Image
import os

# Since the interface module uses tkinter, we need to mock it
import sys
sys.modules['tkinter'] = MagicMock()
sys.modules['PIL.ImageTk'] = MagicMock()

from annotpics.modules.interface import AnnotationInterface

@pytest.fixture
def mock_master():
    """Fixture for a mocked tkinter master."""
    master = MagicMock()
    master.title = MagicMock()
    master.geometry = MagicMock()
    return master

@pytest.fixture
def setup_test_environment(tmpdir):
    """Fixture to set up a test environment with dummy data."""
    image_dir = tmpdir.mkdir("images")
    # Create a dummy image
    dummy_image = Image.new('RGB', (100, 100), color = 'red')
    dummy_image_path = os.path.join(image_dir, "test_image.png")
    dummy_image.save(dummy_image_path)
    dummy_image_path2 = os.path.join(image_dir, "test_image2.png")
    dummy_image.save(dummy_image_path2)


    classes = ["cat", "dog"]
    bindings = {"c": "cat", "d": "dog"}
    data = {
        "image": ["test_image.png", "test_image2.png"],
        "cat": [0, 1],
        "dog": [1, 0]
    }
    data_df = pd.DataFrame(data)
    save_csv = os.path.join(tmpdir, "annotations.csv")

    return {
        "image_dir": str(image_dir),
        "classes": classes,
        "bindings": bindings,
        "data_df": data_df,
        "save_csv": save_csv
    }

def test_annotation_interface_init(mock_master, setup_test_environment):
    """Test the initialization of AnnotationInterface."""
    env = setup_test_environment
    with patch('annotpics.modules.interface.ImageTk.PhotoImage'):
        with patch('annotpics.modules.interface.Image.open'):
            ai = AnnotationInterface(
                master=mock_master,
                classes=env["classes"],
                image_dir=env["image_dir"],
                data_df=env["data_df"],
                bindings=env["bindings"],
                save_csv=env["save_csv"]
            )
            assert ai.master == mock_master
            assert ai.CURR_I == 0
            assert np.array_equal(ai.classes, np.array(env["classes"]))
            assert ai.data_df.equals(env["data_df"])
            mock_master.title.assert_called_with("Image 0")

def test_next_picture(mock_master, setup_test_environment):
    """Test the next_picture method."""
    env = setup_test_environment
    with patch('annotpics.modules.interface.ImageTk.PhotoImage'):
        with patch('annotpics.modules.interface.Image.open'):
            ai = AnnotationInterface(
                master=mock_master,
                classes=env["classes"],
                image_dir=env["image_dir"],
                data_df=env["data_df"].copy(),
                bindings=env["bindings"],
                save_csv=env["save_csv"]
            )
            ai.update_image = MagicMock()
            ai.update_labels = MagicMock()

            ai.next_picture(None)

            assert ai.CURR_I == 1
            ai.update_image.assert_called_once()
            ai.update_labels.assert_called_once()
            assert os.path.exists(env["save_csv"])

def test_prev_picture(mock_master, setup_test_environment):
    """Test the prev_picture method."""
    env = setup_test_environment
    with patch('annotpics.modules.interface.ImageTk.PhotoImage'):
        with patch('annotpics.modules.interface.Image.open'):
            ai = AnnotationInterface(
                master=mock_master,
                classes=env["classes"],
                image_dir=env["image_dir"],
                data_df=env["data_df"].copy(),
                bindings=env["bindings"],
                save_csv=env["save_csv"],
                start_i=1
            )
            ai.update_image = MagicMock()
            ai.update_labels = MagicMock()

            ai.prev_picture(None)

            assert ai.CURR_I == 0
            ai.update_image.assert_called_once()
            ai.update_labels.assert_called_once()

def test_set_to(mock_master, setup_test_environment):
    """Test the set_to method."""
    env = setup_test_environment
    df = env["data_df"].copy()
    with patch('annotpics.modules.interface.ImageTk.PhotoImage'):
        with patch('annotpics.modules.interface.Image.open'):
            ai = AnnotationInterface(
                master=mock_master,
                classes=env["classes"],
                image_dir=env["image_dir"],
                data_df=df,
                bindings=env["bindings"],
                save_csv=env["save_csv"]
            )
            ai.update_labels = MagicMock()

            # Test setting a value from 0 to 1
            assert ai.data_df.loc[0, "cat"] == 0
            ai.set_to(0, "cat")
            assert ai.data_df.loc[0, "cat"] == 1
            ai.update_labels.assert_called_once()

            # Test setting a value from 1 to 0
            assert ai.data_df.loc[0, "dog"] == 1
            ai.set_to(0, "dog")
            assert ai.data_df.loc[0, "dog"] == 0

            with pytest.raises(AssertionError):
                ai.set_to(0, "bird")
