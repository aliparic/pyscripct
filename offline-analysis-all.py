
import os
import sys

"""
Offline analysis by replaying logs
"""

#Import MobileInsight modules
from mobile_insight.monitor import OfflineReplayer
from mobile_insight.analyzer import MsgLogger, LteRrcAnalyzer,WcdmaRrcAnalyzer,LteNasAnalyzer,UmtsNasAnalyzer,MmAnalyzer

if __name__ == "__main__":

     # Initialize the 3G/4G monitor for offline analysis. It "replays" the log previously captured
     path_to_mi2log = './'
     mi_files = [pos_mi for pos_mi in os.listdir(path_to_mi2log) if pos_mi.endswith('.mi2log')]
  

     for index,mi_file in enumerate(mi_files):
       
     
         src = OfflineReplayer()
         src.set_input_path(mi_file)

         # Save the decoded messages extracted from the log
         logger = MsgLogger()
         logger.set_decode_format(MsgLogger.XML)
         logger.set_dump_type(MsgLogger.FILE_ONLY)
         logger.save_decoded_msg_as("./%s.xml" %mi_file)
         logger.set_source(src)
                                            
         #Analyzers. Use them according to technology in your logs
         # RRC analyzer for both LTE and UMTS
         src.enable_log_all() 
        # lte_rrc_analyzer.set_source(src) #bind with the monitor
                                                                
        # lte_nas_analyzer = LteNasAnalyzer()
        # lte_nas_analyzer.set_source(src)

        # umts_nas_analyzer = UmtsNasAnalyzer()
        # umts_nas_analyzer.set_source(src)
                                                                                   
        # wcdma_rrc_analyzer = WcdmaRrcAnalyzer()
        # wcdma_rrc_analyzer.set_source(src) #bind with the monitor
                                                                                            
       #Start the monitoring
         src.run()
