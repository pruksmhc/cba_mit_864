from numpy import * 

phi = .5*(1+sqrt(5))

#sgn = lambda x: (1, -1)[x<0]
def mnbrak(ax,bx,f,glimit=1e2,eps=1e-6):
    #given distinct initial points ax and bx, search for a bracketing triple ax,bx,cx
    #from numerical recipes, 10.1
    if f(bx)>f(ax):
        tmp = ax; ax = bx; bx = tmp; #switch
    cx = bx + phi*(bx-ax);
    while True:
        r=(bx-ax)*(f(bx)-f(cx)) #do parabolic fit
        q=(bx-cx)*(f(bx)-f(ax))
        denom = q-r if q-r!=0 else eps*sgn(q-r)
        u=bx-((bx-cx)*q-(bx-ax)*r)/(2*denom)
        ulim=bx+glimit*(cx-bx)
        if (bx-u)*(u-cx) > 0:
            if f(u) < f(cx):
                return bx,u,cx
            elif f(u) > f(bx):
                return ax,bx,u
            u = cx+phi*(cx-bx) #parabolic fit didn't help, use default magnification
        elif (cx-u)*(u-ulim) > 0:
            if f(u) < f(cx):
                bx=cx
                cx=u
                u = cx+phi*(cx-bx)
        elif (u-ulim)*(ulim-cx) > 0:
            u = ulim
        else:
            u = cx+phi*(cx-bx)
        ax=bx; bx=cx; cx=u;
        if f(bx) < f(cx): break
    return ax,bx,cx
def linemin(xi,d,f,alpha=1,eps=1e-3,just_result=False):
    #golden section line minimization
    fs = lambda a: f(xi+a*d) #scalar
    x0,x1,x2 = mnbrak(0,alpha,fs)
    print("thebottom bound")
    print(xi+x0*d)
    print("The upper bound")
    print(xi+x2*d)
    now()
    #x0,x1,x2 = map(lambda a: x0+a*d,mnbrak(0,alpha,fs))
    x = array([[x0,x1,x2]])
    #l = lambda x: sum(x**2,axis=0)
    i=0
    while(x2-x0 > eps):
        #print 'linemin',l(x2-x0)
        i = i+1
        if x1-x0 > x2-x1:
            x3 = x0 + (x1-x0)/phi
            if fs(x3)<fs(x1):
                x0,x1,x2 = x0,x3,x1
            else:
                x0,x1,x2 = x1,x3,x2
        else:
            x3 = x1 + (x2-x1)/phi
            if fs(x3)<fs(x1):
                x0,x1,x2 = x1,x3,x2
            else:
                x0,x1,x2 = x0,x1,x3
        x = vstack((x,array([[x0,x1,x2]])))

    if just_result:
        return x[-1,1] #just return x1 from last iteration
    else:
        return x
def rosenbrock(v):
    return (1-v[...,0])**2 + 100*(v[...,0]-v[...,1]**2)**2

def powell(x0,f,alpha=1.,eps=1e-4,max_iter=100):
    #powell direction set method, start x0, function f
    x = array([x0])
    print("the intitial point")
    print(x)
    n_dim = shape(x)[-1]
    print("and the dimensions")
    print(n_dim)
    d = eye(n_dim) #take coordinate axes as initial directions
    print("the initail direcitons")
    print(d)
    #it is important to make sure these are descent directions, else linemin will fail
    i=0
    while(True):
        df = []    #changes in objective along each direction
        i = i+1
        for di in d:
            print("for the di")
            print(di)
            print("x input")
            print(x[-1])

            a_min = linemin(x[-1],di,f,alpha=alpha,just_result=True) #minimize in this direction
            xnew = x[-1]+a_min*di
            x = vstack((x,array([xnew])))
            df.append(f(x[-2])-f(x[-1])) #save change in objective
        if max(df) < eps or i>max_iter: break
        d[argmax(df)] = sum(d,axis=0)/n_dim #replace old direction with overall change
        #d[argmax(df)] /= linalg.norm(d[argmax(df)])
    return x

# What is goign on witht ehlin eminimization. 
x=powell([-1,-1],rosenbrock,alpha=.1,eps=1e-5,max_iter=100);
print(x)
