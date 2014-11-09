import time
import difflib
import heapq
import itertools

def main():
    with open("../Dataset/reads5.txt") as f:
        substrings = [line.rstrip() for line in f]
        substrings_copy = substrings[:]
        start = time.time()
        res = find_string(substrings, substrings_copy)
        print res
        end = time.time()
        print end - start
        with open("output5.txt", "w") as f:
            f.write(res +"\n")

def find_string(substrings, substrings_copy):
    removed = set()

    added = set()
    while len(substrings) > 2:
        s1 = substrings[0]
        overlaps = []
        for i in range(1, len(substrings)):
            t = get_max_overlap_2(s1, substrings[i])
            if t[1] != None:
                overlaps.append(t)
        if not overlaps:
            print "HIII"
            substrings.remove(s1)
            substrings.append(s1)
        else:
            print overlaps
            line =  min(overlaps, key=lambda x: x[0])
            print line
            if line[2] in substrings:
                substrings.remove(line[2])
                removed.add(line[2])
            if line[3] in substrings:
                substrings.remove(line[3])
                removed.add(line[3])
            if not line[1] in substrings:
                substrings.append(line[1])
        #substrings = substrings_copy[:]
        #print substrings
    return get_max_overlap_2(substrings[0], substrings[1])[1]




    """
    imm = []
    seen = set()
    for r1 in substrings:
        for r2 in substrings:
            if r1 != r2 and not (r1, r2) in seen and not (r2, r1) in seen:
                res = get_max_overlap_2(r1, r2)
                heapq.heappush(imm, res)
                seen.add((r1, r2))
                seen.add((r2, r1))
    #print imm
    while len(substrings) != 1:
        #print len(substrings)
        max_overlap = heapq.heappop(imm)
        #print max_overlap
        if check_for_solution(substrings_copy, max_overlap[1]):
            return max_overlap[1]
        if max_overlap[2] in substrings:
            substrings.remove(max_overlap[2])
        if max_overlap[3] in substrings:
            substrings.remove(max_overlap[3])
        for s in substrings:
            if s!=max_overlap[1] and not (max_overlap[1], s) in seen and not (s, max_overlap[1]) in seen:
                res = get_max_overlap_2(max_overlap[1], s)
                heapq.heappush(imm, res)
                seen.add((max_overlap[1], s))
                seen.add((s,max_overlap[1]))
        substrings.append(max_overlap[1])
        """


def check_for_solution(substrings_copy, curr_res):
    for s in substrings_copy:
        if not s in curr_res:
            return False
    return True

def get_max_overlap_2(s1, s2):
    if s1 in s2:
        return (-len(s1), s2, s1, s2)

    if s2 in s1:
        return (-len(s2), s1, s1, s2)

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
        return (-res[1], res[0], s1, s2)
    #no overlap 
    return (0.0, None, s1, s2)


def is_prefix(pre, post):
    return post.startswith(pre)

def get_max_overlap(s1, s2):
    #smallest possible result is one string is a substring of the other
    if s1 in s2:
        return s2, 1, s1, s2
    if s2 in s1:
        return s1, 1, s1, s2
    possible = []

    i = len(s1) - 1
    j = len(s2) - 1
    total_length = len(s1) + len(s2)
    matched = 0
    #abcccc, cca
    start_matching = False
    fail = False
    #import pdb; pdb.set_trace()
    while i >= 0 and j >= 0 and not fail:
        #print matched
        if j == 0:
            if s1[i] == s2[j]:
                tmp = s1[:i+1] + tmp
                i = -1
                matched += 2 + i + 1
            else:
                tmp = None
                fail = True
        elif s1[i] == s2[j]:
            tmp = s1[i] + tmp
            i -= 1
            j -= 1
            matched += 2
            start_matching = True
        else:
            if not start_matching:
                tmp = s2[j] + tmp
                j -= 1
            else: #bad tmp
                #tmp = None
                tmp = tmp[1:]
                i = min(i+ 1, len(s1) - 1)
                j -= 1
                start_matching = True
             #   matched -= 2
                #fail= True
    return tmp, float(matched/float(total_length)), s1, s2 #if none, there is no match at all



def get_overlaps(s1, s2):
    res = difflib.SequenceMatcher(None, s1, s2).get_matching_blocks()
    #TODO:  returns bad matches, maybe just implement it yourself, or filter.
    #TODO:  filter doesn't work for some cases ("abcccc", "ccd")
    #TODO:  just implement it myself-- just need to check if min size of str1 prepended to str2, and str2 prepended to s1
    print res
    matches = [(r.size,(r.a, r.b)) for r in res]
    print matches
    max_match = max(matches)
    
    while matches:
        s1_start = max_match[1][0]
        s2_start = max_match[1][1]
        size = max_match[0]
        s1_end = s1_start + size
        s2_end = s2_start + size
        
        #no match:  do we return s1 + s2 or s2 + s1
        if size == 0:
            print "HI"
            return min(s2 + s1, s1 + s2)
        #Check if either string is a substring of the other
        if s1 in s2:
            return s2
        if s2 in s1:
            return s1

        #Check if one string can be prepended to the other
        if s1_start == 0 and s2_end == len(s2):
            print "HI"
            return s2[:s2_end] + s1[s1_end:]
        if s2_start == 0 and s1_end == len(s1):
            print "HI"
            return s1[:s1_end] + s2[s2_end:]
        if s1_end == len(s1) and s2_start == 0 and s2_end == len(s2): #maybe unnecessary
            print "HI"
        else:
            matches.remove(max_match)
            max_match = max(matches)
# get_overlaps("abcccc", "ccd")  will overlap ccd in the middle of abcccc --> invalid
            print "FAIL"
        #Different valid cases:
        """
            1.  str1 is a substring of str2 (merged string is just str2)
            2.  str2 is a substring of str1 (merged string is just str1)
            3.  str1's match with str2 begins at str2 and is the rest of str1 (prepend str1 unmatched prefix to str2)
            4.  str2's match with str1 begins at str1 and is the rest of str2 (prepend str2 unmatched prefix to str1)
            5.  str1's match goes to the rest of str1 and str2's match goes to the rest of str2 (append str2 unmatched to str1) 
        """


if __name__ == "__main__":
    main()


