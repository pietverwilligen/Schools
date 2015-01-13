from CMSDAS.Muons.Analyzer import Analyzer
import ROOT
ROOT.gROOT.ProcessLine('.x tdrstyle.C')

analyzer = Analyzer()


def softID(muon,vertex):
    return muon.isSoftMuon(vertex)

def looseID(muon,vertex):
    return muon.isLooseMuon()

def tightID(muon,vertex):
    return muon.isTightMuon(vertex)

# analyzer.addSelection('softMuonSelection',softID,20,ROOT.kRed)
# analyzer.addSelection('looseMuonSelection',looseID,21,ROOT.kBlue)
# analyzer.addSelection('tightMuonSelection',tightID,22,ROOT.kBlack)


def detIso(muon,vertex):
    return (muon.isolationR03().sumPt+muon.isolationR03().emEt+muon.isolationR03().hadEt)/muon.pt()

def pfIso(muon,vertex):
    return (muon.chargedHadronIso()+muon.photonIso()+muon.neutralHadronIso())/muon.pt()

def pfdBIso(muon,vertex):
    return (muon.chargedHadronIso()+max(0,muon.photonIso()+muon.neutralHadronIso()-0.5*muon.puChargedHadronIso()))/muon.pt()

# analyzer.addMultipleSelection('detIso', detIso, 20,ROOT.kGreen,20,0,0.5)
# analyzer.addMultipleSelection('pfIso',  pfIso,  20,ROOT.kBlue, 20,0,0.5)
# analyzer.addMultipleSelection('pfdBIso',pfdBIso,20,ROOT.kRed,  20,0,0.5)

def detTkIso(muon,vertex):
    return muon.isolationR03().sumPt/muon.pt()

def pfTkIso(muon,vertex):
    return muon.chargedHadronIso()/muon.pt()

def pfAllTkIso(muon,vertex):
    return (muon.chargedHadronIso()+muon.puChargedHadronIso())/muon.pt()

# analyzer.addMultipleSelection('detTkIso',  detTkIso,  20,ROOT.kGreen,20,0,0.5)
# analyzer.addMultipleSelection('pfTkIso',   pfTkIso,   20,ROOT.kBlue, 20,0,0.5)
# analyzer.addMultipleSelection('pfAllTkIso',pfAllTkIso,20,ROOT.kRed,  20,0,0.5)

# Calculate Significance :: this did not work ...
# analyzer.addSelection('tightMuonSelection',tightID,22,ROOT.kBlack)
# analyzer.addMultipleSelection('pfIso',  pfIso,  20,ROOT.kBlue, 20,0,0.5)
# analyzer.addMultipleSelection('pfdBIso',pfdBIso,20,ROOT.kRed,  20,0,0.5)
# analyzer.calculateSignificance(10,500)

def mySelTightPFdBIso(muon,vertex):
    return (muon.isTightMuon(vertex) and ((muon.chargedHadronIso()+max(0,muon.photonIso()+muon.neutralHadronIso()-0.5*muon.puChargedHadronIso()))/muon.pt() < 0.1))
def mySelTightPFIso(muon,vertex):
    return (muon.isTightMuon(vertex) and ((muon.chargedHadronIso()+muon.photonIso()+muon.neutralHadronIso())/muon.pt() < 0.1))
def mySelTightDetIso(muon,vertex):
    return (muon.isTightMuon(vertex) and ((muon.isolationR03().sumPt+muon.isolationR03().emEt+muon.isolationR03().hadEt)/muon.pt() < 0.1))

# analyzer.addSelection('tightID_PFdBIso',mySelTightPFdBIso,20,ROOT.kBlack)
# analyzer.addSelection('tightID_PFIso',  mySelTightPFIso,  20,ROOT.kBlack)
analyzer.addSelection('tightID_DetIso', mySelTightDetIso, 20,ROOT.kBlack)

analyzer.run()
canvas,g=analyzer.summarize()
canvas.Update()


