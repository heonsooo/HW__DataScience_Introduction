from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pymysql
import numpy as np
from sklearn.metrics import confusion_matrix


## 고정##
conn = pymysql.connect(host = 'localhost', user = 'Soo', password = '1234' , db = 'data_science')
curs = conn.cursor(pymysql.cursors.DictCursor)
sql = 'select*from db_score'
curs.execute(sql)
data = curs.fetchall()
curs.close()
conn.close()
X = [ ( t['homework'], t['discussion'], t['midterm'] )  for t in data ]
y = [ 0 if (t['grade'] == 'A')  else 1 if (t['grade'] == 'B') else 2 for t in data ]            # muliti class 
# y = [ 1 if (t['grade'] == 'B') else -1 for t in data ]                  # binary 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33 , random_state=42)
X = np.array(X)
y = np.array(y)
## 고정 ## 

Lr = LogisticRegression(C=1, random_state=0,solver= 'liblinear')
Lr.fit(X_train, y_train)
predict = Lr.predict(X_test)

cnf_matrix = confusion_matrix(y_test, predict)


FP = cnf_matrix.sum(axis=0) - np.diag(cnf_matrix) 
FN = cnf_matrix.sum(axis=1) - np.diag(cnf_matrix)
TP = np.diag(cnf_matrix)
TN = cnf_matrix.sum() - (FP + FN + TP)
FP = FP.astype(float)
FN = FN.astype(float)
TP = TP.astype(float)
TN = TN.astype(float)


ACC = (TP+TN)/(TP+FP+FN+TN)

prec =TP/(TP+FP)
recall = TP/(TP+FN)
f1_score = 2*prec*recall / (prec + recall)

print( ' < train_test_split by_Logistic Regression_Multi-class > ' ,'\n')
print('accuracy =', ACC)
print('precision = ' ,prec)
print('recall =  ' ,recall)
print('F1_score = ', f1_score,'\n')





from sklearn.model_selection import KFold

Accuracy = []
Precision = []
Recall = []
F1_score = []
mean_acc ,mean_prec , mean_rec, mean_f1 = [0,0,0],[0,0,0],[0,0,0],[0,0,0]
k= int(4)
kf = KFold(n_splits =k, random_state = 42, shuffle = True)


for train_index, test_index in kf.split(X):
    X_train , X_test = X[train_index], X[test_index]
    y_train , y_test = y[train_index], y[test_index]
    

########################################################################

    Lr = LogisticRegression(C=1, random_state=0, solver= 'liblinear' ).fit(X_train, y_train)
    y_predict = Lr.predict(X_test)
    cnf_matrix = confusion_matrix(y_test, y_predict)

############################################################################

    FP = cnf_matrix.sum(axis=0) - np.diag(cnf_matrix) 
    FN = cnf_matrix.sum(axis=1) - np.diag(cnf_matrix)
    TP = np.diag(cnf_matrix)
    TN = cnf_matrix.sum() - (FP + FN + TP)
    FP = FP.astype(float)
    FN = FN.astype(float)
    TP = TP.astype(float)
    TN = TN.astype(float)
    # Overall accuracy for each class
    ACC = (TP+TN)/(TP+FP+FN+TN) 
    # Precision or positive predictive value
    prec =TP/(TP+FP)
    recall = TP/(TP+FN)
    f1_score = 2*prec*recall / (prec + recall)

    Accuracy.append(ACC)
    Precision.append(prec)
    Recall.append(recall)
    F1_score.append(f1_score)



for i in range(0, k):
    for j in range(0,3):
        mean_acc[j] += float(Accuracy[i][j])
        mean_prec[j] += float(Precision[i][j])
        mean_rec[j] += float(Recall[i][j])
        mean_f1[j] += float(F1_score[i][j])

for j in range(0,3):
    mean_acc[j] = round(mean_acc[j]/k,4)
    mean_prec[j] = round(mean_prec[j]/k,4)
    mean_rec[j] =round(mean_rec[j]/k,4)
    mean_f1[j] = round(mean_f1[j]/k,4)

    
#print(mean_acc,'\n' ,mean_prec,'\n' , mean_rec,'\n', mean_f1)

print( ' < K-fold cross validation by_Logistic Regression_Multi-class > ')
print('accuracy_평균 = ', mean_acc)
print('precision_평균 = ', mean_prec )
print('recall_평균 = ', mean_rec)
print('f1_score_평균 = ',mean_f1,'\n')
