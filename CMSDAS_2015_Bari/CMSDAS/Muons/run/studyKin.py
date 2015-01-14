from CMSDAS.Muons.Analyzer import Analyzer
import ROOT
ROOT.gROOT.ProcessLine('.x tdrstyle.C')

analyzer = Analyzer()

# Make your selection here

def softID(muon,vertex):
    return muon.isSoftMuon(vertex)

def looseID(muon,vertex):
    return muon.isLooseMuon()

def tightID(muon,vertex):
    return muon.isTightMuon(vertex)

def detIso(muon,vertex):
    return (muon.isolationR03().sumPt+muon.isolationR03().emEt+muon.isolationR03().hadEt)/muon.pt()<0.25

# analyzer.addSelection('tightMuonSelection',tightID,22,ROOT.kBlack)
analyzer.addSelection('DetectorIsolation',detIso,22,ROOT.kBlack)



# declare plots here like this:
signMuPtBeforeCut = ROOT.TH1F("signMuPtBeforeCut","",100, 0,100)
backMuPtBeforeCut = ROOT.TH1F("backMuPtBeforeCut","",100, 0,100)

signMuPtAfterCut  = ROOT.TH1F("signMuPtAfterCut", "",100, 0,100)
backMuPtAfterCut  = ROOT.TH1F("backMuPtAfterCut", "",100, 0,100)
signMuPtEffCut    = ROOT.TH1F("signMuPtEffCut"  , "",100, 0,100)
backMuPtEffCut    = ROOT.TH1F("backMuPtEffCut"  , "",100, 0,100)




# By writing your analysis code here it will be plugged into the analyzer
# at the appropriate place 
def fillSignalPlotsBeforeCut(mu2Pt, mu2Eta, mu2Phi, mu2Charge, invMass):
    signMuPtBeforeCut.Fill(mu2Pt)

def fillSignalPlotsAfterCut(mu2Pt, mu2Eta, mu2Phi, mu2Charge, invMass):
    signMuPtAfterCut.Fill(mu2Pt)

def fillBackgroundPlotsBeforeCut(mu2Pt, mu2Eta, mu2Phi, mu2Charge, invMass):
    backMuPtBeforeCut.Fill(mu2Pt)

def fillBackgroundPlotsAfterCut(mu2Pt, mu2Eta, mu2Phi, mu2Charge, invMass):
    backMuPtAfterCut.Fill(mu2Pt)


# assign the void functions in the analyzer with the functions you created here above
analyzer.signPlotBeforeCut = fillSignalPlotsBeforeCut
analyzer.signPlotAfterCut  = fillSignalPlotsAfterCut
analyzer.backPlotBeforeCut = fillBackgroundPlotsBeforeCut
analyzer.backPlotAfterCut  = fillBackgroundPlotsAfterCut

# run the analyzer
analyzer.run()

# make a nice plot
signMuPtBeforeCut.SetMarkerStyle(20)
signMuPtBeforeCut.SetMarkerColor(ROOT.kRed)  
signMuPtAfterCut.SetMarkerStyle(24)
signMuPtAfterCut.SetMarkerColor(ROOT.kRed)  
backMuPtBeforeCut.SetMarkerStyle(20)
backMuPtBeforeCut.SetMarkerColor(ROOT.kBlue)  
backMuPtAfterCut.SetMarkerStyle(24)
backMuPtAfterCut.SetMarkerColor(ROOT.kBlue)  

signMuPtEffCut.Divide(signMuPtAfterCut,signMuPtBeforeCut,1,1,"")
backMuPtEffCut.Divide(backMuPtAfterCut,backMuPtBeforeCut,1,1,"")
signMuPtEffCut.SetMarkerStyle(28)
signMuPtEffCut.SetMarkerColor(ROOT.kRed)  
backMuPtEffCut.SetMarkerStyle(28)
backMuPtEffCut.SetMarkerColor(ROOT.kBlue)  


c = ROOT.TCanvas("c","c",800,600)
c.Divide(2,1)
c.cd(1)
signMuPtBeforeCut.Draw("P")
signMuPtAfterCut.Draw("Psame")
backMuPtBeforeCut.Draw("Psame")
backMuPtAfterCut.Draw("Psame")
c.Update()
c.cd(2)
signMuPtEffCut.Draw("P")
backMuPtEffCut.Draw("Psame")
c.Update()
