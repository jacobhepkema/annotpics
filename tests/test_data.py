import pytest
import pandas as pd
import numpy as np
import os
from annotpics.modules.data import AnnotationData

@pytest.fixture
def setup_test_environment(tmpdir):
    """Fixture to set up a test environment with dummy data."""
    image_dir = tmpdir.mkdir("images")
    # Create dummy image files
    open(os.path.join(image_dir, "test_image1.png"), 'a').close()
    open(os.path.join(image_dir, "test_image2.png"), 'a').close()

    classes = ["cat", "dog"]
    output_csv = os.path.join(tmpdir, "output.csv")

    return {
        "image_dir": str(image_dir),
        "classes": classes,
        "output_csv": output_csv,
    }

def test_annotation_data_init_no_csv(setup_test_environment):
    """Test AnnotationData initialization without a starting CSV."""
    env = setup_test_environment
    ad = AnnotationData(image_dir=env["image_dir"], classes=env["classes"], o=env["output_csv"])

    assert ad.num_images == 2
    assert list(ad.data_df.columns) == ['image', 'cat', 'dog']
    assert ad.data_df['cat'].sum() == 0
    assert ad.data_df['dog'].sum() == 0

def test_annotation_data_init_with_csv(setup_test_environment, tmpdir):
    """Test AnnotationData initialization with a starting CSV."""
    env = setup_test_environment

    # Create a dummy CSV
    input_csv_path = os.path.join(tmpdir, "input.csv")
    data = {
        "image": ["test_image1.png", "test_image2.png"],
        "cat": [1, 0],
        "dog": [0, 1]
    }
    df = pd.DataFrame(data)
    df.to_csv(input_csv_path, index=False)

    ad = AnnotationData(image_dir=env["image_dir"], classes=env["classes"], o=env["output_csv"], csv=input_csv_path)

    assert ad.num_images == 2
    assert ad.data_df['cat'][0] == 1
    assert ad.data_df['dog'][1] == 1

def test_toggle_annotation(setup_test_environment):
    """Test the toggle_annotation method."""
    env = setup_test_environment
    ad = AnnotationData(image_dir=env["image_dir"], classes=env["classes"], o=env["output_csv"])

    # Toggle from 0 to 1
    assert ad.data_df.loc[0, "cat"] == 0
    ad.toggle_annotation(0, "cat")
    assert ad.data_df.loc[0, "cat"] == 1

    # Toggle from 1 to 0
    ad.toggle_annotation(0, "cat")
    assert ad.data_df.loc[0, "cat"] == 0

    with pytest.raises(AssertionError):
        ad.toggle_annotation(0, "bird")

def test_save(setup_test_environment):
    """Test the save method."""
    env = setup_test_environment
    ad = AnnotationData(image_dir=env["image_dir"], classes=env["classes"], o=env["output_csv"])
    ad.toggle_annotation(0, "cat")
    ad.save()

    assert os.path.exists(env["output_csv"])
    saved_df = pd.read_csv(env["output_csv"])
    assert saved_df.loc[0, "cat"] == 1
