"""Three figures: no raw data, no synthetic empirical-performance numbers."""
import json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(Path(os.environ.get('TEMP','/tmp'))/'fgmotion-matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':180})
data=json.loads((ROOT/'docs/evidence/verified_aggregates.json').read_text())
out=ROOT/'figures';out.mkdir(exist_ok=True)
fig,ax=plt.subplots(figsize=(11,4.1));ax.set_xlim(-.2,11.2);ax.set_ylim(0,4);ax.axis('off')
boxes=[(.1,2.15,'Local research video\n(private; rights restricted)'),(2.9,2.15,'Fixed 16-frame evidence\nUniform / GT-local oracle'),(5.7,2.15,'Frozen VideoMAE\n8 contextual positions'),(8.5,2.15,'Probe / diagnostic head\nSaved predictions')]
for x,y,t in boxes:
 ax.add_patch(FancyBboxPatch((x,y),2.35,.95,boxstyle='round,pad=.12',facecolor='#edf2f7',edgecolor='#35566f'))
 ax.text(x+1.175,y+.475,t,ha='center',va='center',fontsize=9)
 if x<8:ax.annotate('',xy=(x+2.7,y+.475),xytext=(x+2.48,y+.475),arrowprops=dict(arrowstyle='->',color='#35566f'))
ax.text(5.5,3.65,'Representation and evidence audit',ha='center',fontsize=16,weight='bold')
ax.text(5.5,1.45,'Controls: same-frame shuffle / repeated static / fixed appearance views',ha='center',fontsize=11)
ax.text(5.5,.82,'Fit-only normalization  →  Inner selection  →  frozen Validation evaluation',ha='center',fontsize=11)
ax.text(5.5,.2,'Conceptual diagnostic pipeline • GT-local is an oracle • No validated original motion module',ha='center',fontsize=9,color='#555555')
fig.tight_layout();fig.savefig(out/'pipeline.png');plt.close(fig)

fig,ax=plt.subplots(figsize=(8,4.8));colors=['#286780','#c57d32'];x=np.arange(3)
for j,seed in enumerate([42,1601]):
 vals=[100*next(r['local_map'] for r in data if r['study']=='appearance' and r['model']==case and r['seed']==seed and r['partition']=='val' and r['view']=='clean') for case in ['B0','B1','B2']]
 bars=ax.bar(x+(j-.5)*.32,vals,.31,color=colors[j],label=f'Seed {seed}')
 ax.bar_label(bars,fmt='%.2f',padding=3,fontsize=9)
ax.set_xticks(x,['B0: existing probe','B1: augmentation','B2: + consistency']);ax.set_ylim(0,14);ax.set_ylabel('Local multi-label mAP (%)');ax.set_title('Standard baselines on retained Validation');ax.legend(frameon=False,loc='upper right');ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
fig.text(.5,.015,'GT-local oracle • reused development partition • two seeds, not independent test sets',ha='center',fontsize=9)
fig.tight_layout(rect=[0,.06,1,1]);fig.savefig(out/'comparison.png');plt.close(fig)

fig,ax=plt.subplots(figsize=(8,4.8))
for model,color in [('Small','#286780'),('Base','#c57d32')]:
 for seed,style in [(42,'-'),(1601,'--')]:
  vals=[]
  for part in ['fit','inner','val']:
   r=next(r for r in data if r['seed']==seed and r['partition']==part and ((model=='Small' and r['study']=='appearance' and r['model']=='B0' and r['view']=='clean') or (model=='Base' and r['study']=='encoder' and r['view']=='gt16')))
   vals.append(100*r['local_map'])
  ax.plot([0,1,2],vals,style,marker='o',color=color,label=f'{model}, seed {seed}',linewidth=1.7)
ax.set_xticks([0,1,2],['Fit (1,024)','Inner (454)','Validation (1,459)']);ax.set_ylim(0,100);ax.set_ylabel('Local multi-label mAP (%)');ax.set_title('Development partition gap with fixed GT-local evidence');ax.legend(frameon=False);ax.grid(axis='y',alpha=.2)
fig.text(.5,.015,'Partition comparison only: source/subject identities are not established; GT-local is an oracle.',ha='center',fontsize=8.7)
fig.tight_layout(rect=[0,.06,1,1]);fig.savefig(out/'partition_gap.png');plt.close(fig)
print('Regenerated three figures from aggregate evidence; no training or raw media access.')
