import cadquery as cq

d_exterior_acople = 2*25.4
h_acople = 40
espesor_acople = 3
d_interior_acople =d_exterior_acople - 2*espesor_acople

lado_foto = 50
borde_foto = 8
a_placa_foto = 3
a_papel = 1
borde_papel=3
lado_agarre = 5
alto_cubre_papel = a_placa_foto
bisel_agarre = 1.4
alto_agarre = alto_cubre_papel + bisel_agarre
sobre_agarre = bisel_agarre

ancho_placa_foto = lado_foto+borde_foto*2+lado_agarre*2
def placa_foto():
    return (cq.Workplane()
              .rect(lado_foto*2+borde_foto*3,ancho_placa_foto)
              .extrude(a_placa_foto)
              .faces("<Z").edges("|X")
              .chamfer(bisel_agarre)
              .faces(">Z")
              .workplane()
              .pushPoints([((lado_foto+borde_foto)/-2,0),
                           ((lado_foto+borde_foto)/2,0)])
              .rect(lado_foto,lado_foto)
              .cutBlind(-a_papel)
              .pushPoints([((lado_foto+borde_foto)/-2,0),
                           ((lado_foto+borde_foto)/2,0)])
              .rect(lado_foto-borde_papel*2,lado_foto-borde_papel*2)
              .cutThruAll()
              .faces(">Z")
              .rect(lado_foto*2+borde_foto*3,lado_foto+borde_foto*2+lado_agarre*2)
              .extrude(alto_agarre + sobre_agarre)
              .faces(">Z").edges("|X")
              .chamfer(bisel_agarre)
              .faces("<X")
              .workplane()
              .hLine(lado_foto/2+borde_foto+bisel_agarre)
              .vLine(alto_agarre-bisel_agarre)
              .line(-bisel_agarre,bisel_agarre)
              .vLine(bisel_agarre)
              .lineTo(0,alto_agarre+bisel_agarre).mirrorY()
              .cutThruAll()
              )

holgura = .25

def cubre_papel():
    return (cq.Workplane("YZ")
              .sketch()
              .rect(lado_foto+borde_foto*2+2*bisel_agarre-holgura*2,alto_agarre)
              .finalize()
              .extrude(lado_foto+borde_foto*1.5)
              .edges("|X")
              .chamfer(bisel_agarre)
              .faces(">Z")
              .workplane(centerOption="CenterOfMass")
              .rect(lado_foto-borde_papel*2,lado_foto-borde_papel*2)
              .cutThruAll()
              .faces(">Z")
              .rect(lado_foto+borde_foto*1.5,lado_foto+borde_foto*2-holgura*2)
              .extrude(alto_agarre + sobre_agarre - alto_cubre_papel/2)
              .faces(">Z").edges("|X")
              .chamfer(bisel_agarre)
              .faces("<X")
              .workplane()
              .vLine(-alto_agarre+alto_cubre_papel)
              .hLine(lado_foto/2+borde_foto/2)
              .vLine(alto_agarre-bisel_agarre)
              .line(-bisel_agarre,bisel_agarre)
              .vLine(bisel_agarre+alto_cubre_papel)
              .lineTo(0,alto_agarre+bisel_agarre).mirrorY()
              .cutThruAll()
              )

def cortina():
    return(cq.Workplane("YZ")
             .sketch()
             .rect(lado_foto+borde_foto-holgura*2,alto_agarre)
             .finalize()
             .extrude(lado_foto+borde_foto*1.75)
             .edges("|X")
             .chamfer(bisel_agarre)
             )

alto_cuerpo = a_placa_foto*4+alto_agarre+sobre_agarre
largo_cuerpo = lado_foto+borde_foto*2
def cuerpo():
    return (cq.Workplane()
              .box(largo_cuerpo,
                   lado_foto+borde_foto*2+lado_agarre*4,
                   alto_cuerpo)
              .edges()
              .chamfer(bisel_agarre)
              .copyWorkplane(cq.Workplane("YZ"))
              .vLine(-alto_cuerpo/2+a_placa_foto)
              .hLine(ancho_placa_foto/2+holgura)
              .vLine(a_placa_foto+alto_agarre+sobre_agarre-bisel_agarre+holgura)
              .line(-bisel_agarre,bisel_agarre)
              .hLine(-lado_agarre+bisel_agarre-holgura)
              .vLine(alto_agarre-a_placa_foto+bisel_agarre+holgura/2)
              .hLine(-(lado_foto+borde_foto*2)/2)
              .mirrorY()
              .cutThruAll()
              .faces(">Z")
              .workplane()
              .circle(d_exterior_acople/2-holgura)
              .extrude(h_acople)
              .faces(">Z")
              .hole(d_exterior_acople-2*espesor_acople)
              .faces("<Z")
              .workplane()
              .rect(lado_foto,lado_foto)
              .cutBlind(-a_placa_foto)              
              )

asm = cq.Assembly()

asm.add(placa_foto(), name="placa foto", color=cq.Color("red"))
asm.add(cubre_papel(), name="cubre papel", color=cq.Color("green"), loc=cq.Location(cq.Vector(0,0,a_placa_foto+alto_agarre/2)))
asm.add(cortina(), name="cortina", color=cq.Color("blue"), loc=cq.Location(cq.Vector(-.25*borde_foto,0,a_placa_foto*2+alto_agarre/2)))
asm.add(cuerpo(), name="cuerpo", color=cq.Color("orange"), loc=cq.Location(cq.Vector((largo_cuerpo/2-borde_foto/2),0,alto_cuerpo/2-a_placa_foto)))

show_object(asm)