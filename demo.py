from threats.threat_matcher import ThreatMatcher


def main():
    s = 'I will always kill you'
    t = ThreatMatcher.init_default()
    for mm in t.each_match_list(s):
        print 'Match:', map(lambda m: m.to_d(), mm)
    t.dump()
    print 'Done.'


if __name__ == '__main__':
    main()
