# Corrupted Network Capture

**Score：** 600

**Challenge：**  
Ember Jackals have corrupted a network capture file that may contain information on when they first began gathering info about our network. Help us restore the file to working order and recover the response data in the protocol capture.

What is the timestamp of the response packet?

Flag Format: Mmm DD, YYYY HH:MM:SS

**Hits：**  
* It looks like the beginning portion of the file is corrupted
* Recover or recreate a Section Header Block
* The timestamp must be set to the correct epoch (What epoch value does the TIME protocol use?)
* https://github.com/wireshark/wireshark/blob/8bbd491f0f39640e9ff84ec608e77e80b5021b93/epan/dissectors/packet-time.c#L69

---
**Flag：**  
**Write-Up：**  