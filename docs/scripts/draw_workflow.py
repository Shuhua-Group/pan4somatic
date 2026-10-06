from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({'font.family':'Arial','svg.fonttype':'none','pdf.fonttype':42})
OUT=Path(__file__).resolve().parent.parent / 'figures'
OUT.mkdir(parents=True, exist_ok=True)
fig,ax=plt.subplots(figsize=(180/25.4,110/25.4)); fig.subplots_adjust(0,0,1,1)
ax.set(xlim=(0,180),ylim=(114,0)); ax.axis('off'); fig.patch.set_facecolor('#FFFFFF')
ink='#172A3A'; muted='#526477'; blue='#21649B'; teal='#087D78'; border='#CBD5DF'
def txt(x,y,s,size=12,color=ink,weight='normal',ha='left'):
 return ax.text(x,y,s,fontsize=max(6, size*0.47),color=color,weight=weight,ha=ha,va='center',linespacing=1.5)
def box(x,y,w,h,title,sub='',color=blue,fill='#FFFFFF',fs=12):
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.0,rounding_size=1.4',ec=color,fc=fill,lw=.75))
 txt(x+w/2,y+h*.36 if sub else y+h/2,title,fs,color,'bold','center')
 if sub: txt(x+w/2,y+h*.72,sub,9.5,muted,ha='center')
def arrow(x1,y1,x2,y2,color=muted,dashed=False):
 ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=7,lw=.8,color=color,linestyle='--' if dashed else '-'))
txt(5,6,'pan4somatic',26,ink,'bold'); txt(49,6,'From reads or aligned BAMs to variant calls',18)
txt(175,6,'v1.0.4',11,muted,ha='right')
# configuration ribbon
ax.add_patch(FancyBboxPatch((5,12),170,17,boxstyle='round,pad=0,rounding_size=1.5',fc='#F3F6F9',ec='none'))
txt(8,16,'01  SELECT REFERENCE + GRAPH',10,muted,'bold')
box(8,20,43,6,'GRCh38 / HPRC1',color=ink,fs=11)
box(55,20,53,6,'GRCh38 / CPC1 + HPRC1',color=ink,fs=11)
box(112,20,35,6,'CHM13 / CPC2*',color=ink,fs=11)
txt(150,22,'Same choice governs\ngraph and coordinates',9,muted)
txt(5,33,'02  CHOOSE AN INPUT AND PLATFORM',10,muted,'bold')
txt(127,33,'03  SELECT VARIANT OUTPUTS',10,muted,'bold')
for y,label,c,fill in [(38,'NGS  ·  Illumina',blue,'#EFF6FC'),(66,'HiFi  ·  PacBio',teal,'#EDF8F5')]:
 ax.add_patch(FancyBboxPatch((5,y-2),170,23,boxstyle='round,pad=0,rounding_size=1.4',fc=fill,ec='none'))
 txt(8,y+1,label,12,c,'bold')
 box(8,y+5,21,11,'FASTQ','R1 + R2' if y==38 else 'HiFi reads',c)
 box(35,y+5,27,11,'Personalized graph',color=c,fs=11)
 box(68,y+5,31,11,'Graph alignment',color=c,fs=11)
 box(105,y+5,22,11,'BAM checks',color=c,fs=11)
 for x1,x2 in [(29,35),(62,68),(99,105)]:arrow(x1,y+10.5,x2,y+10.5,c)
 txt(83.5,y+19,'NGS: normalize + dedup' if y==38 else 'HiFi: normalize + index',8.5,muted,ha='center')
# callers
box(134,43,20,11,'Mutect2','small',blue,fs=12); box(160,43,13,11,'SNV','+ Indel',blue,fs=11)
arrow(127,48.5,134,48.5,blue);arrow(154,48.5,160,48.5,blue)
box(134,67,20,8,'DeepSomatic','small',teal,fs=10);box(160,67,13,8,'SNV','+ Indel',teal,fs=10)
box(134,79,20,8,'Sniffles2','sv',teal,fs=11);box(160,79,13,8,'SV','VCF + SNF',teal,fs=11)
arrow(127,76.5,134,71,teal);arrow(127,76.5,134,83,teal);arrow(154,71,160,71,teal);arrow(154,83,160,83,teal)
txt(153.5,63,'HiFi: small / sv / all',9,teal,'bold','center')
# midline call-from-bam entry arrows no graph re-entry
box(105,59,22,7,'BAM + BAI',color=ink,fill='#FFFFFF',fs=9)
arrow(116,59,116,54,ink,True);arrow(116,66,116,71,ink,True)
txt(101,62.5,'Direct entry →',9,ink,ha='right')
# graph role logic annotation in interlane space
# below tracks
ax.plot([5,175],[91,91],color=border,lw=.9)
txt(5,95,'GRAPH SOURCE',9,muted,'bold');txt(34,95,'Paired: normal → shared graph*  |  Tumor-only: tumor → graph',10)
# scopes footer with three clear compact cards
box(5,100,53,8,'full','FASTQ → BAM checks → callers',ink,fill='#F3F6F9',fs=11)
box(63,100,53,8,'align_only','FASTQ → BAM checks → stop',ink,fill='#F3F6F9',fs=11)
box(121,100,54,8,'call_from_bam','BAM → checks → callers',ink,fill='#F3F6F9',fs=11)
txt(5,111,'* CPC2 not public. Paired FASTQ: known issue (see audit). Paired SV: separate calls, no subtraction.',8.5,muted)
# save
for ext in ['svg','pdf','png']:
 fig.savefig(OUT/f'pan4somatic_workflow_v1.0.4.{ext}',dpi=300,facecolor='white')
print(OUT)
