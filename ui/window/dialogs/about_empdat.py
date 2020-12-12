from tkinter.ttk import Label, Button

from ui.window import TkinterDialog

_LICENSES = """
 Name                           Version     License                                            
 Babel                          2.9.0       BSD License                                        
 Pillow                         8.0.1       Historical Permission Notice and Disclaimer (HPND) 
 SQLAlchemy                     1.3.20      MIT License                                        
 altgraph                       0.17        MIT License                                        
 astroid                        2.4.2       LGPL                                               
 colorama                       0.4.4       BSD License                                        
 dictdiffer                     0.8.1       MIT License                                        
 future                         0.18.2      MIT License                                        
 isort                          5.6.4       MIT License                                        
 lazy-object-proxy              1.4.3       BSD License                                        
 mccabe                         0.6.1       MIT License                                        
 numpy                          1.19.3      BSD                                                
 pdfkit                         0.6.1       MIT                                                
 pefile                         2019.4.18   UNKNOWN                                            
 pyfaker                        0.1         MIT                                                
 pyinstaller                    4.1         GNU General Public License v2 (GPLv2)              
 pyinstaller-hooks-contrib      2020.10     UNKNOWN                                            
 pylint                         2.6.0       GNU General Public License (GPL)                   
 pytz                           2020.4      MIT License                                        
 pywin32-ctypes                 0.2.0       BSD                                                
 six                            1.15.0      MIT License                                        
 tkcalendar                     1.6.1       GNU General Public License v3 (GPLv3)              
 tkintertable                   1.3.2       GNU General Public License v3 (GPLv3)              
 toml                           0.10.2      MIT License                                        
 ttkthemes                      3.2.0       GNU General Public License v3 (GPLv3)              
 typed-ast                      1.4.1       Apache License 2.0                                 
 wrapt                          1.12.1      BSD License                                        
"""


class AboutEmpDatDialog(TkinterDialog):

    def __init__(self):
        super().__init__({})

        self.title('About EmpDat')

        Label(self, text="EmpDat").pack()
        Label(self, text="-------").pack()
        Label(self, text="Team 2 - CS 2450-001 Fall2020").pack()
        Label(self, text="Kevin Thorne, Tanner Olsen, Kim Soto, "
                         "Luke Barrett, Caleb Probst, Colton Robbins, Joshua Ley").pack()

        Label(self, text="-------").pack()
        Label(self, text="Libraries and Attributions:").pack()
        Label(self, text=_LICENSES).pack()

        Button(self, text="Close", command=self.destroy).pack()
