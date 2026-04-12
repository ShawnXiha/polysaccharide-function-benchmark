# Case Study Candidate Pool

This file groups candidate cases for biology-facing case studies. Candidates are screened from the clean masked-link benchmark and the paired ontology stability runs, then enriched with KG evidence previews.

## ontology_rescue

1. `dolphin::34783` / `osteogenic` / stratum `tail_1_10` / support `2` / evidence `5` / clean `-` / baseline `43` / ontology `3` / rescue16 `5`
   organisms: Alhagi maurorum
   monosaccharides: glucose; mannose; galactose; xylose; ...(+2)
   bonds: α-Araf-(1→3); α-Araf-(1→5); β-Xylp-(1→4); α-Araf-(1→3,5); ...(+8)
   diseases: organ injury
   publications: 10.1016/j.ijbiomac.2020.12.189

## clean_success

1. `dolphin::34001` / `antitumor` / stratum `head_gt_50` / support `706` / evidence `5` / clean `1` / baseline `-` / ontology `-` / rescue16 `-`
   organisms: Laminaria saccharina
   monosaccharides: glucose; mannose; galactose; xylose; ...(+3)
   bonds: α-Fucp-(4→6)
   diseases: Malignant neoplasms
   publications: 10.1016/j.phytochem.2010.05.021
2. `dolphin::33862` / `immunomodulatory` / stratum `head_gt_50` / support `1294` / evidence `5` / clean `1` / baseline `-` / ontology `-` / rescue16 `-`
   organisms: Boletus edulis
   monosaccharides: glucose; galactose; arabinose; rhamnose
   bonds: β-Glcp-(1→6); β-Galp-(1→6); β-Rhap-(1→3)
   diseases: Malignant neoplasms; 04-Diseases of the immune system
   publications: 10.1016/j.carbpol.2013.12.085
3. `dolphin::32815` / `immunomodulatory` / stratum `head_gt_50` / support `1294` / evidence `5` / clean `1` / baseline `-` / ontology `-` / rescue16 `-`
   organisms: Alhagi sparsifolia
   monosaccharides: glucose; mannose; galactose; galacturonic acid
   bonds: β-GalA-(1→4); β-Galp-(1→6); α-Glcp-(1→4)
   diseases: Malignant neoplasms; 04-Diseases of the immune system
   publications: 10.1080/10286020.2014.898633
4. `dolphin::32749` / `antioxidant` / stratum `head_gt_50` / support `1915` / evidence `5` / clean `1` / baseline `-` / ontology `-` / rescue16 `-`
   organisms: Fusarium solani
   monosaccharides: glucose; mannose; galactose; arabinose
   bonds: α-Arap-(1→5); α-Manp-(1→3); α-Glcp-(1→4); α-Glcp-(1→6); ...(+1)
   diseases: 04-Diseases of the immune system
   publications: 10.1016/j.ijbiomac.2019.07.019
5. `dolphin::32736` / `antioxidant` / stratum `head_gt_50` / support `1915` / evidence `5` / clean `1` / baseline `-` / ontology `-` / rescue16 `-`
   organisms: Amanita caesarea
   monosaccharides: glucose; lyxose
   bonds: α-Glcp-(1→4); α-Glcp-(1→3,6)
   diseases: Aging-related disorders
   publications: 10.3892/mmr.2016.5693
6. `dolphin::33495` / `antioxidant` / stratum `head_gt_50` / support `1915` / evidence `5` / clean `1` / baseline `-` / ontology `-` / rescue16 `-`
   organisms: Armillaria mellea
   monosaccharides: glucose; galactose; glucuronic acid
   bonds: β-Glcp-(1→1); α-Glcp-(1→3,6); β-Glcp-(1→3)
   diseases: 04-Diseases of the immune system
   publications: 10.1016/j.ijbiomac.2019.11.196
7. `dolphin::33898` / `antioxidant` / stratum `head_gt_50` / support `1915` / evidence `5` / clean `1` / baseline `-` / ontology `-` / rescue16 `-`
   organisms: Ziziphus Jujuba cv. Muzao
   monosaccharides: glucose; mannose; galactose; xylose; ...(+1)
   bonds: α-Manp-(1→3)
   diseases: 04-Diseases of the immune system
   publications: 10.1016/j.foodchem.2017.11.058
8. `dolphin::33999` / `anticoagulant` / stratum `head_gt_50` / support `157` / evidence `5` / clean `1` / baseline `-` / ontology `-` / rescue16 `-`
   organisms: Laminaria saccharina
   monosaccharides: glucose; mannose; galactose; xylose; ...(+3)
   bonds: α-Fucp-(4→6)
   diseases: Malignant neoplasms
   publications: 10.1016/j.phytochem.2010.05.021

## ontology_failure

1. `dolphin::33382` / `antiinflammatory` / stratum `head_gt_50` / support `124` / evidence `5` / clean `-` / baseline `19` / ontology `19` / rescue16 `-`
   organisms: Amygdalus scoparia Spach
   monosaccharides: galactose; xylose; arabinose; rhamnose
   bonds: β-Galp-(1→3); α-Araf-(1→3); β-Xylp-(1→3); α-Rhap-(1→6); ...(+2)
   diseases: Malignant neoplasms; 04-Diseases of the immune system
   publications: 10.1016/j.carbpol.2017.10.099
2. `dolphin::33967` / `antimicrobial` / stratum `head_gt_50` / support `98` / evidence `5` / clean `-` / baseline `28` / ontology `28` / rescue16 `-`
   organisms: Aloe vera
   monosaccharides: glucose; mannose; galactose
   bonds: β-Manp-(1→4); β-Glcp-(1→4); α-Galp-(1→6)
   diseases: 04-Diseases of the immune system; 01-Certain infectious or parasitic diseases; 5A44-Insulin-resistance syndromes
   publications: https://good-days.ro/files/file/aloe/biological_properties_of_acemannan.pdf
3. `dolphin::32805` / `antiproliferative` / stratum `mid_11_50` / support `40` / evidence `5` / clean `-` / baseline `29` / ontology `30` / rescue16 `-`
   organisms: Ziziphus jujuba Mill
   monosaccharides: glucose; mannose; galactose; xylose; ...(+5)
   bonds: α-Araf-(1→4); β-Galp-(1→4)
   diseases: Malignant neoplasms; 04-Diseases of the immune system
   publications: 10.3389/fnut.2022.1001334
4. `dolphin::34766` / `organ_protective` / stratum `head_gt_50` / support `128` / evidence `5` / clean `-` / baseline `42` / ontology `42` / rescue16 `-`
   organisms: Coriolus versicolor
   monosaccharides: glucose; mannose; galactose; xylose; ...(+1)
   bonds: α-Galp-(1→4); α-Galp-(1→2); α-Manp-(1→4); α-Manp-(1→6); ...(+5)
   diseases: 04-Diseases of the immune system; organ injury
   publications: 10.1016/j.ijbiomac.2019.06.242
5. `dolphin::33792` / `microbiota_regulation` / stratum `head_gt_50` / support `83` / evidence `5` / clean `-` / baseline `45` / ontology `45` / rescue16 `-`
   organisms: Hylocereus undatus
   monosaccharides: glucose; arabinose
   bonds: β-GlcA-(1→4); β-Galp-(1→6); α-Rhap-(1→4); α-Araf-(1→5)
   diseases: 5A40-Intermediate hyperglycaemia; 04-Diseases of the immune system
   publications: 10.1016/j.carbpol.2016.03.060
6. `dolphin::32986` / `lipid_lowering` / stratum `head_gt_50` / support `100` / evidence `5` / clean `-` / baseline `49` / ontology `49` / rescue16 `-`
   organisms: Anoectochilus roxburghii
   monosaccharides: glucose; galactose
   bonds: β-Glcp-(1→3)
   diseases: 5A40-Intermediate hyperglycaemia
   publications: 10.1039/c9fo00860h
7. `dolphin::33197` / `antiaging` / stratum `head_gt_50` / support `78` / evidence `5` / clean `-` / baseline `56` / ontology `56` / rescue16 `-`
   organisms: Cornus officinalis
   monosaccharides: glucose; mannose; galactose; xylose; ...(+2)
   bonds: α-Manp-(1→4)
   diseases: 04-Diseases of the immune system; Aging-related disorders
   publications: 10.1016/j.carres.2010.06.009
8. `dolphin::33742` / `antiaging` / stratum `head_gt_50` / support `78` / evidence `5` / clean `-` / baseline `57` / ontology `58` / rescue16 `-`
   organisms: Hippophae rhamnoides
   monosaccharides: glucose; mannose; galactose; arabinose
   bonds: α-Glcp-(1→4); α-Manp-(1→4); α-Araf-(1→3,5); α-Araf-(1→5); ...(+1)
   diseases: Aging-related disorders
   publications: 10.1016/j.carbpol.2021.118648

## clean_failure

1. `dolphin::33382` / `antiinflammatory` / stratum `head_gt_50` / support `126` / evidence `5` / clean `12` / baseline `-` / ontology `-` / rescue16 `-`
   organisms: Amygdalus scoparia Spach
   monosaccharides: galactose; xylose; arabinose; rhamnose
   bonds: β-Galp-(1→3); α-Araf-(1→3); β-Xylp-(1→3); α-Rhap-(1→6); ...(+2)
   diseases: Malignant neoplasms; 04-Diseases of the immune system
   publications: 10.1016/j.carbpol.2017.10.099
2. `dolphin::33568` / `antiinflammatory` / stratum `head_gt_50` / support `126` / evidence `5` / clean `17` / baseline `-` / ontology `-` / rescue16 `-`
   organisms: Grifola frondosa
   monosaccharides: glucose; mannose; galactose; xylose; ...(+2)
   bonds: β-Glcp-(1→6)
   diseases: Malignant neoplasms; 04-Diseases of the immune system; MG22-Fatigue
   publications: 10.1007/s00253-015-7260-3
3. `dolphin::33668` / `antiobesity` / stratum `mid_11_50` / support `36` / evidence `5` / clean `22` / baseline `-` / ontology `-` / rescue16 `-`
   organisms: Plantago asiatica L.
   monosaccharides: glucose; galactose; xylose; arabinose; ...(+1)
   bonds: β-Xylp-(1→3,4)
   diseases: 5A40-Intermediate hyperglycaemia; Malignant neoplasms; 04-Diseases of the immune system; organ injury; ...(+1)
   publications: 10.1016/j.bcdf.2021.100276
4. `dolphin::33378` / `antimicrobial` / stratum `head_gt_50` / support `94` / evidence `5` / clean `26` / baseline `-` / ontology `-` / rescue16 `-`
   organisms: Cyclocarya paliurus
   monosaccharides: glucose; mannose; galactose
   bonds: β-Glcp-(1→2,6); β-Manp-(1→4); β-Galp-(1→1)
   diseases: 01-Certain infectious or parasitic diseases; 5C8Z/5C8Y-lipoprotein metabolism disorder
   publications: 10.1016/j.ijbiomac.2019.11.212
5. `dolphin::32904` / `antiobesity` / stratum `mid_11_50` / support `36` / evidence `5` / clean `28` / baseline `-` / ontology `-` / rescue16 `-`
   organisms: Ipomoea batatas
   monosaccharides: glucose; galactose; arabinose; glucuronic acid; ...(+1)
   bonds: α-Araf-(1→2,4); α-Rhap-(1→4); α-Glcp-(1→4); β-Galp-(1→6)
   diseases: 5C8Z/5C8Y-lipoprotein metabolism disorder; 5C80.0-Hypercholesterolemia; 5B81-Obesity
   publications: 10.1002/jsfa.12239
6. `dolphin::32745` / `antimicrobial` / stratum `head_gt_50` / support `94` / evidence `5` / clean `28` / baseline `-` / ontology `-` / rescue16 `-`
   organisms: Lilium davidii var. unicolor Cotton
   monosaccharides: glucose; mannose
   bonds: α-Glcp-(1→4)
   diseases: 01-Certain infectious or parasitic diseases
   publications: 10.1016/j.ijbiomac.2019.04.082
7. `dolphin::32917` / `antimicrobial` / stratum `head_gt_50` / support `94` / evidence `5` / clean `29` / baseline `-` / ontology `-` / rescue16 `-`
   organisms: Glehnia littoralis
   monosaccharides: galactose
   bonds: α-Glcp-(1→4)
   diseases: 01-Certain infectious or parasitic diseases
   publications: 10.1016/j.ijbiomac.2021.04.178
8. `dolphin::33586` / `antimicrobial` / stratum `head_gt_50` / support `94` / evidence `5` / clean `30` / baseline `-` / ontology `-` / rescue16 `-`
   organisms: Dioscorea opposita
   monosaccharides: glucose; galactose
   bonds: α-Glcp-(1→6)
   diseases: 01-Certain infectious or parasitic diseases
   publications: 10.1016/j.carbpol.2014.09.082
