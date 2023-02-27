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
ancho_traba = 4
margen_agujeritos = 5

largo_base = 2*lado_foto+4*borde_foto
ancho_base_foto = lado_foto+2*borde_foto+2*espesor_garra
ancho_base_cubre = lado_foto+2*borde_foto
ancho_cortina = ancho_base_cubre - 4*bisel - 2*espesor_garra
xAgujero = lado_foto/2+borde_foto
largo_caja = largo_base/2
ancho_caja = ancho_base_foto + 2*borde_caja
alto_caja = 2*borde_caja + alto_base + alto_cubre + alto_cortina + 2*bisel + holgura_movil
largo_cortina = largo_base/2+ancho_traba

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

def base_foto():
    lado_margen = lado_foto+margen_foto*2
    return (base(alto_base,ancho_base_foto)
            .faces(">Z")
            .workplane()
            .pushPoints([(xAgujero,0),(-xAgujero,0)])
            .rect(lado_margen,lado_margen)
            .cutBlind(-alto_papel)
            # garras
            .copyWorkplane(cq.Workplane("YZ"))
            .center(0,alto_base)
            .polyline([(-ancho_base_foto/2,-bisel),
                       (-ancho_base_foto/2,alto_cubre+holgura_justa),
                       (-ancho_base_foto/2+bisel,alto_cubre+bisel+holgura_justa),
                       (-ancho_base_foto/2+espesor_garra,alto_cubre+bisel+holgura_justa),
                       (-ancho_base_foto/2+espesor_garra+bisel-holgura_justa,alto_cubre+holgura_justa),
                       (-ancho_base_foto/2+espesor_garra-holgura_justa,alto_cubre+holgura_justa-bisel),
                       (-ancho_base_foto/2+espesor_garra-holgura_justa,0)
                       ])
            .close()
            .mirrorY()
            .extrude(largo_base/2,both=True)
            # Huecos muescas
            .copyWorkplane(cq.Workplane())
            .workplane(offset=alto_base)
            .pushPoints([(-largo_base/4,0),(largo_base/4,0)])
            .rect(largo_base/2-2*ancho_garras+holgura_justa,ancho_base_foto)
            .cutBlind(alto_cubre+bisel+holgura_justa)
            )

def cubre(foto=False):
    return (base(alto_cubre,ancho_base_cubre)
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
            .center(0,alto_cortina/2+bisel-holgura_justa)
            .lineTo(ancho_cortina/2-2*bisel,0)
            .threePointArc((0,3*borde_caja),
                           (-(ancho_cortina/2-2*bisel),0))
            .close()
            .extrude(-ancho_traba)
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
                       (ancho_base_foto/2-espesor_garra-2*bisel,alto_base+alto_cubre+bisel+2*holgura_movil-bisel+alto_cortina+2*bisel),
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
asm = cq.Assembly()

asm.add(base_foto(), name="base", color=cq.Color("red"))
asm.add(cubre(), name="cubre_translucido",
        color=cq.Color("green"),
        loc=cq.Location(cq.Vector(0,0,alto_base+extra_alto)))
asm.add(cubre(), name="cubre_fotografico",
        color=cq.Color("cyan"),
        loc=cq.Location(cq.Vector(-largo_base/2,0,alto_base+extra_alto)))
# asm.add(cortina(), name="cortina",
#         color=cq.Color("blue"),
#         loc=cq.Location(cq.Vector(-(largo_base-largo_cortina)/2,0,alto_base+alto_cubre+2*extra_alto)))
# asm.add(caja(), name="caja",
#         color=cq.Color("orange"),
#         loc=cq.Location(cq.Vector(-largo_base/4,0,-borde_caja)))

show_object(asm)
# show_object(base_foto())
