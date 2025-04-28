import pandas as pd

# === STEP 1: Load Data ===
file_path = r"C:\Users\USER\Desktop\Paturellacea-21-04\Combined_Pasteurellaceae.xlsx"
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
    "Exotoxin", "Effector_delivery_system", "Regulation", "Stress_survival",
    "Antimicrobial_activity/Competitive_advantage", "Exoenzyme",
    "Motility", "Invasion", "Biofilm", "Adherence"
}

high_res = {
    "Aminoglycoside_resistance", "Oxazolidinone_and_Phenicol", "Fosfomycin_resistance"
}

low_vir = {
    "Nutritional/Metabolic_factor", "Immune_modulation"
}

low_res = {
    "Trimethoprim_resistance", "Chloramphenicol_resistance", "Phenicol_resistance",
    "Macrolide_resistance", "Tetracycline_resistance"
}

mobile_elements = {
    "Other_Mobile_Elements", "ICE", "IME"
}

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

    # Mobile Elements Classification
    if mobile_elements & present_genes:
        mobile = "Present Mobile Elements"
    else:
        mobile = "No Mobile Elements"

    return pd.Series([zoonotic, resistance, virulence, mobile])

rf_matrix[['Zoonotic_Potential', 'Resistance_Potential', 'LowVirulence_Level', 'Mobile_Elements_Potential']] = rf_matrix.apply(classify, axis=1)

# === STEP 5: Final Classification ===
def final_status(row):
    zoonotic = row['Zoonotic_Potential'] in {"Highly Zoonotic", "Potential Zoonotic"}
    resistance = row['Resistance_Potential'] in {"Highly Resistant", "Low–Moderate Resistance"}
    mobile_elements_flag = row['Mobile_Elements_Potential'] == "Present Mobile Elements"
    low_virulence = row['LowVirulence_Level'] == "Low–Moderate Chance"

    if zoonotic and resistance and mobile_elements_flag:
        return "Highly dangerous-zoonotic bacteria"
    elif zoonotic and resistance and not mobile_elements_flag:
        return "High-risk zoonotic bacteria"
    elif zoonotic and not resistance and mobile_elements_flag:
        return "Potential zoonotic bacteria"
    elif resistance and not zoonotic and mobile_elements_flag:
        return "Resistance threat bacteria"
    elif not zoonotic and not resistance and low_virulence:
        return "Virulent bacteria"
    else:
        return "Low risk bacteria"

rf_matrix["Final_Classification"] = rf_matrix.apply(final_status, axis=1)

# === STEP 6: Save to File ===
output_path = r"C:\Users\Lenovo\Desktop\april18\rf-classified.csv"
rf_matrix.to_csv(output_path, index=False)
print("✔️ Full classification matrix with final status saved to:\n", output_path)
