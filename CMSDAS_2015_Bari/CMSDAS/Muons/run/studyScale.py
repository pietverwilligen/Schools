from CMSDAS.Muons.Analyzer import Analyzer
import ROOT
ROOT.gROOT.ProcessLine('.x tdrstyle.C')

analyzer = Analyzer()

# declare plots here like this:
zMassU = ROOT.TH1F("zMassU","",50,80,120)
zMassC = ROOT.TH1F("zMassC","",50,80,120)

zDiffU = ROOT.TH1F("zDiffU","",50,-15,15)
zDiffC = ROOT.TH1F("zDiffC","",50,-15,15)



hprofPos  = ROOT.TProfile("hprofPos","",100,-3.1415,3.1415,-20,20);
hprofNeg  = ROOT.TProfile("hprofNeg","",100,-3.1415,3.1415,-20,20);



#Put the analysis code in the method below .
#The inputs are TLorentzVectors
def fillPlots(muPos,muNeg,muPosCorrected,muNegCorrected):
    # difference of reconstructed mass with pdg mass
    zDiffU.Fill((muPos+muNeg).M()-91.1876)
    zDiffC.Fill((muPosCorrected+muNegCorrected).M()-91.1876)
    # reconstructed mass
    zMassU.Fill((muPos+muNeg).M())
    zMassC.Fill((muPosCorrected+muNegCorrected).M())
    # 1/pt - 1/ptcorr vs phi
    hprofPos.Fill(muPos.Phi(),1/muPos.Pt()-1/muPosCorrected.Pt())
    hprofNeg.Fill(muNeg.Phi(),1/muNeg.Pt()-1/muNegCorrected.Pt())


analyzer.processFunc = fillPlots
analyzer.run()



