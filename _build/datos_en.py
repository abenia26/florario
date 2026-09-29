# Versión en inglés de los datos de datos.py. Solo lleva lo que cambia con el idioma (textos y
# slugs); fechas, colores, fotos y países se siguen leyendo de datos.py. build.py combina los dos
# ficheros con localize() y genera la web inglesa en /en/.
#
# Si añades una fecha, una flor, una guía o una página en datos.py o en _build/paginas/, añade
# aquí su traducción y su slug inglés: el build avisa de lo que falte.

# Slug español -> slug inglés de cada página (la portada es "" en los dos idiomas).
SLUGS = {
    # índices
    "meses": "months", "flores": "flowers", "guias": "guides", "paises": "countries",
    # meses
    "enero": "january", "febrero": "february", "marzo": "march", "abril": "april", "mayo": "may",
    "junio": "june", "julio": "july", "agosto": "august", "septiembre": "september",
    "octubre": "october", "noviembre": "november", "diciembre": "december",
    # flores
    "rosa": "rose", "girasol": "sunflower", "tulipan": "tulip", "peonia": "peony", "clavel": "carnation",
    "margarita": "daisy", "lilium": "lily", "hortensia": "hydrangea", "violeta": "violet",
    "crisantemo": "chrysanthemum", "cempasuchil": "cempasuchil", "mimosa": "mimosa",
    "lirio-de-los-valles": "lily-of-the-valley", "nochebuena": "poinsettia",
    # guías
    "flores-amarillas": "yellow-flowers", "flores-amarillas-21-de-marzo": "yellow-flowers-march-21",
    "flores-azules": "blue-flowers", "flores-moradas": "purple-flowers", "san-valentin": "valentines-day",
    "dia-de-la-mujer": "womens-day", "dia-del-padre": "fathers-day", "sant-jordi": "sant-jordi",
    "dia-de-la-madre": "mothers-day", "dia-del-maestro": "teachers-day", "dia-de-la-novia": "girlfriend-day",
    "amor-y-amistad": "amor-y-amistad", "todos-los-santos-dia-de-muertos": "all-saints-day-of-the-dead",
    "virgen-de-guadalupe": "our-lady-of-guadalupe", "flores-para-cumpleanos": "birthday-flowers",
    "flores-para-aniversario": "anniversary-flowers", "flores-para-condolencias": "sympathy-flowers",
    "significado-colores-flores": "flower-color-meanings",
    # países
    "espana": "spain", "mexico": "mexico", "argentina": "argentina", "colombia": "colombia",
    "chile": "chile", "peru": "peru",
    # otras
    "calendario-de-flores-para-imprimir": "printable-flower-calendar", "sobre-florario": "about",
    "contacto": "contact", "prensa": "press", "politica-de-privacidad": "privacy-policy",
    "aviso-legal": "legal-notice",
}

COLORS = {"amarillo": "Yellow", "rojo": "Red", "rosa": "Pink", "azul": "Blue", "morado": "Purple",
          "naranja": "Orange", "blanco": "White"}
TYPES = {"clasico": "Classic", "trend": "Trend", "memoria": "Remembrance"}
# En inglés los meses se escriben con mayúscula; aquí van en minúscula porque también son el slug.
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august",
          "september", "october", "november", "december"]
MONTH_SHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

IMAGES = {
    "rosa-roja": {"alt": "An open red rose, the flower of Valentine’s Day and Sant Jordi",
                  "alt_corto": "Open red rose"},
    "rosa-rosa": {"alt": "A pale pink rose on a rosebush, the flower of Girlfriend Day and Korea’s Rose Day",
                  "alt_corto": "Pale pink rose on a rosebush"},
    "ramo-rosas": {"alt": "A bouquet of pink roses, a classic gift for Valentine’s Day and Mother’s Day",
                   "alt_corto": "Bouquet of pink roses"},
    "ramo-tulipanes": {"alt": "A bouquet of colorful tulips, typical of Galentine’s Day and spring",
                       "alt_corto": "Bouquet of colorful tulips"},
    "mimosa": {"alt": "Mimosa branches with little yellow pompoms, the flower of March 8 in Italy",
               "alt_corto": "Mimosa branches with yellow pompoms"},
    "girasol": {"alt": "An open yellow sunflower, the flower of the September 21 yellow flowers trend",
                "alt_corto": "Open yellow sunflower"},
    "muguet": {"alt": "A stem of lily of the valley (muguet) with white bells, the flower of May 1 in France",
               "alt_corto": "Stem of lily of the valley (muguet) with white bells"},
    "clavel": {"alt": "Fuchsia carnations, the classic Mother’s Day flower",
               "alt_corto": "Fuchsia carnations"},
    "peonia": {"alt": "An open pink peony, a May flower for Mother’s Day",
               "alt_corto": "Open pink peony"},
    "lilium": {"alt": "A white and pink lily, the flower of Mother’s Day in Argentina and of sympathy bouquets",
               "alt_corto": "White and pink lily"},
    "hortensia-azul": {"alt": "A blue and violet hydrangea, a blue flower for Boyfriend Day on October 3",
                       "alt_corto": "Blue and violet hydrangea"},
    "crisantemo": {"alt": "A white long-petalled chrysanthemum, the flower of All Saints’ Day",
                   "alt_corto": "White long-petalled chrysanthemum"},
    "cempasuchil": {"alt": "Orange and yellow cempasúchil flowers, the flower of the Day of the Dead altar",
                    "alt_corto": "Orange and yellow cempasúchil flowers"},
    "violeta": {"alt": "A purple violet among leaves, the flower of the November 9 purple flowers trend",
                "alt_corto": "Purple violet among leaves"},
    "nochebuena": {"alt": "Red poinsettia plants, the Mexican Christmas flower celebrated on December 8",
                   "alt_corto": "Red poinsettia plants"},
    "ramo-silvestre": {"alt": "A bouquet of daisies and wildflowers in a glass jar, a gift for any day",
                       "alt_corto": "Bouquet of daisies and wildflowers in a glass jar"},
}

# name = nombre del país; "in" = "in Spain"… para frases como "Flower dates in Mexico".
COUNTRIES = {
    "ES": {"name": "Spain", "in": "in Spain"},
    "MX": {"name": "Mexico", "in": "in Mexico"},
    "AR": {"name": "Argentina", "in": "in Argentina"},
    "CO": {"name": "Colombia", "in": "in Colombia"},
    "CL": {"name": "Chile", "in": "in Chile"},
    "PE": {"name": "Peru", "in": "in Peru"},
}

EVENTS = {
    "rose-day": {"name": "Rose Day", "flower": "Roses", "region": "India",
                 "story": "It opens Valentine’s Week: each of the seven days before Valentine’s Day has its own theme, and the first one is for giving roses. It is everywhere in Bollywood edits and reels."},
    "galentines": {"name": "Galentine’s Day", "flower": "Bouquets for your friends", "region": "Worldwide, especially on social media",
                   "story": "It was born in 2010 in the series Parks and Recreation, when Leslie Knope celebrates her friends the day before Valentine’s Day. Social media turned it into a real plan: breakfast, shared bouquets and a group photo."},
    "san-valentin": {"name": "Valentine’s Day", "flower": "Red roses", "region": "Worldwide · in Mexico and other countries, Day of Love and Friendship",
                     "story": "The biggest day of the year for flowers. The red rose is the universal code for “I like you”; in several Latin American countries friendship is celebrated too, so giving flowers to friends also counts."},
    "8m": {"name": "International Women’s Day", "flower": "Mimosa or tulips", "region": "Italy, Russia and Eastern Europe",
           "story": "In Italy a sprig of mimosa has been given since 1946; in Russia and Eastern Europe tulips are typical. In Spain and Latin America 8M is above all a day of protest: if you give flowers, make them a recognition, not a substitute for listening."},
    "padre-es": {"name": "Father’s Day", "flower": "Sunflowers or a plant", "region": "Spain, Portugal, Italy, Bolivia and Honduras",
                 "story": "It falls on Saint Joseph’s Day, the father of Jesus in Christian tradition. Flowers are not the most typical gift, but more and more people give sunflowers or a plant that lasts: a present that doesn’t wilt in a week."},
    "amarillas-marzo": {"name": "Yellow flowers (northern spring)", "flower": "Sunflowers, tulips or yellow roses", "region": "Mexico and Central America, and increasingly Peru",
                        "story": "The September 21 trend doubled: with spring arriving in the northern hemisphere, Mexico adopted a second yellow flowers day. Same song, same idea, different season."},
    "sant-jordi": {"name": "Sant Jordi", "flower": "A red rose and a book", "region": "Catalonia",
                   "story": "Legend has it that a rosebush sprang from the blood of the dragon slain by Saint George (Sant Jordi). Barcelona fills with rose and book stalls; the book was added in the 20th century and coincides with World Book Day."},
    "muguet": {"name": "Muguet du 1er mai", "flower": "Lily of the valley (muguet)", "region": "France",
               "story": "Since King Charles IX (1561), a sprig of lily of the valley has been given on May 1 to wish good luck. On that day selling muguet in the street is tolerated without a license."},
    "madre-es": {"name": "Mother’s Day", "ruleText": "1st Sunday of May", "flower": "Carnations, roses or peonies", "region": "Spain and Portugal",
                 "story": "In Spain it is celebrated on the first Sunday of May, the month Catholic tradition dedicates to the Virgin Mary. Carnations and peonies are the classics."},
    "madre-mx": {"name": "Mother’s Day (Día de las Madres)", "flower": "Roses and carnations", "region": "Mexico, Guatemala and El Salvador",
                 "story": "In Mexico it has been a fixed date since 1922, when the newspaper Excélsior promoted the celebration. Serenade, family lunch and a bouquet that can’t be missing."},
    "madre-mayo2": {"name": "Mother’s Day", "ruleText": "2nd Sunday of May", "flower": "Carnations", "region": "USA, Colombia, Peru, Chile, Venezuela, Brazil, Italy and more",
                    "story": "Anna Jarvis promoted the day in the USA in 1908 and chose the carnation, her mother’s favorite flower. From there it spread to much of the Americas and Europe."},
    "rose-day-kr": {"name": "Rose Day", "flower": "Roses", "region": "South Korea",
                    "story": "In Korea the 14th of every month has a theme for couples. May’s is roses: if you follow K-dramas or K-pop, it will sound familiar."},
    "maestro": {"name": "Teachers’ Day", "flower": "Daisies, sunflowers or a small plant", "region": "Mexico and Colombia",
                "story": "Mexico has celebrated its teachers every May 15 since 1918, and Colombia does so on the same day in memory of Saint John Baptist de La Salle, patron saint of teachers. A flower with a handwritten note is the most common gesture in classrooms."},
    "namorados": {"name": "Dia dos Namorados", "flower": "Red roses", "region": "Brazil",
                  "story": "Brazil’s Valentine’s Day falls on the eve of Saint Anthony’s Day, the matchmaker saint. It became popular in 1949 with an advertising campaign and today it is one of the biggest dates of the year there."},
    "padre-junio": {"name": "Father’s Day", "ruleText": "3rd Sunday of June", "flower": "Sunflowers, blue flowers or a plant", "region": "Mexico, Argentina, Chile, Colombia, Peru, Venezuela, USA and more",
                    "story": "The US date, which spread to almost all of Latin America. Flowers for dad are gaining ground thanks to the “men deserve flowers too” trend: sunflowers, blue tones or a plant for the office."},
    "novia": {"name": "Girlfriend Day (Día de la Novia)", "flower": "Roses", "region": "Mexico, Peru, Ecuador, Costa Rica",
              "variant": "In some countries it is celebrated on the first Sunday of April; August 1 is the version that circulates most on social media.",
              "story": "It comes from the American National Girlfriend Day and on social media it works as a second Valentine’s Day. It isn’t official in any country, but florists already have it marked."},
    "amor-amistad-co": {"name": "Amor y Amistad (Love and Friendship Day)", "ruleText": "3rd Saturday of September", "flower": "Roses and sunflowers", "region": "Colombia",
                        "story": "Colombia has celebrated its own Valentine’s Day in September since the 1960s. It is for partners and friends alike, secret Santa included."},
    "amarillas": {"name": "Yellow flowers", "flower": "Sunflowers, tulips or yellow roses", "region": "All of Latin America · it started in Argentina, Chile, Peru and Uruguay",
                  "variant": "Viral variant: the 22nd for cousins or aunts, the 23rd for mom or grandma and the 24th for your best friend.",
                  "story": "In Floricienta, the 2004 Argentine series, the heroine dreams of someone giving her yellow flowers. In September 2021 TikTok revived the song to welcome spring in the southern hemisphere, and the trend hasn’t stopped since."},
    "novio": {"name": "Boyfriend Day (Día del Novio)", "flower": "Blue flowers or a Hot Wheels bouquet", "region": "Mexico, Peru, Chile, Colombia, Spain",
              "story": "It was born in 2014 as #NationalBoyfriendDay and in Latin America it became the answer to yellow flowers: blue flowers and bouquets made of Hot Wheels cars wrapped in paper and ribbons."},
    "madre-ar": {"name": "Mother’s Day", "ruleText": "3rd Sunday of October", "flower": "Roses and lilies", "region": "Argentina",
                 "story": "Argentina celebrates mothers in spring, on the third Sunday of October, so it coincides with the best flower season of the southern hemisphere."},
    "todos-santos": {"name": "All Saints’ Day", "flower": "Chrysanthemums", "region": "Spain and much of Latin America",
                     "story": "Families clean and decorate the graves of their loved ones. The chrysanthemum is the flower of the day: bringing one is a way of saying they are remembered."},
    "muertos": {"name": "Day of the Dead", "flower": "Cempasúchil (Mexican marigold)", "region": "Mexico",
                "story": "The color and scent of cempasúchil mark the path of the souls to the altar (ofrenda). Its orange petals are one of the visual symbols of the celebration."},
    "moradas": {"name": "Purple flowers", "flower": "Violets or any purple flower", "region": "Mexico, Peru, Colombia, Spain",
                "variant": "In Colombia an October 9 variant also circulates.",
                "story": "The song tells of someone who sent violets to a woman every November 9, with no card; in the end it was her own husband. On TikTok they are given to your “purple person”: someone who arrived recently and is already essential."},
    "hombre": {"name": "International Men’s Day", "flower": "Blue flowers, sunflowers or Hot Wheels", "region": "Latin America, especially on social media",
               "story": "It has been celebrated since 1999. On social media the idea that men deserve flowers too became popular: blue roses, sunflowers or Hot Wheels bouquets to break the habit of only giving flowers to women."},
    "nochebuena": {"name": "National Poinsettia Day (Mexico)", "flower": "Poinsettia (cuetlaxóchitl)", "region": "Mexico",
                   "story": "The Christmas flower is Mexican: in Nahuatl it is called cuetlaxóchitl. On December 8 its origin is celebrated and the season for giving and decorating with it begins."},
    "guadalupe": {"name": "Our Lady of Guadalupe", "flower": "Roses", "region": "Mexico",
                  "story": "According to tradition, in 1531 Juan Diego carried roses from Tepeyac hill in his cloak (tilma), in the middle of December. That is why every December 12 millions of people bring roses to the Basilica."},
}
SONGS = {
    "amarillas-marzo": {"title": "Flores amarillas (Yellow flowers)", "by": "Floricienta (Florencia Bertotti), 2004"},
    "amarillas": {"title": "Flores amarillas (Yellow flowers)", "by": "Floricienta (Florencia Bertotti), 2004"},
    "moradas": {"title": "Un ramito de violetas (A little bunch of violets)", "by": "Cecilia, 1975 · viral version by Zalo Reyes"},
}

SEASON_REGIONS = {"es": "Spain", "mx": "Mexico and Central America", "sur": "Argentina, Chile and Uruguay"}
SEASON = [
    {"es": ["mimosa", "anemone", "ranunculus", "tulip", "daffodil", "camellia"],
     "mx": ["rose", "calla lily", "gerbera", "baby’s breath (gypsophila)", "carnation"],
     "sur": ["sunflower", "hydrangea", "agapanthus", "lavender", "gladiolus"]},
    {"es": ["mimosa", "tulip", "anemone", "ranunculus", "daffodil", "violet"],
     "mx": ["rose", "calla lily", "carnation", "gerbera", "sunflower"],
     "sur": ["sunflower", "dahlia", "hydrangea", "zinnia", "gladiolus"]},
    {"es": ["tulip", "daffodil", "ranunculus", "freesia", "hyacinth", "violet"],
     "mx": ["sunflower", "calla lily", "daisy", "gerbera", "lilium"],
     "sur": ["dahlia", "chrysanthemum", "rose", "aster", "lisianthus"]},
    {"es": ["tulip", "lilac", "ranunculus", "freesia", "stock", "rose"],
     "mx": ["calla lily", "lilium", "gerbera", "carnation", "daisy"],
     "sur": ["chrysanthemum", "rose", "dahlia", "aster", "lisianthus"]},
    {"es": ["peony", "rose", "carnation", "lilac", "iris", "lily of the valley"],
     "mx": ["rose", "carnation", "lilium", "gerbera", "sunflower"],
     "sur": ["chrysanthemum", "rose", "camellia", "lilium", "alstroemeria"]},
    {"es": ["peony", "rose", "hydrangea", "lavender", "daisy", "sunflower"],
     "mx": ["sunflower", "gladiolus", "tuberose", "hydrangea", "rose"],
     "sur": ["camellia", "calla lily", "alstroemeria", "carnation", "rose"]},
    {"es": ["sunflower", "lavender", "hydrangea", "dahlia", "gladiolus", "zinnia"],
     "mx": ["sunflower", "gladiolus", "tuberose", "dahlia", "hydrangea"],
     "sur": ["mimosa (aromo)", "camellia", "calla lily", "hyacinth", "carnation"]},
    {"es": ["sunflower", "dahlia", "gladiolus", "zinnia", "hydrangea", "lisianthus"],
     "mx": ["dahlia", "gladiolus", "tuberose", "sunflower", "daisy"],
     "sur": ["mimosa (aromo)", "freesia", "daffodil", "hyacinth", "tulip"]},
    {"es": ["dahlia", "sunflower", "rose", "aster", "chrysanthemum", "hydrangea"],
     "mx": ["dahlia", "sunflower", "cempasúchil (from late in the month)", "gerbera", "rose"],
     "sur": ["freesia", "tulip", "ranunculus", "daffodil", "lilac", "sunflower (greenhouse)"]},
    {"es": ["chrysanthemum", "dahlia", "rose", "aster", "hypericum"],
     "mx": ["cempasúchil", "cockscomb (terciopelo)", "baby’s breath (gypsophila)", "chrysanthemum", "rose"],
     "sur": ["rose", "lilium", "lilac", "stock", "ranunculus"]},
    {"es": ["chrysanthemum", "anemone", "amaryllis", "hellebore", "rose"],
     "mx": ["cempasúchil", "cockscomb (terciopelo)", "chrysanthemum", "poinsettia", "calla lily"],
     "sur": ["peony", "rose", "lilium", "jasmine", "lavender"]},
    {"es": ["poinsettia", "amaryllis", "anemone", "hellebore", "ranunculus", "cyclamen"],
     "mx": ["poinsettia", "rose", "calla lily", "gerbera", "carnation"],
     "sur": ["hydrangea", "lilium", "agapanthus", "lavender", "peony"]},
]
SEASON_NOTE = ("In Colombia, Ecuador and the Andes, the high-altitude climate lets growers produce roses, "
               "carnations, chrysanthemums, alstroemerias and hydrangeas all year round: that is why they are "
               "two of the world’s largest flower exporters.")

# name = nombre de la flor; match = palabras de la tabla de temporada que enlazan a su página.
FLOWERS = {
    "rosa": {"name": "Rose", "match": ["rose"]},
    "girasol": {"name": "Sunflower", "match": ["sunflower"]},
    "tulipan": {"name": "Tulip", "match": ["tulip"]},
    "peonia": {"name": "Peony", "match": ["peony"]},
    "clavel": {"name": "Carnation", "match": ["carnation"]},
    "margarita": {"name": "Daisy", "match": ["daisy"]},
    "lilium": {"name": "Lily (lilium)", "match": ["lilium"]},
    "hortensia": {"name": "Hydrangea", "match": ["hydrangea"]},
    "violeta": {"name": "Violet", "match": ["violet"]},
    "crisantemo": {"name": "Chrysanthemum", "match": ["chrysanthemum"]},
    "cempasuchil": {"name": "Cempasúchil", "match": ["cempasúchil"]},
    "mimosa": {"name": "Mimosa", "match": ["mimosa"]},
    "lirio-de-los-valles": {"name": "Lily of the valley", "match": ["lily of the valley"]},
    "nochebuena": {"name": "Poinsettia", "match": ["poinsettia"]},
}

GUIDES = {
    "flores-amarillas": {"name": "Yellow flowers", "small": "Sep 21", "desc": "Why they are given on September 21"},
    "flores-amarillas-21-de-marzo": {"name": "Yellow flowers on March 21", "small": "Mar 21", "desc": "Mexico’s spring version"},
    "flores-azules": {"name": "Blue flowers", "small": "Oct 3 · Nov 19", "desc": "Boyfriend Day, Hot Wheels and Men’s Day"},
    "flores-moradas": {"name": "Purple flowers", "small": "Nov 9", "desc": "The purple person and “Un ramito de violetas”"},
    "san-valentin": {"name": "Valentine’s Day", "small": "Feb 14", "desc": "Red roses and the other Valentine’s Days of the year"},
    "dia-de-la-mujer": {"name": "Women’s Day (8M)", "small": "Mar 8", "desc": "Mimosa, tulips and when giving flowers makes sense"},
    "dia-del-padre": {"name": "Father’s Day", "small": "Mar 19 · Jun", "desc": "Flowers for dad and the date in each country"},
    "sant-jordi": {"name": "Sant Jordi", "small": "Apr 23", "desc": "Why people give a rose and a book"},
    "dia-de-la-madre": {"name": "Mother’s Day", "small": "May · Oct", "desc": "Which flowers to give and the date in each country"},
    "dia-del-maestro": {"name": "Teachers’ Day", "small": "May 15 and more", "desc": "Flowers for your teacher and the date in each country"},
    "dia-de-la-novia": {"name": "Girlfriend Day", "small": "Aug 1", "desc": "Latin America’s second Valentine’s Day"},
    "amor-y-amistad": {"name": "Amor y Amistad", "small": "3rd Sat Sep", "desc": "Colombia’s Valentine’s Day, for partners and friends"},
    "todos-los-santos-dia-de-muertos": {"name": "All Saints’ Day and Day of the Dead", "small": "Nov 1 & 2", "desc": "Chrysanthemum and cempasúchil"},
    "nochebuena": {"name": "Poinsettia", "small": "Dec 8", "desc": "Mexico’s Christmas flower"},
    "virgen-de-guadalupe": {"name": "Our Lady of Guadalupe", "small": "Dec 12", "desc": "Why people bring roses to the Basilica"},
    "flores-para-cumpleanos": {"name": "Birthday flowers", "small": "All year", "desc": "Which bouquet to give depending on the person"},
    "flores-para-aniversario": {"name": "Anniversary flowers", "small": "All year", "desc": "Which flowers to give by years together"},
    "flores-para-condolencias": {"name": "Sympathy flowers", "small": "When needed", "desc": "What to send to a funeral and what to write"},
    "significado-colores-flores": {"name": "Flower color meanings", "small": "All year", "desc": "What each color says and when to give it"},
}

# Tarjetas de los índices: (texto pequeño, nombre, descripción).
HUB_CARDS = {
    "meses": ("Calendar", "Flowers by month", "What to give and what’s in season each month"),
    "flores": ("Calendar", "Flowers A to Z", "Meaning and season of each flower"),
    "guias": ("Calendar", "All guides", "Dates and occasions for giving flowers"),
    "paises": ("Calendar", "Dates by country", "Spain, Mexico, Argentina, Colombia, Chile and Peru"),
}

# Textos de SITE que cambian con el idioma.
SITE = {
    "author_bio": "Developer in training (Multiplatform Application Development). He created Florario to gather in one place the dates on which flowers are given in Spain and Latin America, and he checks every date and every trend against at least two media outlets from different countries before publishing it.",
}
