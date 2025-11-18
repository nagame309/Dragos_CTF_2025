# College, it ain’t easy

**Score：** 800

**Challenge：**  
After identifying the technique the Ember Jackals used to transfer an offensive tool into the environment, we still don’t know what the tool is or what it does. Adversaries often rename or obfuscate tools to evade defenses. However, there’s a way to recover the tool and identify its true name and function. Use the Security.evtx, PowerShellLogs.evtx, or PowerShellLogs.csv files to identify the tool.

What is the codename of the tool the adversary transferred into the environment?

Flag Format: flag{lots of strings}

**Hits：**  
* The adversary already used the command to reassemble the executable. You just have to replicate it.
* This problem can be solved manually, but that will be an incredibly tedious task with 1009 sections. Try automating your analysis.

---
**Flag：**  ```flag{All I want for Christmas is a better name for this}```

**Write-Up：**  
從 ```Security.evtx``` 中可觀察到攻擊者執行：
```
certutil -decode lats.txt lats.exe
```
證實前題推論無誤。
![alt text](image-2.png)


```PowerShellLogs.csv``` 和 ```PowerShellLogs.evtx``` 內容相同，可以看到 ```SequenceNumber=231``` 後緊接著的 ```SequenceNumber=233``` 由多個 Base64 的 value 組成，利用 Python 讀取 csv 檔的 Message 欄位的 value 字串內容進行組合再解碼，得到攻擊者使用的惡意程式。

![alt text](image.png)

Python Code：
```python=
import pandas as pd
import re
import base64
import sys

# === 使用者設定 ===
# 1. 原始 PowerShell CSV 檔案名稱
CSV_FILE = "PowerShellLogs.csv"

# 2. 目標事件 SequenceNumber
TARGET_SEQ_NUM = "233"

# 3. 最終輸出的檔案名稱
OUTPUT_FILENAME = "decoded_payload.exe"
# ==================


def extract_sequence_number(message_text):
    """使用正規表示式從 Message 欄位中提取 SequenceNumber。"""
    if not isinstance(message_text, str):
        return None
    match = re.search(r"SequenceNumber=(\d+)", message_text)
    return match.group(1) if match else None


def filter_by_sequence(csv_file, target_seq):
    """讀取 CSV 並篩選出指定 SequenceNumber 的日誌。"""
    try:
        df = pd.read_csv(csv_file, usecols=["Message"], dtype={"Message": "str"})
        print(f"成功讀取 {csv_file}，共 {len(df)} 筆日誌。")
    except FileNotFoundError:
        print(f"錯誤：找不到檔案 {csv_file}")
        sys.exit(1)
    except pd.errors.ParserError as e:
        print(f"警告：CSV 檔案格式錯誤 ({e})，嘗試跳過壞行。")
        df = pd.read_csv(csv_file, usecols=["Message"], dtype={"Message": "str"}, on_bad_lines="skip")
    except ValueError:
        print("錯誤：CSV 檔案中缺少 'Message' 欄位。")
        sys.exit(1)

    # 提取 SequenceNumber 並篩選
    df["Extracted_SeqNum"] = df["Message"].apply(extract_sequence_number)
    filtered_df = df[df["Extracted_SeqNum"] == target_seq]

    if filtered_df.empty:
        print(f"錯誤：未找到 SequenceNumber={target_seq} 的日誌。")
        sys.exit(1)

    print(f"成功篩選出 {len(filtered_df)} 筆 SequenceNumber={target_seq} 的日誌。")
    return filtered_df


def reconstruct_base64_from_logs(df):
    """從過濾後的日誌中依序重建 Base64 字串。"""
    seq_pattern = re.compile(r"DetailSequence=(\d+)")
    value_pattern = re.compile(r'ParameterBinding\(Out-Default\): name="InputObject"; value="(.*?)"')

    fragments = []
    print("正在解析日誌碎片...")

    for _, row in df.iterrows():
        msg = row["Message"]
        seq_match = seq_pattern.search(msg)
        if not seq_match:
            continue
        detail_seq = int(seq_match.group(1))
        values = value_pattern.findall(msg)
        fragments.append((detail_seq, values))

    if not fragments:
        print("錯誤：未找到任何 DetailSequence 或 Base64 內容。")
        sys.exit(1)

    fragments.sort(key=lambda x: x[0])
    print("已按照 DetailSequence 進行排序。")

    stitched_b64 = ""
    total_count = 0
    for seq, val_list in fragments:
        for frag in val_list:
            if "CERTIFICATE" not in frag:
                stitched_b64 += frag
                total_count += 1

    print(f"成功拼湊 {total_count} 個 Base64 碎片。")

    if not stitched_b64:
        print("錯誤：拼湊後的 Base64 字串為空。")
        sys.exit(1)

    return stitched_b64


def decode_and_save(b64_data, output_filename):
    """將 Base64 字串解碼並輸出為二進位檔案。"""
    try:
        decoded = base64.b64decode(b64_data)
        with open(output_filename, "wb") as f:
            f.write(decoded)

        print("===============================================")
        print("惡意 Payload 已成功解碼並輸出。")
        print(f"輸出檔案名稱：{output_filename}")

        if decoded.startswith(b"MZ"):
            print("檔案特徵確認：開頭為 'MZ'，這是一個 Windows 可執行檔。")
        else:
            print(f"檔案開頭十位元組：{decoded[:10]}")

        print("===============================================")
        print("警告：請勿在實體主機上執行此檔案，建議於沙箱中分析。")

    except base64.binascii.Error as e:
        print(f"Base64 解碼失敗：{e}")
        print("可能是因為 CSV 檔案內容不完整或被截斷。")
        sys.exit(1)
    except Exception as e:
        print(f"寫入檔案時發生錯誤：{e}")
        sys.exit(1)


def main():
    """主程式執行流程。"""
    filtered_df = filter_by_sequence(CSV_FILE, TARGET_SEQ_NUM)
    b64_data = reconstruct_base64_from_logs(filtered_df)
    decode_and_save(b64_data, OUTPUT_FILENAME)


if __name__ == "__main__":
    main()
```

上傳 VT 之後，Behavior 頁面搜尋 codename。
![alt text](image-1.png)