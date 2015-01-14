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

czDiff = ROOT.TCanvas("czDiff","czDiff",600,600)
legend=ROOT.TLegend(0.6,0.6,0.95,0.85)
legend.SetFillColor(0)
legend.SetLineColor(0)
legend.SetTextSize(0.02);
#legend.SetHeader("GE1/1, p_{T} = 200 GeV/c")
zDiffU.SetLineColor(1) # UNCORRECTED muons in BLACK
zDiffU.SetMarkerColor(1) # UNCORRECTED muons in BLACK
zDiffU.GetXaxis().SetTitle("m_{#mu#mu} - m_{#mu#mu}^{PDG} [GeV/c^{2}]")
width = zDiffU.GetBinWidth(1)
zDiffU.GetYaxis().SetTitle("Entries/" + str(round(width,2)) + " GeV/c^{2}")
zDiffU.GetXaxis().SetTitleOffset(1.7);
zDiffU.GetYaxis().SetTitleOffset(2.0);
zDiffU.GetYaxis().SetTitleSize(0.04);
zDiffU.GetXaxis().SetTitleSize(0.04);
zDiffU.Draw("histe1")
zDiffC.SetLineColor(2) # CORRECTED muons in RED
zDiffC.SetMarkerColor(2) # CORRECTED muons in RED
zDiffC.Draw("histsamee1")
legend.AddEntry(zDiffU, "Uncorrected, Mean: "+str(round(zDiffU.GetMean(),2))+"GeV/c^{2}", "pl")
legend.AddEntry(zDiffC, "Corrected, Mean: "+str(round(zDiffC.GetMean(),2))+"GeV/c^{2}", "pl")
legend.Draw("same")
czDiff.Update()
czDiff.SaveAs("diffMass.png")

chprof = ROOT.TCanvas("chprof","chprof",600,600)
#chprof.Divide(2,1)
#chprof.cd(1)
hprofPos.GetXaxis().SetTitle("#phi [rad]")
hprofPos.GetYaxis().SetTitle("< 1/p_{T} - 1/p_{T,corr} > [1/GeV/c]")
hprofPos.GetXaxis().SetTitleOffset(1.7);
hprofPos.GetYaxis().SetTitleOffset(1.8);
hprofPos.GetYaxis().SetTitleSize(0.04);
hprofPos.GetXaxis().SetTitleSize(0.04);
hprofPos.Draw()
#chprof.cd(2)
#hprofNeg.GetXaxis().SetTitle("#phi [rad]")
#hprofNeg.GetYaxis().SetTitle("< 1/p_{T} - 1/p_{T,corr} > [1/GeV/c]")
#hprofNeg.GetXaxis().SetTitleOffset(1.7);
#hprofNeg.GetYaxis().SetTitleOffset(2.0);
#hprofNeg.GetYaxis().SetTitleSize(0.04);
#hprofNeg.GetXaxis().SetTitleSize(0.04);
#hprofNeg.Draw()
chprof.Update()
chprof.SaveAs("invPt.png")
