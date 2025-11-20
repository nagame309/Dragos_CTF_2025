import pandas as pd
import re
import base64
import os

# -------------
CSV_FILE = "PowerShellLogs.csv"
OUTPUT_FILE = "decoded_payload.exe"
TARGET_SEQ = "233"  # 題目指定的 SequenceNumber
# -------------

def main():
    # 1. 讀取檔案
    if not os.path.exists(CSV_FILE):
        print(f"[-] Error: 找不到檔案 {CSV_FILE}")
        return

    print(f"[*] Reading {CSV_FILE}...")
    try:
        # 讀取 Message 欄位
        df = pd.read_csv(CSV_FILE, usecols=['Message'], dtype={'Message': 'str'})
    except Exception as e:
        print(f"[-] Error reading CSV: {e}")
        return

    # 2. 過濾目標 SequenceNumber
    # 使用 regex 快速篩選包含 SequenceNumber=233 的行
    print(f"[*] Filtering logs for SequenceNumber={TARGET_SEQ}...")
    df = df[df['Message'].str.contains(f"SequenceNumber={TARGET_SEQ}", na=False)]

    if df.empty:
        print(f"[-] No logs found for SequenceNumber={TARGET_SEQ}")
        return

    # 3. 提取與排序
    print("[*] Extracting and sorting fragments...")
    
    # 編譯 Regex 
    re_detail_seq = re.compile(r"DetailSequence=(\d+)")
    re_payload_val = re.compile(r'ParameterBinding\(Out-Default\): name="InputObject"; value="(.*?)"')

    fragments = []

    for msg in df['Message']:
        # 抓取排序用的序號
        seq_match = re_detail_seq.search(msg)
        if not seq_match:
            continue
        
        seq_num = int(seq_match.group(1))
        
        # 抓取 payload 內容 (可能有多個 value)
        values = re_payload_val.findall(msg)
        
        if values:
            fragments.append((seq_num, values))

    # 根據 DetailSequence (tuple 的第一個元素) 進行排序
    fragments.sort(key=lambda x: x[0])
    print(f"[*] Sorted {len(fragments)} log entries.")

    # 4. 拼接 Base64
    full_b64 = ""
    for _, val_list in fragments:
        for val in val_list:
            # 過濾雜訊
            if "CERTIFICATE" not in val:
                full_b64 += val

    if not full_b64:
        print("[-] Error: Reconstructed Base64 string is empty.")
        return

    # 5. 解碼與存檔
    try:
        binary_data = base64.b64decode(full_b64)
        
        # 檢查 MZ 檔頭
        if binary_data.startswith(b'MZ'):
            print("[+] Magic Header found: 'MZ' (Valid Windows Executable)")
        else:
            print(f"[!] Warning: File starts with {binary_data[:10]}, not 'MZ'.")

        with open(OUTPUT_FILE, "wb") as f:
            f.write(binary_data)
        
        print(f"[+] Success! Payload saved to: {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"[-] Decoding failed: {e}")

if __name__ == "__main__":
    main()