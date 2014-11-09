import time

def main():
    with open("../Dataset/reads4.txt") as f:
        substrings = [line.rstrip() for line in f]
        substrings_copy = substrings[:]
        start = time.time()
        res = find_string(substrings, substrings_copy)
        print res
        end = time.time()
        print end - start
        with open("output4.txt", "w") as f:
            f.write(res +"\n")

def find_string(substrings, substrings_copy):
    while len(substrings) > 2:
        s1 = substrings[0]
        overlaps = []
        for i in range(1, len(substrings)):
            t = get_max_overlap(s1, substrings[i])
            if t[1] != None:
                overlaps.append(t)
        if not overlaps:
            substrings.remove(s1)
            substrings.append(s1)
        else:
            line =  max(overlaps, key=lambda x: x[0])
            if line[2] in substrings:
                substrings.remove(line[2])
            if line[3] in substrings:
                substrings.remove(line[3])
            if not line[1] in substrings:
                substrings.append(line[1])
    if len(substrings) == 2:
        return get_max_overlap(substrings[0], substrings[1])[1]
    return substrings[0]

def get_max_overlap(s1, s2):
    if s1 in s2:
        return (len(s1), s2, s1, s2)

    if s2 in s1:
        return (len(s2), s1, s1, s2)

    if len(s1) == len(s2):
        small = s1
        large = s2
    else:
        small = min([s1, s2], key=len)
        large = max([s1, s2], key=len)

    len_small = len(small)
    len_large = len(large)

    pos_res = []
    for i in range(len_small):
        if is_prefix(small[i:len_small+1], large):
            prefix = small[:i]
            pos_res.append((prefix + large, float(2.0*(len_small - len(prefix)))))

    for j in range(len_large):
        if is_prefix(large[j:len_large+1], small):
            prefix = large[:j]
            pos_res.append((prefix + small, float(2.0*(len_large - len(prefix)))))
    if pos_res:
        res = max(pos_res, key=lambda x: x[1])
        return (res[1], res[0], s1, s2)
    #no overlap 
    return (0.0, None, s1, s2)


def is_prefix(pre, post):
    return post.startswith(pre)

if __name__ == "__main__":
    main()


