def eleTrigScale_TauEle_2012_53X(elept, eleeta):

  if( 10.0 < elept and elept <= 15.0 ):
    if( 0.0 <= abs(eleeta) and abs(eleeta) < 0.8 ):      return 0.9548
    elif( 0.8 <= abs(eleeta) and abs(eleeta) < 1.5 ): return 0.9015
    elif( 1.5 <= abs(eleeta) ):                      return 0.9017 

  elif( 15.0 < elept and elept <= 20.0 ):		            
    if( 0.0 <= abs(eleeta) and abs(eleeta) < 0.8 ):      return 0.9830
    elif( 0.8 <= abs(eleeta) and abs(eleeta) < 1.5 ): return 0.9672
    elif( 1.5 <= abs(eleeta) ):                      return 0.9463 

  elif( 20.0 < elept and elept <= 25.0 ):		            
    if( 0.0 <= abs(eleeta) and abs(eleeta) < 0.8 ):      return 0.9707
    elif( 0.8 <= abs(eleeta) and abs(eleeta) < 1.5 ): return 0.9731
    elif( 1.5 <= abs(eleeta) ):                      return 0.9691 

  elif( 25.0 < elept and elept <= 30.0 ):		            
    if( 0.0 <= abs(eleeta) and abs(eleeta) < 0.8 ):      return 0.9768
    elif( 0.8 <= abs(eleeta) and abs(eleeta) < 1.5 ): return 0.9870
    elif( 1.5 <= abs(eleeta) ):                      return 0.9727 

  elif( 30.0 < elept and elept <= 35.0 ):		            
    if( 0.0 <= abs(eleeta) and abs(eleeta) < 0.8 ):      return 1.0047
    elif( 0.8 <= abs(eleeta) and abs(eleeta) < 1.5 ): return 0.9891
    elif( 1.5 <= abs(eleeta) ):                      return 0.9858 

  else:
    if( 0.0 <= abs(eleeta) and abs(eleeta) < 0.8 ):      return 1.0063
    elif( 0.8 <= abs(eleeta) and abs(eleeta) < 1.5 ): return 1.0047
    elif( 1.5 <= abs(eleeta) ):                      return 1.0015 

  return 0.



def eleIDscale_TauEle_2012_53X(elept, eleeta):
  if( 24.0 < elept and elept <= 30.0 ):		            
    if( 0.0 <= abs(eleeta) and abs(eleeta) < 1.479 ):      return 0.8999*0.9417
    elif( 1.479 <= abs(eleeta)):                           return 0.7945*0.9471

  elif( 30.0 < elept):		            
    if( 0.0 <= abs(eleeta) and abs(eleeta) < 1.479 ):      return 0.9486*0.9804
    elif( 1.479 <= abs(eleeta)):                           return 0.8866*0.9900


  return  0.
