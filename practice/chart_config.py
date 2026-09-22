import platform
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import font_manager

# =====================
#  차트 이미지 저장 경로
# =====================
# 현재 chart_config.py 위치 기준 상위 또는 동림 output (프로젝트 루트 기준)
OUTPUT_DIR = Path(__file__).resolve().parent / "output"

def out(name):
    """ output/ 폴더 내의 파일 경로 반환 """
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    return OUTPUT_DIR / name

def saved_files():
    """ output/ 폴더에 저장된 파일 이름 목록 반환 """
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    return sorted(p.name for p in OUTPUT_DIR.iterdir() if p.is_file())

# =======================
#  설정
# =======================
def setup(theme=True):
    if theme:
        import seaborn as sns
        sns.set_theme(style="whitegrid")

    system = platform.system()
    chosen_font = "sans-serif"

    if system == "Windows":
        ttf_path = Path("C:/Windows/Fonts/malgun.ttf")
        if ttf_path.exists():
            font_manager.fontManager.addfont(str(ttf_path))
            chosen_font = "Malgun Gothic"
    elif system == "Darwin":
        chosen_font = "AppleGothic"
    else:
        installed = {f.name for f in font_manager.fontManager.ttflist}
        for candidate in ["NanumGothic", "Noto Sans CJK KR", "DejaVu Sans"]:
            if candidate in installed:
                chosen_font = candidate
                break

    plt.rcParams["font.family"] = chosen_font
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["savefig.bbox"] = "tight"