import pandas as pd

# === STEP 1: Load Data ===
file_path = r"C:\Users\Lenovo\Desktop\april18\Paturellacea-21-04\Paturellacea-21-04\Combined_Pasteurellaceae.xlsx"
df = pd.read_excel(file_path)

# Clean column headers
df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()
print("🔍 Columns:", df.columns.tolist())

# === STEP 2: Create Presence Matrix ===
rf_matrix = df.drop_duplicates().assign(present=1)
rf_matrix = rf_matrix.pivot_table(index='genome_id',
                                  columns='functional_category',
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

    zoonotic_hits = high_vir & present_genes
    num_hits = len(zoonotic_hits)

    if num_hits >= 3:
        zoonotic = "Highly Zoonotic"
    elif num_hits in [1, 2]:
        zoonotic = "Virulent"
    else:
        zoonotic = "No Chance"

    if high_res & present_genes:
        resistance = "Highly Resistant"
    elif low_res & present_genes:
        resistance = "Low–Moderate Resistance"
    else:
        resistance = "No Resistance"

    if mobile_elements & present_genes:
        mobile = "Presence of Mobile Elements"
    else:
        mobile = "No Mobile Elements"

    return pd.Series([resistance, mobile, zoonotic, num_hits])

# Apply classification
rf_matrix[['Resistance_Potential', 'Mobile_Elements_Potential', 'Zoonotic_Potential', 'Virulence_Gene_Count']] = rf_matrix.apply(classify, axis=1)

# === STEP 5: Final Classification ===
def final_status(row):
    if (row['Zoonotic_Potential'] == "Highly Zoonotic" and
        row['Resistance_Potential'] == "Highly Resistant" and
        row['Mobile_Elements_Potential'] == "Presence of Mobile Elements"):
        return "Highly dangerous-zoonotic bacteria"
    elif row['Zoonotic_Potential'] == "Highly Zoonotic":
        return "Potential zoonotic bacteria"
    elif (row['Zoonotic_Potential'] == "Virulent" and
          row['Resistance_Potential'] in {"Highly Resistant", "Low–Moderate Resistance"} and
          row['Mobile_Elements_Potential'] == "Presence of Mobile Elements"):
        return "Early chance zoonotic bacteria"
    elif (row['Zoonotic_Potential'] == "Virulent" and
          row['Resistance_Potential'] in {"Highly Resistant", "Low–Moderate Resistance"}):
        return "Potential zoonotic bacteria"
    elif (row['Resistance_Potential'] in {"Highly Resistant", "Low–Moderate Resistance"} and
          row['Mobile_Elements_Potential'] == "Presence of Mobile Elements"):
        return "Resistance threat bacteria"
    else:
        return "Low risk bacteria"

# Apply final classification
rf_matrix["Final_Classification"] = rf_matrix.apply(final_status, axis=1)

# === STEP 6: Save the Full Output ===
output_path = r"C:\Users\Lenovo\Downloads\Matrix1.csv"
rf_matrix.to_csv(output_path, index=False)

print("✔️ Full matrix (including gene counts and classifications) saved to:\n", output_path)
