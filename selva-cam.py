import cadquery as cq

d_exterior_acople = 2*25.4
h_acople = 40
espesor_acople = 3
d_interior_acople = d_exterior_acople - 2*espesor_acople

lado_foto = 50
borde_foto = 8
margen_foto = 3
alto_base = 3
alto_cubre = alto_base
alto_papel = 1
borde_agarre = 5
bisel = 1
espesor_abrazadera = 2

largo_base = 2*lado_foto+3*borde_foto
ancho_base = lado_foto+2*borde_foto+2*borde_agarre

def base():
    yMuesca = ancho_base/2-borde_agarre
    return(cq.Workplane()
             .rect(largo_base,ancho_base)
             .extrude(alto_base)
             .edges("|X")
             .chamfer(bisel)
             .faces("<X")
             .workplane()
             .pushPoints(((yMuesca,0),(-yMuesca,0)))
             .center(yMuesca,0)             
             .polyline([(bisel,0),(-bisel,0),(0,bisel)],
                       forConstruction=False)
             .close()
             .cutThruAll()
             
           )

asm = cq.Assembly()

asm.add(base(), name="base", color=cq.Color("red"))
#asm.add(cubre_papel(), name="cubre papel", color=cq.Color("green"), loc=cq.Location(cq.Vector(0,0,a_placa_foto+alto_agarre/2)))
#asm.add(cortina(), name="cortina", color=cq.Color("blue"), loc=cq.Location(cq.Vector(-.25*borde_foto,0,a_placa_foto*2+alto_agarre/2)))
#asm.add(cuerpo(), name="cuerpo", color=cq.Color("orange"), loc=cq.Location(cq.Vector((largo_cuerpo/2-borde_foto/2),0,alto_cuerpo/2-a_placa_foto)))

show_object(asm)