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

a=acople().translate([0,0,40])

lado_foto = 50
borde_foto = 8
a_placa_foto = 2
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
              .copyWorkplane(cq.Workplane("YZ"))
              .workplane(centerOption="CenterOfMass")
              .center(0,a_placa_foto+alto_agarre/2)
              .rect(lado_foto+borde_foto*2+lado_agarre*2,alto_agarre)
              .extrude((lado_foto*2+borde_foto*3)/2, both=True)
              .faces(">X").edges("<Z")
              .center(0,0)
              .sketch()
              .rect(lado_foto+borde_foto*2+2*bisel_agarre,alto_agarre)
              .vertices(">Y")
              .chamfer(bisel_agarre)
              .finalize()
              .cutThruAll()
              .faces(">Z")
              .workplane()
              .pushPoints([(0,lado_foto/2+borde_foto+lado_agarre/2),
                           (0,-(lado_foto/2+borde_foto+lado_agarre/2))])
              .rect(lado_foto*2+borde_foto*3,lado_agarre)
              .extrude(sobre_agarre)
              )

p_foto = placa_foto()

holgura = .5
def cubre_papel():
    return (cq.Workplane("YZ")
              .sketch()
              .rect(lado_foto+borde_foto*2+2*bisel_agarre-holgura*2,alto_agarre)
              .vertices(">Y")
              .chamfer(bisel_agarre)
              .finalize()
              .extrude((lado_foto*2+borde_foto*3)/2,both=True)
              .faces(">Z")
              .workplane()
              .pushPoints([((lado_foto+borde_foto)/-2,0),
                           ((lado_foto+borde_foto)/2,0)])
              .rect(lado_foto-borde_papel*2,lado_foto-borde_papel*2)
              .cutThruAll()
              )

c_papel = cubre_papel().translate([0,0,a_placa_foto+alto_agarre/2])