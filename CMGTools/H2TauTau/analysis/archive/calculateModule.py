from ROOT import TMatrixD, TVectorD
from ROOT import TLorentzVector, Double # for M(l2,tau) calculation

def calculateSphericity(particles):
    momentumTensor = TMatrixD(3, 3)
    p2_sum = 0.

    for iparticle in particles:
        px = iparticle.Px()
        py = iparticle.Py()
        pz = iparticle.Pz()

        momentumTensor[0][0] += px * px
        momentumTensor[0][1] += px * py
        momentumTensor[0][2] += px * pz
        momentumTensor[1][0] += py * px
        momentumTensor[1][1] += py * py
        momentumTensor[1][2] += py * pz
        momentumTensor[2][0] += pz * px
        momentumTensor[2][1] += pz * py
        momentumTensor[2][2] += pz * pz
        
        p2_sum += (px * px + py * py + pz * pz)


#    print 'before momentumTensor'
#    momentumTensor.Print()

    if p2_sum != 0.:
        for i in range(3):
            for j in range(3):
                momentumTensor[i][j] = momentumTensor[i][j] / p2_sum

    print 'after momentumTensor by dividing ', p2_sum
    momentumTensor.Print()

    ev = TVectorD(3)
    momentumTensor.EigenVectors(ev);

    #some checks & limited precision of TVectorD

    ev0 = abs(ev[0])
    ev1 = abs(ev[1])
    ev2 = abs(ev[2])

    if ev0 < 0.000000000000001:
        ev0 = 0.
    if ev1 < 0.000000000000001:
        ev1 = 0.
    if ev2 < 0.000000000000001:
        ev2 = 0.
    
    if ((ev0 < ev1) or (ev1 < ev2)):
        print 'Calculating eigenvectors failed.'

    return 3*ev2/2., 3*(ev1+ev2)/2.

#    print ev0, ev1, ev2
#    return ev2

#def calculateAplanarity(sphericity):
#    return 3./2.*sphericity


if __name__ == '__main__':
    
    electron = TLorentzVector()
    electron.SetPtEtaPhiM(20,2,1.3,0.05)

    muon = TLorentzVector()
    muon.SetPtEtaPhiM(20,1,1.2,0.1)

    aplanarity, sphericity = calculateSphericity([electron, muon])
    print aplanarity, sphericity
    
