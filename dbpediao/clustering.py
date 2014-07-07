import Levenshtein

class StringCluster(object):
    def __init__(self):
        pass

    def clusterStrings(self, stringList):
        for string_1 in stringList:
            for string_2 in stringList:
                similarity = Levenshtein.jaro_winkler(string_1, string_2)
                if(similarity > 0.95):
                    print similarity
                    print string_1
                    print string_2
                break


if __name__ == "__main__":
    myset = list(myset)
    stringCluster = StringCluster()
    stringCluster.clusterStrings(myset)
