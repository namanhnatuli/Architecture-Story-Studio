# Gói duyệt biên tập: "How Gothic Cathedrals Reached Impossible Heights" (narration `g-r3`)

> **Đang chờ duyệt.** Agent soạn gói này nhưng không tự duyệt claim, giọng hay phát âm. Tới khi chủ kênh duyệt, mọi bản dựng mang nhãn INTERNAL REVIEW.

## Cần chủ kênh quyết định

1. Lời dẫn: mỗi câu đúng với claim nó trích (xem cột trích dẫn nguồn).
2. Chữ trên card: tiêu đề, nhãn, chú thích ảnh, thang nhịp và dòng thời gian.
3. Ảnh lưu trữ: chọn ảnh, cách cắt viền phim, dòng ghi công (xem `review/RIGHTS_PROVENANCE.md`).
4. Nhãn 'Illustrative model' trên các mô hình 3D (B05, B07, B12, B13, B16, B17).
5. Phát âm các tên mới (narration.voice.pronunciation_review.terms).
6. Giọng: quyền dùng `am_michael` cho phim này (licence LICENSE_REVIEW_REQUIRED, owner_confirmation_for_this_film = PENDING).

Cách ghi quyết định (agent chỉ ghi lại lời chủ kênh; xem `docs/production/NEW_DOCUMENTARY_PLAYBOOK.md` bước 23): `research/editorial_approval.json` (id claim, `claims_text_sha256`, `narration_revision` của revision này), rồi chạy `research/build_sources.py`; `project.json` → `factual_review: verified`; `narration.voice.pronunciation_review` (`ACCEPTED_BY_OWNER` hoặc `CONFIRMED`, gắn với hash audio); `review/OWNER_APPROVALS.json`.

## Các điểm cần lưu ý (agent tự nêu)

- Không có.

## Lời dẫn theo câu


### C1 · Hook

**B01** (fact; claim: CLM_103, CLM_104, CLM_106, CLM_181, CLM_182)

- `0:00` In November 1284, in the French city of Beauvais, part of the highest stone vaults of the Middle Ages came down.
- `0:09` They stood more than 45 meters above the floor.
- `0:13` The choir beneath them, the eastern arm of the cathedral, had been in use for just twelve years.
  - CLM_103: SRC_ISSMGE_BEAUVAIS_1 Abstract (English): "Saint Peter’s cathedral in Beauvais (France) has the highest vaults ever built during the Middle Ages. It was affected by two famous structural accidents, in the choir in 1284, and later at the transept crossing, in 1573."
  - CLM_104: SRC_ABC_HISTORY Around 1260, the choir is completed: "Its vault rises to nearly 47 m, 4 m higher than Amiens. It is the tallest Gothic stone vault in the world." · SRC_ABC_DESCRIPTION The choir: "The choir has the tallest vault of any Gothic choir: 46.7 m." · SRC_ABC_FRENCH_ART The 13th century: "Its choir vaults rise above 48 metres" · SRC_CU_AMIENS_UPPER_NAVE Amiens Cathedral, upper nave, north: "Amiens at 43.3 meters is a little lower than Beauvais at 46m." · SRC_CU_MURRAY_PHASE3 Phase III: "In royal feet of thirty-two and a half centimeters the keystones of the vaults are about 144 feet above the pavement" — giả định: The figures disagree, even within one association's pages (nearly 47 m, 46.7 m, above 48 m; Columbia: 46 m). The narration says only 'more than 45 meters', which all of them support, and the card lists the published figures, from 46 m to above 48 m (owner's script review, 2026-11-05). Murray's 144 royal feet of 32.5 cm come to about 46.8 m, the agent's multiplication.
  - CLM_106: SRC_CU_AMIENS_ETEXT_11 E-Text 11: "The eastern arm of the cathedral is commonly called the choir" · SRC_CU_AMIENS_ETEXT_4 E-Text 4: "the long, boat-like body of the cathedral is intersected by a cross-arm or transept" — giả định: E-Text 11 adds that the term is 'something of a misnomer' because the choir proper is where the clergy sat; the film uses the common meaning. 'Crossing piers' is the term used in CLM_190.
  - CLM_181: SRC_ISSMGE_BEAUVAIS_1 2.1.2 1225-1340: "Dans les années 1250, les deux premiers niveaux de construction étant achevés (grandes arcades et triforium), l’évêque Guillaume de Grès décida apparemment pour le troisième et dernier étage de l’édifice de sortir des proportions prévues originellement en ajoutant quelques mètres (de l’ordre de cinq) aux fenêtres hautes et donc aux voûtes. En 1272, le nouveau chœur put être occupé par le clergé" — giả định: 'Apparemment': the paper presents the decision as probable, and the film says 'apparently'.
  - CLM_182: SRC_ISSMGE_BEAUVAIS_1 2.1.2 1225-1340: "Le 29 novembre 1284, durant cette nouvelle phase de chantier, des voûtains des travées droites du chœur, les plus vulnérables, s’effondrèrent" · SRC_ISSMGE_BEAUVAIS_1 2.1.2 1225-1340: "« la dernière limite à laquelle la construction des grandes églises du XIIIe s. ait pu arriver »" · SRC_ISSMGE_BEAUVAIS_1 2.1.2 1225-1340: "chantier qui s’en suivi s’acheva en 1340. « On mit donc plus de temps à réparer le chœur qu’à le construire » (Murray, 2000)." · SRC_ISSMGE_BEAUVAIS_2 2.1 Cause d’après les sources: "la durée de stabilité de 12 ans des parties hautes" — giả định: The film shows no collapse or destruction; it says 'in 1284' (the association gives 'a Friday in November 1284').

**B02** (fact; claim: CLM_110, CLM_101, CLM_102, CLM_156)

- `0:21` And yet many buildings like it are still standing.
- `0:25` At Amiens, begun in 1220, the vault rises more than 42 meters, in a building that is tall, slender and filled with light.
  - CLM_110: SRC_MIT_BLOCK_2005 1.1 Introduction, p. 9: "The master builders of the Middle Ages were able to use geometrical rules, developed through centuries of trial and error, to build structural elements by scaling up the same proportions for new larger elements [Huerta 2004]. In those days, there was no knowledge of material properties or allowable stresses." · SRC_MIT_BLOCK_2005 1.1 Introduction, p. 9: "Yet, many of these architectural marvels are still standing in a state of equilibrium." · SRC_MIT_BLOCK_2006 Graphic Statics, p. 10: "Culmann [1866] was the first to formalize graphical analysis as a powerful method for equilibrium analysis in structural engineering." · SRC_CU_AMIENS_GEOMETRY 1. Ease and Security of Construction: "The templates necessary for manufacturing the elements of multiple piers, windows and vaults were designed with straight-edge and compass." — giả định: Block writes 'no knowledge of material properties or allowable stresses'. The film does not repeat that phrase (owner's script review, 2026-11-05): heard alone it denies the builders' practical knowledge, which the film itself shows (CLM_121, CLM_170, CLM_172, CLM_173). 'Without modern structural calculations' is the narrower reading: formal structural analysis came centuries later.
  - CLM_101: SRC_CU_AMIENS_ETEXT_1 E-Text 1, paragraph 2: "beginning in 1220 with the start of work on a new cathedral after a disastrous fire" · SRC_CU_AMIENS_MASONS First Phase, c.1220-25: "An inscription on the south transept façade records that the foundation stone was laid in 1220" · SRC_CU_AMIENS_ETEXT_1 E-Text 1, paragraph 2: "The main roof was not finished until c.1310."
  - CLM_102: SRC_CU_AMIENS_UPPER_NAVE Amiens Cathedral, upper nave, north: "Amiens at 43.3 meters is a little lower than Beauvais at 46m." · SRC_ABC_HISTORY Around 1260, the choir is completed: "Its vault rises to nearly 47 m, 4 m higher than Amiens." — giả định: Published heights differ: Columbia gives Amiens 43.3 m and Beauvais 46 m; the Beauvais association gives Beauvais nearly 47 m and 4 m more than Amiens. The film says only 'more than 42 metres' for Amiens and 'more than 45 metres' for Beauvais, which all of these support.
  - CLM_156: SRC_CU_AMIENS_UPPER_NAVE Amiens Cathedral, upper nave, north: "These are "flying buttresses" (arcs boutants) that allowed the builders to create such tall, slender, light-filled stuctures. The first flying buttresses had been deployed some eighty years earlier and builders learned how to exploit them to achieve cathedrals that were ever taller." · SRC_CU_AMIENS_UPPER_NAVE Amiens Cathedral, upper nave, north: "The upper nave was built by Master Thomas de Cormont in the 1230s."

**B03** (fact; claim: CLM_110)

- `0:36` The people who built them worked without modern structural calculations, relying on geometry, craft knowledge and experience.
- `0:45` So how did they raise stone that high?
- `0:48` And why, sometimes, did it come down?
  - CLM_110: SRC_MIT_BLOCK_2005 1.1 Introduction, p. 9: "The master builders of the Middle Ages were able to use geometrical rules, developed through centuries of trial and error, to build structural elements by scaling up the same proportions for new larger elements [Huerta 2004]. In those days, there was no knowledge of material properties or allowable stresses." · SRC_MIT_BLOCK_2005 1.1 Introduction, p. 9: "Yet, many of these architectural marvels are still standing in a state of equilibrium." · SRC_MIT_BLOCK_2006 Graphic Statics, p. 10: "Culmann [1866] was the first to formalize graphical analysis as a powerful method for equilibrium analysis in structural engineering." · SRC_CU_AMIENS_GEOMETRY 1. Ease and Security of Construction: "The templates necessary for manufacturing the elements of multiple piers, windows and vaults were designed with straight-edge and compass." — giả định: Block writes 'no knowledge of material properties or allowable stresses'. The film does not repeat that phrase (owner's script review, 2026-11-05): heard alone it denies the builders' practical knowledge, which the film itself shows (CLM_121, CLM_170, CLM_172, CLM_173). 'Without modern structural calculations' is the narrower reading: formal structural analysis came centuries later.


### C2 · Stone and its outward push

**B04** (fact; claim: CLM_111)

- `0:52` Start with the stone itself.
- `0:55` Stone has little or no strength when it is pulled apart.
- `0:59` So a stone building stands largely by keeping its stones pressed together.
  - CLM_111: SRC_MIT_BLOCK_2005 1.1 Introduction, p. 9: "masonry has no tensile strength; it can resist infinite compression; and no sliding will occur within the masonry." · SRC_MIT_BLOCK_2005 3.2, p. 19: "Stone has no or very little tensile capacity, so, the structure would collapse if it cannot contain a thrust line in compression." — giả định: These are the assumptions of limit analysis (Heyman), and the film states them as such: 'never crush' is its plain wording of 'infinite compression'.

**B05** (fact; claim: CLM_120, CLM_121)

- `1:05` Now put a heavy stone vault on top of two walls.
- `1:09` A vault does not simply press down: it also pushes outward, like a bow being bent.
- `1:16` That outward push is called thrust, and a document from Amiens shows that builders there were well aware of it.
  - CLM_120: SRC_ABC_THRUST The Romanesque problem: "A vault, whatever its shape, does not simply press downward: it also pushes outward, like a bow being bent." · SRC_ABC_THRUST What is “thrust”?: "In structural mechanics, thrust is the horizontal component of the force exerted by a vault or an arch on its support."
  - CLM_121: SRC_CU_AMIENS_POINTED_ARCH The Pointed Arch: "A contemporary document reveals that the builders were well aware of the existence of "thrust" in the arcade arches--it is termed boutture." — giả định: 'Contemporary' refers to the late-medieval Amiens context of the paragraph (the 1497 crisis); the film says only that builders there knew about it, not that every medieval builder did.

**B06** (fact; claim: CLM_122)

- `1:25` Romanesque builders had several ways of covering a great church.
- `1:30` In the barrel-vaulted type shown here, the heavy vault pushes outward along the whole length of the wall, so walls and supports are thick, stiffened by buttresses.
- `1:41` Large openings would weaken the wall that holds the vault, so windows tend to stay small.
  - CLM_122: SRC_CU_AMIENS_REVOLUTION Antithesis (Romanesque): "Since the heavy masonry of the vaulting creates considerable outward thrust it has been necessary to thicken the main supports (no longer columns but compound piers) and outer walls which are stiffened by shallow buttresses. Windows are small. The interior is now dark" · SRC_ABC_THRUST The Romanesque problem: "In Romanesque architecture, this oblique thrust is spread along the entire length of the wall, which must therefore be thick and pierced with only small openings to remain stable." · SRC_CU_STALLEY_STRUCTURE Development of the Vaulted Ceiling: "By the late eleventh century various alternative ways of vaulting the main spaces of a great church were available to medieval masons" · SRC_CU_STALLEY_STRUCTURE Development of the Vaulted Ceiling: "whereas stone vaulting was eschewed altogether in east Anglia" — giả định: Limited to the type illustrated, because Stalley lists barrel vaults, groin vaults and wooden ceilings around 1100. Columbia's page also calls the interior 'dark'; the film drops that word (owner's script review, 2026-11-05), so as not to set a dark Romanesque against a bright Gothic.

**B07** (fact; claim: CLM_123, CLM_153)

- `1:49` Gothic builders rearranged that system of support.
- `1:54` Instead of spreading the push along a thick wall, they directed it toward particular points, and carried it to supports outside.
- `2:03` Three tools made that possible: the pointed arch, the rib vault, and the flying buttress.
  - CLM_123: SRC_ABC_THRUST Introduction: "master builders stopped fighting the thrust of vaults with sheer wall thickness. They learned to channel it instead. Three technical innovations made this revolution possible: the pointed arch, the ribbed vault, and the flying buttress." · SRC_CU_AMIENS_ETEXT_18 E-Text 18: "This revolution is made possible through the use of pointed arches and lightweight rib vaults, but above all by the creation of rigid peripheral supports ( culées) from which flying buttresses can be launched to support the high vaults." — giả định: The association's wording ('stopped fighting ... with sheer wall thickness') is broader than this claim, which follows B07 (owner's script review, 2026-11-05). Columbia's 'rigid peripheral supports' backs the narrower wording; mass and buttressing still mattered.
  - CLM_153: SRC_CU_AMIENS_REVOLUTION Synthesis (Gothic): "It is as if the outer wall (labeld F) has been broken into segments, each of which is rotated 90 degrees to provide rigid transverse supports for exposed arches (flying buttresses) which support the high vaults."


### C3 · The pointed arch

**B08** (fact; claim: CLM_130, CLM_134)

- `2:10` A pointed arch is two arcs of a circle that meet at a point.
- `2:15` Over the same span, it can rise higher than a round arch, and a taller arch can push less to the sides.
- `2:22` How much less depends on its exact shape, its thickness and the weight it carries.
- `2:28` One comparison by MIT engineers, of two other arches, did find that the pointed one pushed less, but that result belongs to those two arches, not to every arch.
  - CLM_130: SRC_ABC_THRUST Innovation No. 1: "the pointed arch is formed by two arcs of a circle meeting at a point." · SRC_BNF_ARC_BRISE Arc brisé et voûte sur croisée d’ogive: "Il a pour avantage d’exercer des poussées latérales réduites, ce qui permet de l’élever nettement plus haut." · SRC_CU_AMIENS_REVOLUTION Synthesis (Gothic): "The pointed arch. Appropriated from Islamic sources and applied to reduce outward thrust." · SRC_MIT_ROMANO Comparison of Pointed vs. Circular Arches: "In Gothic cathedrals the use of pointed arches is widespread because of the decreased thrust compared to the circular arch. While this fact is widely acknowledged and accepted, there has been little theory developed to determine exactly the different behavior of the two arches." · SRC_MIT_ROMANO Comparison of Pointed vs. Circular Arches: "a parametric study of whole and half arches has been performed varying the angle of embrace, the thickness and the eccentricity of the centers of the arches" · SRC_MIT_BLOCK_2006 Arch on spreading supports, p. 16: "This makes sense since the deforming arch becomes more and more shallow, resulting in an increase of horizontal thrust." — giả định: BnF and Columbia state the reduction without conditions; the film adds them (owner's script review, 2026-11-05). 'Half its span' is the geometry of a semicircle. The link between shallowness and thrust is quoted from an arch on spreading supports, so the film says 'can', and gives no general figure.
  - CLM_134: SRC_MIT_BLOCK_2006 Semi-circular versus pointed arch, p. 14: "The two arches of fig. 4 have the same thickness to radius (t/R) ratio of 18%." · SRC_MIT_BLOCK_2006 Semi-circular versus pointed arch, p. 14: "Their minimum and maximum thrusts, expressed as a percentage of their self-weight, are respectively 16% and 25% for the semicircular arch (fig. 4a), and 14% and 23% for the pointed arch (fig. 4b)." · SRC_MIT_BLOCK_2006 Semi-circular versus pointed arch, p. 14: "However, the pointed arch thrusts about 15% less than the circular arch." — giả định: The paper's text says 'about 15% less', while its own rounded figures give about 12.5% (minimum) and 8% (maximum). The film narrates no percentage and shows none (owner's second review, 2026-11-05): the arches on the card are not those of the study, and the ranges would need the study's geometry and an explanation of minimum and maximum thrust.

**B09** (fact; claim: CLM_114, CLM_115)

- `2:42` In 1675, the scientist Robert Hooke summed up an idea about arches in one line.
- `2:50` As hangs the flexible line, so but inverted will stand the rigid arch.
- `2:56` Hang a chain with a set of weights, and it takes a shape.
- `3:00` Turn that shape upside down, and it shows a path the force can follow through an arch carrying the same weights.
- `3:08` Change the weights, and the shape changes too.
  - CLM_114: SRC_MIT_BLOCK_2005 Preface, p. 7: "written by Robert Hooke (1635-1703) in 1675" · SRC_MIT_BLOCK_2005 Preface, footnote 1: "As hangs the flexible line, so but inverted will stand the rigid arch, translation by Heyman [1995]."
  - CLM_115: SRC_MIT_BLOCK_2006 Robert Hooke's hanging chain, p. 10: "Generalized, this idea signifies that the shape a string takes under a set of loads, if rigidified and inverted, illustrates a path of compressive forces for an arched structure to support the same set of loads." · SRC_MIT_BLOCK_2006 Robert Hooke's hanging chain, p. 10: "This shape of the string and the inverted arch is called a funicular shape for these loads."

**B10** (fact; claim: CLM_131)

- `3:12` The pointed arch was not a Gothic invention.
- `3:16` It already appears in Burgundy, at the great abbey church of Cluny, whose construction began around 1088, and Columbia University's Amiens project traces it to Islamic sources.
- `3:30` At the abbey of Saint-Denis, it was used systematically, together with the other new ideas.
  - CLM_131: SRC_ABC_THRUST Innovation No. 1: "The pointed arch was not born with Gothic art: examples already appear in Burgundian Romanesque architecture, notably on the rebuilding site of the abbey of Cluny (Cluny III), around 1088. It was at the abbey of Saint-Denis, under Abbot Suger between 1130 and 1144, that it was used systematically and combined with the other Gothic innovations." · SRC_CU_AMIENS_REVOLUTION Synthesis (Gothic): "The pointed arch. Appropriated from Islamic sources" · SRC_CMN_CLUNY Maior ecclesia: "In 1088 , he planned the construction of a new and ever larger abbey church" · SRC_BNF_ARC_BRISE Arc brisé et voûte sur croisée d’ogive: "L’art roman privilégie l’arc en plein cintre (qui dessine un demi-cercle parfait), même s’il utilise à l’occasion l’arc brisé." · SRC_HARVARD_CLUNY The abbey church: "The last and greatest of these, begun in 1088" · SRC_HARVARD_CLUNY The abbey church: "was among the earliest buildings north of the Alps to have an ambulatory with radiating chapels, pointed arches, and flying buttresses in the nave" · SRC_NCE_CLUNY Cluny III: "under its pointed, ribbed barrel vault (part of which collapsed in 1125 but was rebuilt by 1130)" — giả định: 1088 dates the building project (the monument's own page, Harvard), not the pointed arches themselves, so the film gives no year for the arches (owner's script review, 2026-11-05). The New Catholic Encyclopedia puts the church between its founding in 1088 and its dedication in 1130. Its 'for the first time on such a scale' is not used.

**B11** (fact; claim: CLM_132)

- `3:38` It had a subtler advantage too.
- `3:41` Unlike a round arch, a pointed arch can span sections of different widths, called bays, and still reach the same height at its crown.
- `3:50` That was a valuable asset for keeping complex vaults regular.
  - CLM_132: SRC_ABC_THRUST Innovation No. 1: "unlike the round arch, the pointed arch allows bays of different widths to be spanned while keeping the same keystone height — a valuable asset for regularising complex vaults." · SRC_CU_STALLEY_STRUCTURE Development of the Vaulted Ceiling: "The exploitation of the pointed arch in this position allowed the apex of the vault to be kept level throughout its length" · SRC_CU_STALLEY_STRUCTURE Development of the Vaulted Ceiling: "While it could be argued that pointed arches were first introduced into English architecture to solve a geometrical problem, they may also have helped to improve the stability of the vault." — giả định: Geometric property also shown on the card: a semicircular arch's rise is half its span. Stalley's second sentence is why the film treats the pointed arch as a geometric tool first.


### C4 · The rib vault

**B12** (fact; claim: CLM_140)

- `3:56` The second tool is the rib vault.
- `4:00` In the four-part vault shown here, two ribs cross diagonally over each bay of the building.
- `4:06` In this simplified picture, they direct the vault's load toward four points: the piers, or stone pillars, at its corners.
  - CLM_140: SRC_ABC_THRUST Innovation No. 2: "two pointed arches cross diagonally above each bay, gathering the vault’s load onto four precise points — the corner piers." · SRC_BNF_SAINT_DENIS Une nouvelle conception de la spiritualité: "Elle dirige les poussées de la voûte sur des piliers, et non plus sur des murs" · SRC_CU_STALLEY_DESCRIBE The Interior Elevations: "It is important to note that the diagonal ribs are depressed, following only a segment of a circle" · SRC_CU_STALLEY_DESCRIBE The Interior Elevations: "These transverse arches are pointed in profile" — giả định: Both quoted sources simplify, and how such vaults stand is debated (CLM_141), so the film says 'in this simplified picture' (owner's script review, 2026-11-05). The association and BnF call the crossing ribs 'two pointed arches'; Stalley describes Durham's diagonal ribs as segments of a circle and its pointed arches as transverse, so the film says only 'two ribs'.

**B13** (fact; claim: CLM_141)

- `4:16` How exactly these vaults stand has been debated for centuries.
- `4:21` Engineers following Jacques Heyman assume that the main ribs bring the forces down, and treat the stone between them as a series of parallel arches.
- `4:32` So even in that reading, the stone between the ribs carries load.
  - CLM_141: SRC_MIT_BLOCK_2005 3.6 Gothic quadripartite vault, p. 23: "The structural behavior of the quadripartite vault has been the focus of debate for centuries." · SRC_MIT_BLOCK_2005 3.6 Gothic quadripartite vault, p. 23: "We use the assumptions made by Heyman that the main ribs bring down the forces to the buttresses and the web is considered to be a collection of parallel arches spanning between the cross ribs" — giả định: One analysis's assumptions for four-part vaults, attributed as such. 'The web carries load' follows from treating it as arches spanning between the ribs.

**B14** (fact; claim: CLM_142)

- `4:38` Ribs were not new either.
- `4:41` Durham Cathedral in England, begun in 1093, was completely covered by ribbed vaults by the time it was finished in 1133.
- `4:51` Its masons refined them in phases over some forty years.
- `4:56` Columbia's project traces ribs to Islamic, Roman and Byzantine sources.
  - CLM_142: SRC_CU_STALLEY_STRUCTURE Development of the Vaulted Ceiling: "When Durham Cathedral was completed in 1133 it was the first building in England to be completely covered by ribbed vaults" · SRC_CU_STALLEY_STRUCTURE Development of the Vaulted Ceiling: "there is no question that the Durham masons learnt to handle ribbed vaulting with increasing assurance over the course of forty years. The structure of the vaults falls into at least three technical phases" · SRC_DURHAM_CATHEDRAL The Norman cathedral: "Between 1093 and 1133, Durham Cathedral was completely rebuilt by the Normans" · SRC_CU_AMIENS_REVOLUTION Synthesis (Gothic): "The ribbed vault. Also from Islamic, Roman and Byzantine sources" — giả định: 1093 is when the building began, not a date for any vault (owner's script review, 2026-11-05). The association's 'very first ribbed vaults ... as early as 1093' is no longer used, and the film says nothing about who was first: Stalley calls that contentious for northern Europe.

**B15** (fact; claim: CLM_143)

- `5:03` This kind of vault changes the job of the wall.
- `5:07` With the vault's load directed toward the piers, the wall between them was no longer its main support.
- `5:15` It could be thinned, and opened up with wide windows.
  - CLM_143: SRC_ABC_THRUST Innovation No. 2: "Direct consequence: between the piers, the walls no longer carry any load. They can be thinned, hollowed out, and eventually replaced with wide glazed openings." · SRC_BNF_ARC_BRISE La voûte sur croisée d’ogive: "Les murs perdent ainsi leur rôle de soutien, et peuvent être percés de larges ouvertures." — giả định: The sources are absolute ('no longer carry any load', 'perdent ainsi leur rôle de soutien'). The film says 'main support': a wall still carries at least its own weight, and how vaults stand is debated (CLM_141).


### C5 · The flying buttress

**B16** (fact; claim: CLM_150)

- `5:20` But gathering the thrust does not make it go away.
- `5:24` Even reduced, that sideways push remains a threat to the stability of the whole building.
- `5:31` It still has to be contained somewhere.
  - CLM_150: SRC_BNF_ARCS_BOUTANTS Les arcs-boutants: "Ces structures sont plus légères mais toujours présentes, car les poussées latérales, même réduites, demeurent une menace pour la stabilité de l’ensemble." · SRC_ABC_THRUST Innovation No. 3: "The ribbed vault concentrates thrust onto piers, but that thrust still has to be contained somewhere."

**B17** (fact; claim: CLM_151, CLM_152)

- `5:35` The answer stands outside the building: the flying buttress.
- `5:40` It is a stone arch that picks up the thrust where it leaves the vault, carries it across the aisle roof, and brings it down to a massive pier buttress.
- `5:50` Often a pinnacle on top adds weight, to help stabilize the thrust.
  - CLM_151: SRC_BNF_ARCS_BOUTANTS Les arcs-boutants: "Pour contrer les poussées exercées sur les murs par les voûtes, les églises romanes les renforcent par des contreforts, renforts de maçonnerie en saillie accolés au mur extérieur." · SRC_BNF_ARCS_BOUTANTS Les arcs-boutants: "Dans les édifices gothiques, les contreforts deviennent des arcs-boutants, comme des contreforts éloignés de la paroi et évidés en arc."
  - CLM_152: SRC_ABC_THRUST Innovation No. 3: "this external arch picks up the thrust at the point where it leaves the vault, carries it across the aisle roof, and channels it down to a massive pier buttress, often topped with a pinnacle that weighs it down to better stabilise the thrust."

**B18** (fact; claim: CLM_153)

- `5:57` One way to picture it comes from Columbia's Amiens project.
- `6:01` It is as if the thick outer wall had been cut into segments, and each segment turned 90 degrees.
- `6:09` Those segments become rigid supports, standing out from the building, with exposed arches reaching up to the high vaults.
  - CLM_153: SRC_CU_AMIENS_REVOLUTION Synthesis (Gothic): "It is as if the outer wall (labeld F) has been broken into segments, each of which is rotated 90 degrees to provide rigid transverse supports for exposed arches (flying buttresses) which support the high vaults."

**B19** (fact; claim: CLM_154, CLM_155)

- `6:18` According to France's national library, the first flying buttresses were used to consolidate Romanesque churches that threatened to collapse.
- `6:28` It also says that the slanting timber props used while building the vaults were, in effect, made permanent in stone.
- `6:37` At Chartres, flying buttresses were part of the original plans.
- `6:42` And around the east end of Notre-Dame in Paris, they look almost like a giant external skeleton.
  - CLM_154: SRC_BNF_ARCS_BOUTANTS Les arcs-boutants: "Les premiers arcs-boutants ont été utilisés pour consolider les églises romanes qui menaçaient de s’effondrer." · SRC_BNF_ARCS_BOUTANTS Les arcs-boutants: "C’est lors de la construction de la cathédrale de Chartres que les arcs-boutants sont intégrés pour la première fois dans les plans d’origine" · SRC_BNF_ARCS_BOUTANTS Les arcs-boutants: "À Notre-Dame de Paris, les immenses arcs-boutants aériens qui soutiennent l’abside évoquent presque un gigantesque squelette externe !" · SRC_ABC_THRUST Innovation No. 3: "at Notre-Dame de Paris, systematic buttressing was put in place around 1180." — giả định: The BnF page says Chartres was the first time ('pour la première fois'). The film drops 'first' and says only 'part of the original plans': flying buttresses at Notre-Dame around 1180 are earlier, and whether those were planned from the start is a question the sources here do not settle.
  - CLM_155: SRC_BNF_ARCS_BOUTANTS Les arcs-boutants: "Les étais extérieurs obliques en bois utilisés par les maîtres ouvriers dans la construction des voûtes sont ainsi pérennisés et intégrés en pierre dans la structure de l’architecture gothique." — giả định: An explanation given by the BnF educational page; the film attributes it ('according to France's national library').

**B20** (fact; claim: CLM_156, CLM_157)

- `6:50` Flying buttresses even help carry rainwater off the roof.
- `6:55` But above all, builders learned how to exploit them, and cathedrals grew ever taller.
  - CLM_156: SRC_CU_AMIENS_UPPER_NAVE Amiens Cathedral, upper nave, north: "These are "flying buttresses" (arcs boutants) that allowed the builders to create such tall, slender, light-filled stuctures. The first flying buttresses had been deployed some eighty years earlier and builders learned how to exploit them to achieve cathedrals that were ever taller." · SRC_CU_AMIENS_UPPER_NAVE Amiens Cathedral, upper nave, north: "The upper nave was built by Master Thomas de Cormont in the 1230s."
  - CLM_157: SRC_BNF_ARCS_BOUTANTS Les arcs-boutants: "Les arcs-boutants servent aussi à l’évacuation de l’eau de pluie tombée sur le toit."


### C6 · Walls of light

**B21** (fact; claim: CLM_160, CLM_161)

- `7:02` Why go to all this trouble?
- `7:05` Part of the answer is light.
- `7:08` At the abbey church of Saint-Denis, Abbot Suger built a new choir between 1140 and 1144.
- `7:16` Pointed arches run throughout, every vault is ribbed, and monumental stained glass seems to dissolve the whole structure.
  - CLM_160: SRC_FM_TIMBERT_SAINT_DENIS paragraph 2: "Entre 1130 et 1140, l’abbé Suger (1122-1151) choisit de greffer sur la nef carolingienne de son abbatiale un massif de façade* voûté d’ogives* et structuré par des arcs brisés*. Puis, entre 1140 et 1144, il érigea un chevet*" · SRC_FM_TIMBERT_SAINT_DENIS Au-dessus de la crypte: "Ici, l’arc brisé est généralisé (fenêtres, arcs formerets* et doubleaux*), l’emploi de la voûte d’ogives est exclusif, les supports appareillés sont supplantés par des colonnes monolithes, les murs intermédiaires des chapelles sont élidés et, enfin, des vitraux monumentaux dématérialisent l’ensemble."
  - CLM_161: SRC_CU_SAINT_DENIS Significance and Basic Concepts: "For Suger light functioned as a sign or bridge to the divine." · SRC_CU_SAINT_DENIS Building Campaigns: "This Choir was built in new, gothic style and dedicated in 1144."

**B22** (fact; claim: CLM_161, CLM_164)

- `7:26` For Suger, light was a sign, a bridge to the divine.
- `7:30` France's national library says the new style had to let in as much light as possible.
  - CLM_161: SRC_CU_SAINT_DENIS Significance and Basic Concepts: "For Suger light functioned as a sign or bridge to the divine." · SRC_CU_SAINT_DENIS Building Campaigns: "This Choir was built in new, gothic style and dedicated in 1144."
  - CLM_164: SRC_BNF_SAINT_DENIS Le rôle clé de la lumière: "Le nouveau style de la basilique de Saint-Denis doit rendre sensible aux fidèles cette conception dès leur entrée dans l’édifice : il devient nécessaire d’y faire entrer un maximum de lumière."

**B23** (fact; claim: CLM_162)

- `7:38` At Chartres, some 2,500 square meters of stained glass survive, most of it original.
  - CLM_162: SRC_BNF_ARCS_BOUTANTS Notre-Dame de Chartres (image caption): "La cathédrale Notre-Dame de Chartres est la cathédrale gothique la plus représentative, la plus complète et la mieux conservée avec son dallage orné d’un labyrinthe, plus de 600 sculptures et 2 500 m2 de vitraux pour la plupart d’origine."

**B24** (fact; claim: CLM_163)

- `7:47` How new was all of this?
- `7:50` Some historians call Gothic a revolution in the art of building, while others see a creative step rooted in continuity.
- `7:59` Suger's own crypt still relies almost entirely on round arches and groin vaults.
  - CLM_163: SRC_CU_AMIENS_REVOLUTION The Gothic Structural Revolution: "Following Viollet-le-Duc's premise of Gothic understood as "An Entire Revolution in the Art of Building."" · SRC_FM_TIMBERT_SAINT_DENIS conclusion: "C’est pourquoi il n’y a pas de « révolution » et, donc, de rupture gothique, mais une proposition créative inscrite dans la permanence." · SRC_FM_TIMBERT_SAINT_DENIS La crypte: "La voûte d’arêtes et l’arc en plein cintre y sont employés de manière quasi exclusive." · SRC_ISSMGE_BEAUVAIS_1 1 Introduction: "Eugène Viollet-le-Duc, connu pour son œuvre de restauration de Notre-Dame de Paris au XIXe siècle" — giả định: Since g-r2 the narration gives the two readings without names (owner's script review, 2026-11-05); the card keeps the attributions in small type.


### C7 · Building by geometry

**B25** (fact; claim: CLM_110)

- `8:06` So how did they do all this, without modern structural calculations?
- `8:12` Master builders used geometrical rules, developed through centuries of trial and error.
- `8:19` They scaled up the same proportions for new, larger elements.
  - CLM_110: SRC_MIT_BLOCK_2005 1.1 Introduction, p. 9: "The master builders of the Middle Ages were able to use geometrical rules, developed through centuries of trial and error, to build structural elements by scaling up the same proportions for new larger elements [Huerta 2004]. In those days, there was no knowledge of material properties or allowable stresses." · SRC_MIT_BLOCK_2005 1.1 Introduction, p. 9: "Yet, many of these architectural marvels are still standing in a state of equilibrium." · SRC_MIT_BLOCK_2006 Graphic Statics, p. 10: "Culmann [1866] was the first to formalize graphical analysis as a powerful method for equilibrium analysis in structural engineering." · SRC_CU_AMIENS_GEOMETRY 1. Ease and Security of Construction: "The templates necessary for manufacturing the elements of multiple piers, windows and vaults were designed with straight-edge and compass." — giả định: Block writes 'no knowledge of material properties or allowable stresses'. The film does not repeat that phrase (owner's script review, 2026-11-05): heard alone it denies the builders' practical knowledge, which the film itself shows (CLM_121, CLM_170, CLM_172, CLM_173). 'Without modern structural calculations' is the narrower reading: formal structural analysis came centuries later.

**B26** (fact; claim: CLM_170)

- `8:24` At Amiens, setting out the site began with ropes pegged to the ground.
- `8:30` Squares with perfect right angles controlled the plan, and templates for piers, windows and vaults were designed with straight-edge and compass.
  - CLM_170: SRC_CU_AMIENS_GEOMETRY 1. Ease and Security of Construction: "The templates necessary for manufacturing the elements of multiple piers, windows and vaults were designed with straight-edge and compass." · SRC_CU_AMIENS_GEOMETRY 1. Ease and Security of Construction: "Plotting the site began with the stretching of ropes pegged to the ground. Spatial control was achieved through the formation of squares whose perfect right-angled corners were achieved through the application of a Pythagorean triangle or through an optical surveying instrument."

**B27** (fact; claim: CLM_172)

- `8:41` Arches were usually drawn full size on the ground, then divided into wedge-shaped stones called voussoirs.
- `8:48` Each voussoir was cut to a wooden template, and the stones were laid on a rigid wooden frame called centering.
- `8:56` The frame came away only once the mortar had set: at Amiens, after a couple of months or so.
  - CLM_172: SRC_BNF_ARCS_BOUTANTS Des modèles en bois pour les tailleurs de pierre: "La forme des arcs est généralement tracée au sol à l’échelle 1, puis divisée en segments qui correspondent aux voussoirs , pierres qui vont constituer l’arc, surmonté par la "clé de voûte". Des gabarits en bois sont préparés aux dimensions de chaque voussoir : ils servent de modèle aux tailleurs de pierre. Les voussoirs sont ensuite disposés sur une armature de cintres en bois que l’on retire une fois le mortier pris." · SRC_CU_AMIENS_ETEXT_17 E-Text 17: "All concave surfaces (arches, vaults) were formed over rigid wooden centering : the carefully-cut stones were laid up with a thin layer of mortar, left in place for a period (a couple of months or so) and then the formwork was removed."

**B28** (fact; claim: CLM_173)

- `9:04` Carpenters built the scaffolding, the formwork for the vaults and the lifting gear.
- `9:10` They also tied the upper piers with wood, and later iron, to stop the arches pushing them over.
  - CLM_173: SRC_CU_AMIENS_CARPENTERS Working with the masons: "The carpenters built scaffolding to provide access and temporary support; tying the upper piers with wooden (later, iron) ties to prevent them from being pushed over by the arches; wooden formwork for the vaults; lifting gear."

**B29** (fact; claim: CLM_171)

- `9:18` And there was little room for error.
- `9:22` The whole stone skeleton relies on lining up the thrust of each arch with the buttress that supports it.
  - CLM_171: SRC_CU_AMIENS_GEOMETRY 1. Ease and Security of Construction: "The skeletal structure of Gothic relies upon the correct alignment of the thrust of an arch with the support of a buttress--there is little room for error."

**B30** (fact; claim: CLM_101)

- `9:30` All of this took generations of work.
- `9:33` The foundation stone of Amiens was laid in 1220, and its main roof was not finished until about 1310.
  - CLM_101: SRC_CU_AMIENS_ETEXT_1 E-Text 1, paragraph 2: "beginning in 1220 with the start of work on a new cathedral after a disastrous fire" · SRC_CU_AMIENS_MASONS First Phase, c.1220-25: "An inscription on the south transept façade records that the foundation stone was laid in 1220" · SRC_CU_AMIENS_ETEXT_1 E-Text 1, paragraph 2: "The main roof was not finished until c.1310."


### C8 · The limit: Beauvais

**B31** (fact; claim: CLM_180)

- `9:43` Which brings us back to Beauvais.
- `9:46` In 1225, a fire damaged the old Romanesque choir, and the bishop decided to rebuild it, inspired by the greatest buildings of his time.
  - CLM_180: SRC_ISSMGE_BEAUVAIS_1 2.1.1 Avant 1225: "En 1225, un incendie endommageait le chœur roman. L’évêque Milon de Nanteuil décida alors de le reconstruire en s’inspirant des plus grandes réalisations de son époque, dans le style français (gothique, alors rayonnant)"

**B32** (fact; claim: CLM_181)

- `9:59` By the 1250s, the two lower levels of the new choir were finished.
- `10:04` Then the bishop apparently decided to go beyond the planned proportions, adding about five meters to the upper windows, and so to the vaults.
- `10:14` By 1272, the clergy could use the new choir.
  - CLM_181: SRC_ISSMGE_BEAUVAIS_1 2.1.2 1225-1340: "Dans les années 1250, les deux premiers niveaux de construction étant achevés (grandes arcades et triforium), l’évêque Guillaume de Grès décida apparemment pour le troisième et dernier étage de l’édifice de sortir des proportions prévues originellement en ajoutant quelques mètres (de l’ordre de cinq) aux fenêtres hautes et donc aux voûtes. En 1272, le nouveau chœur put être occupé par le clergé" — giả định: 'Apparemment': the paper presents the decision as probable, and the film says 'apparently'.

**B33** (fact; claim: CLM_102, CLM_103, CLM_104)

- `10:20` Its vault rose more than 45 meters, a few meters above Amiens.
- `10:26` These were the highest vaults built in the Middle Ages.
  - CLM_102: SRC_CU_AMIENS_UPPER_NAVE Amiens Cathedral, upper nave, north: "Amiens at 43.3 meters is a little lower than Beauvais at 46m." · SRC_ABC_HISTORY Around 1260, the choir is completed: "Its vault rises to nearly 47 m, 4 m higher than Amiens." — giả định: Published heights differ: Columbia gives Amiens 43.3 m and Beauvais 46 m; the Beauvais association gives Beauvais nearly 47 m and 4 m more than Amiens. The film says only 'more than 42 metres' for Amiens and 'more than 45 metres' for Beauvais, which all of these support.
  - CLM_103: SRC_ISSMGE_BEAUVAIS_1 Abstract (English): "Saint Peter’s cathedral in Beauvais (France) has the highest vaults ever built during the Middle Ages. It was affected by two famous structural accidents, in the choir in 1284, and later at the transept crossing, in 1573."
  - CLM_104: SRC_ABC_HISTORY Around 1260, the choir is completed: "Its vault rises to nearly 47 m, 4 m higher than Amiens. It is the tallest Gothic stone vault in the world." · SRC_ABC_DESCRIPTION The choir: "The choir has the tallest vault of any Gothic choir: 46.7 m." · SRC_ABC_FRENCH_ART The 13th century: "Its choir vaults rise above 48 metres" · SRC_CU_AMIENS_UPPER_NAVE Amiens Cathedral, upper nave, north: "Amiens at 43.3 meters is a little lower than Beauvais at 46m." · SRC_CU_MURRAY_PHASE3 Phase III: "In royal feet of thirty-two and a half centimeters the keystones of the vaults are about 144 feet above the pavement" — giả định: The figures disagree, even within one association's pages (nearly 47 m, 46.7 m, above 48 m; Columbia: 46 m). The narration says only 'more than 45 meters', which all of them support, and the card lists the published figures, from 46 m to above 48 m (owner's script review, 2026-11-05). Murray's 144 royal feet of 32.5 cm come to about 46.8 m, the agent's multiplication.

**B34** (fact; claim: CLM_182)

- `10:31` Then, in November 1284, part of the vaults over the choir came down.
- `10:37` The architect Viollet-le-Duc, writing centuries later, called it the last limit that the great churches of the 13th century could reach.
  - CLM_182: SRC_ISSMGE_BEAUVAIS_1 2.1.2 1225-1340: "Le 29 novembre 1284, durant cette nouvelle phase de chantier, des voûtains des travées droites du chœur, les plus vulnérables, s’effondrèrent" · SRC_ISSMGE_BEAUVAIS_1 2.1.2 1225-1340: "« la dernière limite à laquelle la construction des grandes églises du XIIIe s. ait pu arriver »" · SRC_ISSMGE_BEAUVAIS_1 2.1.2 1225-1340: "chantier qui s’en suivi s’acheva en 1340. « On mit donc plus de temps à réparer le chœur qu’à le construire » (Murray, 2000)." · SRC_ISSMGE_BEAUVAIS_2 2.1 Cause d’après les sources: "la durée de stabilité de 12 ans des parties hautes" — giả định: The film shows no collapse or destruction; it says 'in 1284' (the association gives 'a Friday in November 1284').

**B35** (fact; claim: CLM_183, CLM_184)

- `10:48` Why it happened is still debated.
- `10:51` Some blame settling masonry that broke the flying buttresses.
- `10:56` Others point to gusts of wind setting the buttress system resonating, or to slow settlement of the foundations.
- `11:04` A 2024 study found nothing to justify a foundation cause.
- `11:10` Its authors argue that raising the vaults, against proven proportions, left the upper parts too flexible.
  - CLM_183: SRC_ISSMGE_BEAUVAIS_2 2.1 Cause d’après les sources: "Il existe trois types d’interprétations pour expliquer l’effondrement partiel de voûtes du chœur en 1284, deux en partie haute de l’édifice, une en fondation." · SRC_ISSMGE_BEAUVAIS_2 2.1 Cause d’après les sources: "Il s’agit pour la première de la rupture de colonnettes monolithes solidaires d’une maçonnerie appareillée dont les mortiers auraient progressivement tassé, provoquant la rupture d’arcs-boutants" · SRC_ISSMGE_BEAUVAIS_2 2.1 Cause d’après les sources: "La deuxième invoque la mise en résonnance du système culée/arc-boutant au même endroit" · SRC_ISSMGE_BEAUVAIS_2 2.1 Cause d’après les sources: "causée par un vent en rafale" · SRC_ISSMGE_BEAUVAIS_2 2.1 Cause d’après les sources: "La troisième suggère l’existence d’un tassement différentiel lent dans les fondations" · SRC_ISSMGE_BEAUVAIS_2 2.2 Origine géotechnique en 1284?: "un raidissement généralisé des parties hautes atteintes. Elles s’étaient avérées trop souples, non pas en soi, mais en raison de la décision" · SRC_ISSMGE_BEAUVAIS_2 2.2 Origine géotechnique en 1284?: "en cours de chantier de surélever de plusieurs mètres les voûtes de la cathédrale. Cette décision dû être prise au mépris des dimensions choisies pour les parties sous-jacentes, des proportions éprouvées" · SRC_ISSMGE_BEAUVAIS_2 Abstract (English): "We here show that nothing appears to justify a geotechnical origin in the 1284 collapse." · SRC_ISSMGE_BEAUVAIS_2 2.2 Origine géotechnique en 1284?: "Ainsi, nous ne souscrivons pas à l’hypothèse d’une origine géotechnique dans l’accident de 1284." — giả định: The sentence on the raised vaults runs across a page break of the paper, so it is quoted in two excerpts. This is the authors' argument, not a settled result: the film attributes it to them. The association's view (CLM_184) is that a storm was the likely trigger.
  - CLM_184: SRC_ABC_HISTORY A first catastrophe: "On a Friday in November 1284, the flying buttresses twist and break, causing the collapse of the choir’s vault. The cathedral, being very tall, rises above the neighboring plateau and is highly exposed to wind. It was likely a storm that triggered this catastrophe."

**B36** (fact; claim: CLM_185, CLM_182)

- `11:19` The repair tells its own story.
- `11:22` New piers went up between the old ones, turning three bays into six.
- `11:28` The work was not finished until 1340: as the historian Stephen Murray put it, it took longer to repair the choir than to build it.
  - CLM_185: SRC_ABC_HISTORY The reconstruction: "As a precaution, the bays were subdivided with new, narrower intermediate piers. This changed the straight section of the choir from 3 to 6 bays." · SRC_CU_MURRAY_COLLAPSE The Collapse of the Choir in 1284: "In the straight bays additional supports have been interposed between the piers of the main arcade, transforming three bays into six and quadripartite vaults to sexpartite"
  - CLM_182: SRC_ISSMGE_BEAUVAIS_1 2.1.2 1225-1340: "Le 29 novembre 1284, durant cette nouvelle phase de chantier, des voûtains des travées droites du chœur, les plus vulnérables, s’effondrèrent" · SRC_ISSMGE_BEAUVAIS_1 2.1.2 1225-1340: "« la dernière limite à laquelle la construction des grandes églises du XIIIe s. ait pu arriver »" · SRC_ISSMGE_BEAUVAIS_1 2.1.2 1225-1340: "chantier qui s’en suivi s’acheva en 1340. « On mit donc plus de temps à réparer le chœur qu’à le construire » (Murray, 2000)." · SRC_ISSMGE_BEAUVAIS_2 2.1 Cause d’après les sources: "la durée de stabilité de 12 ans des parties hautes" — giả định: The film shows no collapse or destruction; it says 'in 1284' (the association gives 'a Friday in November 1284').

**B37** (fact; claim: CLM_186, CLM_187, CLM_106)

- `11:39` In the sixteenth century, work began again, with a new transept, the cross-arm of the building.
- `11:46` Then, instead of a nave, the builders raised a lantern tower and spire about 150 meters high, finished in 1569.
- `11:56` It rested on four slender piers, and the sources point to a lack of support on the west side, where the nave had not been built.
- `12:05` In 1573, just four years after it was finished, the tower came down.
- `12:12` The great Gothic nave was never built.
  - CLM_186: SRC_ABC_HISTORY 150 years later, work resumes: "Begun in May 1500, this masterpiece of the Flamboyant period took 50 long years to build." · SRC_ABC_HISTORY An oversized spire: "Instead of extending the cathedral with a nave — which would have stabilized the building — it was decided to build a lantern tower at the crossing of the transept" · SRC_ABC_HISTORY An oversized spire: "Completed in 1569, this tower, topped with a spire, reached 150 m. It collapsed four years later" · SRC_ISSMGE_BEAUVAIS_2 3.1 Cause d’après les sources: "un défaut de contrebutement à l’ouest, où la nouvelle nef n’était pas encore construite. La tour tout entière portait sur les quatre piliers élancés de la croisée du transept" · SRC_ISSMGE_BEAUVAIS_1 2.1.3 1499-1605: "un support de la tour lanterne s’effondra le jour de l’Ascension 1573, un 30 avril" — giả định: 'About 150 metres' is the association's figure for the tower with its spire; the film rounds it as 'about 150 metres'.
  - CLM_187: SRC_ISSMGE_BEAUVAIS_1 1 Introduction: "sa nef gothique n’a jamais été construite (Murray, 2000)" · SRC_ABC_HISTORY The cathedral remains unfinished: "work stopped at a nave reduced to a single bay" — giả định: The paper says the Gothic nave was never built; the association says work stopped at a nave reduced to a single bay. The film says 'the great Gothic nave was never built', which both support.
  - CLM_106: SRC_CU_AMIENS_ETEXT_11 E-Text 11: "The eastern arm of the cathedral is commonly called the choir" · SRC_CU_AMIENS_ETEXT_4 E-Text 4: "the long, boat-like body of the cathedral is intersected by a cross-arm or transept" — giả định: E-Text 11 adds that the term is 'something of a misnomer' because the choir proper is where the clergy sat; the film uses the common meaning. 'Crossing piers' is the term used in CLM_190.

**B38** (fact; claim: CLM_190, CLM_191, CLM_106)

- `12:16` Beauvais was not alone.
- `12:19` At Amiens, within two centuries, the piers at the crossing, where the arms of the building meet, were threatening collapse.
- `12:27` Between 1497 and 1500, an iron chain was installed to stop the movement, and it still runs through the building today.
  - CLM_190: SRC_CU_AMIENS_ETEXT_1 E-Text 1, paragraph 2: "the enlarged central bays began to fail; the main crossing piers, burdened with weight of a great central steeple buckled inward at arcade level and outward in their upper parts, threatening collapse. This deformation was arrested through the installation (1497-1500) of an iron chain" · SRC_CU_AMIENS_TRIFORIUM_CHAIN Triforium passage, south side of nave: "On the pavement to the left runs the iron chain (actually a series of iron rods linked together) that runs the length of the nave and ties the crossing pier." — giả định: 'Still runs' rests on the present tense of Columbia's page (copyright 2017, with a note dated 2017).
  - CLM_191: SRC_CU_AMIENS_ETEXT_17 E-Text 17: "Within two centuries the crossing piers were threatening collapse."
  - CLM_106: SRC_CU_AMIENS_ETEXT_11 E-Text 11: "The eastern arm of the cathedral is commonly called the choir" · SRC_CU_AMIENS_ETEXT_4 E-Text 4: "the long, boat-like body of the cathedral is intersected by a cross-arm or transept" — giả định: E-Text 11 adds that the term is 'something of a misnomer' because the choir proper is where the clergy sat; the film uses the common meaning. 'Crossing piers' is the term used in CLM_190.


### C9 · Why they stand

**B39** (fact; claim: CLM_112)

- `12:38` So why do these buildings stand at all?
- `12:41` One answer from modern engineers is that the stone's strength is rarely the limit.
- `12:48` Stresses in masonry are typically only a fraction of what the stone can bear, and in most cases structures fail through instability, not a lack of strength.
  - CLM_112: SRC_MIT_BLOCK_2005 1.1 Introduction, p. 9: "In most cases, masonry structures fail due to instability rather than a lack of material strength [Heyman 1995]. Stresses in masonry structures are typically only a fraction of the crushing capacity of the stone. Therefore, rigid block models with the same proportions as the structures are good models to understand their stability. Unlike problems in elasticity, stability problems can be scaled." — giả định: A statement about what such models help to understand, not a safety test of a real building: see CLM_116.

**B40** (fact; claim: CLM_113, CLM_111, CLM_117, CLM_118)

- `13:00` Picture one idealized arch, and the path of the force through its stones, which engineers call the line of thrust.
- `13:08` This analysis assumes that the stones resist no pulling, never slide and never crush.
- `13:15` Under those assumptions and a given load, many such lines can fit inside the masonry, and finding one is enough to show the arch can stand.
- `13:26` Now move its supports apart, and the arch deforms.
- `13:30` Past a certain point, no line can fit inside it, and this idealized arch collapses.
  - CLM_113: SRC_MIT_BLOCK_2005 1.1 Introduction, p. 9: "This is a theoretical line, which represents the path of the resultants of the compressive forces through the stone structure. For a pure compression structure to be in equilibrium with the applied loads there must be a line of thrust that lies entirely within the section." · SRC_MIT_BLOCK_2005 3.2, p. 19: "if a line that fits within the arch’s profile for the given loading can no longer be found, then the arch will collapse." · SRC_MIT_BLOCK_2006 Robert Hooke's hanging chain, p. 10: "If a line of force can be found that lies everywhere within the masonry, then the structure can be shown to be safe for that set of loads" — giả định: Narrated for one idealized arch and a given load, with the assumptions of CLM_111 stated first (owner's script review, 2026-11-05).
  - CLM_111: SRC_MIT_BLOCK_2005 1.1 Introduction, p. 9: "masonry has no tensile strength; it can resist infinite compression; and no sliding will occur within the masonry." · SRC_MIT_BLOCK_2005 3.2, p. 19: "Stone has no or very little tensile capacity, so, the structure would collapse if it cannot contain a thrust line in compression." — giả định: These are the assumptions of limit analysis (Heyman), and the film states them as such: 'never crush' is its plain wording of 'infinite compression'.
  - CLM_117: SRC_MIT_BLOCK_2006 Semi-circular versus pointed arch, p. 13: "For every masonry structural element, there is an infinite amount of valid thrust lines that fit within its section, all lying between a maximum and minimum value" · SRC_MIT_BLOCK_2006 Robert Hooke's hanging chain, p. 10: "If a line of force can be found that lies everywhere within the masonry, then the structure can be shown to be safe for that set of loads"
  - CLM_118: SRC_MIT_BLOCK_2006 Fig. 5, p. 15: "This shows an arch on spreading supports with a t/R = 15% and a total angle of embrace of 160°" · SRC_MIT_BLOCK_2006 Arch on spreading supports, p. 16: "The limit of displacement at which collapse occurs can be explored by applying displacements until it is no longer possible to fit a thrust line in the deformed structure. Failure occurs when there are more than three hinges, i.e. when the thrust line touches the boundaries of the structure in more than three places" · SRC_MIT_BLOCK_2006 Arch on spreading supports, p. 14: "Masonry arches commonly collapse due to instability caused by large displacements (ground settlements, leaning buttresses etc.)." · SRC_CAM_OCHSENDORF_2002 5.4: "For most arches, failure will be governed by the five-hinge collapse mechanism, in which the central portion of the arch is a three-hinged arch, which deforms to accommodate the span increase." · SRC_CAM_OCHSENDORF_2002 5.5: "This demonstrates that the intrados hinge locations may move substantially as the arch deforms to the collapse state." — giả định: The card's geometry is the agent's port of Ochsendorf's program ArchSpread (script/arch_statics.py, self-weight only, voussoirs of 0.1 degree, 1000 steps, span measured on the intrados), applied to this example; it is not a tracing of the figure. Checked against thesis table 5.3 (t/R 0.10, half-angle 60): hinge 53.8 to 42.8 degrees (thesis 42.7), span +8.20% (8.2), thrust 2.16 Hmin (2.16), dip 1.71 t (1.73); and the thesis's text (t/R 0.1075): 54.5 to 52.2 degrees at half-angle 80, 54.5 to 43.2 at 60, both exact. For voussoirs of 1 to 10 degrees the spans agree (7.95 to 9.26%; thesis 8.0 to 9.3) but the final hinges do not (43 to 50; thesis 40 to 42), and the film uses neither. On this example: hinge 57.9 to 53.9 degrees (figure 54.4), span +11.17% (11.49), thrust +83.8% (85.10); at span +5.00%, thrust +22.6% (24.59). Figure values are read from its labels. The film and the card state none of these numbers, and the narration says 'this idealized arch', not any building.

**B41** (fact; claim: CLM_112, CLM_116, CLM_110)

- `13:38` That puts shape and proportion at the center of the question.
- `13:42` Unlike some other engineering problems, stability can be scaled, so a small model with the same proportions helps show what proportion does.
- `13:53` On its own, that does not show a whole real building is safe: this kind of analysis can miss effects such as local crushing, cracking and sliding.
- `14:03` But it helps explain how rules of geometry, learned by trial and error, could carry builders so far.
  - CLM_112: SRC_MIT_BLOCK_2005 1.1 Introduction, p. 9: "In most cases, masonry structures fail due to instability rather than a lack of material strength [Heyman 1995]. Stresses in masonry structures are typically only a fraction of the crushing capacity of the stone. Therefore, rigid block models with the same proportions as the structures are good models to understand their stability. Unlike problems in elasticity, stability problems can be scaled." — giả định: A statement about what such models help to understand, not a safety test of a real building: see CLM_116.
  - CLM_116: SRC_MIT_BLOCK_2006 Conclusion, p. 17: "The strong assumptions necessary to apply limit analysis to masonry provide complex analyses easily and quickly. After this first order analysis, the analyst must check if the assumptions have been violated. In some cases, the method will lead to unconservative results since second order effects such as local crushing, crack propagation and sliding have not been considered." · SRC_MIT_BLOCK_2005 Ch. 5, p. 33: "The assumptions that the masonry blocks have infinite compressive strength and that no sliding occurs are clearly unsafe."
  - CLM_110: SRC_MIT_BLOCK_2005 1.1 Introduction, p. 9: "The master builders of the Middle Ages were able to use geometrical rules, developed through centuries of trial and error, to build structural elements by scaling up the same proportions for new larger elements [Huerta 2004]. In those days, there was no knowledge of material properties or allowable stresses." · SRC_MIT_BLOCK_2005 1.1 Introduction, p. 9: "Yet, many of these architectural marvels are still standing in a state of equilibrium." · SRC_MIT_BLOCK_2006 Graphic Statics, p. 10: "Culmann [1866] was the first to formalize graphical analysis as a powerful method for equilibrium analysis in structural engineering." · SRC_CU_AMIENS_GEOMETRY 1. Ease and Security of Construction: "The templates necessary for manufacturing the elements of multiple piers, windows and vaults were designed with straight-edge and compass." — giả định: Block writes 'no knowledge of material properties or allowable stresses'. The film does not repeat that phrase (owner's script review, 2026-11-05): heard alone it denies the builders' practical knowledge, which the film itself shows (CLM_121, CLM_170, CLM_172, CLM_173). 'Without modern structural calculations' is the narrower reading: formal structural analysis came centuries later.


### C10 · Never impossible

**B42** (interpretation; claim: CLM_130, CLM_132, CLM_140, CLM_152, CLM_143)

- `14:12` So the heights were never impossible.
- `14:15` Pointed arches gave builders taller, more adaptable shapes, ribs helped direct the load toward the piers, and flying buttresses carried the thrust outside and down to the ground.
- `14:28` The walls in between could open up to glass.
  - CLM_130: SRC_ABC_THRUST Innovation No. 1: "the pointed arch is formed by two arcs of a circle meeting at a point." · SRC_BNF_ARC_BRISE Arc brisé et voûte sur croisée d’ogive: "Il a pour avantage d’exercer des poussées latérales réduites, ce qui permet de l’élever nettement plus haut." · SRC_CU_AMIENS_REVOLUTION Synthesis (Gothic): "The pointed arch. Appropriated from Islamic sources and applied to reduce outward thrust." · SRC_MIT_ROMANO Comparison of Pointed vs. Circular Arches: "In Gothic cathedrals the use of pointed arches is widespread because of the decreased thrust compared to the circular arch. While this fact is widely acknowledged and accepted, there has been little theory developed to determine exactly the different behavior of the two arches." · SRC_MIT_ROMANO Comparison of Pointed vs. Circular Arches: "a parametric study of whole and half arches has been performed varying the angle of embrace, the thickness and the eccentricity of the centers of the arches" · SRC_MIT_BLOCK_2006 Arch on spreading supports, p. 16: "This makes sense since the deforming arch becomes more and more shallow, resulting in an increase of horizontal thrust." — giả định: BnF and Columbia state the reduction without conditions; the film adds them (owner's script review, 2026-11-05). 'Half its span' is the geometry of a semicircle. The link between shallowness and thrust is quoted from an arch on spreading supports, so the film says 'can', and gives no general figure.
  - CLM_132: SRC_ABC_THRUST Innovation No. 1: "unlike the round arch, the pointed arch allows bays of different widths to be spanned while keeping the same keystone height — a valuable asset for regularising complex vaults." · SRC_CU_STALLEY_STRUCTURE Development of the Vaulted Ceiling: "The exploitation of the pointed arch in this position allowed the apex of the vault to be kept level throughout its length" · SRC_CU_STALLEY_STRUCTURE Development of the Vaulted Ceiling: "While it could be argued that pointed arches were first introduced into English architecture to solve a geometrical problem, they may also have helped to improve the stability of the vault." — giả định: Geometric property also shown on the card: a semicircular arch's rise is half its span. Stalley's second sentence is why the film treats the pointed arch as a geometric tool first.
  - CLM_140: SRC_ABC_THRUST Innovation No. 2: "two pointed arches cross diagonally above each bay, gathering the vault’s load onto four precise points — the corner piers." · SRC_BNF_SAINT_DENIS Une nouvelle conception de la spiritualité: "Elle dirige les poussées de la voûte sur des piliers, et non plus sur des murs" · SRC_CU_STALLEY_DESCRIBE The Interior Elevations: "It is important to note that the diagonal ribs are depressed, following only a segment of a circle" · SRC_CU_STALLEY_DESCRIBE The Interior Elevations: "These transverse arches are pointed in profile" — giả định: Both quoted sources simplify, and how such vaults stand is debated (CLM_141), so the film says 'in this simplified picture' (owner's script review, 2026-11-05). The association and BnF call the crossing ribs 'two pointed arches'; Stalley describes Durham's diagonal ribs as segments of a circle and its pointed arches as transverse, so the film says only 'two ribs'.
  - CLM_152: SRC_ABC_THRUST Innovation No. 3: "this external arch picks up the thrust at the point where it leaves the vault, carries it across the aisle roof, and channels it down to a massive pier buttress, often topped with a pinnacle that weighs it down to better stabilise the thrust."
  - CLM_143: SRC_ABC_THRUST Innovation No. 2: "Direct consequence: between the piers, the walls no longer carry any load. They can be thinned, hollowed out, and eventually replaced with wide glazed openings." · SRC_BNF_ARC_BRISE La voûte sur croisée d’ogive: "Les murs perdent ainsi leur rôle de soutien, et peuvent être percés de larges ouvertures." — giả định: The sources are absolute ('no longer carry any load', 'perdent ainsi leur rôle de soutien'). The film says 'main support': a wall still carries at least its own weight, and how vaults stand is debated (CLM_141).

**B43** (interpretation; claim: CLM_185, CLM_190, CLM_163, CLM_110)

- `14:33` But it is not a simple story of progress.
- `14:36` Beauvais needed new piers, Amiens needed an iron chain, and Suger's bright choir rose above a crypt of older forms.
- `14:45` Each cathedral was a test in stone, built by people who learned from centuries of trial and error.
  - CLM_185: SRC_ABC_HISTORY The reconstruction: "As a precaution, the bays were subdivided with new, narrower intermediate piers. This changed the straight section of the choir from 3 to 6 bays." · SRC_CU_MURRAY_COLLAPSE The Collapse of the Choir in 1284: "In the straight bays additional supports have been interposed between the piers of the main arcade, transforming three bays into six and quadripartite vaults to sexpartite"
  - CLM_190: SRC_CU_AMIENS_ETEXT_1 E-Text 1, paragraph 2: "the enlarged central bays began to fail; the main crossing piers, burdened with weight of a great central steeple buckled inward at arcade level and outward in their upper parts, threatening collapse. This deformation was arrested through the installation (1497-1500) of an iron chain" · SRC_CU_AMIENS_TRIFORIUM_CHAIN Triforium passage, south side of nave: "On the pavement to the left runs the iron chain (actually a series of iron rods linked together) that runs the length of the nave and ties the crossing pier." — giả định: 'Still runs' rests on the present tense of Columbia's page (copyright 2017, with a note dated 2017).
  - CLM_163: SRC_CU_AMIENS_REVOLUTION The Gothic Structural Revolution: "Following Viollet-le-Duc's premise of Gothic understood as "An Entire Revolution in the Art of Building."" · SRC_FM_TIMBERT_SAINT_DENIS conclusion: "C’est pourquoi il n’y a pas de « révolution » et, donc, de rupture gothique, mais une proposition créative inscrite dans la permanence." · SRC_FM_TIMBERT_SAINT_DENIS La crypte: "La voûte d’arêtes et l’arc en plein cintre y sont employés de manière quasi exclusive." · SRC_ISSMGE_BEAUVAIS_1 1 Introduction: "Eugène Viollet-le-Duc, connu pour son œuvre de restauration de Notre-Dame de Paris au XIXe siècle" — giả định: Since g-r2 the narration gives the two readings without names (owner's script review, 2026-11-05); the card keeps the attributions in small type.
  - CLM_110: SRC_MIT_BLOCK_2005 1.1 Introduction, p. 9: "The master builders of the Middle Ages were able to use geometrical rules, developed through centuries of trial and error, to build structural elements by scaling up the same proportions for new larger elements [Huerta 2004]. In those days, there was no knowledge of material properties or allowable stresses." · SRC_MIT_BLOCK_2005 1.1 Introduction, p. 9: "Yet, many of these architectural marvels are still standing in a state of equilibrium." · SRC_MIT_BLOCK_2006 Graphic Statics, p. 10: "Culmann [1866] was the first to formalize graphical analysis as a powerful method for equilibrium analysis in structural engineering." · SRC_CU_AMIENS_GEOMETRY 1. Ease and Security of Construction: "The templates necessary for manufacturing the elements of multiple piers, windows and vaults were designed with straight-edge and compass." — giả định: Block writes 'no knowledge of material properties or allowable stresses'. The film does not repeat that phrase (owner's script review, 2026-11-05): heard alone it denies the builders' practical knowledge, which the film itself shows (CLM_121, CLM_170, CLM_172, CLM_173). 'Without modern structural calculations' is the narrower reading: formal structural analysis came centuries later.

**B44** (framing; claim: không, câu dẫn dắt)

- `14:54` These models are illustrations, not structural analyses, and the arrows show ideas, not calculated forces.

**B45** (framing; claim: không, câu dẫn dắt)

- `15:03` Which building or structure should we explain next?
- `15:07` Suggest a topic in the comments.
- `15:10` And if you enjoyed this film, please like it and subscribe.

**B46** (framing; claim: không, câu dẫn dắt)

- `15:16` Thank you very much for watching.
- `15:19` The sources are listed in the description.

## Bộ kiểm nhất quán lời/hình: cần người duyệt xác nhận

- B26.s1 (SIDE, UNCERTAIN): "Squares with perfect right angles controlled the plan, and templates for piers, windows and vaults were designed with straight-edge and compass." — left/right wording; no annotation to locate - confirm the referent in review
- B35.s4 (SIDE, UNCERTAIN): "Its authors argue that raising the vaults, against proven proportions, left the upper parts too flexible." — left/right wording; no annotation to locate - confirm the referent in review
- B44.s0 (ARROWS, UNCERTAIN): "These models are illustrations, not structural analyses, and the arrows show ideas, not calculated forces." — generic reference to the arrows (shown in earlier beats); editorial check

## Chữ trên card

- **SC_001** (B01): Photo: Dguendel, CC BY 4.0, Wikimedia Commons | Photo: Dguendel, CC BY 4.0, Wikimedia Commons | Beauvais Cathedral today | Beauvais, November 1284 | Vault: more than 45 m above the floor | Published heights differ: 46 m to above 48 m | The choir today: the eastern arm | In use from 1272: twelve years
- **SC_002** (B02): Photo: Eusebius, CC BY 3.0, Wikimedia Commons | Amiens Cathedral today | Amiens, begun 1220 | Vault: more than 42 m
- **SC_003** (B03): How Gothic Cathedrals Reached | Impossible Heights | How did they raise stone that high? | And why, sometimes, did it come down? | Section of Beauvais: Viollet-le-Duc, 1856
- **SC_004** (B04): 2 · Stone and its outward push | Conceptual diagram, not to scale | Pulled apart: little or no strength | Stones pressed together: it stands
- **SC_008** (B08): 3 · The pointed arch | Pointed arch | Round arch | Rise: half the span | Same span, higher rise | Conceptual arrows: direction only, not calculated | Shape | Thickness | Weight carried | Illustrations, not the arches of the study (Block, DeJong and Ochsendorf, 2006)
- **SC_009** (B09): Robert Hooke, 1675 | “As hangs the flexible line, so but inverted | will stand the rigid arch.” | “As hangs the flexible line, so but inverted | will stand the rigid arch.”  Robert Hooke, 1675 | A chain with its weights | Turned upside down: | a path for the force | Different weights, different curve | Conceptual diagram
- **SC_010** (B10): 1060 | 1080 | 1100 | 1120 | 1140 | 1160 | 1088  Cluny III: construction begins | Saint-Denis: used systematically | Not a Gothic invention
- **SC_011** (B11): Round arches | Crowns at different heights | Pointed arches | Same crown height | Regular crowns help keep complex vaults regular | Wide bay, narrow bay: conceptual diagram
- **SC_014** (B14): Photo: A. D. White Architectural Photographs, Cornell University Library | Durham Cathedral, interior | (photograph about 1865–1895) | 1080 | 1100 | 1120 | 1140 | 1088  Cluny III: construction begins | Durham, begun 1093, finished 1133: ribbed vaults, in phases | At least three technical phases, some forty years | Earlier sources: Islamic, Roman, Byzantine (Columbia)
- **SC_015** (B15): One bay, seen from inside (schematic) | The load goes | to the piers | The wall: no longer | the main support | Wall thickness (schematic) | Wide windows
- **SC_018** (B18): The picture from Columbia's Amiens project | Plan, seen from above (schematic) | Inside the building | A thick outer wall | Each segment turned 90° | Rigid supports, standing out from the building | Exposed arches: flying buttresses
- **SC_019** (B19): A church section (schematic) | Added outside to consolidate (BnF) | Timber props, while building | made permanent in stone (BnF) | Photo: Florestan, CC BY 3.0, Wikimedia Commons | Photo: Jebulon, CC0, Wikimedia Commons | Chartres today: flying buttresses of the nave | part of the original plans | Notre-Dame de Paris: the east end (photograph 2011)
- **SC_020** (B20): Half a section (schematic) | Rainwater led off the roof | (schematic) | Ever taller
- **SC_021** (B21): 6 · Walls of light | Photo: Guilhem Vellut, CC BY 2.0, Wikimedia Commons | Photo: Ninaras, CC BY 4.0, Wikimedia Commons | Part of the answer: light | Saint-Denis today | Abbot Suger's new choir: 1140–1144 | Pointed arches | Every vault ribbed | Stained glass
- **SC_022** (B22): Photo: Ninaras, CC BY 4.0, Wikimedia Commons | “A sign, a bridge to the divine” | Light, for Abbot Suger | The new style had to let in as much light as possible | Bibliothèque nationale de France
- **SC_023** (B23): Photo: Eusebius, public domain, Wikimedia Commons | Chartres today: the north rose | About 2,500 m² of stained glass survive, | most of it original
- **SC_024** (B24): How new was Gothic? | “An entire revolution | in the art of building” | After Viollet-le-Duc, 19th century | No Gothic break: a creative | proposal rooted in continuity | Arnaud Timbert, art historian | Suger's crypt: round arches, groin vaults
- **SC_025** (B25): 7 · Building by geometry | Without modern structural calculations | A geometrical rule: compass and line | The same proportions, scaled up
- **SC_026** (B26): Ropes pegged to the ground | Squares with right angles | Templates: straight edge and compass | Schematic, not the Amiens plan
- **SC_027** (B27): Drawn full size on the ground | Divided into voussoirs | Each cut to a wooden template | Centering (temporary) | Centering removed | once the mortar has set | Amiens: after a couple of months or so | Sequence after the sources, schematic
- **SC_028** (B28): The carpenters (schematic) | Scaffolding | Formwork for the vault | Lifting gear | Ties: wood, later iron | held against the arches' push
- **SC_030** (B30): 1200 | 1240 | 1280 | 1320 | 1220  Foundation stone | 1310  Main roof finished (about) | Amiens Cathedral
- **SC_031** (B31): 8 · The limit: Beauvais | Photo: Dguendel, CC BY 4.0, Wikimedia Commons | Beauvais Cathedral today: the choir | 1225: fire in the old Romanesque choir
- **SC_032** (B32): Photo: Dguendel, CC BY 4.0, Wikimedia Commons | Arcade | Triforium | 1250s: arcade and triforium finished | Upper windows: + about 5 m | the added height is schematic | 1272: the choir in use
- **SC_033** (B33): Amiens: more than 42 m | Beauvais: more than 45 m | The highest vaults built in the Middle Ages | Published for Beauvais: 46 m, 46.7 m, nearly 47 m, above 48 m | Photo: Eusebius, CC BY 3.0, Wikimedia Commons | Photo: Dguendel, CC BY 4.0, Wikimedia Commons
- **SC_034** (B34): Plan of Beauvais: Viollet-le-Duc, 1856 | 29 November 1284 | Vault cells over the choir's straight bays fell | “The last limit”: Viollet-le-Duc, who drew this plan
- **SC_035** (B35): Section of Beauvais: Viollet-le-Duc, 1856; marks schematic | Why did the vaults fall? Still debated. | Hypothesis: settling masonry broke | the flying buttresses | Hypothesis: gusts of wind set the | buttress system resonating | Hypothesis: slow settlement | of the foundations | Not supported by this study | Vernhes, Renault and Zotna, 2024: | “nothing appears to justify | a geotechnical origin” | Their hypothesis: vaults raised against proven | proportions left the upper parts too flexible | ECSMGE 2024: an argument, not a settled result
- **SC_036** (B36): 1 | 2 | 3 | 1 | 2 | 3 | 4 | 5 | 6 | Plan of Beauvais: Viollet-le-Duc, 1856 | The repair | New piers between the old ones (positions schematic) | Finished in 1340 | “Longer to repair the choir than to build it”: Stephen Murray
- **SC_037** (B37): 1480 | 1520 | 1560 | 1600 | 1500  Transept begun | 1569  Tower and spire, about 150 m | 1573  The tower falls | Photo: Chris06, CC0, Wikimedia Commons; plan: Viollet-le-Duc, 1856 | Beauvais Cathedral today: transept and choir | No nave: no support to the west | The Gothic nave: never built
- **SC_038** (B38): Photo: Eusebius, CC BY 3.0, Wikimedia Commons | Plan of Amiens: Viollet-le-Duc, 1854 | Amiens Cathedral today | Crossing piers: threatening collapse within two centuries | Iron chain, 1497–1500 | route schematic | Iron rods linked together, along the nave, tying the crossing pier
- **SC_040** (B40): The line of thrust | Assumed: stones resist no pulling, never slide, never crush | Many lines can fit. One is enough | Supports moved apart: the arch deforms | At the limit, the line touches the stone at five points | Any further, and no line can fit | After Block, DeJong and Ochsendorf, 2006, Fig. 5, recalculated by Ochsendorf's 2002 method. One idealized arch, self-weight only
- **SC_041** (B41): Small model | Real building | Same proportions | Shows the role of proportion | Does not prove a real building safe | Rules of geometry, learned by trial and error
- **SC_043** (B43): Not a simple story of progress | Beauvais: new piers | Amiens: an iron chain | Saint-Denis: a bright choir over a crypt of older forms | Centuries of trial and error
- **SC_045** (B45): What should we explain next? | Suggest a topic in the comments | SUBSCRIBE | SUBSCRIBED
- **SC_046** (B46): How Gothic Cathedrals Reached Impossible Heights | Sources: Columbia University (Life of a Cathedral; S. Murray; R. Stalley); Harvard (Loeb Library); New Catholic Encyclopedia; | MIT (P. Block, 2005; Block, DeJong and Ochsendorf, 2006; Romano and Ochsendorf); Cambridge (J. Ochsendorf, 2002); | Bibliothèque nationale de France; France Mémoire (A. Timbert); Durham Cathedral; Abbaye de Cluny (CMN); | ECSMGE 2024 (Vernhes, Renault, Zotna); Association Beauvais Cathédrale | 3D models and diagrams are illustrative, not structural analyses | Architecture Story Studio

## Chú thích trên cảnh 3D

- B05 `B05_note` NOTE: "Illustrative model, arrows are conceptual"
- B05 `B05_down` LOAD_ARROW: "Presses down" (CLM_120)
- B05 `B05_thrust` THRUST_ARROW: "Thrust" (CLM_120)
- B05 `B05_word` NOTE: "An Amiens document calls it “boutture”"
- B06 `B06_note` NOTE: "One Romanesque type, illustrative model"
- B06 `B06_wall` COMPONENT_LABEL: "Thick wall"
- B06 `B06_butt` COMPONENT_LABEL: "Shallow buttress"
- B06 `B06_window` COMPONENT_LABEL: "Small window"
- B07 `B07_note` NOTE: "Illustrative model"
- B07 `B07_arch` COMPONENT_LABEL: "Pointed arch"
- B07 `B07_rib` COMPONENT_LABEL: "Rib vault"
- B07 `B07_flyer` COMPONENT_LABEL: "Flying buttress"
- B12 `B12_ch` NOTE: "4 · The rib vault"
- B12 `B12_note` NOTE: "Illustrative model, one type: a four-part vault"
- B12 `B12_rib` COMPONENT_LABEL: "Diagonal ribs"
- B12 `B12_pier` COMPONENT_LABEL: "Pier"
- B13 `B13_note` NOTE: "Illustrative model of one analysis, still debated"
- B13 `B13_ribs` COMPONENT_LABEL: "Main ribs"
- B13 `B13_arches` COMPONENT_LABEL: "A series of arches"
- B13 `B13_web` COMPONENT_LABEL: "Stone web"
- B16 `B16_ch` NOTE: "5 · The flying buttress"
- B16 `B16_note` NOTE: "Illustrative model"
- B16 `B16_thrust` THRUST_ARROW: "Thrust" (CLM_150)
- B17 `B17_note` NOTE: "Illustrative model"
- B17 `B17_flyer` COMPONENT_LABEL: "Flying buttress"
- B17 `B17_pier` COMPONENT_LABEL: "Pier buttress"
- B17 `B17_weight` LOAD_ARROW: "Weight" (CLM_152)
- B17 `B17_pinnacle` COMPONENT_LABEL: "Pinnacle"
- B39 `B39_ch` NOTE: "9 · Why they stand"
- B42 `B42_ch` NOTE: "10 · Never impossible"
- B44 `B44_note` NOTE: "Models are illustrations, not structural analyses"

## Bản ghi sửa câu (ASR / tốc độ đọc)

- B24.s1 (g-r1): "Historians still disagree." → "On that question, historians still disagree." (three-word sentence: trailing silence put it at 1.17 words/s, under the 1.5 truncation guard (three takes rejected))
- B37.s3 (g-r1): "In 1573, the tower fell." → "In 1573, just four years after it was finished, the tower came down." (short sentence with a spoken year: 1.48 words/s, under the 1.5 truncation guard (three takes rejected))
- B24.s2, B34.s1 (g-r1): "nineteenth-century, thirteenth century" → "19th-century, 13th century" (Same words when spoken; digits match the subtitle style and what the ASR check transcribes.)
- B34.s1 (g-r1): "Viollet-le-Duc later called it the last limit that the great churches of the 13th century could reach." → "The architect Viollet-le-Duc, writing centuries later, called it the last limit that the great churches of the 13th century could reach." (Viewers need reminding who he is and when he wrote; the ASR check also failed on the name (WER 0.16), which proves nothing about pronunciation. The threshold was not changed.)
- B01.s2, B06.s0, B11.s1, B12.s2, B15.s0, B19.s1, B20, B25.s0, B37.s0, B38.s1, B41.s0, B41.s1: Agent's read-through before the first owner review: terms explained where they first matter (choir, bay, pier, transept, crossing), B15 and B25 connect to what precedes them, B19.s1 keeps the attribution explicit, B20 ends on the main point, B41 keeps 'stability' as the source says.
- B08, B09, B42 (owner_review: 1): The pointed arch no longer always pushes less: it can rise higher over the same span, and that can reduce thrust depending on shape, thickness and load. One MIT comparison is given as a result for those two arches. Hooke's chain now depends on its loads. CLM_133 (a garbled source sentence) is no longer narrated.
- B39, B40, B41 (owner_review: 2): The line of thrust is limited to one idealized arch, with its assumptions spoken. A scaled model shows the role of proportion and does not prove a real building safe. 'What matters most' is gone.
- B03.s0, B25.s0 (owner_review: 3): 'No knowledge of material properties' replaced with 'without modern structural calculations, relying on geometry, craft knowledge and experience'.
- B12, B13, B15 (owner_review: 4): Limited to the four-part vault shown, in a simplified picture; the stone web carries load too; the wall is no longer the vault's main support, rather than carrying nothing. 'Two pointed arches' became 'two ribs', since Stalley describes Durham's diagonal ribs as segments of a circle.
- B01.s1, B33.s0 (owner_review: 5): 'Nearly 47 meters' replaced with 'more than 45 meters', which all sources support; the card lists every published figure, including above 48 m.
- B14 (owner_review: 6): Durham is 'begun in 1093' and 'finished in 1133', with the vaults in phases over some forty years, on a band instead of one date. Stalley's reading of why ribs were used there is added, attributed.
- B06, B07 (owner_review: remark on narration): Limited to the barrel-vaulted type shown; 'dark' removed; the emphasis is on rearranging the supports, not on Gothic being cleverer.
- B24 (owner_review: remark on narration): Shortened; the names of Viollet-le-Duc and Arnaud Timbert are no longer spoken here, and stay in small type on the card. The Timbert pronunciation override is removed.
- B35 (card only) (owner_review: remark on visuals): Every explanation is labelled 'Hypothesis'; the 2024 argument carries its authors on the card. Narration unchanged.
- B22 (claim link) (owner_review: evidence gap): New CLM_164 links the sentence attributed to France's national library to that source.
- B04.s2, B05.s2, B10.s1 (owner_review: agent's sweep after the review): Same kind of over-generalization: 'has to stand by' became 'stands largely by', since the film itself shows ties; 'medieval builders' became builders at Amiens, as the source says; B10 names the Columbia project now that B09 no longer does.
- B40 (owner_review: second review, 1): One line that does not fit does not show that no line fits. The card now shows several valid lines in one arch, then the same arch with its supports moved apart up to the limit, after Block et al. 2006, Fig. 5, recalculated (script/arch_statics.py). The narration names the change of the supports.
- B08 (card, s3) (owner_review: second review, 2): The percentages left the card: the arches drawn are not those of the study. The narration says 'of two other arches'.
- B10.s1 (and the timelines of B10, B14) (owner_review: second review, 3): 1088 is when construction began at Cluny, not a date for the pointed arches.
- B14.s2, B15.s0 (owner_review: second review, editorial): The sentence naming Roger Stalley is gone, for pacing; his remark stays in the sources (CLM_144). B15 no longer needs 'Whatever first inspired them'.
- B40 (card only) (owner_review: third remark: 'B40 chưa chốt: cần sửa và kiểm chứng phép tính giới hạn sập'): The earlier calculation measured the span on the centreline and fixed the hinge, with a tolerance of its own. arch_statics.py now ports Ochsendorf's ArchSpread (span on the intrados, a hinge that moves toward the crown) and is tested against his table 5.3. Narration unchanged.
- B07, B12, B23 (visuals) (owner_review: owner's remark on long runs of word cards): These beats moved from 2D cards to the model: the three tools named on the section, the ribs from below, the windows lit. Narration unchanged.
- B05, B16, B17, B18, B19, B34 (intent, annotations) (owner_review: building the models): Bound to the new cathedral family: thrust arrows (new annotation type), labels, a conceptual path, one shared scale for the Romanesque and Gothic models in B18. Narration unchanged.
- B05, B06, B11, B13, B14, B34 (on-screen text) (owner_review: building the models): Text or labels added so that no stretch stays static past the 14 s limit, which was not changed.
