import pandas as pd

# === STEP 1: Load Data ===
file_path = r"C:\Users\USER\Downloads\april18\april18\combine\Combined.xlsx"
df = pd.read_excel(file_path)
df.columns = df.columns.str.strip()  # Clean column headers

# === STEP 2: Create Presence Matrix ===
rf_matrix = df.drop_duplicates().assign(present=1)
rf_matrix = rf_matrix.pivot_table(index='Genome Name',
                                  columns='Functional_Category',
                                  values='present',
                                  fill_value=0).reset_index()

# === STEP 3: Define Functional Gene Sets ===
high_vir = {
    "Effector_delivery_system", "Regulation", "Stress_survival",
    "Antimicrobial_activity/Competitive_advantage", "Exoenzyme",
    "Motility", "Invasion", "Biofilm", "Exotoxin"
}

high_res = {
    "Aminoglycoside_resistance", "Oxazolidinone_and_Phenicol", "Fosfomycin_resistance"
}

low_vir = {
    "Nutritional/Metabolic_factor", "Adherence", "Immune_modulation"
}

low_res = {
    "Trimethoprim_resistance", "Chloramphenicol_resistance", "Phenicol_resistance",
    "Macrolide_resistance", "Tetracycline_resistance"
}

hgt_high = {"ICE"}
hgt_medium = {"IME", "Other_Mobile_Elements"}

# === STEP 4: Rule-Based Category Assignment ===
def classify(row):
    present_genes = {col for col in row.index if row[col] == 1}

    # Zoonotic Classification
    zoonotic_hits = high_vir & present_genes
    if len(zoonotic_hits) >= 2:
        zoonotic = "Highly Zoonotic"
    elif len(zoonotic_hits) == 1:
        zoonotic = "Potential Zoonotic"
    else:
        zoonotic = "No Zoonotic Risk"

    # Resistance Classification
    if high_res & present_genes:
        resistance = "Highly Resistant"
    elif low_res & present_genes:
        resistance = "Low–Moderate Resistance"
    else:
        resistance = "No Resistance"

    # Low-priority Virulence Classification
    if low_vir & present_genes:
        virulence = "Low–Moderate Chance"
    else:
        virulence = "No Chance"

    # HGT Classification
    if hgt_high & present_genes:
        hgt = "High Chance of HGT"
    elif hgt_medium & present_genes:
        hgt = "Low–Moderate Chance of HGT"
    else:
        hgt = "No HGT Evidence"

    return pd.Series([zoonotic, resistance, virulence, hgt])

rf_matrix[['Zoonotic_Potential', 'Resistance_Potential', 'LowVirulence_Level', 'HGT_Potential']] = rf_matrix.apply(classify, axis=1)

# === STEP 5: Final Classification ===
def final_status(row):
    zoonotic = row['Zoonotic_Potential'] in {"Highly Zoonotic", "Potential Zoonotic"}
    resistance = row['Resistance_Potential'] in {"Highly Resistant", "Low–Moderate Resistance"}
    hgt_high_flag = row['HGT_Potential'] == "High Chance of HGT"
    hgt_medium_flag = row['HGT_Potential'] == "Low–Moderate Chance of HGT"
    low_virulence = row['LowVirulence_Level'] == "Low–Moderate Chance"

    if zoonotic and resistance and hgt_high_flag:
        return "Highly dangerous-zoonotic bacteria"
    elif zoonotic and resistance and hgt_medium_flag:
        return "High-risk zoonotic bacteria"
    elif zoonotic and not resistance and (hgt_high_flag or hgt_medium_flag):
        return "Potential zoonotic bacteria"
    elif resistance and not zoonotic and (hgt_high_flag or hgt_medium_flag):
        return "Resistance threat bacteria"
    elif not zoonotic and not resistance and low_virulence:
        return "Virulent bacteria"
    else:
        return "Low risk bacteria"

rf_matrix["Final_Classification"] = rf_matrix.apply(final_status, axis=1)

# === STEP 6: Save to File ===
output_path = r"C:\Users\USER\Downloads\april18\april18\rf-classified.csv"
rf_matrix.to_csv(output_path, index=False)
print("✔️ Full classification matrix with final status saved to:\n", output_path)
