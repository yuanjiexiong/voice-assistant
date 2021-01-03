import os
from record import record
from to_text import to_text
import time
from pynput.keyboard import Key, Controller
import clipboard


def press(key_list, delay=0.05):
    keyboard = Controller()
    for k in key_list[:-1]:
        keyboard.press(k)
        time.sleep(delay)
    keyboard.type(key_list[-1])  # 必须瞬发
    for k in reversed(key_list[:-1]):
        keyboard.release(k)
        time.sleep(delay)
    time.sleep(delay)


silent_mode = False
while True:
    record()
    text = to_text()
    is_valid = len(text) > 0
    if len(text) > 0:
        if "静音模式" in text or "精英模式" in text or "经营模式" in text:
            silent_mode = True
        if "工作模式" in text:
            silent_mode = False
        if silent_mode:
            continue
        if "所选文本" in text or "选中文本" in text:
            old_content = clipboard.paste()
            press([Key.ctrl.value, "c"])
            new_content = clipboard.paste()
            text = text.replace("所选文本", new_content).replace("选中文本", new_content)
            clipboard.copy(old_content)
        if "打开" in text and len(text) < 10:
            new_text = (
                text.replace("浏览器", "www.baidu.com")
                .replace("百度", "www.baidu.com")
                .replace("谷歌", "www.google.com")
                .replace("碧绿碧绿", "www.bilibili.com")
                .replace("哔哩哔哩", "www.bilibili.com")
                .replace("文件夹", "explorer")
                .replace("扣的", "code")
                .replace("透的", "code")
            )
            os.system("start " + new_text.replace("打开", ""))
        elif "关闭" in text and len(text) < 10:
            press([Key.ctrl.value, "w"])
        elif "最大化" in text and len(text) < 10:
            press([Key.alt.value, " ", "X"], 0.1)
        elif "最小化" in text and len(text) < 10:
            press([Key.alt.value, " ", "N"], 0.1)
        elif "切换" in text and len(text) < 10:
            press([Key.alt.value, "\t"], 0.1)
        elif "搜索" in text and len(text) < 30:
            if "谷歌" in text:
                os.system(
                    "start https://www.google.com/search?q="
                    + text.replace("搜索", "").replace("谷歌", "")
                )
            else:
                os.system(
                    "start https://www.baidu.com/s?wd="
                    + text.replace("搜索", "").replace("百度", "")
                )
        elif "翻译" in text and len(text) < 30:
            os.system(
                "start https://translate.google.cn/?sl=auto^&tl=en^&text="
                + text.replace("翻译", "")
            )
        elif "输入" in text and len(text) < 30:
            old_content = clipboard.paste()
            clipboard.copy(text[text.index("输入") + 2 :])
            time.sleep(0.1)
            press([Key.ctrl.value, "v"])
            time.sleep(0.1)
            clipboard.copy(old_content)
        elif "记录" in text and len(text) < 30:
            pass
        elif "生成折线图" in text and len(text) < 30:
            pass
        elif "生成柱形图" in text and len(text) < 30:
            pass
        elif "生成词云" in text and len(text) < 30:
            pass
        elif "统计词语频率" in text and len(text) < 30:
            pass
        else:
            is_valid = False
    if is_valid:
        print("有效:" + text)
