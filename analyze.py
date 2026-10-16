"""Exploratory unsupervised anomaly detection. Predictions are NOT ground-truth labels."""
import os,pandas as pd,numpy as np,matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
ROOT=os.path.dirname(__file__)
df=pd.read_csv(os.path.join(ROOT,'results.csv'))
X=StandardScaler().fit_transform(df[['level','latency_ms']])
model=IsolationForest(n_estimators=200,contamination=.08,random_state=42)
df['ai_anomaly']=model.fit_predict(X)==-1
threshold=df.loc[df.level==1,'latency_ms'].quantile(.95)
df['fixed_threshold_alert']=df.latency_ms>threshold
print('Baseline P95 (1 worker):',round(threshold,2),'ms')
print('AI anomalies:',int(df.ai_anomaly.sum()),'Threshold alerts:',int(df.fixed_threshold_alert.sum()))
print('NOTE: These are alert counts, not precision/recall; ground-truth labels are absent.')
df.to_csv(os.path.join(ROOT,'analyzed_results.csv'),index=False)
fig,ax=plt.subplots(figsize=(11,5.5));ax.scatter(range(len(df)),df.latency_ms,s=12,alpha=.5,label='HTTP requests');idx=np.flatnonzero(df.ai_anomaly);ax.scatter(idx,df.loc[idx,'latency_ms'],s=24,marker='x',label='Isolation Forest flag');ax.set(xlabel='Request sequence',ylabel='Latency (ms)',title='Local student-search API: observed latency and AI flags');ax.legend();fig.tight_layout();fig.savefig(os.path.join(ROOT,'measured_chart.png'),dpi=170)
