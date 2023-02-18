import cadquery as cq

d_exterior_acople = 44
h_acople = 40
d_interior_acople = 42 # Comprobar
d_saliente_acople = 47.5
h_saliente_acople = 1.88 # 0.2+7*.28

def acople():
    return (cq.Workplane()
              .circle(radius=d_exterior_acople/2)
              .extrude(h_acople)
              .faces(">Z")
              .circle(radius=d_saliente_acople/2)
              .extrude(h_saliente_acople)
              .faces(">Z")
              .hole(diameter=d_interior_acople)
              )

lado_foto = 50
borde_foto = 8
a_placa_foto = 1.5
a_papel = 1
borde_papel=3
lado_agarre = 5
alto_cubre_papel = a_placa_foto
bisel_agarre = 1
alto_agarre = alto_cubre_papel + bisel_agarre
sobre_agarre = bisel_agarre

def placa_foto():
    return (cq.Workplane()
              .rect(lado_foto*2+borde_foto*3,lado_foto+borde_foto*2+lado_agarre*2)
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
              .extrude((lado_foto*2+borde_foto*3)/2,both=True)
              .edges("|X")
              .chamfer(bisel_agarre)
              .faces(">Z")
              .workplane()
              .pushPoints([((lado_foto+borde_foto)/-2,0),
                           ((lado_foto+borde_foto)/2,0)])
              .rect(lado_foto-borde_papel*2,lado_foto-borde_papel*2)
              .cutThruAll()
              .faces(">Z")
              .rect(lado_foto*2+borde_foto*3,lado_foto+borde_foto*2-holgura*2)
              .extrude(alto_agarre + sobre_agarre)
              .faces(">Z").edges("|X")
              .chamfer(bisel_agarre)
              .faces("<X")
              .workplane()
              .hLine(lado_foto/2+borde_foto/2)
              .vLine(alto_agarre-bisel_agarre)
              .line(-bisel_agarre,bisel_agarre)
              .vLine(bisel_agarre)
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

a=acople().translate([0,0,40])
p_foto = placa_foto()
c_papel = cubre_papel().translate([0,0,a_placa_foto+alto_agarre/2])
cort = cortina().translate([-.25*borde_foto,0,a_placa_foto+alto_agarre*1.5])