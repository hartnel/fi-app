from impact_family.models import Fi
from sectors.constants import SectorTypeCts
from sectors.models import Sector, SectorType
from django.db import transaction

data = {
    "Yaoundé 1" : [
        "Bastos 1",
        "Bastos 2",
        "Dispensaire Messassi",
        "Dragage, non loin de KAZOO",
        "Emana Quartier Anglo 1",
        "Total Etoudi",
        "Emana Fokou",
        "Emana pont 1",
        "Emana Résidence",
        "Emana Dallas",
        "Manguiers 1",
        "Manguiers 2",
        "Manguiers 3",
        "Total Yannick",
        "Nkozoa",
        "Santa Barbara face résidence",
        "KAMTO",
        "Santa Barbara Rails",
        "Tsinga village",
        "Ngousso Savannah"
    ],
    "Yaoundé 2" : [
        "Descente 8ème",
        "Cité Verte, Batiment N",
        "Cité Verte 2",
        "Mbankolo Cité de la Paix",
        "Madagascar",
        "Parcours Vita",
        "Tsinga, polyclinique",
        "Tsinga, Fecafoot"
    ],
    "Yaoundé 3" : [
        "Ahala",
        "Damas 1",
        "Damas 2",
        "Damas 4",
        "Mvan Texaco",
        "Ngoa Ekelle",
        "Nsimeyong",
        "Obobogo 1",
        "Obobogo 2",
        "Ecole des postes"
    ],
    "Yaoundé 4" : [
        "Ekoumdoum 1",
        "Ekoumdoum 2",
        "Ekoumdoum 3",
        "Messamendongo",
        "Nkolnda, Collège La Relève",
        "Odza Borne 10",
        "Odza-Dispensaire",
        "Odza-Maison Blanche 2",
        "Odza-Petit marché",
        "Mimboman-Château",
        "Mimboman-Ecole Publique 1",
        "Mimboman-Ecole Publique 2",
        "Mimboman-Eloundou",
        "Mimboman Liberté II",
        "NkoaBang",
        "Awae-carrefour concorde",
        "Awae-Ewankang",
        "GP- Biteng",
        "Nkongoa Essabah",
        "Rejoindre via WhatsApp",
        "Rejoindre via WhatsApp",
        "Ekounou Carrosel",
        "Ekié-Stade",
        "Ekié, Nord",
        "Ekounou-Montée",
        "Ekounou-Pays-Bas",
        "Ekié, Chambre froide 1",
        "Ekié, Chambre froide 2",
        "Nkondengui",
        "Ahala Barrière",
        "Obam Ongola",
        "Nsam-SCDP",
        "Meyo",
        "Mbalmayo, mecanicien",
        "Mbalmayo Ngallan bloc 4",
        "Mbalmayo Newton",
        "Mbalmayo Nkol -Nguet",
        "Mbalmayo ngallan",
        "Mbalmayo Oyack",
        "Bafia",
        "Mbankomo"
    ],
    "Yaoundé 5" : [
        "Essos Chapelle",
        "Essos Titi Garage",
        "Essos, Lycée bilingue",
        "Mimboman Liberté I",
        "Mimboman Opep",
        "Ngousso Descente eleveur",
        "Hôpital Général pharmacie bleue",
        "Ngousso Hôpital Général",
        "Ngousso, Tradex Eleveur",
        "Nkolmesseng",
        "Nkolfoulou, carrefour",
        "Nkolfoulou",
        "Rejoindre via WhatsAppFourgerolles 1",
        "Fourgerolles pont"
    ],
    "Yaoundé 6" : [
        "Carrefour jouvence",
        "Biyemassi, Superette",
        "Etoug Ebe",
        "SimbockTradex",
        "Simbock collège Mario",
        "TamTam 1",
        "Obili",
        "Simbock usine cladel",
        "Centre des handicapés",
        "Damas Ebom City 2",
        "Damas Rue Damas",
        "Damas Essono City"
    ],
    "Yaoundé 7" : [
        "Nkolbisson 1",
        "Nkolbisson 2",
        "Nkolbisson 3",
        "Oyom Abang 1",
        "Oyom Abang 2",
        "Oyom Abang 3",
        "Oyom Abang 4"
    ],
    "SOA" : [
        "Soa entrée Millenium",
        "Soa, Centre",
        "Soa,Nkolfoulou wague",
        "Soa,Entrée Capitaine",
        "Soa,Nkolfoulou chapelle",
        "Soa,Enrée Complexe",
        "Soa,Entrée capitaine",
        "Soa, derrière lycée",
        "Soa,Ebogo 1",
        "Soa , pharmacie",
        "Soa,Lycée Technique",
        "Soa, ELN B",
        "Soa, entrée Jean 23",
        "Soa, Maison rose",
        "Soa, carrefour foe",
        "Soa, entrée Millénium 2"
    ],
    "BAFOUSSAM" : [
        "BAFOUSSAM"
    ],
    "DSCHANG" : [
        "DSCHANG"
    ],
    "SANGMELIMA" : [
        "SANGMELIMA"
    ],
    "EBOLOWA" : [
        "EBOLOWA"
    ],
    "GAROUA" : [
        "GAROUA"
    ]
}


@transaction.atomic
def save_fis():
    sectors = data.keys()
    root = Sector.objects.get(label__icontains="Yaoundé", type__name=SectorTypeCts.CITY)
    for sector in sectors:
        sector_obj = Sector.objects.filter(label=sector).first()
        if not sector_obj:
            sector_type,_ = SectorType.objects.get_or_create(name=SectorTypeCts.SECTOR)
            sector_obj = root.add_child(
                label=sector,
                type=sector_type
            )
            print(f"Sector {sector} created")
        for fi in data[sector]:
            fi_obj = Fi.objects.create(
                name=fi,
                sector=sector_obj
            )
            print(f"Fi {fi} created")
            
save_fis()