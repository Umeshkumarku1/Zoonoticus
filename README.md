🦠 Zoonoticus


Zoonoticus is a cutting-edge resource designed to predict the zoonotic potential, resistance gene transfer capability, and virulence risk of bacterial pathogens.
Built using Zento, this database powers an advanced classification pipeline to help researchers and bioinformaticians rapidly identify bacteria that pose a serious threat to human and animal health.


✨ Features:

Zoonotic Potential Detection

Resistance Gene Transfer Risk Prediction

Virulence Factor Profiling

Rule-based & Machine Learning Integration

⚡ Why Zoonoticus?

Fast, accurate screening of whole genome data

Early detection of zoonotic threats

Data-driven support for infectious disease research and epidemiology

Essential tool for microbiology, genomics, and public health surveillance


## Gene Categories and Counts

A total of 37,291 gene sequences were used for this analysis. Below is a list of gene categories and their respective counts:

| **Gene Category**                                   | **No. of Genes** |
|-----------------------------------------------------|------------------|
| Effector delivery system                            | 9,597            |
| Immune modulation                                   | 5,329            |
| Adherence                                           | 5,130            |
| Nutritional/Metabolic factor                        | 3,798            |
| Motility                                            | 3,120            |
| Beta-lactam resistance genes                        | 2,006            |
| Exotoxin                                            | 1,283            |
| Hypothetical protein                                | 1,085            |
| ICE (Integrative Conjugative Elements)              | 977              |
| Biofilm                                             | 835              |
| Regulation                                          | 815              |
| Exoenzyme                                           | 454              |
| Invasion                                            | 409              |
| Stress survival                                     | 388              |
| Other Mobile Elements                               | 370              |
| Aminoglycoside resistance genes                     | 259              |
| IME (Integrative Mobilizable Elements)              | 191              |
| Post-translational modification                     | 188              |
| Tetracycline resistance genes                       | 146              |
| Antimicrobial activity/Competitive advantage        | 144              |
| Fluoroquinolone resistance genes                    | 124              |
| Macrolide resistance genes                          | 120              |
| Trimethoprim resistance genes                       | 109              |
| Phenicol resistance genes                           | 68               |
| Colistin (Polymyxin) resistance genes               | 56               |
| Sulfonamide resistance genes                        | 54               |
| Vancomycin resistance genes                         | 43               |
| Fosfomycin resistance genes                         | 39               |
| Chloramphenicol resistance genes                    | 33               |
| Streptogramin A resistance genes                    | 27               |
| Oxazolidinone and Phenicol resistance genes         | 26               |
| Methicillin (Beta-Lactams) resistance genes         | 23               |
| Nitroimidazole resistance genes                     | 15               |
| Quaternary Ammonium Compound resistance genes       | 11               |
| Rifamycin resistance genes                          | 10               |
| Fusidic Acid resistance genes                       | 3                |
| Multidrug Resistance Efflux Pump                    | 2                |
| Oleandomycin resistance genes                       | 2                |
| Carbapenem resistance genes                         | 1                |
| Metal Ion Transport                                 | 1                |

### Total Gene Sequences: 37,291



## Scoring Pattern for Bacterial Classification

Zoonoticus Database v1.0 isn’t just about identifying bacterial risks – it **scores** them!

Using a scoring pattern based on key traits like **Zoonotic Potential**, **Resistance**, **Mobile Elements**, and **Virulence**, each bacterium is assigned a risk score. The higher the score, the greater the risk.

### How It Works:
- **Zoonotic Potential**: A "Highly Zoonotic" classification automatically triggers a higher score (3 points) and is classified as **Potential Zoonotic Bacteria**.
- **Resistance**: Bacteria with resistance traits earn additional points (2 points for resistance).
- **Mobile Elements**: Presence of mobile elements adds 1 point.
- **Virulence**: Low virulence bacteria add a lesser weight (1 point).

### Final Classification:
Based on the accumulated score, bacteria are classified into risk categories such as:
- **Highly Dangerous-Zoonotic Bacteria**: High zoonotic risk, resistance, and mobile elements.
- **High-Risk Zoonotic Bacteria**: High zoonotic risk and resistance (without mobile elements).
- **Resistance Threat Bacteria**: Resistance with mobile elements, but no zoonotic risk.
- **Virulent Bacteria**: Low zoonotic risk and low resistance but still potentially virulent.
- **Low Risk Bacteria**: Minimal zoonotic, resistance, and virulence traits.

This innovative scoring system adds depth to classification, offering **data-driven insights** to help researchers quickly pinpoint high-risk zoonotic pathogens.



🔑 Keywords:

zoonotic pathogens | antimicrobial resistance | bacterial virulence | genomic epidemiology | bioinformatics tool


Datasets:

All datasets used in the development of the Zoonoticus Database v1.0 can be found at the following link: https://doi.org/10.5281/zenodo.15294863
