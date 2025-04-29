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
    elif virulence_count == 2:
        virulence_status = "Strong Virulence"
    elif virulence_count == 1:
        virulence_status = "Early Sign of Virulence"
    else:
        virulence_status = "No Virulence Detected"

    # Resistance scoring
    resistance_count = len(res_hits)
    if resistance_count >= 3:
        resistance_status = "Dangerously Resistant"
    elif resistance_count == 2:
        resistance_status = "Strong Resistance"
    elif resistance_count == 1:
        resistance_status = "Early Resistance Detected"
    else:
        resistance_status = "No Resistance Detected"

    # Mobile elements scoring
    if "ICE" in mob_hits:
        mobile_status = "Potential Horizontal Gene Transfer"
    elif len(mob_hits) > 0:
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

# Load classification rules from text file
classification_rules = []
with open(r"C:\Users\USER\Downloads\Classification.txt", "r") as f:
    headers = f.readline().strip().split("\t")
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) == 4:
            classification_rules.append({
                "Virulence": parts[0],
                "Resistance": parts[1],
                "Mobile_Element": parts[2],
                "Classification": parts[3]
            })

# Convert to DataFrame for easier lookup
rules_df = pd.DataFrame(classification_rules)

# === STEP 5: Final Classification Logic ===
def final_classification(row):
    vir = row['Virulence_Status']
    res = row['Resistance_Status']
    mob = row['Mobile_Element_Status']
    
    # First try to match all three criteria
    match = rules_df[
        (rules_df['Virulence'] == vir) & 
        (rules_df['Resistance'] == res) & 
        (rules_df['Mobile_Element'] == mob)
    ]
    
    if not match.empty:
        return match.iloc[0]['Classification']
    
    # If no match, try without mobile element
    match = rules_df[
        (rules_df['Virulence'] == vir) & 
        (rules_df['Resistance'] == res) & 
        (rules_df['Mobile_Element'] == "Any")
    ]
    
    if not match.empty:
        return match.iloc[0]['Classification']
    
    # If still no match, try with only virulence and resistance
    match = rules_df[
        (rules_df['Virulence'] == vir) & 
        (rules_df['Resistance'] == res)
    ]
    
    if not match.empty:
        return match.iloc[0]['Classification']
    
    # If still no match, return the most specific classification we can
    if vir != "No Virulence Detected" and res != "No Resistance Detected":
        return f"Combined Threat: {vir} and {res}"
    elif vir != "No Virulence Detected":
        return f"Virulence Threat: {vir}"
    elif res != "No Resistance Detected":
        return f"Resistance Threat: {res}"
    else:
        return "Low Risk Bacterial Strain"

# Apply final classification
rf_matrix["Final_Classification"] = rf_matrix.apply(final_classification, axis=1)

# === STEP 6: Save Final Output ===
output_path = r"C:\Users\USER\Downloads\april18\april18\Matrix.csv"
rf_matrix.to_csv(output_path, index=False)

print("✔️ Full matrix with classifications saved to:\n", output_path)
