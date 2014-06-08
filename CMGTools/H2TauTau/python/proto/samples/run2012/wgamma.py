import CMGTools.RootTools.fwlite.Config as cfg
# from CMGTools.H2TauTau.proto.samples.sampleShift import sampleShift

WgammaInc = cfg.MCComponent(
    name = 'WgammaInc',
    files = [],
    xSection = 553.92,
    nGenEvents = 1,
    triggers = [],
    effCorrFactor = 1 )

Wgammaee = cfg.MCComponent(
    name = 'Wgammaee',
    files = [],
    xSection = 5.873,
    nGenEvents = 1,
    triggers = [],
    effCorrFactor = 1 )


mc_wgamma = [
    WgammaInc,
    Wgammaee
    ]


