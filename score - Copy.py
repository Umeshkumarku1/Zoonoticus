import pandas as pd

file_path = r"C:\Users\USER\Downloads\april18\april18\Combined.xlsx"
df = pd.read_excel(file_path)

# Clean column headers
df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()
print("🔍 Columns:", df.columns.tolist())


# Define groups
virulence_genes = {
    "Exotoxin", "Effector_delivery_system", "Regulation", "Stress_survival",
    "Antimicrobial_activity/Competitive_advantage", "Exoenzyme",
    "Motility", "Invasion", "Biofilm", "Adherence"
}

resistance_genes = {
    "Aminoglycoside_resistance", "Oxazolidinone_and_Phenicol", "Fosfomycin_resistance",
    "Trimethoprim_resistance", "Chloramphenicol_resistance", "Phenicol_resistance",
    "Macrolide_resistance", "Tetracycline_resistance"
}

mobile_elements = {"Other_Mobile_Elements", "ICE", "IME"}

# === STEP 3: Create Presence Matrix ===
rf_matrix = df.drop_duplicates().assign(present=1)
rf_matrix = rf_matrix.pivot_table(index='genome_id',
                                  columns='functional_category',
                                  values='present',
                                  fill_value=0).reset_index()

# === STEP 4: Classification Functions ===
def classify(row):
    present_genes = {col for col in row.index if row[col] == 1}

    vir_hits = virulence_genes & present_genes
    res_hits = resistance_genes & present_genes
    mob_hits = mobile_elements & present_genes

    # Virulence scoring
    virulence_count = len(vir_hits)
    if virulence_count >= 3:
        virulence_status = "Dangerously Virulent"
    elif 2 <= virulence_count == 2:
        virulence_status = "Strong Virulence"
    elif virulence_count == 1:
        virulence_status = "Early Sign of Virulence"
    else:
        virulence_status = "No Virulence Detected"

    # Resistance scoring
    resistance_count = len(res_hits)
    if resistance_count >= 3:
        resistance_status = "Dangerously Resistant"
    elif 2 <= resistance_count == 2:
        resistance_status = "Strong Resistance"
    elif resistance_count == 1:
        resistance_status = "Early Resistance Detected"
    else:
        resistance_status = "No Resistance Detected"

    # Mobile elements scoring
    if "ICE" in mob_hits:
        mobile_status = "Potential Horizontal Gene Transfer"
    elif "IME" in mob_hits or "Other_Mobile_Elements" in mob_hits:
        mobile_status = "Genomic Instability"
    else:
        mobile_status = "Stable Genome"

    return pd.Series([
        virulence_status, virulence_count,
        resistance_status, resistance_count,
        mobile_status
    ])

# Apply classification
rf_matrix[['Virulence_Status', 'Virulence_Gene_Count',
           'Resistance_Status', 'Resistance_Gene_Count',
           'Mobile_Element_Status']] = rf_matrix.apply(classify, axis=1)

# === STEP 5: Final Classification Logic ===
def final_classification(row):
    vir = row['Virulence_Status']
    res = row['Resistance_Status']
    mob = row['Mobile_Element_Status']

    # === PRIMARY CLASSIFICATIONS ===
    if vir == "Dangerously Virulent" and res == "Dangerously Resistant":
        return "Critical Threat: Highly Dangerous Zoonotic Bacterial Strain"
    
    if vir == "Strong Virulence" and res == "Strong Resistance":
        return "Very High Threat: Potentially Dangerous Zoonotic Bacterial Strain"
    
    if vir in {"Dangerously Virulent", "Strong Virulence"} and res in {"Early Resistance Detected", "Strong Resistance"}:
        return "High Threat: Virulent and Resistant Zoonotic Bacterial Strain"
    
    if vir in {"Dangerously Virulent", "Strong Virulence"} and res == "No Resistance Detected":
        return "Moderately-High Threat: Virulent Zoonotic Bacterial Strain"
    
    if res in {"Dangerously Resistant", "Strong Resistance"} and vir == "No Virulence Detected":
        return "Moderate Threat: Resistant Zoonotic Bacterial Strain"

    # === MOBILE ELEMENT COMBINATIONS ===
    if res in {"Dangerously Resistant", "Strong Resistance"} and mob == "Genomic Instability":
        return "Resistance Threat with Genomic Instability"
    
    if res in {"Dangerously Resistant", "Strong Resistance"} and mob == "Potential Horizontal Gene Transfer":
        return "Resistance Threat with Potential for Horizontal Gene Transfer"

    # === EARLY STAGE RISK ===
    if vir == "Early Sign of Virulence" and res == "No Resistance Detected":
        return "Potential Early Risk: Virulent Bacterial Strain"
    
    if res == "Early Resistance Detected" and vir == "No Virulence Detected":
        return "Potential Early Risk: Resistant Bacterial Strain"

    # === MINOR CASES ===
    if vir == "No Virulence Detected" and res in {"Early Resistance Detected", "Strong Resistance"}:
        return "Potential Resistant Bacterial Strain"
    
    if vir == "Early Sign of Virulence" and res == "No Resistance Detected":
        return "Potential Virulent Bacterial Strain"

    # === DEFAULT ===
    return "Low Risk Bacterial Strain"



# Apply final classification
rf_matrix["Final_Classification"] = rf_matrix.apply(final_classification, axis=1)

# === STEP 6: Save Final Output ===
output_path = r"C:\Users\USER\Downloads\april18\april18\Matrix.csv"
rf_matrix.to_csv(output_path, index=False)

print("✔️ Full matrix with classifications saved to:\n", output_path)
