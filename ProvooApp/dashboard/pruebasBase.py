from datetime import date


portafolio, created = Portafolio.objects.get_or_create(
        Ruc="17100000", UserID_id=3,
        Nombre="Prueba")

portafolio = Portafolio.objects.get(
        Ruc="17100000", UserID_id=4,
        Nombre="Prueba")


portafolio = Portafolio.objects.get(UserID_id=4, Ruc="1711635571", Nombre="CARLOS VELASCO DE LA ROSA")


document, exits = documento.objects.get_or_create( rucDocumento=portafolio, numeroDeDocumento="0000000", nombreDocumento="0000000", RucEmisor="0000000", NombreEmisor="0000000", DireccionEmisor="0000000", fecha=date(2005, 7, 27), Impuesto=14, totalGastosf=12, totalImpuestos=12, totalDocumento=12, deducible_vestimenta=12, deducible_educacion=12, deducible_comida=12, deducible_salud=12, deducible_vivienda=12, no_deducible=12, archivo="cualquierarchiv")
