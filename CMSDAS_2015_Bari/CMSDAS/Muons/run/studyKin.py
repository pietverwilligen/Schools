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

# def detIso(muon,vertex):
#     return (muon.isolationR03().sumPt+muon.isolationR03().emEt+muon.isolationR03().hadEt)/muon.pt()

analyzer.addSelection('tightMuonSelection',tightID,22,ROOT.kBlack)



# declare plots here like this:
signDiMuMassBeforeCut = ROOT.TH1F("signDiMuMassBeforeCut","",120, 0,120)
signDiMuMassAfterCut  = ROOT.TH1F("signDiMuMassAfterCut", "",120, 0,120)
backDiMuMassBeforeCut = ROOT.TH1F("backDiMuMassBeforeCut","",120, 0,120)
backDiMuMassAfterCut  = ROOT.TH1F("backDiMuMassAfterCut", "",120, 0,120)

signPtBeforeCut = ROOT.TH1F("signMuPtBeforeCut","",120, 0,120)
signPtAfterCut  = ROOT.TH1F("signMuPtAfterCut", "",120, 0,120)
backPtBeforeCut = ROOT.TH1F("backMuPtBeforeCut","",120, 0,120)
backPtAfterCut  = ROOT.TH1F("backMuPtAfterCut", "",120, 0,120)





# By writing your analysis code here it will be plugged into the analyzer
# at the appropriate place 
def fillSignalPlotsBeforeCut(mu2Pt, mu2Eta, mu2Phi, mu2Charge, invMass):
    signDiMuMassBeforeCut.Fill(invMass)
    signPtBeforeCut.Fill(mu2Pt)

def fillSignalPlotsAfterCut(mu2Pt, mu2Eta, mu2Phi, mu2Charge, invMass):
    signDiMuMassAfterCut.Fill(invMass)
    signPtAfterCut.Fill(mu2Pt)

def fillBackgroundPlotsBeforeCut(mu2Pt, mu2Eta, mu2Phi, mu2Charge, invMass):
    backDiMuMassBeforeCut.Fill(invMass)
    backPtBeforeCut.Fill(mu2Pt)

def fillBackgroundPlotsAfterCut(mu2Pt, mu2Eta, mu2Phi, mu2Charge, invMass):
    backDiMuMassAfterCut.Fill(invMass)
    backPtAfterCut.Fill(mu2Pt)


# assign the void functions in the analyzer with the functions you created here above
analyzer.signPlotBeforeCut = fillSignalPlotsBeforeCut
analyzer.signPlotAfterCut  = fillSignalPlotsAfterCut
analyzer.backPlotBeforeCut = fillBackgroundPlotsBeforeCut
analyzer.backPlotAfterCut  = fillBackgroundPlotsAfterCut

# run the analyzer
analyzer.run()

# make a nice plot

signDiMuMassBeforeCut.SetMarkerStyle(20)
signDiMuMassBeforeCut.SetMarkerColor(ROOT.kRed)  
signDiMuMassAfterCut.SetMarkerStyle(24)
signDiMuMassAfterCut.SetMarkerColor(ROOT.kRed)  
backDiMuMassBeforeCut.SetMarkerStyle(20)
backDiMuMassBeforeCut.SetMarkerColor(ROOT.kBlue)  
backDiMuMassAfterCut.SetMarkerStyle(24)
backDiMuMassAfterCut.SetMarkerColor(ROOT.kBlue)  

c = ROOT.TCanvas("c","c",800,600)
c.Divide(1,2)
c.cd(1)
signDiMuMassBeforeCut.Draw("P")
signDiMuMassAfterCut.Draw("Psame")
backDiMuMassBeforeCut.Draw("Psame")
backDiMuMassAfterCut.Draw("Psame")
c.Update()

signMuPtBeforeCut.SetMarkerStyle(20)
signMuPtBeforeCut.SetMarkerColor(ROOT.kRed)  
signMuPtAfterCut.SetMarkerStyle(24)
signMuPtAfterCut.SetMarkerColor(ROOT.kRed)  
backMuPtBeforeCut.SetMarkerStyle(20)
backMuPtBeforeCut.SetMarkerColor(ROOT.kBlue)  
backMuPtAfterCut.SetMarkerStyle(24)
backMuPtAfterCut.SetMarkerColor(ROOT.kBlue)  


c.cd(2)
signMuPtBeforeCut.Draw("P")
signMuPtAfterCut.Draw("Psame")
backMuPtBeforeCut.Draw("Psame")
backMuPtAfterCut.Draw("Psame")
c.Update()
