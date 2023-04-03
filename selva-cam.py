import cadquery as cq

d_exterior_acople = 2*25.4
h_acople = 40
espesor_acople = 3
d_interior_acople = d_exterior_acople - 2*espesor_acople

lado_foto = 50
borde_foto = 8
margen_foto = 3
alto_base = 3
alto_cubre = 2.5
alto_cortina = 3
alto_papel = 1
espesor_garra = 2.5
bisel = 1
espesor_abrazadera = 2
holgura_justa = .2
holgura_movil = .3
ancho_garras = 10
borde_caja = 8
ancho_traba = 1
ancho_tope = 3
margen_agujeritos = 5
base_perilla = 20
tope_perilla = 30

largo_base = 2*lado_foto+4*borde_foto
ancho_base_foto = lado_foto+2*borde_foto+2*espesor_garra
ancho_base_cubre = lado_foto+2*borde_foto
ancho_cortina = ancho_base_cubre - 2*bisel - 2*espesor_garra
xAgujero = lado_foto/2+borde_foto
largo_caja = largo_base/2
ancho_caja = ancho_base_foto + 2*borde_caja
alto_caja = 2*borde_caja + alto_base + alto_cubre + alto_cortina + 2*bisel + holgura_movil
largo_cortina = largo_base/2+ancho_traba-ancho_tope
alto_traba = alto_cortina+2*bisel+holgura_movil
ancho_perilla = borde_foto-ancho_traba
alto_perilla = alto_cortina + alto_traba + 5*bisel

def base(alto,ancho):
    return(cq.Workplane()
             .rect(largo_base,ancho)
             .extrude(alto)
             .edges("|X")
             .chamfer(bisel)
             .copyWorkplane(cq.Workplane())
             .pushPoints([(xAgujero,0),(-xAgujero,0)])
             .rect(lado_foto,lado_foto)
             .cutThruAll()
           )

puntos_garra = [(-ancho_base_foto/2,-bisel),
                (-ancho_base_foto/2,alto_cubre+holgura_justa),
                (-ancho_base_foto/2+bisel,alto_cubre+bisel+holgura_justa),
                (-ancho_base_foto/2+espesor_garra,alto_cubre+bisel+holgura_justa),
                (-ancho_base_foto/2+espesor_garra+bisel-holgura_justa,alto_cubre+holgura_justa),
                (-ancho_base_foto/2+espesor_garra-holgura_justa,alto_cubre+holgura_justa-bisel),
                (-ancho_base_foto/2+espesor_garra-holgura_justa,0)
                ]

def base_foto():
    lado_margen = lado_foto+margen_foto*2
    return (base(alto_base,ancho_base_foto)
            .faces(">Z")
            .workplane()
            .pushPoints([(xAgujero,0),(-xAgujero,0)])
            .rect(lado_margen,lado_margen)
            .cutBlind(-alto_papel)
            # garras
            .copyWorkplane(cq.Workplane("YZ")) # La redundancia desde aqui a la linea 92 es ridicula...
            .center(0,alto_base)
            .polyline(puntos_garra)
            .close()
            .mirrorY()
            .extrude(ancho_garras,both=False)
            .polyline(puntos_garra)
            .close()
            .mirrorY()
            .extrude(-ancho_garras,both=False)
            .faces(">X")
            .workplane()            
            .polyline(puntos_garra)
            .close()
            .mirrorY()
            .extrude(-ancho_garras,both=False)
            .faces("<X")
            .workplane()            
            .polyline(puntos_garra)
            .close()
            .mirrorY()
            .extrude(-ancho_garras,both=False)
            )

def cubre(foto=False):
    result = (base(alto_cubre,ancho_base_cubre)
                 .copyWorkplane(cq.Workplane("YZ"))
                 .split(keepTop=True, keepBottom=False)
                 .copyWorkplane(cq.Workplane("YZ"))
                 .workplane(offset=largo_base/4)
                 .center(0,0)
                 .polyline([(-ancho_base_cubre/2+bisel,0),
                            (-ancho_base_cubre/2+bisel-espesor_garra,0),
                            (-ancho_base_cubre/2-espesor_garra,bisel),
                            (-ancho_base_cubre/2-espesor_garra,alto_cubre-bisel),
                            (-ancho_base_cubre/2-espesor_garra+bisel,alto_cubre),
                            (-ancho_base_cubre/2+bisel,alto_cubre)
                            ])
                 .close()
                 .mirrorY()
                 .extrude(largo_base/4-ancho_garras-holgura_justa, both=True)
                 # garras
                 .copyWorkplane(cq.Workplane("YZ"))
                 .workplane(offset=largo_base/4)
                 .center(0,alto_cubre)
                 .polyline([(-ancho_base_cubre/2+1*bisel,-bisel),
                            (-ancho_base_cubre/2+1*bisel,alto_cortina+bisel+holgura_movil),
                            (-ancho_base_cubre/2+2*bisel,alto_cortina+2*bisel+holgura_movil),
                            (-ancho_base_cubre/2+2*bisel+espesor_garra,alto_cortina+2*bisel+holgura_movil),
                            (-ancho_base_cubre/2+3*bisel+espesor_garra-holgura_movil,alto_cortina+bisel+holgura_movil),
                            (-ancho_base_cubre/2+1*bisel+espesor_garra-holgura_movil,alto_cortina+holgura_movil-bisel),
                            (-ancho_base_cubre/2+1*bisel+espesor_garra-holgura_movil,0)
                            ])
                 .close()
                 .mirrorY()
                 .extrude(largo_base/4,both=True)
                 )
    if foto:
        result = (result.faces("<X")
                  .workplane()
                  .center(0,alto_traba/2)
                  .rect(ancho_cortina+2*holgura_movil,alto_traba)
                  .extrude(-ancho_tope)
                  )
    return result

def cortina():
    return (cq.Workplane()
            .rect(largo_cortina,ancho_cortina)
            .extrude(alto_cortina)
            .edges("|X")
            .chamfer(bisel)
            .faces("<X")
            .workplane()
            .center(0,alto_cortina)
            .polyline([(0,0),
                       (ancho_cortina/2-bisel,0),
                       (ancho_cortina/2-2*bisel,bisel),
                       (ancho_cortina/2-2*bisel,2*bisel+holgura_movil),
                       (0,2*bisel+holgura_movil)
                       ])
            .mirrorY()
            .extrude(-largo_cortina)
            .faces(">X")
            .workplane()
            .center(0,(alto_traba+borde_caja)/2-2*holgura_justa)
            .rect(ancho_cortina-4*bisel,borde_caja)
            .extrude(-ancho_traba)
            .faces(">X").edges("<Z")
            .workplane(centerOption="CenterOfMass")
            .center(0,alto_perilla/2)
            .rect(base_perilla,alto_perilla)
            .workplane(offset=ancho_perilla)
            .rect(tope_perilla,alto_perilla)
            .loft(combine=True)
            .faces(">X").edges("|Z")
            .fillet(bisel)
            )

def caja():
    return (cq.Workplane()
            .rect(largo_caja,ancho_caja)
            .extrude(alto_caja)
            .chamfer(bisel)
            .copyWorkplane(cq.Workplane("YZ"))
            .center(0,borde_caja)
            .polyline([(0,0),
                       (ancho_base_foto/2+holgura_movil,0),
                       (ancho_base_foto/2+holgura_movil,alto_base+alto_cubre+holgura_justa+holgura_movil),
                       #(ancho_base_foto/2+holgura_movil-espesor_garra-2*bisel,alto_base+alto_cubre+bisel+holgura_justa+holgura_movil),
                       (ancho_base_foto/2-espesor_garra-2*bisel+holgura_movil,alto_base+alto_cubre+bisel+2*holgura_movil-bisel+alto_cortina+2*bisel),
                       (0,alto_base+alto_cubre+bisel+2*holgura_movil-bisel+alto_cortina+2*bisel),
                       ])
            .mirrorY()
            .cutThruAll()
            # acople
            .faces(">Z")
            .workplane()
            .circle(d_exterior_acople/2)
            .extrude(h_acople)
            .faces(">Z")
            .circle(d_exterior_acople/2-espesor_acople)
            .cutBlind('next')
            # agujeritos
            .faces("<Z")
            .rect(largo_caja-2*margen_agujeritos,ancho_caja-2*margen_agujeritos, forConstruction=True)
            .vertices()
            .circle(1.75/2+.1)
            .cutThruAll()
            )

extra_alto=0
explo = 0 #1.3
asm = cq.Assembly()

asm.add(base_foto(), name="base", color=cq.Color("red"),
        loc=cq.Location(cq.Vector(largo_base/2*explo,0,0)))
asm.add(cubre(False), name="cubre_translucido",
        color=cq.Color("green"),
        loc=cq.Location(cq.Vector(largo_base/2*explo,0,alto_base+extra_alto+6*alto_base*explo)))
asm.add(cubre(True), name="cubre_fotografico",
        color=cq.Color("cyan"),
        loc=cq.Location(cq.Vector(-largo_base/2+largo_base/2*explo,0,alto_base+extra_alto+12*alto_base*explo)))
asm.add(cortina(), name="cortina",
        color=cq.Color("blue"),
        loc=cq.Location(cq.Vector(-(largo_base-largo_cortina)/2+ancho_tope+largo_base*.9*explo,0,alto_base+alto_cubre+2*extra_alto+12*alto_base*explo)))
asm.add(caja(), name="caja",
        color=cq.Color("orange"),
        loc=cq.Location(cq.Vector(-largo_base/4,0,-borde_caja)))

show_object(asm)
# show_object(base_foto())
