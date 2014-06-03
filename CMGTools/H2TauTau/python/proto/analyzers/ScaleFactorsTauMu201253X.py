def muTrigScale_TauMu_2012_53X(mupt, mueta):

  if( 10.0 < mupt and mupt <= 15.0 ):
    if( 0.0 <= abs(mueta) and abs(mueta) < 0.8):    return 0.9829
    elif( 0.8 <= abs(mueta) and abs(mueta) < 1.2 ): return 0.9745
    elif( 1.2 <= abs(mueta) and abs(mueta) < 1.6 ): return 0.9943
    elif( 1.6 <= abs(mueta) ):                      return 0.9158
    
  elif( 15.0 < mupt and mupt <= 20.0 ):
    if( 0.0 <= abs(mueta) and abs(mueta) < 0.8 ):   return 0.9850
    elif( 0.8 <= abs(mueta) and abs(mueta) < 1.2 ): return 0.9852
    elif( 1.2 <= abs(mueta) and abs(mueta) < 1.6 ): return 0.9743
    elif( 1.6 <= abs(mueta) ):                      return 0.9333 

  elif( 20.0 < mupt and mupt <= 25.0 ):		          
    if( 0.0 <= abs(mueta) and abs(mueta) < 0.8 ):   return 0.9951
    elif( 0.8 <= abs(mueta) and abs(mueta) < 1.2 ): return 0.9610
    elif( 1.2 <= abs(mueta) and abs(mueta) < 1.6 ): return 0.9716
    elif( 1.6 <= abs(mueta) ):                      return 0.9459 

  elif( 25.0 < mupt and mupt <= 30.0 ):		          
    if( 0.0 <= abs(mueta) and abs(mueta) < 0.8 ):   return 0.9869
    elif( 0.8 <= abs(mueta) and abs(mueta) < 1.2 ): return 0.9779
    elif( 1.2 <= abs(mueta) and abs(mueta) < 1.6 ): return 0.9665
    elif( 1.6 <= abs(mueta) ):                      return 0.9501 

  elif( 30.0 < mupt and mupt <= 35.0 ):		          
    if( 0.0 <= abs(mueta) and abs(mueta) < 0.8 ):   return 0.9959
    elif( 0.8 <= abs(mueta) and abs(mueta) < 1.2 ): return 0.9881
    elif( 1.2 <= abs(mueta) and abs(mueta) < 1.6 ): return 0.9932
    elif( 1.6 <= abs(mueta) ):                      return 0.9391 

  else:							          
    if( 0.0 <= abs(mueta) and abs(mueta) < 0.8 ):   return 0.9986
    elif( 0.8 <= abs(mueta) and abs(mueta) < 1.2 ): return 0.9540
    elif( 1.2 <= abs(mueta) and abs(mueta) < 1.6 ): return 0.9549
    elif( 1.6 <= abs(mueta) ):                      return 0.9386 

  return 0.



def muIDscale_TauMu_2012_53X(mupt, mueta):
  if( 20.0 < mupt and mupt <= 30.0 ):		           
    if( 0.0 <= abs(mueta) and abs(mueta) < 0.8 ):       return 0.9818*0.9494
    elif( 0.8 <= abs(mueta) and abs(mueta) < 1.2 ):  return 0.9828*0.9835
    elif( 1.2 <= abs(mueta) and abs(mueta) < 2.1 ):  return 0.9869*0.9923
    
  elif( 30.0 < mupt ):
    if ( 0.0 <= abs(mueta) and abs(mueta) < 0.8 ):      return 0.9852*0.9883
    elif( 0.8 <= abs(mueta) and abs(mueta) < 1.2 ):  return 0.9852*0.9937
    elif( 1.2 <= abs(mueta) and abs(mueta) < 2.1 ):  return 0.9884*0.9996

  return 0.

