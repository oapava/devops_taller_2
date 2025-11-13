import os
import sys
import tempfile
import pytest

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from funtions import load_file

def create_test_csv():
    """Create a temporary CSV file for testing"""
    content = """id;name;gender;eye_color;race;hair_color;height;publisher;skin_color;alignment;weight
1;A-Bomb;Male;yellow;Human;No Hair;203;Marvel Comics;;good;441
2;Abe Sapien;Male;blue;Icthyo Sapien;No Hair;191;Dark Horse Comics;blue;good;65
3;Abin Sur;Male;blue;Ungaran;No Hair;185;DC Comics;red;good;90
"""
    # Create a temporary file
    fd, path = tempfile.mkstemp(suffix='.csv')
    try:
        with os.fdopen(fd, 'w') as tmp:
            tmp.write(content)
        return path
    except Exception as e:
        os.remove(path)
        raise e

def test_load_file():
    """Test that load_file correctly reads and parses a CSV file"""
    # Setup
    test_file = create_test_csv()
    
    try:
        # Exercise
        result = load_file(test_file)
        
        # Verify
        assert len(result) == 3, "Should load 3 heroes"
        
        # Test first hero
        hero1 = result['1']
        assert hero1['name'] == 'A-Bomb'
        assert hero1['gender'] == 'Male'
        assert hero1['eye_color'] == 'yellow'
        assert hero1['weight'] == '441'
        
        # Test second hero
        hero2 = result['2']
        assert hero2['name'] == 'Abe Sapien'
        assert hero2['race'] == 'Icthyo Sapien'
        
        # Test third hero
        hero3 = result['3']
        assert hero3['publisher'] == 'DC Comics'
        assert hero3['skin_color'] == 'red'
        
    finally:
        # Cleanup
        os.remove(test_file)

def test_load_file_nonexistent():
    """Test that load_file handles non-existent files gracefully"""
    with pytest.raises(FileNotFoundError):
        load_file('nonexistent_file.csv')
