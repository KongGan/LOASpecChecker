# main.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageGrab  # Image와 ImageGrab을 함께 가져옴
import subprocess
import os


# 클립보드에서 이미지를 가져와 저장하는 함수
def paste_image_from_clipboard():
    try:
        # 클립보드에서 이미지를 가져옴
        img = ImageGrab.grabclipboard()
        if isinstance(img, Image.Image):
            # 이미지를 임시 파일로 저장
            img_path = os.path.join(os.getcwd(), "clipboard_image.png")
            img.save(img_path)
            img_label.config(text="이미지가 성공적으로 붙여넣기되었습니다.")
            return img_path
        else:
            messagebox.showerror("오류", "클립보드에 이미지가 없습니다.")
            return None
    except Exception as e:
        messagebox.showerror("오류", f"이미지를 붙여넣는 중 오류가 발생했습니다: {e}")
        return None


# main.py를 실행하고 출력을 GUI에 표시하는 함수
def run_main_py():
    text = text_input.get("1.0", "end-1c")  # 텍스트 상자에서 텍스트 가져오기
    if not text:
        messagebox.showerror("오류", "API를 입력하세요.")
        return

    if not img_path:
        messagebox.showerror("오류", "클립보드에서 이미지를 붙여넣어 주세요.")
        return

    # main.py를 실행하고 출력 결과를 받아서 처리
    try:
        result = subprocess.run(
            ["python", "search.py", text, img_path],  # 텍스트와 이미지 경로를 전달
            check=True,
            capture_output=True,  # 출력 캡처
            text=True,  # 출력을 문자열로 반환
            encoding="utf-8"  # UTF-8 인코딩 사용
        )

        # 실행 결과를 텍스트 상자에 출력
        output_text.delete("1.0", "end")

        if result.stdout:  # 출력된 내용이 있는 경우에만 삽입
            output_text.insert("1.0", result.stdout)
        else:
            output_text.insert("1.0", "No output from search.py.")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("오류", f"에러발생 API를 확인해주세요.\n\n{e}")
        return

    # 이미지 삭제
    try:
        if os.path.exists(img_path):
            os.remove(img_path)  # 임시로 저장된 이미지 삭제
            img_label.config(text="이미지가 삭제되었습니다.")
    except Exception as e:
        messagebox.showerror("오류", f"이미지를 삭제하는 중 오류가 발생했습니다: {e}")


# tkinter 윈도우 생성
root = tk.Tk()
root.title("간단 군장 검사(by 노래듣고갈래(아브섭))")

# 텍스트 입력 상자
tk.Label(root, text="API 입력").pack()
text_input = tk.Text(root, height=5, width=40)
text_input.pack()

# 이미지 붙여넣기 버튼
img_path = None


def paste_image():
    global img_path
    img_path = paste_image_from_clipboard()


paste_button = tk.Button(root, text="이미지 붙여넣기 (클립보드)", command=paste_image)
paste_button.pack()

# 이미지 붙여넣기 상태 라벨
img_label = tk.Label(root, text="이미지가 붙여넣기되지 않았습니다.")
img_label.pack()

# search.py 실행 버튼
run_button = tk.Button(root, text="검색", command=run_main_py)
run_button.pack()

# search.py 실행 결과를 표시할 텍스트 상자
tk.Label(root, text="검색 결과").pack()
output_text = tk.Text(root, height=60, width=50)
output_text.pack()

# tkinter 메인 루프 실행
root.mainloop()
