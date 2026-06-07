import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_frontend_sentiment():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("http://localhost:5000")
        
        # Element IDs
        text_input = driver.find_element(By.ID, "text-input")
        submit_btn = driver.find_element(By.ID, "submit-btn")
        
        # Test Action
        text_input.send_keys("This app is incredibly intuitive and has made my daily workflow dramatically more efficient")
        submit_btn.click()
        
        # Assert non-empty and contains POSITIVE, NEGATIVE, or Confidence
        result_output = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result-output"))
        )
        
        # Wait for text to appear
        time.sleep(2)
        text = result_output.text
        
        assert text != ""
        assert "POSITIVE" in text or "NEGATIVE" in text or "Confidence" in text
    finally:
        driver.quit()
