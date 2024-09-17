from poseidon_constants import *
modul = 21888242871839275222246405745257275088548364400416034343698204186575808495617

def Sigma(input) :
    return pow(input, 5, modul)


def Ark(t, C, r, input) :
    out = [0 for i in range(t)]
    for i in range(t) :
        out[i] = (input[i] + C[i + r]) % modul
    return out
    

def Mix(t, M, input) :
    out = [0 for i in range(t)]
    for i in range(t) :
        lc = 0
        for j in range(t) :
            lc = (lc + M[j][i]*input[j]) % modul
        out[i] = lc
    return out

def MixLast(t, M, s, input) :
    lc = 0
    for j in range(t) :
        lc = (lc + M[j][s]*input[j]) % modul
    out = lc
    return out

def MixS(t, S, r, input) :
    out = [0 for i in range(t)]

    lc = 0
    for i in range(t) :
        lc = (lc + S[(t*2-1)*r+i]*input[i]) % modul
        
    out[0] = lc
    for i in range(1,t) :
        out[i] = (input[i] +  input[0] * S[(t*2-1)*r + t + i - 1]) % modul
    return out

def PoseidonEx(nOuts, inputs, initialState) :
    out = [0 for i in range(nOuts)]
    nInputs = len(inputs)
    # Using recommended parameters from whitepaper https://eprint.iacr.org/2019/458.pdf (table 2, table 8)
    # Generated by https://extgit.iaik.tugraz.at/krypto/hadeshash/-/blob/master/code/calc_round_numbers.py
    # And rounded up to nearest integer that divides by t
    N_ROUNDS_P = [56, 57, 56, 60, 60, 63, 64, 63, 60, 66, 60, 65, 70, 60, 64, 68]
    t = nInputs + 1
    nRoundsF = 8
    nRoundsP = N_ROUNDS_P[t - 2]
    C = [0 for i in range(t*nRoundsF + nRoundsP)]
    C = POSEIDON_C(t)
    S = [0 for i in range(N_ROUNDS_P[t-2]  *  (t*2-1))]
    S  = POSEIDON_S(t)
    M = [[0 for i in range(t)] for j in range(t)]
    M = POSEIDON_M(t)
    P = [[0 for i in range(t)] for j in range(t)]
    P = POSEIDON_P(t)

    ark = [0 for i in range(nRoundsF)]
    sigmaF = [[0 for i in range(t)] for j in range(nRoundsF)]
    sigmaP = [0 for i in range(nRoundsP)]
    mix = [0 for i in range(nRoundsF-1)]
    mixS = [0 for i in range(nRoundsP)]
    mixLast = [0 for i in range(nOuts)]

    input = [inputs[j-1] if j > 0 else initialState for j in range(t)]
    ark[0] = Ark(t, C, 0, input)
    for r in range(nRoundsF//2-1) :
        for j in range(t) :
            input = ark[0][j] if r == 0 else mix[r-1][j]
            sigmaF[r][j] = Sigma(input)
        input = [sigmaF[r][j] for j in range(t)]
        ark[r+1] = Ark(t, C, (r+1)*t, input)
        input = [ark[r+1][j] for j in range(t)]
        mix[r] = Mix(t,M, input)
    
    for j in range(t) :
        sigmaF[nRoundsF//2-1][j] = Sigma(mix[nRoundsF//2-2][j])
    
    input = [sigmaF[nRoundsF//2-1][j] for j in range(t)]
    ark[nRoundsF//2] = Ark(t, C, (nRoundsF//2)*t, input)
    
    input = [ark[nRoundsF//2][j] for j in range(t)]
    mix[nRoundsF//2-1] = Mix(t,P, input)

    for r in range(nRoundsP) :
        if (r == 0) :
            sigmaP[r] = Sigma(mix[nRoundsF//2-1][0])
        else :
            sigmaP[r] = Sigma(mixS[r-1][0])
        input = [0 for j in range(t)]
        for j in range(t) :
            if j == 0 :
                input[j] = (sigmaP[r] + C[(nRoundsF//2+1)*t + r]) % modul
            else :
                if r == 0 :
                    input[j] = mix[nRoundsF//2-1][j]
                else :
                    input[j] = mixS[r-1][j]
        mixS[r] = MixS(t, S, r, input)
    
    for r in range(nRoundsF//2-1) :
        for j in range(t) :
            if (r == 0) :
                sigmaF[nRoundsF//2 + r][j] = Sigma(mixS[nRoundsP-1][j])
            else :
                sigmaF[nRoundsF//2 + r][j] = Sigma(mix[nRoundsF//2+r-1][j])
        
        input = [sigmaF[nRoundsF//2 + r][j] for j in range(t)]
        ark[nRoundsF//2 + r + 1] = Ark(t, C,  (nRoundsF//2+1)*t + nRoundsP + r*t, input )

        input = [ark[nRoundsF//2 + r + 1][j] for j in range(t)]
        mix[nRoundsF//2 + r] = Mix(t,M, input)
    
    for j in range(t) :
        sigmaF[nRoundsF-1][j] =  Sigma(mix[nRoundsF-2][j])

    for i in range(nOuts) :
        input = [sigmaF[nRoundsF-1][j] for j in range(t)]
        mixLast[i] = MixLast(t,M,i,input)
    
    return mixLast
 

def poseidon(inputs) :
    
    pEx = PoseidonEx(1, inputs, 0)
    return pEx[0]