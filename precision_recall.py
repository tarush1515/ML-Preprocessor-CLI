import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

y_true = [1, 0, 1, 0, 1, 0, 1, 0, 0, 1]
y_pred = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]

precision = precision_score(y_true, y_pred)
print("precision = ", precision)

recall = recall_score(y_true, y_pred)
print("recall = ", recall)

f1 = f1_score(y_true, y_pred)
print("f1 = ", f1)

cf_matrix = confusion_matrix(y_true, y_pred)
sns.heatmap(cf_matrix / np.sum(cf_matrix), fmt='.2%', annot=True)
plt.show()
precision = precision_score(y_true, y_pred, average='binary')
