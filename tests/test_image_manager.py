import pytest
from unittest.mock import patch, MagicMock
from PIL import Image
import os
from annotpics.modules.image_manager import ImageManager

@pytest.fixture
def setup_test_image(tmpdir):
    """Fixture to create a dummy image file."""
    image_path = os.path.join(tmpdir, "test.png")
    Image.new('RGB', (100, 100), 'red').save(image_path)
    return image_path

def test_image_manager_init():
    """Test ImageManager initialization."""
    im = ImageManager(resize_w=128, resize_h=128)
    assert im.resize_w == 128
    assert im.resize_h == 128
    assert im._cache == {}

@patch('annotpics.modules.image_manager.ImageTk')
@patch('PIL.Image.open')
def test_get_image_loading_and_resizing(mock_open, mock_imagetk, setup_test_image):
    """Test that an image is loaded and resized."""
    mock_img = MagicMock(spec=Image.Image)
    mock_img.mode = "RGB"
    mock_img.size = (100, 100)
    mock_img.resize.return_value = mock_img
    mock_open.return_value = mock_img

    im = ImageManager(resize_w=200, resize_h=200)
    img_path = setup_test_image

    im.get_image(img_path)

    mock_open.assert_called_once_with(img_path)
    mock_img.resize.assert_called_once_with((200, 200))
    mock_imagetk.PhotoImage.assert_called_once_with(mock_img)

@patch('annotpics.modules.image_manager.ImageTk')
@patch('PIL.Image.open')
def test_get_image_caching(mock_open, mock_imagetk, setup_test_image):
    """Test that the image cache is used."""
    mock_img = MagicMock(spec=Image.Image)
    mock_img.mode = "RGB"
    mock_img.size = (100, 100)
    mock_img.resize.return_value = mock_img
    mock_open.return_value = mock_img

    im = ImageManager(resize_w=200, resize_h=200)
    img_path = setup_test_image

    # Call get_image twice for the same path
    im.get_image(img_path)
    im.get_image(img_path)

    # Image.open should only be called once
    mock_open.assert_called_once_with(img_path)
    # PhotoImage should also only be called once
    mock_imagetk.PhotoImage.assert_called_once()

@patch('annotpics.modules.image_manager.ImageTk')
@patch('PIL.Image.new')
def test_get_image_file_not_found(mock_new, mock_imagetk):
    """Test that a placeholder is returned for a missing file."""
    mock_placeholder = MagicMock(spec=Image.Image)
    mock_new.return_value = mock_placeholder

    im = ImageManager(resize_w=200, resize_h=200)

    result = im.get_image("non_existent_file.png")

    mock_new.assert_called_once_with('RGB', (200, 200), 'black')
    mock_imagetk.PhotoImage.assert_called_once_with(mock_placeholder)
    assert result is not None
