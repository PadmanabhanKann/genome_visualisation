#!/usr/bin/env python3

import sys
import re

if __name__ == "__main__":
    # Check if the input file argument was provided
    if len(sys.argv) < 2:
        print("Usage: python script1.py <input_file> <genome_length>" )
        sys.exit(1)
 # Get the input file from the command-line argument
    input_file = sys.argv[1]
    genome_length = int(sys.argv[2])
    seq_id = sys.argv[3]





with open('genome.html', 'w') as file:
    file.write(f'''<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>NGCircos.js</title>
    </head>
    <body>
        
         <script src="lib/jquery.js"></script>
        <script src="lib/d3.js"></script>
        <script src="lib/NGCircos_.js"></script>
        <script src="snp.js"></script> 
        <script src="del.js"></script>
        <script src="ins.js"></script>
        <script src="mob.js"></script>   
        <script src="amp.js"></script>
        <script src="ins.js"></script>
        <script src="inv.js"></script>
        <script src="invarc.js"></script>    
        <script src="delarc.js"></script>
        <script src="amparc.js"></script> 
        <div id="NGCircos"></div>
        
        <script>
        var BACKGROUNDSNP = [ "BACKGROUNDSNP" , {{
            BginnerRadius: 159,
            BgouterRadius: 177,
            BgFillColor: "#F2F2F2",
            BgborderColor : "#000",
            BgborderSize : 0.3
        }}];
        var BACKGROUNDDEL = [ "BACKGROUNDDEL" , {{
            BginnerRadius: 138,
            BgouterRadius: 157,
            BgFillColor: "#F2F2F2",
            BgborderColor : "#000",
            BgborderSize : 0.3
        }}];
        var BACKGROUNDAMP = [ "BACKGROUNDAMP" , {{
            BginnerRadius: 179,
            BgouterRadius: 197,
            BgFillColor: "#F2F2F2",
            BgborderColor : "#000",
            BgborderSize : 0.3
        }}];
        var BACKGROUNDINS = [ "BACKGROUNDINS" , {{
            BginnerRadius: 199,
            BgouterRadius: 217,
            BgFillColor: "#F2F2F2",
            BgborderColor : "#000",
            BgborderSize : 0.3
        }}];
        </script> 
        
        <!-- Genome configuration -->
        <script>
            var NGCircosGenome = [
            [
                ["{seq_id}", {genome_length}],
            ]
            ];
            NGCircos01 = new NGCircos(SCATTER01,SCATTER02,SCATTER03,SCATTER05,SCATTER06,ARC01,ARC02,ARC03,NGCircosGenome, {{  // Initialize NG-Circos with "NGCircosGenome" and Main configuration
            //Main configuration
                target : "NGCircos",                       // Main configuration "target"
                svgWidth : 900,                             // Main configuration "svgWidth"
                svgHeight : 900,                            // Main configuration "svgHeight"
                svgClassName: "NGCircos",                  // Main configuration "svgClassName"
                chrPad : 0,                              // distance between chromosomes
                innerRadius: 300,                           // Main configuration "innerRadius"
                outerRadius: 301,
                genomeLabel: {{
                            display: false,
                            textSize: 18,       // Larger font
                            textColor: "#FF5733", // Orange color
                            dx: 0,          // Shift labels outward
                            dy: "0em" ,
                            textAnchor: "middle"  // Adjust vertical positioning
                        }},
                 ticks: {{
                        display: true,
                        len: 5,
                        color: "#000",
                        textSize: 10,
                        textColor: "#000",
                        scale: 1000000,  // Adjust this value for tick interval
                        realLength: false,
                        offset: 0,
            }},
                SNPMouseOverDisplay : true,
                SNPMouseOverColor : "blue",
                SNPMouseOverCircleSize : 5,
                SNPMouseOverCircleOpacity : 1.0,
                SNPMouseOverCircleStrokeColor : "#F26223",
                SNPMouseOverCircleStrokeWidth : 3,
                SNPMouseOverTooltipsSetting :"1",
                SNPMouseOverTooltipsHtml : " ",
                SNPMouseOverTooltipsBorderWidth : 1,
                SNPMouseOutDisplay : true,
                SNPMouseOutAnimationTime : 700,
                SNPMouseOutColor : "none",
                SNPMouseOutCircleSize : "none",
                SNPMouseOutCircleOpacity : 1.0,
                SNPMouseOutCircleStrokeWidth : 0,
                ARCMouseEvent: true,
                ARCMouseClickDisplay: true,
                ARCMouseClickColor: "red",
                ARCMouseClickArcOpacity: 1,
                ARCMouseClickArcStrokeColor: "#F26223",
                ARCMouseClickArcStrokeWidth: 0,
                ARCMouseClickTextFromData: "fifth",
                ARCMouseClickTextOpacity: 1,
                ARCMouseClickTextColor: "red",
                ARCMouseClickTextSize: 8,
                ARCMouseClickTextPostionX: 0,
                ARCMouseClickTextPostionY: 0,
                ARCMouseClickTextDrag: true,
                ARCMouseMoveDisplay: true,
                ARCMouseMoveColor: "none",
                ARCMouseMoveArcOpacity: 1,
                ARCMouseMoveArcStrokeColor: "#F26223",
                ARCMouseMoveArcStrokeWidth: 3,
                ARCMouseOutDisplay: true,
                ARCMouseOutAnimationTime: 500,
                ARCMouseOutColor: "none",
                ARCMouseOutArcOpacity: 1,
                ARCMouseOutArcStrokeColor: "red",
                ARCMouseOutArcStrokeWidth: 0,
                ARCMouseOverDisplay: true,
                ARCMouseOverColor: "none",
                ARCMouseOverArcOpacity: 1,
                ARCMouseOverArcStrokeColor: "#F26223",
                ARCMouseOverArcStrokeWidth: 3,
                SCATTERMouseEvent:true,
                SCATTERMouseClickDisplay: true,
                SCATTERMouseClickColor: "none",
                SCATTERMouseClickCircleSize: "none",
                SCATTERMouseClickCircleOpacity: 1,
                SCATTERMouseClickCircleStrokeColor: "#F26223",
                SCATTERMouseClickCircleStrokeWidth: 0,
                SCATTERMouseClickTextFromData: "fourth",
                SCATTERMouseClickTextOpacity: 1,
                SCATTERMouseClickTextColor: "red",
                SCATTERMouseClickTextSize: 8,
                SCATTERMouseClickTextPostionX: 5,
                SCATTERMouseClickTextPostionY: 15,
                SCATTERMouseClickTextDrag: true,
                SCATTERMouseOverDisplay: true,
                SCATTERMouseOverColor: "none",
                SCATTERMouseOverCircleSize: "none",
                SCATTERMouseOverCircleOpacity: 1,
                SCATTERMouseOverCircleStrokeColor: "none",
                SCATTERMouseOverCircleStrokeWidth: 0,
            
                SCATTERMouseOutDisplay: true,
                SCATTERMouseOutColor: "none",
                SCATTERMouseOutCircleSize: "none",
                SCATTERMouseOutCircleOpacity: 1,
                SCATTERMouseOutCircleStrokeColor: "none",
                SCATTERMouseOutCircleStrokeWidth: 0,
            }});
   
            NGCircos01.draw_genome(NGCircos01.genomeLength); // NG-Circos callback
            NGCircos01.draw_genome(NGCircos01.genomeLength2); // NG-Circos callback second time
           
        </script>
    </body>
    </html>
    
    ''')    



