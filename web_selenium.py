from selenium import webdriver

# Chrome 드라이버의 새 인스턴스 만들기
driver = webdriver.Chrome()

# 대상 웹 사이트로 이동
driver.get("https://www.kisec.com/accounts/login_pd.do")

# 페이지에서 모든 input 요소 찾기
input_elements = driver.find_elements("tag name", "input")

# 각 입력 요소를 반복하고 이름 특성을 가져오기
for element in input_elements:
    input_name = element.get_attribute("name")
    if input_name:
        # SQL 테스트 구현
        print(f"Input element with name '{input_name}' found on the page.")

# 브라우저 닫기
driver.quit()