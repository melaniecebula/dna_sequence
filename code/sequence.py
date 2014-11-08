import difflib

#TODO:  take two elements which have the most overlap total number out of all of them and merge together
#TODO:  take longest substring and merge that with second largest substring or maybe string with most overlap
def main():
    with open("../Dataset/reads2.txt") as f:
        substrings = [line.rstrip() for line in f]
        substrings_copy = substrings[:]
#new idea:  keep track of "most overlap":  greedily choose with most overlap (ex:  substrings)

    #TODO:  use max heap

        imm = [] 
        for r1 in substrings:
            for r2 in substrings:
                if r1 != r2:
                    res1 = get_max_overlap_2(r1, r2)
                    print res1
                    #max overlap is either none, or the result and the overlap 0..1 if the result
                    imm.append(res1)
        max_overlap = max(imm, key=lambda x: x[1])
        if check_for_solurion(substrings_copy, max_overlap):
            return max_overlap
        

def check_for_solurion(substrings_copy, curr_res):
    for s in substrings_copy:
        if s not in curr_res:
            return False
    return True

def get_max_overlap_2(s1, s2):
    if s1 in s2:
        return s2, len(s1)

    if s2 in s1:
        return s1, len(s2)

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
        return max(pos_res, key=lambda x: x[1])
    #no overlap 
    return None, 0.0


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





