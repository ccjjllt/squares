
extern "C" {
__device__ double sg(double x){return (x>1e-12)-(x < -1e-12);}
__device__ double dot(const double*a,const double*b,int m,double*r){
 double z=0;for(int k=threadIdx.x;k<m;k+=blockDim.x)z+=a[k]*b[k];
 r[threadIdx.x]=z;__syncthreads();
 for(int t=blockDim.x/2;t;t/=2){if(threadIdx.x<t)r[threadIdx.x]+=r[threadIdx.x+t];__syncthreads();}
 double answer=r[0];__syncthreads();return answer;
}
__device__ double objective(double*q,double*g,int n,double L,int nc,int*head,int*next,double*cs,double*r,double*maxpen){
 int tid=threadIdx.x;
 for(int k=tid;k<nc*nc;k+=blockDim.x)head[k]=-1;
 __syncthreads();
 for(int i=tid;i<n;i+=blockDim.x){
  cs[2*i]=cos(q[3*i+2]);cs[2*i+1]=sin(q[3*i+2]);
  int x=max(0,min(nc-1,int(floor((q[3*i]+3)/1.5))));
  int y=max(0,min(nc-1,int(floor((q[3*i+1]+3)/1.5))));
  next[i]=atomicExch(head+y*nc+x,i);
 }__syncthreads();
 double energy=0,mp=0;
 for(int i=tid;i<n;i+=blockDim.x){
  double x=q[3*i],y=q[3*i+1],c=cs[2*i],s=cs[2*i+1];
  double gx=0,gy=0,ga=0,h=.5*(fabs(c)+fabs(s)),dh=.5*(-s*sg(c)+c*sg(s));
  double b[4]={h-x,h-y,x+h-L,y+h-L};
  for(int k=0;k<4;k++)if(b[k]>0){double p=b[k];energy+=2*p*p;mp=fmax(mp,p);ga+=4*p*dh;
   if(k==0)gx-=4*p;if(k==1)gy-=4*p;if(k==2)gx+=4*p;if(k==3)gy+=4*p;}
  int cx=max(0,min(nc-1,int(floor((x+3)/1.5)))),cy=max(0,min(nc-1,int(floor((y+3)/1.5))));
  for(int yy=max(0,cy-1);yy<=min(nc-1,cy+1);yy++)for(int xx=max(0,cx-1);xx<=min(nc-1,cx+1);xx++)
   for(int j=head[yy*nc+xx];j>=0;j=next[j])if(j!=i){
    double dx=q[3*j]-x,dy=q[3*j+1]-y;if(dx*dx+dy*dy>2.00000001)continue;
    double cj=cs[2*j],sj=cs[2*j+1],cd=c*cj+s*sj,sd=c*sj-s*cj;
    double rad=.5*(1+fabs(cd)+fabs(sd))+2e-10,rd=.5*(-sd*sg(cd)+cd*sg(sd));
    double ux[4]={c,-s,cj,-sj},uy[4]={s,c,sj,cj};int a=0;double z=dx*ux[0]+dy*uy[0];
    for(int k=1;k<4;k++){double v=dx*ux[k]+dy*uy[k];if(fabs(v)>fabs(z)){a=k;z=v;}}
    double p=rad-fabs(z);if(p<=0)continue;
    energy+=.25*p*p;mp=fmax(mp,p);double sign=sg(z);
    gx+=p*sign*ux[a];gy+=p*sign*uy[a];
    ga-=p*(rd+(a<2?sign*(-dx*uy[a]+dy*ux[a]):0));
   }
  g[3*i]=gx;g[3*i+1]=gy;g[3*i+2]=ga;
 }
 r[tid]=energy;r[blockDim.x+tid]=mp;__syncthreads();
 for(int t=blockDim.x/2;t;t/=2){if(tid<t){r[tid]+=r[tid+t];r[blockDim.x+tid]=fmax(r[blockDim.x+tid],r[blockDim.x+tid+t]);}__syncthreads();}
 if(tid==0)*maxpen=r[blockDim.x];double answer=r[0];__syncthreads();return answer;
}
__global__ void eval(double*q,double*g,double*e,int n,int nc,double*Ls,int*head,int*next,double*cs){
 __shared__ double r[512],mp;
 int b=blockIdx.x;double v=objective(q+b*3*n,g+b*3*n,n,Ls[b],nc,head+b*nc*nc,next+b*n,cs+b*2*n,r,&mp);
 if(threadIdx.x==0){e[2*b]=v;e[2*b+1]=mp;}
}
__global__ void lbfgs(double*Q,double*work,double*history,double*out,int n,int nc,double*Ls,int*heads,int*links,double*trigs,int steps,int M){
 __shared__ double r[512],mp,alpha[12],rho[12],syarr[12],yyarr[12];
 int b=blockIdx.x,tid=threadIdx.x,d=3*n;
 double*q=Q+b*d,*g=work+b*d*5,*v=g+d,*trial=v+d,*gt=trial+d,*direction=gt+d;
 double*S=history+b*2*M*d,*Y=S+M*d;int*head=heads+b*nc*nc,*next=links+b*n;double*cs=trigs+b*2*n;
 double L=Ls[b],E=objective(q,g,n,L,nc,head,next,cs,r,&mp);int stored=0,last=0,its=0;
 for(int it=0;it<steps;it++){
  its=it;if(mp<2e-11)break;
  for(int k=tid;k<d;k+=blockDim.x)v[k]=g[k];__syncthreads();
  for(int j=0;j<stored;j++){int h=(last-1-j+M)%M;double z=dot(S+h*d,v,d,r)*rho[h];
   if(tid==0)alpha[h]=z;__syncthreads();for(int k=tid;k<d;k+=blockDim.x)v[k]-=z*Y[h*d+k];__syncthreads();}
  double scale=stored?fmin(10.,fmax(1e-6,syarr[(last-1+M)%M]/yyarr[(last-1+M)%M])):.2;
  for(int k=tid;k<d;k+=blockDim.x)v[k]*=scale;__syncthreads();
  for(int j=stored-1;j>=0;j--){int h=(last-1-j+M)%M;double z=dot(Y+h*d,v,d,r)*rho[h];
   double a=alpha[h]-z;for(int k=tid;k<d;k+=blockDim.x)v[k]+=a*S[h*d+k];__syncthreads();}
  for(int k=tid;k<d;k+=blockDim.x)direction[k]=-v[k];__syncthreads();
  double slope=dot(g,direction,d,r);
  if(slope>=-1e-30){for(int k=tid;k<d;k+=blockDim.x)direction[k]=-.2*g[k];__syncthreads();slope=dot(g,direction,d,r);stored=0;}
  double dm=0;for(int k=tid;k<d;k+=blockDim.x)dm=fmax(dm,fabs(direction[k]));r[tid]=dm;__syncthreads();
  for(int t=blockDim.x/2;t;t/=2){if(tid<t)r[tid]=fmax(r[tid],r[tid+t]);__syncthreads();}
  double step=fmin(1.,.2/fmax(1e-30,r[0])),En=E;bool ok=false;
  for(int ls=0;ls<24;ls++){
   for(int k=tid;k<d;k+=blockDim.x)trial[k]=q[k]+step*direction[k];__syncthreads();
   En=objective(trial,gt,n,L,nc,head,next,cs,r,&mp);
   if(En<=E+1e-4*step*slope){ok=true;break;}step*=.5;
  }
  if(!ok)break;
  for(int k=tid;k<d;k+=blockDim.x){v[k]=trial[k]-q[k];direction[k]=gt[k]-g[k];}__syncthreads();
  double sy=dot(v,direction,d,r),yy=dot(direction,direction,d,r);
  if(sy>1e-24&&yy>1e-30){for(int k=tid;k<d;k+=blockDim.x){S[last*d+k]=v[k];Y[last*d+k]=direction[k];}__syncthreads();
   if(tid==0){rho[last]=1/sy;syarr[last]=sy;yyarr[last]=yy;}__syncthreads();last=(last+1)%M;stored=min(M,stored+1);}
  for(int k=tid;k<d;k+=blockDim.x){q[k]=trial[k];g[k]=gt[k];}__syncthreads();E=En;
 }
 if(tid==0){out[3*b]=E;out[3*b+1]=mp;out[3*b+2]=its;}
}
}
