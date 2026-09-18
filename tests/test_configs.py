from services.config_loader import ConfigLoader


def test_configs_load_successfully():
    comp = ConfigLoader.load_competencies()
    grading = ConfigLoader.load_grading()
    taxonomy = ConfigLoader.load_taxonomy()

    assert "competencies" in comp
    assert "grading" in grading
    assert "safety_taxonomy" in taxonomy
    assert "tem_framework" in taxonomy
