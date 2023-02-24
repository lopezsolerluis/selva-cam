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
alto_papel = 1
espesor_garra = 2.5
bisel = 1
espesor_abrazadera = 2
holgura = .2
ancho_muesca = 10

largo_base = 2*lado_foto+4*borde_foto
ancho_base_foto = lado_foto+2*borde_foto+2*espesor_garra
ancho_base_cubre = lado_foto+2*borde_foto
xAgujero = lado_foto/2+borde_foto

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
                       (-ancho_base_foto/2,alto_cubre+holgura),
                       (-ancho_base_foto/2+bisel,alto_cubre+bisel+holgura),
                       (-ancho_base_foto/2+espesor_garra,alto_cubre+bisel+holgura),
                       (-ancho_base_foto/2+espesor_garra+bisel-holgura,alto_cubre+holgura),
                       (-ancho_base_foto/2+espesor_garra-holgura,alto_cubre+holgura-bisel),
                       (-ancho_base_foto/2+espesor_garra-holgura,0)
                       ])
            .close()
            .mirrorY()
            .extrude(largo_base/2,both=True)
            .copyWorkplane(cq.Workplane())
            .workplane(offset=alto_base)
            .pushPoints([(-largo_base/4,0),(largo_base/4,0)])
            .rect(ancho_muesca+holgura,ancho_base_foto)
            .cutBlind(alto_cubre+bisel+holgura)
            )

def cubre():
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
            .extrude(ancho_muesca/2-holgura, both=True)            
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



#asm.add(cortina(), name="cortina", color=cq.Color("blue"), loc=cq.Location(cq.Vector(-.25*borde_foto,0,a_placa_foto*2+alto_agarre/2)))
#asm.add(cuerpo(), name="cuerpo", color=cq.Color("orange"), loc=cq.Location(cq.Vector((largo_cuerpo/2-borde_foto/2),0,alto_cuerpo/2-a_placa_foto)))

show_object(asm)
# show_object(base_foto())