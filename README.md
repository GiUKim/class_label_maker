# class_label_maker

## usage

### pip install opencv-python
### pip install pyautogui

---

- .jpg 데이터셋이 있는 폴더에 main.py 파일 복제
- 콘솔로 데이터셋 있는 폴더로 이동
   - python label.py
- classes.txt 파일에 클래스 명 입력 (1개 이상)
- 별도 작업 없이 label창에서 keyword 입력 시 해당 keyword를 포함하는 클래스를 bold로 변경
- 우측 클래스 선택(복수 선택 가능) 후 다른 이미지로 이동하면 같은 폴더에 해당 이미지와 같은 이름의 .txt파일로 레이블링되어 저장됨

--- 

- ',': 이전 이미지로 이동
- '.': 다음 이미지로 이동
- 'esc': 종료
- 'R-Button Click': 다음 이미지로 이동 ('.'과 동일)
- other typing: 클래스 검색 기능

