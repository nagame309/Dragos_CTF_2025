# Dragos Trivia - Q4

**Score：** 200

**Challenge：**  
Investigators found that attackers gained access to ACME’s vendor network through a phishing email targeting a contractor, allowing lateral movement into poorly segmented industrial systems.

What critical security control, as defined by the 5CCs, could have prevented this attack from escalating into an OT compromise, according to Dragos’s guidance on KAMACITE?

**Hits：**  
* Open YIR
* Review the KAMACITE Technical Update
* Review the SANS ICS 5 Critical Controls

---
**Flag：**  `Defensible Architecture`  
**Write-Up：**  
題目中提到的 poorly segmented (分割不良) 是指向架構缺陷的線索，如果 ACME 擁有 `Defensible Architecture` (防禦性架構)，即使承包商的網絡被攻陷，攻擊者也無法直接橫向移動至 OT 系統。  
參考資料：[《SANS ICS 5 Critical Controls: Essential Framework for Critical Infrastructure Protection》](https://www.dragos.com/blog/the-sans-ics-five-critical-controls-a-practical-framework-for-ot-cybersecurity/)