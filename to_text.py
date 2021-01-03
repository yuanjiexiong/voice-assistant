from aip import AipSpeech
from setting import APP_ID, API_KEY, SECRET_KEY, WAV_FILE

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def to_text():
    # 读取录音文件
    try:
        with open(WAV_FILE, "rb") as fp:
            voices = fp.read()
        result = client.asr(
            voices,
            "wav",
            8000,
            {"dev_pid": 1537},  # 常用dev_pid参数：1537普通话(纯中文识别)、1737英语、1637粤语、1837四川话
        )
        result_text = result["result"][0].strip()
        if result_text.endswith("。"):
            result_text = result_text[:-1]
        print("我说: " + repr(result_text))
        return result_text
    except Exception:
        print("未知问题")
        return ""
