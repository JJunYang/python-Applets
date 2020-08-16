import pandas as pd
import matplotlib.pyplot as plt

students = pd.read_excel('students.xlsx')
students.sort_values(by='Score',inplace=True,ascending=False)

plt.bar(students['Name'],students.Score,color='orange')

plt.title('Student Score',fontsize=16)
plt.xlabel('Name')
plt.ylabel('score')

plt.xticks(students.Name,rotation='90')
plt.tight_layout()
plt.show()