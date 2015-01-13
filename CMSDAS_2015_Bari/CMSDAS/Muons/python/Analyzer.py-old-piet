from DataFormats.FWLite import Events, Handle,Lumis
import itertools
import ROOT
import os
import json
import math
ROOT.gSystem.Load("libMuScleFitCalibration")

def getFullPath(path):
    return os.environ['CMSSW_BASE']+"/src/"+path

        
class Analyzer (object):
    def __init__(self):
        self.vertexHandle  = Handle ('std::vector<reco::Vertex>')
        self.muonHandle    = Handle('std::vector<pat::Muon>')
        self.selections    = {}
        self.signal        = 0 # total amount of signal events
        self.background    = 0 # total amount of background events
        self.corrector     = ROOT.MuScleFitCorrector(getFullPath("MuScleFit/Calibration/data/MuScleFit_2012D_DATA_53X.txt"))
#        self.corrector = ROOT.rochcor2012()
#        self.corrector = ROOT.MuScleFitCorrector(getFullPath("MuScleFit/Calibration/data/MuScleFit_2012ABC_DATA_53X.txt"))
        self.processFunc = None

        self.histograms    = {}
        self.histograms['pt']  = {}
        self.histograms['eta'] = {}

        self.histograms['pt']['mu2_sign_all'] = ROOT.TH1F("mu2_pt_sign_all", "mu2_pt_sign_all", 40, 20, 100)
        self.histograms['pt']['mu2_sign_sel'] = ROOT.TH1F("mu2_pt_sign_sel", "mu2_pt_sign_sel", 40, 20, 100)
        self.histograms['pt']['mu2_sign_eff'] = ROOT.TH1F("mu2_pt_sign_eff", "mu2_pt_sign_eff", 40, 20, 100)
        self.histograms['pt']['mu2_back_all'] = ROOT.TH1F("mu2_pt_back_all", "mu2_pt_back_all", 40, 20, 100)
        self.histograms['pt']['mu2_back_sel'] = ROOT.TH1F("mu2_pt_back_sel", "mu2_pt_back_sel", 40, 20, 100)
        self.histograms['pt']['mu2_back_eff'] = ROOT.TH1F("mu2_pt_back_eff", "mu2_pt_back_eff", 40, 20, 100)
        self.histograms['eta']['mu2_sign_all'] = ROOT.TH1F("mu2_eta_sign_all", "mu2_eta_sign_all", 50, -2.5, 2.5)
        self.histograms['eta']['mu2_sign_sel'] = ROOT.TH1F("mu2_eta_sign_sel", "mu2_eta_sign_sel", 50, -2.5, 2.5)
        self.histograms['eta']['mu2_sign_eff'] = ROOT.TH1F("mu2_eta_sign_eff", "mu2_eta_sign_eff", 50, -2.5, 2.5)
        self.histograms['eta']['mu2_back_all'] = ROOT.TH1F("mu2_eta_back_all", "mu2_eta_back_all", 50, -2.5, 2.5)
        self.histograms['eta']['mu2_back_sel'] = ROOT.TH1F("mu2_eta_back_sel", "mu2_eta_back_sel", 50, -2.5, 2.5)
        self.histograms['eta']['mu2_back_eff'] = ROOT.TH1F("mu2_eta_back_eff", "mu2_eta_back_eff", 50, -2.5, 2.5)


        
    def readCollections(self,event):
        event.getByLabel('offlinePrimaryVertices',self.vertexHandle)
        event.getByLabel('selectedPatMuons',self.muonHandle)
        self.muons = self.muonHandle.product()         # take all muons
        self.vertex = self.vertexHandle.product()[0]   # take only Primary Vertex


    def addSelection(self,name,selection,markerStyle,markerColor):
        self.selections[name] = {'function':selection,'style':markerStyle,'color':markerColor,'signal':0.0,'background':0.0,'value':-1}

    def addMultipleSelection(self,name,selection,markerStyle,markerColor,points,min,max):
        offset = float(max-min)/points
        for i in range(0,points):
            self.selections[name+'_'+str(i*offset)] = {'function':selection,'style':markerStyle,'color':markerColor,'signal':0.0,'background':0.0,'value':i*offset}

    def analyze(self):

        for mu1,mu2 in itertools.combinations(self.muons,2):
            # signal selection
            # ----------------
            if mu1.isTightMuon(self.vertex) and \
               mu1.pt()>20 and mu2.pt()>20 and \
               mu1.chargedHadronIso()<0.15 and \
               mu1.charge()+mu2.charge() ==0 and \
               (mu1.p4()+mu2.p4()).M()>80 and (mu1.p4()+mu2.p4()).M()<120.:
                self.signal=self.signal+1
                
                # Fill Plots
                self.histograms['pt']['mu2_sign_all'].Fill(mu2.pt())
                self.histograms['eta']['mu2_sign_all'].Fill(mu2.eta())

                # Momentum Scale Corrections
                if self.processFunc is not None and mu2.isTightMuon(self.vertex) and mu2.chargedHadronIso()/mu2.pt()<0.1:
                    # correct momentum scale
                    vector1 = ROOT.TLorentzVector(mu1.px(),mu1.py(),mu1.pz(),mu1.energy())
                    vector2 = ROOT.TLorentzVector(mu2.px(),mu2.py(),mu2.pz(),mu2.energy())
                    vectorC1 = ROOT.TLorentzVector(mu1.px(),mu1.py(),mu1.pz(),mu1.energy())
                    vectorC2 = ROOT.TLorentzVector(mu2.px(),mu2.py(),mu2.pz(),mu2.energy())
                    self.corrector.applyPtCorrection(vectorC1,mu1.charge())
                    self.corrector.applyPtCorrection(vectorC2,mu2.charge())
#                    self.corrector.momcor_data(vectorC1, mu1.charge(), 1);
#                    self.corrector.momcor_data(vectorC2, mu1.charge(), 1);
                    if mu1.charge()>0:
                        self.processFunc(vector1,vector2,vectorC1,vectorC2)
                    else:
                        self.processFunc(vector2,vector1,vectorC2,vectorC1)

                # check whether second muon (mu2) passes additional selection cuts (ID, ISO, ...)
                for name,selection in self.selections.iteritems():
                    if selection['value']<0:
                        if selection['function'](mu2,self.vertex):
                            selection['signal'] = selection['signal']+1
                            self.histograms['pt']['mu2_sign_sel'].Fill(mu2.pt())
                            self.histograms['eta']['mu2_sign_sel'].Fill(mu2.eta())
                    else:        
                        if selection['function'](mu2,self.vertex)<selection['value']:
                            selection['signal'] = selection['signal']+1
                            self.histograms['pt']['mu2_sign_sel'].Fill(mu2.pt())
                            self.histograms['eta']['mu2_sign_sel'].Fill(mu2.eta())

            # background selection
            # --------------------                
            if mu1.pt()>20 and mu2.pt()>20  \
               and mu1.chargedHadronIso()>5.0 and (mu1.p4()+mu2.p4()).M()<80. \
               and mu1.charge()+mu2.charge() !=0 :
                self.background=self.background+1
                self.histograms['pt']['mu2_back_all'].Fill(mu2.pt())
                self.histograms['eta']['mu2_back_all'].Fill(mu2.eta())
                # check whether second muon (mu2) passes additional selection cuts (ID, ISO, ...)
                for name,selection in self.selections.iteritems():
                    if selection['value']<0:
                        if selection['function'](mu2,self.vertex):
                            selection['background'] = selection['background']+1
                            self.histograms['pt']['mu2_back_sel'].Fill(mu2.pt())
                            self.histograms['eta']['mu2_back_sel'].Fill(mu2.eta())
                    else:        
                        if selection['function'](mu2,self.vertex)<selection['value']:
                            selection['background'] = selection['background']+1
                            self.histograms['pt']['mu2_back_sel'].Fill(mu2.pt())
                            self.histograms['eta']['mu2_back_sel'].Fill(mu2.eta())


    def summarize(self):
        graphs=[]
        c = ROOT.TCanvas("c")
        h = c.DrawFrame(0.0,0.0,1.0,1.0)
        h.GetXaxis().SetTitle("background fraction passing selection")
        h.GetYaxis().SetTitle("signal fraction passing selection")
        graphs.append(h)
        for name,selection in self.selections.iteritems():
            selection['signal'] = selection['signal']/self.signal
            selection['background'] = selection['background']/self.background
            print 'Selection:'+str(name),'Signal (%):'+str( selection['signal']),'background (%):'+str( selection['background'])
            g=ROOT.TGraph()
            g.SetName(name+'g')
            g.SetPoint(0,selection['background'],selection['signal'])
            g.SetMarkerColor(selection['color'])
            g.SetMarkerStyle(selection['style'])
            g.Draw("Psame")
            graphs.append(g)
        c.Draw()
        return c,graphs

    def prepareHisto(self,variable,histoname,scale,style,color):
        # print "prepareHisto :: arg = "+str(histoname)+str(scale)+str(style)+str(color)
        self.histograms[variable][histoname].Scale(scale)
        self.histograms[variable][histoname].SetMarkerStyle(style)
        self.histograms[variable][histoname].SetMarkerColor(color)

    def plotHistos(self, variable, axislabel, xmin, xmax):
        graphs=[]
        c = ROOT.TCanvas("c")

        h = c.DrawFrame(xmin, 0.0, xmax, 100.0)                                                                                                                                                                                                           
        h.GetXaxis().SetTitle(axislabel)
        h.GetYaxis().SetTitle("a.u.")
        graphs.append(h)

        # c.Divide(1,2)
        # c.cd(1)
        # p1 = ROOT.TPad(c.GetPad(1))
        # h1 = p1.DrawFrame(xmin, 0.0, xmax, 100.0)
        # h1.GetXaxis().SetTitle(axislabel)
        # h1.GetYaxis().SetTitle("a.u.")
        # p2 = ROOT.TPad(c.GetPad(2))
        # h2 = p2.DrawFrame(xmin, 0.0, xmax, 100.0)
        # h2.GetXaxis().SetTitle(axislabel)
        # h2.GetYaxis().SetTitle("Eff")
        # graphs.append(h1)
        # graphs.append(h2)

        self.prepareHisto(variable,'mu2_sign_all',100.0/self.signal,20,ROOT.kRed)
        self.prepareHisto(variable,'mu2_sign_sel',100.0/self.signal,24,ROOT.kRed)
        self.prepareHisto(variable,'mu2_back_all',100.0/self.signal,20,ROOT.kBlue)
        self.prepareHisto(variable,'mu2_back_sel',100.0/self.signal,24,ROOT.kBlue)

        self.histograms[variable]['mu2_sign_all'].Draw("APsame")
        self.histograms[variable]['mu2_sign_sel'].Draw("Psame")
        self.histograms[variable]['mu2_back_all'].Draw("Psame")
        self.histograms[variable]['mu2_back_sel'].Draw("Psame")

        graphs.append(self.histograms[variable]['mu2_sign_all'])
        graphs.append(self.histograms[variable]['mu2_sign_sel'])
        graphs.append(self.histograms[variable]['mu2_back_all'])
        graphs.append(self.histograms[variable]['mu2_back_sel'])

        # c.Draw()
        # canvasratio = float(0.2)
        # c.SetBottomMargin(canvasratio + (1-canvasratio)*c.GetBottomMargin()-canvasratio*c.GetTopMargin())
        # r = ROOT.TPad("r","",0,0,1,1)
        # r.SetTopMargin((1-canvasratio) - (1-canvasratio)*r.GetBottomMargin()+canvasratio*r.GetTopMargin())
        # r.SetTicks(1,1)
        # r.Draw()
        # r.cd()

        # c.cd(2)
        self.histograms[variable]['mu2_sign_eff'].Divide(self.histograms[variable]['mu2_sign_sel'], self.histograms[variable]['mu2_sign_all'], 1, 1, "")
        self.histograms[variable]['mu2_back_eff'].Divide(self.histograms[variable]['mu2_back_sel'], self.histograms[variable]['mu2_back_all'], 1, 1, "")

        self.prepareHisto(variable,'mu2_sign_eff',100.0,28,ROOT.kRed)
        self.prepareHisto(variable,'mu2_back_eff',100.0,28,ROOT.kBlue)

        self.histograms[variable]['mu2_sign_eff'].Draw("Psame")
        self.histograms[variable]['mu2_back_eff'].Draw("Psame")
        graphs.append(self.histograms[variable]['mu2_sign_eff'])
        graphs.append(self.histograms[variable]['mu2_back_eff'])

        c.Update()
        return c,graphs

    def calculateSignificance(self,s,b):
        for name,selection in self.selections.iteritems():
            if selection['background']>0:
                value = selection['signal']*s/math.sqrt(selection['background']*b)
                print 'Selection:'+str(name),'s/sqrt(b):'+str(value)
            else:
                print 'Selection:'+str(name),'background is zero , signal is :'+str(selection['signal']*s)
                

    def run(self):
        files =[
         # 'root://eoscms//eos/cms//store/cmst3/group/das2014/Muons/input2.root' # at CERN
         '/data/shared/Short_Exercise_Muon/input2.root'                          # at BARI
            ]
        events=Events(files)
        for event in events:
            if self.processFunc is None and self.background>2500:
                break
            self.readCollections(event)
            self.analyze()

