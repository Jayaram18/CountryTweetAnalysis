import matplotlib.pyplot as plt
def plotPieChart(positive, w_positive, s_positive, negative, w_negative, s_negative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(w_positive) + '%]','Strongly Positive [' + str(s_positive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(w_negative) + '%]', 'Strongly Negative [' + str(s_negative) + '%]']
        sizes = [positive, w_positive, s_positive, neutral, negative, w_negative, s_negative]
        colors = ['green','yellow','blue', 'purple', 'aqua','red','brown']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
