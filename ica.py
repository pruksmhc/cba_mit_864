#ICA
def gen_expect(x):
    mean1 = sum(x[0,])/N
    mean2 = sum(x[1,])/N
    return np.array([[mean1],[mean2]])

df = lambda x: tanh(x)
ddf = lambda x: 1/cosh(x)**2
def ica(w):
    i=0
    while True:
        i+=1  
        g1 = gen_expect(df(dot(w,unit_x))*unit_x)
        g2 = gen_expect(ddf(dot(w,unit_x)))
        g1 = np.array([g1[0, 0], g1[1,0]])
        g2 = np.array([g2[0, 0], g2[1,0]])
        w_new = g1 - g2
        w_new /= np.linalg.norm(w_new)
        if abs(np.linalg.norm(w_new-w))<0.000001: 
            break
        w = w_new
    return w

w1 = ica(np.random.rand(2))
w2 = array([-w1[1],w1[0]]) # orthog

print("Least-Gaussian mixture ")
print(w1, w2)

plt.title("After decomposing with ICA")
plt.plot([0,w1[0]],[0,w1[1]],marker='.',lw=4,c='r')
plt.plot([0,w2[0]],[0,w2[1]],marker='.',lw=4,c='r')
plt.gca().set_aspect(1.)

plt.show()


