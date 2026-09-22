from pathlib import Path
import shutil
import matplotlib

cache_dir = Path(matplotlib.get_cachedir())
print("현재 맷플롯립 캐시 경로:", cache_dir)

if cache_dir.exists():
    for f in cache_dir.glob("*"):
        try:
            if f.is_file():
                f.unlink()
            elif f.is_dir():
                shutil.rmtree(f)
        except Exception as e:
            print(f"삭제 실패 ({f}): {e}")
    print("✅ 캐시 청소 완료!")
else:
    print("📂 캐시 폴더가 아직 존재하지 않습니다.")