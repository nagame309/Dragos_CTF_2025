# Home Improvement

**Score：** 400

**Challenge：**  
A victim organization provided two Windows Event log files that they believe contain crucial logs containing information that shows how the adversaries brought offensive tools into the environment. They have provided you with these files for analysis.

What living-off-the-land tool did the adversary use to help bring a tool into the environment?

flag format: flag{xxxxxxxxzxxx} or xxxxxxxxzxxx

**Hits：**  
* SABLOL

---
**Flag：**  ```flag{certutil.exe}```

**Write-Up：**   
從提供的 Windows 事件記錄觀察到攻擊者以 `type` 指令讀取名為 `lats.txt` 的文字檔，該檔案內容包含大量 `Base64` 區塊。

![alt text](image.png)

![alt text](image-1.png)

推測攻擊者使用了混淆技術，將惡意 Payload 以 Base64 形式帶入環境以規避偵測。而在 Windows 環境中，常用的內建方式是使用 `certutil.exe -decode` 將 Base64 文字還原為二進位檔案。

以此推測攻擊者使用的工具為 `certutil.exe`。

