# Silly Jackals, PCAPs are for Kids!

**Score：** 800

**Challenge：**  
Ember Jackals have been probing some of our other servers. I have been able to capture some of their traffic but I think I messed up the capture somehow.

Please help make sense of the data and retrieve the 'Originate Timestamp' field from the ICMP packet so we can identify the time of day this scan occurred.

Flag Format: dddddddd

**Hits：**  
* Network captures record the LinkType the frames were captured on
* ICMP packets only operate on Ethernet network links
* The LinkType field for the correct Interface ID needs to be fixed

---
**Flag：**  
**Write-Up：**  