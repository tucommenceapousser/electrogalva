# electrogalva
### just for continue to manipulate code for not lost the hand
## gui interface for calcul of intensity needed for a give piece with type of material 

---

<img width="1024" height="1536" alt="1000371612" src="https://github.com/user-attachments/assets/7f1b0c52-26c5-474b-8520-ef2309c4cc14" />

---

## run vnc and launch main.py

launch the ``main.py`` script and access from vnc viewer (on android avnc, rvnc,...)
if needed 

```bash
vncserver -kill :1
rm -f ~/.vnc/*.pid
rm -f ~/.vnc/*.lock
vncserver :1 -geometry 1280x720 -depth 24
```

```bash
export DISPLAY=:1
```

```bash
python3 main.py
```

---

![1000371613](https://github.com/user-attachments/assets/9a63f989-5fac-429f-a717-5abdc33a96b7)
