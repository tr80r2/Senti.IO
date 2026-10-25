import main
import pytest
from fastapi.testclient import TestClient

client = TestClient(main.app)

def test_positive_sentence():
    response = client.post("/analyze", json={"text": "Это самый лучший день в моей жизни, всё супер!"})
    assert response.status_code == 200
    
    json_data = response.json()
    assert "sentiment" in json_data
    assert "confidence" in json_data
    assert json_data["sentiment"].upper() == "POSITIVE"

def test_empty_payload_validation():
    response = client.post("/analyze", json={"wrong_key": "тест"})
    assert response.status_code == 422

def test_model_not_loaded_503():
    original_classifier = main.classifier
    main.classifier = None
    
    response = client.post("/analyze", json={"text": "Привет"})
    assert response.status_code == 503
    assert response.json()["detail"] == "Модель не запущена."
    
    main.classifier = original_classifier