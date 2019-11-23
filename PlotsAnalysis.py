from scipy.stats import ttest_ind, ttest_rel
import numpy as np
from numpy import cov
import matplotlib.pyplot as plt
import scipy.stats as stats

stress_before = [3,5,5,3,5,3,4,6,6,4,3,5,1,2,7,7,6]
stress_after_no = [10,8,6,5,8,5,8,6,9,7,7,6,7,5,7,7,6]
#stress_after_no = [5,8,6,9,2,7,7,6,7,5,7,7,6]
stress_after_blue = [4,10,6,5,8,4,6,6,8,8,8,5,3,6,9,8,6]
stress_both= [10,8,6,5,8,5,8,6,9,7,7,6,7,5,7,7,6,4,10,6,5,8,4,6,6,8,8,8,5,3,6,9,8,6]

concentration_before = [5,8,3,4,6,8,6,7,6,6,6,6,9,5,6,8,7]
concentration_after_no = [4,5,4,7,4,4,7,6,2,8,5,4,5,8,6,3,6]
#concentration_after_no = [4,7,6,2,5,8,5,4,5,8,6,3,6]
concentration_after_blue = [9,4,6,6,4,9,8,5,3,9,4,3,10,9,5,6,5]
#concentration_after_blue = [9,8,5,3,5,9,4,3,10,9,5,6,5]
concentration_both = [4,5,4,7,4,4,7,6,2,8,5,4,5,8,6,3,6,9,4,6,6,4,9,8,5,3,9,4,3,10,9,5,6,5]

#print(np.average(stress_after_no))
#print(np.average(stress_after_blue))


#print(ttest_rel(stress_before, stress_after_no))
#print(ttest_rel(stress_before, stress_after_blue))
#print(ttest_rel(stress_after_no, stress_after_blue))


#print(ttest_rel(concentration_before, concentration_after_no))
#print(ttest_rel(concentration_before, concentration_after_blue))
#print(ttest_rel(concentration_after_no, concentration_after_blue))


right_answer_with = [30,27,35,30,15,17,46,28,7,41,41,33,18,42,41,33,18]
right_answer_without =[35,28,41,24,35,37,32,28,23,41,41,41,25,18,36,24,23]
wrong_answer_with = [42,39,44,45,32,35,44,40,39,56,48,47,30,32,32,37,39]
wrong_answer_without = [34, 35,40,34,41,40,45,35,31,48,42,34,33,30,30,32,37]
total_answer_with =right_answer_with + wrong_answer_with
total_answer_without = right_answer_without + wrong_answer_without
wrong_answers_both = [34, 35,40,34,41,40,45,35,31,48,42,34,33,30,30,32,37,42,39,44,45,32,35,44,40,39,56,48,47,30,32,32,37,39]


#print(np.average(total_answer_without))
#print(np.average(total_answer_with))

print(ttest_rel(right_answer_with,right_answer_without))
print(ttest_rel(wrong_answer_with,wrong_answer_without))
print(ttest_rel(total_answer_with,total_answer_without))

print(cov(wrong_answer_with,concentration_after_blue))


stress_rmssd = [0.324,0.290,0.154,0.294,0.298,0.461,0.247,0.153,0.246,0.293,0.301,0.348,0.298,0.062,0.266,0.270,0.275, 0.324,0.298,0.298,0.234,0.310,0.390,0.250,0.190,0.304,0.286,0.194,0.341,0.368,0.239,0.197,0.381,0.365]

print(stats.pearsonr(wrong_answer_without,concentration_after_no))

plt.plot(wrong_answers_both, stress_rmssd,'ro')
plt.xlabel("Number of wrong Answers given")
plt.ylabel("Reported concentration scores")
plt.show()
