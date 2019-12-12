def Ry(Vs,G,R1,R3,Vout):
    numerator= Vs*G*R1*R3 - Vout*(R3*R1 + R2*R3)
    denom= Vs*G*R1 + Vout(R1 +R2)
    return numerator/denom
