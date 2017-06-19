

with open("text/follow_the_color_line.txt", "r") as f:
    t = f.read()
    words = [ w.strip().lower() for w in t.split()]
    d = {}
    for w in words:
        x = d.get(w, 0)
        d[w] = x+1
    print d
    print len(d)
